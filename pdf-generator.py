#!/usr/bin/env python3
"""Download a complete tutorial PDF from tutorialspoint.com."""

import argparse
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

TLD = "https://www.tutorialspoint.com/"

# The name is interpolated straight into the URL path, so restrict it to
# characters that cannot escape that path. Anything else is a typo.
VALID_NAME = re.compile(r"^[a-z0-9_+-]+$")


class NotAPdfError(Exception):
    """The server returned 200 but the body was not a PDF."""


def human(size):
    """Format a byte count for display."""
    size = float(size)
    for unit in ("B", "KB", "MB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def parse_name(raw):
    """Return a usable tutorial name, or raise ValueError explaining why not."""
    name = raw.strip().lower()
    if not name:
        raise ValueError("no tutorial name given")

    # The README tells people to copy the name off the site, so accept a
    # pasted URL too and take the first path segment from it.
    if name.startswith(("http://", "https://")):
        segments = [s for s in urllib.parse.urlparse(name).path.split("/") if s]
        if not segments:
            raise ValueError(f"could not find a tutorial name in {raw.strip()!r}")
        name = segments[0]

    if not VALID_NAME.match(name):
        raise ValueError(
            f"{name!r} is not a valid tutorial name; expected letters, digits, "
            "'_', '+' or '-' (for example 'python')"
        )
    return name


def report(block_count, block_size, total_size):
    """urlretrieve hook that redraws a progress line in place."""
    downloaded = block_count * block_size
    if total_size > 0:
        percent = min(100.0, downloaded * 100.0 / total_size)
        done = human(min(downloaded, total_size))
        line = f"\r  {percent:6.2f}%  {done} / {human(total_size)}"
    else:
        # No Content-Length, so a percentage would be meaningless.
        line = f"\r  {human(downloaded)} downloaded"
    sys.stdout.write(line)
    sys.stdout.flush()


def download(url, destination):
    """Download url to destination atomically. Raises on any failure."""
    directory = os.path.dirname(destination)
    if directory:
        os.makedirs(directory, exist_ok=True)

    # Write beside the target and rename on success, so a failed or
    # interrupted run never leaves a truncated file where a complete
    # PDF is expected.
    partial = destination + ".part"
    try:
        urllib.request.urlretrieve(url, partial, report)
        sys.stdout.write("\n")

        # A site restructure could answer 200 with an HTML error page;
        # saving that as a .pdf is the silent failure worth catching.
        with open(partial, "rb") as handle:
            if handle.read(5) != b"%PDF-":
                raise NotAPdfError(url)

        os.replace(partial, destination)
    except BaseException:
        # BaseException so an interrupt cleans up after itself too.
        if os.path.exists(partial):
            os.remove(partial)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Download a complete tutorial PDF from tutorialspoint.com.",
        epilog="example: %(prog)s python --output-dir ~/Downloads",
    )
    parser.add_argument(
        "tutorial",
        nargs="?",
        help="tutorial name as it appears in the site URL, e.g. 'python'. "
        "Prompted for when omitted.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        metavar="DIR",
        help="directory to save into (default: current directory)",
    )
    args = parser.parse_args(argv)

    raw = args.tutorial
    if raw is None:
        try:
            raw = input("Name of tutorial? (e.g. 'python') ")
        except (EOFError, KeyboardInterrupt):
            print(file=sys.stderr)
            return 130

    try:
        tutorial = parse_name(raw)
    except ValueError as exc:
        print(f"Error: {exc}.", file=sys.stderr)
        return 2

    url = f"{TLD}{tutorial}/{tutorial}_tutorial.pdf"
    destination = os.path.join(args.output_dir, f"{tutorial}_tutorial.pdf")

    print(f"Downloading {url}")
    try:
        download(url, destination)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(
                f"\nError: no PDF found for '{tutorial}' (HTTP 404). Check the "
                "name against the tutorial's URL on tutorialspoint.com.",
                file=sys.stderr,
            )
        else:
            print(
                f"\nError: server returned HTTP {exc.code} - {exc.reason}.",
                file=sys.stderr,
            )
        return 1
    except urllib.error.URLError as exc:
        print(
            f"\nError: could not reach tutorialspoint.com ({exc.reason}).",
            file=sys.stderr,
        )
        return 1
    except NotAPdfError:
        print(
            f"\nError: '{tutorial}' did not return a PDF. The site may have "
            "moved this tutorial.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130
    except OSError as exc:
        print(f"\nError: could not write {destination} ({exc}).", file=sys.stderr)
        return 1

    print(f"Saved {destination} ({human(os.path.getsize(destination))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
