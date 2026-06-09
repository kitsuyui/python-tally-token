# python-tally-token

[![Python](https://img.shields.io/pypi/pyversions/tally-token.svg?style=plastic)](https://badge.fury.io/py/tally-token)
[![PyPI version shields.io](https://img.shields.io/pypi/v/tally-token.svg)](https://pypi.python.org/pypi/tally-token/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![Coverage](https://raw.githubusercontent.com/kitsuyui/octocov-central/main/badges/kitsuyui/python-tally-token/coverage.svg)

## What is this?

tally-token is a Python library for split data into tokens with same length.

[Tally](https://en.wikipedia.org/wiki/Tally_stick) is a historical object for prove something by splitting wood into tokens and matching tokens.

<a href="https://en.wikipedia.org/wiki/Tally_stick#/media/File:Medieval_tally_sticks.jpg" target="_blank"><img src="https://github.com/kitsuyui/python-tally-token/assets/2596972/103a0184-c508-4ce6-9ed3-1b1eb58bc6cc" style="width:20rem" /></a>
> Medieval English split tally stick (front and reverse view). The stick is notched and inscribed to record a debt owed to the rural dean of Preston Candover, Hampshire, of a tithe of 20d each on 32 sheep, amounting to a total sum of £2 13s. 4d.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes and upgrade notes.

# Usage

## Install

```sh
$ pip install tally-token
```

## CLI Usage

```sh
$ tally-token --help
usage: tally-token [-h] {split,merge} ...

positional arguments:
  {split,merge}  Commands: split: split a file into multiple files merge: merge multiple files into a fileExample: tally-token split example.bin
                 example.bin.1 example.bin.2 example.bin.3 tally-token merge example-merged.bin example.bin.1 example.bin.2 example.bin.3

options:
  -h, --help     show this help message and exit
```

### split

You can use `split` to split a file into multiple files.

```sh
$ tally-token split something.bin split-1.bin split-2.bin split-3.bin
```

### merge

You can use `merge` to merge multiple files into a file.

```sh
$ tally-token merge merged.bin split-1.bin split-2.bin split-3.bin
```

### Large files

Nothing special. You can split and merge large file.

```sh
$ dd if=/dev/urandom of=original.1g.bin bs=1G count=1
$ tally-token split original.1g.bin split-1.bin split-2.bin split-3.bin
$ shasum -a 256 original.1g.bin
> 736a344d99d27e2dcdab8bc37ca94c83eda26f812a3dee87ac98989f89b3f965 original.1g.bin
$ tally-token merge recovery.1g.bin split-1.bin split-2.bin split-3.bin
$ shasum -a 256 recovery.1g.bin
> 736a344d99d27e2dcdab8bc37ca94c83eda26f812a3dee87ac98989f89b3f965 recovery.1g.bin
```

## Example

### split

You can use `split_text` to split text into tokens. `split_text` returns list of random bytes.

```python
>>> from tally_token import split_text
>>> split_text("Hello, World!")
[b'qQ\xa5\x97\x84\x88\xd7U%\xfb(k\xa1', b'94\xc9\xfb\xeb\xa4\xf7\x02J\x89D\x0f\x80']
```

### merge

You can use `merge_text` to merge tokens into text. `merge_text` returns cleartext.

```python
>>> from tally_token import merge_text
>>> merge_text([b'qQ\xa5\x97\x84\x88\xd7U%\xfb(k\xa1', b'94\xc9\xfb\xeb\xa4\xf7\x02J\x89D\x0f\x80'])
'Hello, World!'
```

### split with custom length

```python
>>> from tally_token import split_text, merge_text
>>> split_text("Hello, World!", 5)
[b'N&\xce\\\xbc6dxp\x87\xa8#z', b'\xa3D\\A\xf8\xd1KDX\x1cKx\x87', b'\xffZ\x03\xf5\x92Q\xf52\xc4\x1e\xf2\xf8\x06', b'\xaa\xdd:\x85F\xa1\xcdbp\xf3\xe6P\xe5', b'\xf0\x80\xc7\x01\xff;7;\xf3\x04\x9b\x97?']
>>> merge_text([b'N&\xce\\\xbc6dxp\x87\xa8#z', b'\xa3D\\A\xf8\xd1KDX\x1cKx\x87', b'\xffZ\x03\xf5\x92Q\xf52\xc4\x1e\xf2\xf8\x06', b'\xaa\xdd:\x85F\xa1\xcdbp\xf3\xe6P\xe5', b'\xf0\x80\xc7\x01\xff;7;\xf3\x04\x9b\x97?'])
'Hello, World!'
```

### split with custom encoding

```python
>>> from tally_token import split_text, merge_text
>>> split_text("こんにちは", encoding="CP932")
[b'g\xc3\x12\xeal?\xe5[\x03\xad', b'\xe5r\x90\x1b\xee\xf6g\xe4\x81`']
>>> merge_text([b'g\xc3\x12\xeal?\xe5[\x03\xad', b'\xe5r\x90\x1b\xee\xf6g\xe4\x81`'], encoding="CP932")
'こんにちは'
```

The returned tokens are opaque bytes and do not store the encoding name. When
splitting text with a custom encoding, keep that encoding out of band and pass
the same value to `merge_text`; using a different encoding can raise
`UnicodeDecodeError` or return mojibake if the bytes happen to decode.

### bytes interface

You can use `split_bytes_into` and `merge_bytes_into` to split and merge bytes.
This is useful for split binary data.

```python
>>> from tally_token import split_bytes_into, merge_bytes_into
>>> split_bytes_into(b"Hello, World!", 5)
[b'\xc5b\xf4E)\xe1vO8\xff@\xf9\xdd', b'\x84\xb9X#\x85\xf5\xed\xbcM\xc4\xef\xf4\xd3', b'\xb47\xf6\xfa?\x14\xa8`\xc9\xe0\xe5\x87\x14', b'\x1cd\xb4o\xe8I:\xe5\xf6\x13\xe5\x93G', b'\xa1\xed\x82\x9f\x14e)!%\xba\xc3}|']
>>> merge_bytes_into([b'\xc5b\xf4E)\xe1vO8\xff@\xf9\xdd', b'\x84\xb9X#\x85\xf5\xed\xbcM\xc4\xef\xf4\xd3', b'\xb47\xf6\xfa?\x14\xa8`\xc9\xe0\xe5\x87\x14', b'\x1cd\xb4o\xe8I:\xe5\xf6\x13\xe5\x93G', b'\xa1\xed\x82\x9f\x14e)!%\xba\xc3}|'])
b'Hello, World!'
```

# Security and Logging

This library handles secret material (token bytes) and follows a
**log-nothing policy**: no secret data should appear in log output.

- The library installs a `NullHandler` on its root logger so log records
  are silently discarded unless the *application* configures a handler.
  This is the [standard practice for libraries](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library).
- **Do not log token bytes or plain-text secrets** in your application code.
  Functions such as `split_bytes_into`, `_split1`, `write_split_tokens`, and
  `merge_bytes_into` operate directly on secret material.
- If you add debug logging to code that calls this library, ensure no
  token content is captured in log records or exception messages.

# Reference

- Tally stick https://en.wikipedia.org/wiki/Tally_stick
- Tessera or Symbolum (Hospitium token) https://en.wikipedia.org/wiki/Hospitium
- 割符 https://ja.wikipedia.org/wiki/%E5%89%B2%E7%AC%A6
- One-time pad https://en.wikipedia.org/wiki/One-time_pad

## Development

This repository uses [lefthook](https://lefthook.dev/) to run the same checks as CI
locally, so problems surface before they reach CI.

```sh
# Install dependencies
uv sync

# Install the Git hooks (once; requires lefthook on your PATH)
lefthook install
```

Once installed, the hooks run automatically:

- **pre-commit**: `uv run poe check`
- **pre-push**: `uv run poe check` and `uv run poe test`

You can also run the checks manually:

```sh
uv run poe check
uv run poe test
```

CI still runs the full matrix (see `.github/workflows/`); the hooks only bring that
feedback earlier on your machine.

# LICENSE

BSD 3-Clause License
