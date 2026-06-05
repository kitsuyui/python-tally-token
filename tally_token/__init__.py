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
    output_sizes = len(outfiles)
    for buf in iter(lambda: infile.read(bufsize), b""):
        _write_split_tokens(buf, outfiles, output_sizes)

    _flush_outputs(outfiles)


def _write_split_tokens(
    source: bytes,
    outfiles: list[BufferedWriter],
    output_sizes: int,
) -> None:
    token_bytes = split_bytes_into(source, output_sizes)
    for token, outfile in zip(token_bytes, outfiles, strict=False):
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


def split_bytes_into(source: bytes, into: int) -> list[bytes]:
    """Split a bytes into multiple token bytes.

    Args:
        source: The bytes to be split.
        into: The number of tokens to be generated.
    """
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


def _merge1(token1: bytes, token2: bytes) -> bytes:
    clear_text = bytearray()
    for i in range(len(token1)):
        clear_text.append(token1[i] ^ token2[i])
    return bytes(clear_text)


def _validate_tokens_nonempty(tokens: list[bytes]) -> None:
    if not tokens:
        msg = "tokens must not be empty"
        raise ValueError(msg)


def merge_bytes_into(tokens: list[bytes]) -> bytes:
    """Merge tokens into a secret bytes.

    Args:
        tokens: The tokens to be merged.
    """
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
    token_bytes = []
    while True:
        token_bytes = [infile.read(bufsize) for infile in infiles]
        clear_text_bytes = merge_bytes_into(token_bytes)
        if not clear_text_bytes:
            break
        outfile.write(clear_text_bytes)
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
