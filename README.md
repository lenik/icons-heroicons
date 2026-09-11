# Heroicons Icon Library

This repository contains extracted Heroicons in multiple formats and sizes, along with tools for conversion and management.

## Structure

```
heroicons/
├── orig/
│   ├── svg/      # SVG source files
│   │   ├── normal/   # 24px outline icons
│   │   ├── solid/    # 24px solid icons
│   │   ├── mini/     # 20px solid icons
│   │   └── micro/    # 16px solid icons
│   └── jsx/      # React JSX components (same structure as svg/)
├── data/
│   └── png/      # Generated PNG assets
├── debian/
├── meson.build
└── scripts/      # Utility scripts
```

## Installation

### Prerequisites

- Node.js (for extract_icons.js)
- One of the following SVG converters:
  - `rsvg-convert` (librsvg) - recommended
  - `imagemagick` (convert command)
  - `inkscape`

### Setup

```bash
npm install
```

### System Installation

Install scripts, man pages, and bash completions using the Makefile:

```bash
# Install to /usr/local (default)
make install

# Or specify custom prefix
make install PREFIX=/usr

# Uninstall
make uninstall
```

### Debian Package

Build a Debian package:

```bash
dpkg-buildpackage -us -uc
```

## Usage

### Extracting Icons

To extract icons from the heroicons repository:

```bash
node scripts/extract_icons.js
```

This will:
1. Clone the heroicons repository (if needed)
2. Extract SVG files to `orig/svg/{normal,solid,mini,micro}/`
3. Convert SVG to JSX components in `orig/jsx/{normal,solid,mini,micro}/`

### Building Assets

Build PNG and JPG assets for all icons using the Makefile:

```bash
# Build both PNG and JPG assets
make build-assets

# Build PNG assets only
make build-png

# Build JPG assets only
make build-jpg

# Clean generated assets
make clean
```

The build process uses `batch-convert.sh` which automatically selects appropriate sizes for each icon variant.

### Converting SVG to Image Assets

Use `svg2assets` to convert SVG files to PNG, JPG, or other formats:

```bash
# Basic usage - convert to PNG with default sizes
scripts/svg2assets orig/svg/normal/map.svg

# Specify output type and directory
scripts/svg2assets -t png -o data/png -s 8,16,24 orig/svg/normal/map.svg
# Generates: data/png/normal/map-8x8.png, ...

# Use subdirectories for sizes
scripts/svg2assets -t jpg -o images -d -s 8,16,24 -c red orig/svg/normal/map.svg

# Custom colors and background
scripts/svg2assets -t png -c "#FF0000" -b "#FFFFFF" -s 32,64 orig/svg/solid/home.svg
```

### svg2assets Options

```
-t, --type TYPE          File type to convert (png default, jpg, jpeg)
-C, --converter NAME     Converter to use (rsvg default, imagemagick, inkscape)
-o, --outdir DIR         Where to save the output (default: same as input directory)
-c, --color COLOR        Color of stroke/text
-b, --background COLOR   Color of background
-s, --size SIZES         Sizes, can be NUM or WIDTHxHEIGHT (default: 16,24,48,64,128,256)
-d, --subdirs            Use subdirs instead of name suffix
-q, --quiet              Quiet mode
-v, --verbose            Verbose mode
-h, --help               Show help
    --version            Show version
```

## Documentation

### Man Pages

Man pages are available for the command-line tools:

```bash
man svg2assets
man batch-convert.sh
```

### Bash Completion

Bash completion is available for `svg2assets` and `batch-convert.sh`. After installation, completion will be automatically loaded. To manually enable:

```bash
source /usr/local/share/bash-completion/completions/svg2assets
source /usr/local/share/bash-completion/completions/batch-convert.sh
```

## Icon Variants

- **normal**: 24px outline icons (324 icons)
- **solid**: 24px solid icons (324 icons)
- **mini**: 20px solid icons (324 icons)
- **micro**: 16px solid icons (316 icons)

## License

The Heroicons SVG icons are licensed under the MIT License by Tailwind Labs Inc. See the original [Heroicons repository](https://github.com/tailwindlabs/heroicons) for details.

The scripts, tools, and packaging in this repository are Copyright (c) 2026 Lenik and are licensed under the GNU General Public License, version 3 or later.

## Source

Icons are extracted from [Tailwind Labs Heroicons](https://heroicons.com/).

