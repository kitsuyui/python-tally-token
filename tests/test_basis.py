import random
from io import BytesIO

import pytest

from tally_token import (
    merge_bytes_into,
    merge_io,
    merge_text,
    split_text,
)


def test_split_merge():
    """Test that split_text and merge_text are inverses."""
    clear_text = "Hello World!"
    token1, token2 = split_text(clear_text)
    assert clear_text == merge_text([token1, token2])


def test_split_into_one_and_merge():
    """Test that split_text with into=1 returns the original text."""
    clear_text = "Hello World!"
    tokens = split_text(clear_text, into=1)
    assert tokens == [b"Hello World!"]
    assert clear_text == merge_text(tokens)


def test_split_into_3():
    """Test that split_text accept into=3."""
    clear_text = "Hello World!"
    tokens = split_text(clear_text, into=3)
    assert len(tokens) == 3
    assert clear_text == merge_text(tokens)


def test_merge_order():
    """Test that merge_text accepts tokens in any order."""
    clear_text = "Hello World!"
    tokens = split_text(clear_text, into=10)
    assert len(tokens) == 10
    assert clear_text == merge_text(tokens)
    for _ in range(10):
        random.shuffle(tokens)
        assert clear_text == merge_text(tokens)


def test_merge_bytes_into_rejects_mismatched_token_lengths():
    """Test that merge_bytes_into rejects mismatched token lengths."""
    token1, token2 = split_text("Hello World!")

    with pytest.raises(
        ValueError,
        match="token at index 1 has length 11, expected 12",
    ):
        merge_bytes_into([token1, token2[:-1]])


def test_merge_io_rejects_mismatched_token_lengths():
    """Test that merge_io rejects mismatched token lengths."""
    token1, token2 = split_text("Hello World!")
    output = BytesIO()

    with pytest.raises(
        ValueError,
        match="token at index 1 has length 11, expected 12",
    ):
        merge_io([BytesIO(token1), BytesIO(token2[:-1])], output)


def test_encoding():
    """Test that split_text and merge_text accept custom encoding."""
    clear_text = "こんにちは"
    tokens = split_text(clear_text, encoding="CP932")
    assert clear_text == merge_text(tokens, encoding="CP932")
