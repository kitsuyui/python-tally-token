# python-tally-token

## What is this?

tally-token is a Python library for split data into tokens with same length.

[Tally](https://en.wikipedia.org/wiki/Tally_stick) is a historical object for prove something by splitting wood into tokens and matching tokens.

# Usage

## Install

```sh
$ pip install tally-token
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

# LICENSE

BSD 3-Clause License
