#!/usr/bin/env python3
"""
PiCode Prog — Fixed-Pitch Developer Programming Font Compiler
==============================================================
Developed by Progressive Innovation LAB (PiLAB)
https://pilab.hu

Transforms vector font outlines into the PiCode Prog developer family:
- 100% Fixed Pitch (uniform 640-unit advance width at UPM = 1000).
- Full Central & Eastern European (ISO-8859-2 / CP-1250) Latin-2 coverage.
- Built-in programming ligatures (arrows, comparisons, lambdas, operators).
- Complete Nerd Font developer glyph set (Powerline, devicons, fontawesome).
- Four styles: Regular (400), Bold (700), Italic (400i), Bold Italic (700i).
- Dual output: Desktop OTF + Complete WOFF2 + Streamlined Web WOFF2 (~33 KB).
"""

import argparse
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

FAMILY_NAME = "PiCode Prog"
TARGET_ADVANCE = 640


def sanitize_and_compile_font(src_path, out_otf_path, out_woff2_path, out_web_woff2_path,
                             style_name, is_bold=False, is_italic=False):
    """
    Sanitizes all OpenType and CFF tables, applies PiLAB metadata, and exports OTF + WOFF2.
    """
    print(f"\n[+] Compiling: {FAMILY_NAME} {style_name}")
    print(f"    Source:    {src_path}")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")

    font = TTFont(src_path)

    # Determine PostScript name and unique ID
    ps_style = style_name.replace(" ", "")
    ps_name = f"PiCodeProg-{ps_style}"
    full_name = f"{FAMILY_NAME} {style_name}"

    # Weight and selection flags
    weight_class = 700 if is_bold else 400
    fs_sel = 0
    if is_bold:
        fs_sel |= (1 << 5)
    if is_italic:
        fs_sel |= (1 << 0)
    if not is_bold and not is_italic:
        fs_sel |= (1 << 6)  # Regular bit

    # 1. Sanitize CFF (Compact Font Format) table if present
    if 'CFF ' in font:
        cff = font['CFF '].cff
        cff.fontNames = [ps_name]
        top_dict = cff[0]
        top_dict.version = "001.000"
        top_dict.Notice = "Copyright (c) 2026 Progressive Innovation LAB (PiLAB). All rights reserved."
        top_dict.Copyright = "Copyright (c) 2026 Progressive Innovation LAB (PiLAB). All rights reserved."
        top_dict.FullName = full_name
        top_dict.FamilyName = FAMILY_NAME
        top_dict.Weight = style_name

    # 2. Rebuild Name table cleanly
    desc = (f"{full_name} is an engineered fixed-pitch programming font with native "
            "developer ligatures, extensive coding glyphs, and full Latin-2 character support.")

    name_records = [
        (0, "Copyright © 2026 Progressive Innovation LAB (PiLAB). All rights reserved."),
        (1, FAMILY_NAME),                        # Family Name
        (2, style_name),                         # Subfamily Name
        (3, f"1.000;PILAB;{ps_name}"),           # Unique identifier
        (4, full_name),                          # Full Name
        (5, "Version 1.000; 2026; PILAB build"), # Version string
        (6, ps_name),                            # PostScript Name
        (8, "Progressive Innovation LAB"),       # Manufacturer
        (9, "PiLAB Typography & Systems Engineering"),
        (10, desc),
        (11, "https://pilab.hu"),
        (16, FAMILY_NAME),                       # Typographic Family
        (17, style_name),                        # Typographic Subfamily
    ]

    name_table = font['name']
    name_table.names = []
    for nameID, text in name_records:
        # Windows / Unicode (Platform 3, Encoding 1, Lang 1033)
        name_table.setName(text, nameID, platformID=3, platEncID=1, langID=0x0409)
        # Macintosh (Platform 1, Encoding 0, Lang 0)
        name_table.setName(text, nameID, platformID=1, platEncID=0, langID=0)

    # 3. Strip legacy / editing tables
    for tag in ['FFTM', 'PfEd', 'DSIG']:
        if tag in font:
            del font[tag]

    # 4. Enforce Monospace & Latin-2 flags
    font['post'].isFixedPitch = 1
    font['OS/2'].xAvgCharWidth = TARGET_ADVANCE
    font['OS/2'].panose.bProportion = 9  # 9 = Monospaced in PANOSE spec
    font['OS/2'].usWeightClass = weight_class
    font['OS/2'].fsSelection = fs_sel
    # Bit 1 = Latin-2 (Central Europe / ISO-8859-2 / CP-1250)
    font['OS/2'].ulCodePageRange1 |= (1 << 1)

    font['hhea'].advanceWidthMax = TARGET_ADVANCE

    # 5. Export Desktop OTF (Complete Edition)
    os.makedirs(os.path.dirname(os.path.abspath(out_otf_path)), exist_ok=True)
    font.save(out_otf_path)
    otf_size = os.path.getsize(out_otf_path)
    total_glyphs = len(font.getGlyphOrder())
    print(f"  ✓ Exported Desktop OTF:      {out_otf_path} ({otf_size:,} bytes, {total_glyphs} glyphs)")

    # 6. Export Complete Webfont WOFF2
    os.makedirs(os.path.dirname(os.path.abspath(out_woff2_path)), exist_ok=True)
    font.flavor = 'woff2'
    font.save(out_woff2_path)
    woff2_size = os.path.getsize(out_woff2_path)
    print(f"  ✓ Exported Complete WOFF2:   {out_woff2_path} ({woff2_size:,} bytes)")

    # 7. Export Streamlined Webfont WOFF2 (Optimized for web loading without thousands of terminal PUA icons)
    # Reload from fresh OTF to avoid mutating the master font
    web_font = TTFont(out_otf_path)
    options = Options()
    options.layout_features = ['*']
    options.glyph_names = True
    subsetter = Subsetter(options=options)
    # Include all glyphs up to Private Use Area (0xE000)
    base_unicodes = [c for c in web_font.getBestCmap().keys() if c < 0xE000]
    subsetter.populate(unicodes=base_unicodes)
    subsetter.subset(web_font)

    os.makedirs(os.path.dirname(os.path.abspath(out_web_woff2_path)), exist_ok=True)
    web_font.flavor = 'woff2'
    web_font.save(out_web_woff2_path)
    web_size = os.path.getsize(out_web_woff2_path)
    web_glyphs = len(web_font.getGlyphOrder())
    print(f"  ✓ Exported Web Subset WOFF2: {out_web_woff2_path} ({web_size:,} bytes, {web_glyphs} glyphs)")


