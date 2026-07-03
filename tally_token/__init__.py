"""Tally Token

This module provides a simple way to split a secret into multiple tokens.
The secret can be recovered only if all the tokens are merged together.
"""

from __future__ import annotations

import logging
import secrets
from io import BufferedReader, BufferedWriter

# https://packaging-guide.openastronomy.org/en/latest/advanced/versioning.html
from ._version import __version__

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Token format version for split_bytes_into / merge_bytes_into.
# Version 0: raw XOR pads, no header. Tokens are same length as source.
# Bump this and add a version-byte prefix if the algorithm ever changes
# so that old and new tokens can be distinguished at merge time.
SPLIT_TOKEN_FORMAT_VERSION = 0

_SESSION_ID_SIZE = 16


def split_text(
    clear_text: str,
    into: int = 2,
    *,
    encoding: str = "utf-8",
) -> list[bytes]:
    """Split a text into multiple tokens.

    Args:
        clear_text: The text to be split.
        into: The number of tokens to be generated.
        encoding: The encoding used to convert text to bytes. Tokens do
            not store this value; pass the same encoding to merge_text to
            recover the original text.
    """
    clear_text_bytes = bytes(clear_text, encoding=encoding)
    return split_bytes_into(clear_text_bytes, into)


def split_io(
    infile: BufferedReader,
    outfiles: list[BufferedWriter],
    *,
    bufsize: int = 1024,
) -> None:
    """Split a file into multiple tokens.

    Args:
        infile: The file to be split.
        outfiles: The files to be written.
        bufsize: The buffer size of reading and writing.
    """
    session_id = _generate_random_token(_SESSION_ID_SIZE)
    for outfile in outfiles:
        outfile.write(session_id)
    output_sizes = len(outfiles)
    for buf in iter(lambda: infile.read(bufsize), b""):
        _write_split_tokens_raw(buf, outfiles, output_sizes)

    _flush_outputs(outfiles)


def _write_split_tokens_raw(
    source: bytes,
    outfiles: list[BufferedWriter],
    output_sizes: int,
) -> None:
    token_bytes = _split_bytes_raw(source, output_sizes)
    for token, outfile in zip(token_bytes, outfiles, strict=True):
        outfile.write(token)


def _flush_outputs(outfiles: list[BufferedWriter]) -> None:
    for outfile in outfiles:
        outfile.flush()


def _split1(source: bytes) -> tuple[bytes, bytes]:
    token = _generate_random_token(len(source))
    cipher_text = bytearray()
    for i in range(len(source)):
        cipher_text.append(source[i] ^ token[i])
    return bytes(token), bytes(cipher_text)


def _split_bytes_raw(source: bytes, into: int) -> list[bytes]:
    """Split bytes into raw tokens without session ID (for streaming use)."""
    if into <= 0:
        msg = f"n must be a positive integer, got {into}"
        raise ValueError(msg)
    tokens = []
    token = source
    for _ in range(into - 1):
        generated, token = _split1(token)
        tokens.append(generated)
    tokens.append(token)
    return tokens


def split_bytes_into(source: bytes, into: int) -> list[bytes]:
    """Split a bytes into multiple token bytes.

    Each token is prefixed with a shared 16-byte session ID so that
    merge_bytes_into can detect when tokens from different splits are mixed.

    Args:
        source: The bytes to be split.
        into: The number of tokens to be generated.
    """
    session_id = _generate_random_token(_SESSION_ID_SIZE)
    raw_tokens = _split_bytes_raw(source, into)
    return [session_id + t for t in raw_tokens]


def _merge1(token1: bytes, token2: bytes) -> bytes:
    clear_text = bytearray()
    for i in range(len(token1)):
        clear_text.append(token1[i] ^ token2[i])
    return bytes(clear_text)


def _validate_tokens_nonempty(tokens: list[bytes]) -> None:
    if not tokens:
        msg = "tokens must not be empty"
        raise ValueError(msg)


def _merge_bytes_raw(tokens: list[bytes]) -> bytes:
    """Merge raw token chunks without session ID verification."""
    _validate_tokens_nonempty(tokens)
    token = tokens[0]
    for i in range(1, len(tokens)):
        if len(tokens[i]) != len(token):
            msg = (
                f"token at index {i} has length {len(tokens[i])}, "
                f"expected {len(token)}"
            )
            raise ValueError(msg)
        token = _merge1(token, tokens[i])
    return token


def _check_session_ids(session_ids: list[bytes]) -> None:
    """Raise ValueError if session IDs from different splits are detected."""
    if len(set(session_ids)) > 1:
        raise ValueError(
            "tokens come from different splits: session IDs do not match",
        )


def merge_bytes_into(tokens: list[bytes]) -> bytes:
    """Merge tokens into a secret bytes.

    Verifies that all tokens share the same session ID embedded by
    split_bytes_into, raising ValueError if tokens from different splits
    are mixed.

    Args:
        tokens: The tokens to be merged.
    """
    session_ids = [t[:_SESSION_ID_SIZE] for t in tokens]
    _check_session_ids(session_ids)
    stripped = [t[_SESSION_ID_SIZE:] for t in tokens]
    return _merge_bytes_raw(stripped)


def merge_text(tokens: list[bytes], *, encoding: str = "utf-8") -> str:
    """Merge tokens into a text.

    Args:
        tokens: The tokens to be merged.
        encoding: The encoding used to decode the merged bytes. It must
            match the encoding passed to split_text because tokens do not
            carry encoding metadata.
    """
    clear_text_bytes = merge_bytes_into(tokens)
    return clear_text_bytes.decode(encoding)


def merge_io(
    infiles: list[BufferedReader],
    outfile: BufferedWriter,
    *,
    bufsize: int = 1024,
) -> None:
    """Merge tokens into a file.

    Args:
        infiles: The files to be read.
        outfile: The file to be written.
    """
    session_ids = [f.read(_SESSION_ID_SIZE) for f in infiles]
    _check_session_ids(session_ids)
    while True:
        chunks = [f.read(bufsize) for f in infiles]
        merged = _merge_bytes_raw(chunks)
        if not merged:
            break
        outfile.write(merged)
    outfile.flush()


def _generate_random_token(size: int) -> bytes:
    return secrets.token_bytes(size)


__all__ = [
    "SPLIT_TOKEN_FORMAT_VERSION",
    "__version__",
    "merge_bytes_into",
    "merge_io",
    "merge_text",
    "split_bytes_into",
    "split_io",
    "split_text",
]
