# PiCode Prog

> An engineered fixed-pitch developer programming font with native coding ligatures, complete Central & Eastern European (ISO-8859-2 / CP-1250) Latin-2 coverage, and extended developer glyphs.

Developed by **Progressive Innovation LAB (PiLAB)** — [https://pilab.hu](https://pilab.hu).

---

## Highlights

- **100% Fixed Pitch**: Every character occupies an exact `640` units advance width (aspect ratio 0.640 relative to 1000 UPM, delivering optimal legibility and compact horizontal code density).
- **Four Styles**: Includes **Regular (400)**, **Bold (700)**, **Italic (400i)**, and **Bold Italic (700i)**.
- **Built-in Programming Ligatures (`calt` / `liga`)**:
  - Arrows & Lambdas: `->`, `-->`, `->>`, `->|`, `<-`, `<--`, `<<-`, `|<-`, `=>`, `==>`, `=>>`, `<=`, `<==`, `<=>`
  - Comparisons: `===`, `!==`, `==`, `!=`, `/=`, `<=`, `>=`, `:=`, `=:=`, `<>`
  - HTML / XML: `<!--`, `-->`, `</`, `/>`, `</>`
  - Logicals & Ranges: `&&`, `||`, `||=`, `&&=`, `::`, `:::`, `..`, `...`, `..<`, `??`, `?:`, `??=`
- **Full Latin-2 (Central & Eastern European)**: Complete native coverage for Hungarian (`ő`, `Ő`, `ű`, `Ű`, `á`, `é`, `í`, `ó`, `ö`, `ú`, `ü`), Polish (`ą`, `ć`, `ę`, `ł`, `ń`, `ó`, `ś`, `ź`, `ż`), Czech & Slovak (`č`, `ď`, `ě`, `ľ`, `ň`, `ř`, `š`, `ť`, `ž`, `ů`), Romanian (`ș`, `ț`, `ă`, `â`, `î`), and Croatian/Slovenian (`đ`, `ć`, `č`, `š`, `ž`).
- **Complete Nerd Font Developer Icons**: Contains 4,288 glyphs including Powerline symbols, Devicons, FontAwesome, and Octicons.
- **Dual Web Packaging**:
  - **Complete Editions**: Desktop `.otf` and full `.woff2` carrying the entire 4,288 glyph set (~1.1 MB).
  - **Web Subsets**: Streamlined `.woff2` containing all ASCII, Latin-1, Latin-2, Greek, Cyrillic, Box-Drawing, and coding ligatures at only **~33 KB** per style for instant webpage rendering.

---

## Repository Structure

```text
picode-prog-font/
├── fonts/
│   ├── PiCodeProg-Regular.otf                 # 3.3 MB (Complete Desktop OpenType Regular)
│   ├── PiCodeProg-Regular.woff2               # 1.1 MB (Complete Webfont Regular)
│   ├── PiCodeProg-Web-Regular.woff2           # 32.4 KB (Fast Web Subset Regular)
│   │
│   ├── PiCodeProg-Bold.otf                    # 3.3 MB (Complete Desktop OpenType Bold)
│   ├── PiCodeProg-Bold.woff2                  # 1.1 MB (Complete Webfont Bold)
│   ├── PiCodeProg-Web-Bold.woff2              # 32.9 KB (Fast Web Subset Bold)
│   │
│   ├── PiCodeProg-Italic.otf                  # 3.3 MB (Complete Desktop OpenType Italic)
│   ├── PiCodeProg-Italic.woff2                # 1.1 MB (Complete Webfont Italic)
│   ├── PiCodeProg-Web-Italic.woff2            # 33.8 KB (Fast Web Subset Italic)
│   │
│   ├── PiCodeProg-BoldItalic.otf              # 3.3 MB (Complete Desktop OpenType Bold Italic)
│   ├── PiCodeProg-BoldItalic.woff2            # 1.1 MB (Complete Webfont Bold Italic)
│   └── PiCodeProg-Web-BoldItalic.woff2        # 33.5 KB (Fast Web Subset Bold Italic)
├── css/
│   └── picode-prog.css                        # Ready-to-use @font-face CSS bundle
├── index.html                                 # Interactive live playground, ligatures & pangram showcase
├── build.py                                   # OpenType compiler & table sanitizer
└── README.md
```

---

## Web Integration

### 1. Link CSS
Add the stylesheet to your `<head>`:

```html
<link rel="stylesheet" href="css/picode-prog.css">
```

### 2. Apply in CSS

```css
/* Lightweight web edition (~33 KB) */
code, pre, textarea {
  font-family: 'PiCode Prog', monospace;
  font-feature-settings: 'calt' 1, 'liga' 1;
}

/* Complete edition with all 4,288 Nerd Font icons (~1.1 MB) */
.terminal-icons {
  font-family: 'PiCode Prog Complete', monospace;
}
```

---

## Editor Configuration

### VS Code / Cursor
Add to your `settings.json`:
```json
{
  "editor.fontFamily": "'PiCode Prog', monospace",
  "editor.fontSize": 15,
  "editor.lineHeight": 1.6,
  "editor.fontLigatures": true
}
```

### macOS Terminal / iTerm2 / Ghostty
1. Double-click the `.otf` files in `fonts/` to install in macOS **Font Book**.
2. Open Terminal Preferences → Profiles → Font → Select **PiCode Prog**.

---

## Build Pipeline

To recompile or customize the fonts:

```bash
# Requirements
pip install fonttools brotli

# Compile all styles (Regular, Bold, Italic, Bold Italic)
python3 build.py
```

---

## License

Developed by **Progressive Innovation LAB (PiLAB)**.  
Released under the [SIL Open Font License 1.1](https://scripts.sil.org/OFL) / MIT compatible terms for developer tools and applications. Free to use for personal and commercial software development.
