import os.path
import pattern.text

from pattern.helpers import decode_string
from codecs import BOM_UTF8

BOM_UTF8 = BOM_UTF8.decode("utf-8")
decode_utf8 = decode_string


def _read(path, encoding="utf-8", comment=";;;"):
    """Returns an iterator over the lines in the file at the given path,
    strippping comments and decoding each line to Unicode."""

    if path:
        if isinstance(path, str) and os.path.exists(path):
            # From file path.
            f = open(path, "r", encoding="utf-8")
        elif isinstance(path, str):
            # From string.
            f = path.splitlines()
        else:
            # From file or buffer.
            f = path
        for i, line in enumerate(f):
            line = line.strip(BOM_UTF8) if i == 0 and isinstance(line, str) else line
            line = line.strip()
            line = decode_utf8(line, encoding)
            if not line or (comment and line.startswith(comment)):
                continue
            try:
                yield line
            except StopIteration:
                return


pattern.text._read = _read
