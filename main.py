"""One-line office joke entry for make.fun.

Writes the chosen joke to ``entry.txt`` next to this file (and to
``/output/entry.txt`` when that directory exists, which is where the
competition harness reads it from).

Standard library only; fully deterministic: the same input always
produces the same bytes.
"""

import hashlib
import os

JOKE = (
    "There's a yoghurt in the shared fridge from 2019 \u2014 "
    "it's now technically our longest-serving employee."
)


def validate_entry(text):
    """Check the entry against the competition gate.

    The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
    characters, not only white space. The joke must also be a single
    line (no newline characters).
    """
    if not isinstance(text, str):
        return False, "entry is not a string"
    if not text.strip():
        return False, "entry is empty or only white space"
    if not 1 <= len(text) <= 200:
        return False, "entry is %d characters, must be 1-200" % len(text)
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not valid UTF-8 text"
    return True, "valid (%d characters)" % len(text)


def write_entry(path):
    """Write the joke to *path*, read it back and verify byte-identical."""
    ok, reason = validate_entry(JOKE)
    if not ok:
        raise ValueError("invalid entry: %s" % reason)
    data = JOKE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data:
        raise IOError("read-back mismatch for %s" % path)
    return hashlib.sha256(data).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    paths = [os.path.join(here, "entry.txt")]
    output_dir = "/output"
    if os.path.isdir(output_dir):
        paths.append(os.path.join(output_dir, "entry.txt"))
    for path in paths:
        digest = write_entry(path)
        print("wrote %s (sha256 %s)" % (path, digest))
    print("entry: %s" % JOKE)


if __name__ == "__main__":
    main()
