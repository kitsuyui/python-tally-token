import argparse

from tally_token import merge_bytes_into, split_bytes_into


def split_main(*, source_path: str, dest_paths: str) -> None:
    with open(source_path, "rb") as f:
        source = f.read()
    tokens = split_bytes_into(source, len(dest_paths))
    for token, dest_path in zip(tokens, dest_paths):
        with open(dest_path, "wb") as f:
            f.write(token)


def merge_main(*, dest_path: str, source_paths: str) -> None:
    tokens = []
    for source_path in source_paths:
        with open(source_path, "rb") as f:
            tokens.append(f.read())
    with open(dest_path, "wb") as f:
        f.write(merge_bytes_into(tokens))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        required=True,
        dest="command",
    )
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("src")
    split_parser.add_argument("dst", nargs="+")

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("dst")
    merge_parser.add_argument("src", nargs="+")

    args = parser.parse_args()
    if args.command == "split":
        split_main(source_path=args.src, dest_paths=args.dst)
    elif args.command == "merge":
        merge_main(dest_path=args.dst, source_paths=args.src)


if __name__ == "__main__":
    main()
