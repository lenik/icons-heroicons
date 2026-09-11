# Heroicons Project - Claude AI Context

This document provides context for Claude AI when working with this project.

## Project Overview

This is a curated collection of Heroicons (from Tailwind Labs) organized in a structured format with tools for extraction, conversion, and asset generation.

## Directory Structure

- `orig/svg/` - Source SVG files organized by variant (normal, solid, mini, micro)
- `orig/jsx/` - React JSX components generated from SVG files
- `data/png/` - Generated PNG assets
- `scripts/` - Utility scripts for icon management

## Key Files

### Scripts

1. **`scripts/extract_icons.js`**
   - Node.js script to extract icons from heroicons repository
   - Maps heroicons structure to our structure:
     - `24/outline` → `normal/`
     - `24/solid` → `solid/`
     - `20/solid` → `mini/`
     - `16/solid` → `micro/`
   - Generates both SVG and JSX formats

2. **`scripts/svg2assets`**
   - Bash script for converting SVG to raster formats (PNG, JPG)
   - Uses shlib-import cliboot framework (aligned with sample.sh style)
   - Supports multiple converters: rsvg, imagemagick, inkscape
   - Features:
     - Size specification (NUM or WIDTHxHEIGHT)
     - Color modification (stroke/text)
     - Background color
     - Two output modes: name suffix or subdirectory-based

### Style Guidelines

- Scripts follow the pattern from `sample.sh`:
  - Uses `shlib-import cliboot` for option parsing
  - 4-space indentation for top-level declarations
  - `setopt()` function for option handling
  - `main()` function for core logic
  - `boot "$@"` at the end

## Icon Variants

- **normal**: 24px outline icons (324 icons)
- **solid**: 24px solid icons (324 icons)  
- **mini**: 20px solid icons (324 icons)
- **micro**: 16px solid icons (316 icons)

## Dependencies

- Node.js packages: `@svgr/core`, `@babel/core`, `@babel/plugin-transform-react-jsx`
- System tools: `rsvg-convert`, `imagemagick`, or `inkscape` (for svg2assets)

## Common Tasks

### Adding New Icons
1. Update heroicons repository if needed
2. Run `node scripts/extract_icons.js` to extract

### Converting Icons
- Use `scripts/svg2assets` with appropriate options
- Default output goes to same directory as input
- Use `-d` flag for subdirectory-based organization

### Modifying Scripts
- Follow `sample.sh` style conventions
- Use `opt_` prefix for option variables
- Use `_log1`, `_log2`, `_warn` for logging
- Use `quit` for error handling

## Notes

- SVG files are the source of truth
- JSX files are generated from SVG
- Generated assets (PNG/JPG) are in `.gitignore`
- The project uses standard bash scripting patterns with shlib-import

