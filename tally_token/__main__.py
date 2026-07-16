from __future__ import annotations

import argparse
import os
import sys
import tempfile
from contextlib import ExitStack
from io import BufferedWriter
from pathlib import Path

from tally_token import __version__, merge_io, split_io


def _open_temp_writers(
    dest_paths: list[Path],
    stack: ExitStack,
) -> tuple[list[Path], list[BufferedWriter]]:
    tmp_paths: list[Path] = []
    outfiles: list[BufferedWriter] = []
    for dest in dest_paths:
        fd, tmp = tempfile.mkstemp(dir=dest.parent)
        tmp_paths.append(Path(tmp))
        outfiles.append(stack.enter_context(os.fdopen(fd, "wb")))
    return tmp_paths, outfiles


def _unlink_temps(tmp_paths: list[Path]) -> None:
    for tmp_path in tmp_paths:
        tmp_path.unlink(missing_ok=True)


def _rename_temps(tmp_paths: list[Path], dest_paths: list[Path]) -> None:
    for tmp_path, dest in zip(tmp_paths, dest_paths, strict=True):
        tmp_path.replace(dest)


def _check_duplicate_dest_paths(dest_paths: list[Path]) -> None:
    if len(dest_paths) != len(set(dest_paths)):
        raise ValueError(
            "destination paths must be unique "
            "to avoid overwriting split tokens",
        )


def split_main(
    *,
    source_path: str,
    dest_paths: list[str],
    bufsize: int = 1024,
) -> None:
    dest_path_objects = [Path(p) for p in dest_paths]
    _check_duplicate_dest_paths(dest_path_objects)
    tmp_paths: list[Path] = []
    try:
        with ExitStack() as stack:
            infile = stack.enter_context(Path(source_path).open("rb"))
            tmp_paths, outfiles = _open_temp_writers(dest_path_objects, stack)
            split_io(infile, outfiles, bufsize=bufsize)
        _rename_temps(tmp_paths, dest_path_objects)
    except Exception:
        _unlink_temps(tmp_paths)
        raise


def _check_token_file_sizes(source_paths: list[str]) -> None:
    sizes = [(p, Path(p).stat().st_size) for p in source_paths]
    unique_sizes = {s for _, s in sizes}
    if len(unique_sizes) > 1:
        details = ", ".join(f"{p!r}: {s} bytes" for p, s in sizes)
        raise ValueError(
            "token files have mismatched sizes; they may be truncated or from "
            f"different split operations ({details})",
        )


def merge_main(
    *,
    dest_path: str,
    source_paths: list[str],
    bufsize: int = 1024,
) -> None:
    _check_token_file_sizes(source_paths)
    dest = Path(dest_path)
    fd, tmp = tempfile.mkstemp(dir=dest.parent)
    tmp_path = Path(tmp)
    try:
        with ExitStack() as stack:
            outfile: BufferedWriter = stack.enter_context(os.fdopen(fd, "wb"))
            infiles = [
                stack.enter_context(Path(p).open("rb")) for p in source_paths
            ]
            merge_io(infiles, outfile, bufsize=bufsize)
        tmp_path.replace(dest)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=f"tally-token {__version__}",
    )
    subparsers = parser.add_subparsers(
        required=True,
        dest="command",
        help=(
            "Commands:\n"
            "split: split a file into multiple files\n"
            "merge: merge multiple files into a file\n"
            "Example:\n"
            "tally-token split example.bin "
            "example.bin.1 example.bin.2 example.bin.3\n"
            "tally-token merge "
            "example.bin.1 example.bin.2 example.bin.3 "
            "--output example-merged.bin"
        ),
    )
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("src", help="The source file to be split.")
    split_parser.add_argument("dst", nargs="+", help="The destination files.")
    split_parser.add_argument(
        "--bufsize",
        type=int,
        default=1024 * 2,
        help="The buffer size.",
    )

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("src", nargs="+", help="The source files.")
    merge_parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="The destination file.",
    )
    merge_parser.add_argument(
        "--bufsize",
        type=int,
        default=1024 * 2,
        help="The buffer size.",
    )

    args = parser.parse_args()
    if args.command == "split":
        split_main(
            source_path=args.src,
            dest_paths=args.dst,
            bufsize=args.bufsize,
        )
    elif args.command == "merge":
        merge_main(
            dest_path=args.output,
            source_paths=args.src,
            bufsize=args.bufsize,
        )


def _cli_entry() -> None:
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    _cli_entry()
