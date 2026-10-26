# Changelog

All notable changes to this project will be documented in this file.

Versions are generated from Git tags with setuptools-scm. Release artifacts
and historical release metadata are available from
[GitHub Releases](https://github.com/kitsuyui/python-tally-token/releases).

## Unreleased

### Changed

- Tokens now include a shared 16-byte session ID and are incompatible with
  tokens from 0.6.3 or earlier. Recover old tokens with 0.6.3 and re-split
  using the new version; see the README migration guide.
- Rename the `split_bytes_into` keyword argument `n` to `into`.

### Added

- Added this changelog and linked it from the README and package metadata.

## Release History

Earlier releases were published before this changelog was added. Use the
linked GitHub releases for historical artifacts and tag metadata.

- [v0.6.3](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.6.3) - 2026-02-24
- [v0.6.2](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.6.2) - 2025-01-31
- [v0.6.1](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.6.1) - 2025-01-31
- [v0.6.0](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.6.0) - 2024-10-15
- [v0.5.0](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.5.0) - 2023-10-06
- [v0.4.0](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.4.0) - 2023-09-06
- [v0.3.1](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.3.1) - 2023-07-25
- [v0.3.0](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.3.0) - 2023-07-15
- [v0.2.0](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.2.0) - 2023-07-15
- [v0.1.0](https://github.com/kitsuyui/python-tally-token/releases/tag/v0.1.0) - 2023-07-15