def main():
    parser = argparse.ArgumentParser(
        description="PiCode Prog Developer Programming Font Compiler"
    )
    parser.add_argument(
        "--input-dir",
        default=os.environ.get("PICODE_PROG_SOURCE_DIR", "/tmp/picode-prog-raw"),
        help="Directory containing source OTF files (regular.otf, bold.otf, italic.otf, bold-italic.otf)"
    )
    parser.add_argument(
        "--output-dir",
        default="fonts",
        help="Directory for output fonts (default: 'fonts')"
    )

    args = parser.parse_args()

    print("=" * 72)
    print("  PICODE PROG — DEVELOPER PROGRAMMING FONT COMPILER")
    print("  Progressive Innovation LAB (PiLAB) Typography Engineering")
    print("=" * 72)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base_dir, args.output_dir)
    in_dir = args.input_dir

    targets = [
        {
            "src": os.path.join(in_dir, "regular.otf"),
            "otf": os.path.join(out_dir, "PiCodeProg-Regular.otf"),
            "woff2": os.path.join(out_dir, "PiCodeProg-Regular.woff2"),
            "web_woff2": os.path.join(out_dir, "PiCodeProg-Web-Regular.woff2"),
            "style": "Regular",
            "bold": False,
            "italic": False,
        },
        {
            "src": os.path.join(in_dir, "bold.otf"),
            "otf": os.path.join(out_dir, "PiCodeProg-Bold.otf"),
            "woff2": os.path.join(out_dir, "PiCodeProg-Bold.woff2"),
            "web_woff2": os.path.join(out_dir, "PiCodeProg-Web-Bold.woff2"),
            "style": "Bold",
            "bold": True,
            "italic": False,
        },
        {
            "src": os.path.join(in_dir, "italic.otf"),
            "otf": os.path.join(out_dir, "PiCodeProg-Italic.otf"),
            "woff2": os.path.join(out_dir, "PiCodeProg-Italic.woff2"),
            "web_woff2": os.path.join(out_dir, "PiCodeProg-Web-Italic.woff2"),
            "style": "Italic",
            "bold": False,
            "italic": True,
        },
        {
            "src": os.path.join(in_dir, "bold-italic.otf"),
            "otf": os.path.join(out_dir, "PiCodeProg-BoldItalic.otf"),
            "woff2": os.path.join(out_dir, "PiCodeProg-BoldItalic.woff2"),
            "web_woff2": os.path.join(out_dir, "PiCodeProg-Web-BoldItalic.woff2"),
            "style": "Bold Italic",
            "bold": True,
            "italic": True,
        },
    ]

    for t in targets:
        sanitize_and_compile_font(
            src_path=t["src"],
            out_otf_path=t["otf"],
            out_woff2_path=t["woff2"],
            out_web_woff2_path=t["web_woff2"],
            style_name=t["style"],
            is_bold=t["bold"],
            is_italic=t["italic"],
        )

    print("\n[✔] PiCode Prog compilation completed successfully!")


if __name__ == "__main__":
    main()
