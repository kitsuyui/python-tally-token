import subprocess
import sys
import tempfile
from pathlib import Path

from tally_token import __version__


def test_cli_version():
    """Test the CLI version output."""
    result = subprocess.run(
        [sys.executable, "-m", "tally_token", "--version"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout == f"tally-token {__version__}\n"
    assert result.stderr == ""


def test_cli():
    """Test the CLI."""
    # create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.check_call(
            [
                "dd",
                "if=/dev/urandom",
                "of=example.bin",
                "bs=1M",
                "count=10",
            ],
            cwd=tmpdir,
        )

        # split the file
        subprocess.check_call(
            [
                "python",
                "-m",
                "tally_token",
                "split",
                f"{tmpdir}/example.bin",
                f"{tmpdir}/example.bin.1",
                f"{tmpdir}/example.bin.2",
                f"{tmpdir}/example.bin.3",
            ],
        )

        # merge the split files
        subprocess.check_call(
            [
                "python",
                "-m",
                "tally_token",
                "merge",
                f"{tmpdir}/example.bin.1",
                f"{tmpdir}/example.bin.2",
                f"{tmpdir}/example.bin.3",
                "--output",
                f"{tmpdir}/example-merged.bin",
            ],
        )

        # check that the original file and the merged file are the same
        subprocess.check_call(
            [
                "diff",
                "-s",
                f"{tmpdir}/example.bin",
                f"{tmpdir}/example-merged.bin",
            ],
        )


def test_cli_split_rejects_duplicate_destinations():
    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = Path(tmpdir) / "example.bin"
        source_path.write_bytes(b"secret")
        duplicate_dest = Path(tmpdir) / "example.bin.1"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "tally_token",
                "split",
                str(source_path),
                str(duplicate_dest),
                str(duplicate_dest),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert result.stdout == ""
        assert (
            "destination paths must be unique to avoid overwriting split tokens"
            in result.stderr
        )
        assert not duplicate_dest.exists()
