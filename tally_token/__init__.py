from __future__ import annotations

import secrets


def _generate_random_token(size: int) -> bytes:
    # TODO: seed
    return secrets.token_bytes(size)


def split_text(clear_text: str, into: int = 2) -> list[bytes]:
    clear_text_bytes = bytes(clear_text, "utf-8")
    return split_bytes_into(clear_text_bytes, into)


def split1(source: bytes) -> tuple[bytes, bytes]:
    token = _generate_random_token(len(source))
    cipher_text = bytearray()
    for i in range(len(source)):
        cipher_text.append(source[i] ^ token[i])
    return bytes(token), bytes(cipher_text)


def split_bytes_into(source: bytes, n: int) -> list[bytes]:
    tokens = []
    token = source
    for _ in range(n - 1):
        generated, token = split1(token)
        tokens.append(generated)
    tokens.append(token)
    return tokens


def merge1(token1: bytes, token2: bytes) -> bytes:
    clear_text = bytearray()
    for i in range(len(token1)):
        clear_text.append(token1[i] ^ token2[i])
    return bytes(clear_text)


def merge_bytes_into(tokens: list[bytes]) -> bytes:
    token = tokens[0]
    for i in range(1, len(tokens)):
        token = merge1(token, tokens[i])
    return token


def merge_text(tokens: list[bytes]) -> str:
    clear_text_bytes = merge_bytes_into(tokens)
    return clear_text_bytes.decode("utf-8")
