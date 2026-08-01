#!/usr/bin/env python3
"""Build a minimal EPUB fixture for unpack-epub.py smoke test."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "mini-epub-build"
OUT = Path(__file__).resolve().parent / "mini-test.epub"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "META-INF").mkdir(exist_ok=True)
    (ROOT / "OEBPS").mkdir(exist_ok=True)
    (ROOT / "mimetype").write_text("application/epub+zip", encoding="ascii")
    (ROOT / "META-INF" / "container.xml").write_text(
        """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>""",
        encoding="utf-8",
    )
    (ROOT / "OEBPS" / "content.opf").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Mini Test Book</dc:title>
    <dc:creator>Fixture</dc:creator>
    <dc:identifier id="bookid">mini-test</dc:identifier>
  </metadata>
  <manifest>
    <item id="ch1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="ch1"/>
  </spine>
</package>""",
        encoding="utf-8",
    )
    (ROOT / "OEBPS" / "chapter1.xhtml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Chapter 1</title></head>
<body>
  <h1>The Blindfolded Team</h1>
  <p>Team members stumble without shared objectives.</p>
  <p><strong>Risk:</strong> silent perception gaps.</p>
  <p><strong>Action:</strong> forbid execution before alignment.</p>
</body>
</html>""",
        encoding="utf-8",
    )

    with zipfile.ZipFile(OUT, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for path in [
            ROOT / "META-INF" / "container.xml",
            ROOT / "OEBPS" / "content.opf",
            ROOT / "OEBPS" / "chapter1.xhtml",
        ]:
            zf.write(path, path.relative_to(ROOT).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
    print(OUT)


if __name__ == "__main__":
    main()
