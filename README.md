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

```python
>>> from tally_token import split_text
>>> split_text("Hello, World!")
[b'qQ\xa5\x97\x84\x88\xd7U%\xfb(k\xa1', b'94\xc9\xfb\xeb\xa4\xf7\x02J\x89D\x0f\x80']
```

### merge

```python
>>> from tally_token import merge_text
>>> merge_text([b'qQ\xa5\x97\x84\x88\xd7U%\xfb(k\xa1', b'94\xc9\xfb\xeb\xa4\xf7\x02J\x89D\x0f\x80'])
'Hello, World!'
```

### split with custom length

```python
>>> from tally_token import split_text
>>> split_text("Hello, World!", 5)
[b'N&\xce\\\xbc6dxp\x87\xa8#z', b'\xa3D\\A\xf8\xd1KDX\x1cKx\x87', b'\xffZ\x03\xf5\x92Q\xf52\xc4\x1e\xf2\xf8\x06', b'\xaa\xdd:\x85F\xa1\xcdbp\xf3\xe6P\xe5', b'\xf0\x80\xc7\x01\xff;7;\xf3\x04\x9b\x97?']
>>> merge_text([b'N&\xce\\\xbc6dxp\x87\xa8#z', b'\xa3D\\A\xf8\xd1KDX\x1cKx\x87', b'\xffZ\x03\xf5\x92Q\xf52\xc4\x1e\xf2\xf8\x06', b'\xaa\xdd:\x85F\xa1\xcdbp\xf3\xe6P\xe5', b'\xf0\x80\xc7\x01\xff;7;\xf3\x04\x9b\x97?'])
'Hello, World!'
```

# LICENSE

BSD 3-Clause License
