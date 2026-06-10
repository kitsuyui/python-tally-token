# Contributing

Thank you for improving `tally-token`.

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management
and [Poe the Poet](https://poethepoet.natn.io/) for common tasks.

```sh
uv sync
```

## Local Checks

Run the formatter before opening a pull request:

```sh
uv run poe format
```

Run lint and type checks:

```sh
uv run poe check
```

Run the test suite:

```sh
uv run poe test
```

Run the coverage job used by CI:

```sh
uv run poe coverage-xml
```

Check that the package builds:

```sh
uv build
```

## Pull Requests

Before opening a pull request, make sure that:

- the change is focused on one topic;
- relevant checks pass locally;
- tests or documentation are updated when behavior changes;
- no token bytes, plain-text secrets, or other sensitive data are logged or
  included in fixtures.

When reporting a failing check, include the command you ran and the relevant
error output.

## Security Changes

This library can operate on secret material. If your change affects token
generation, merging, file output, logging, or error messages, explain the
security impact in the pull request.
