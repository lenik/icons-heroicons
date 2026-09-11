const fs = require('fs').promises
const path = require('path')
const { promisify } = require('util')
const { transform } = require('@svgr/core')
const babel = require('@babel/core')

// Mapping from heroicons structure to our structure
const iconMapping = {
  '24/outline': 'normal',
  '24/solid': 'solid',
  '20/solid': 'mini',
  '16/solid': 'micro',
}

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true })
}

async function copySvgFiles(sourceDir, destDir) {
  await ensureDir(destDir)
  const files = await fs.readdir(sourceDir)
  
  for (const file of files) {
    if (file.endsWith('.svg')) {
      const sourcePath = path.join(sourceDir, file)
      const destPath = path.join(destDir, file)
      await fs.copyFile(sourcePath, destPath)
    }
  }
}

async function convertSvgToJsx(sourceDir, destDir) {
  await ensureDir(destDir)
  const files = await fs.readdir(sourceDir)
  
  for (const file of files) {
    if (file.endsWith('.svg')) {
      const svgPath = path.join(sourceDir, file)
      const svgContent = await fs.readFile(svgPath, 'utf8')
      
      // Extract component name from filename (e.g., "academic-cap.svg" -> "AcademicCapIcon")
      const componentName = file
        .replace(/\.svg$/, '')
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('') + 'Icon'
      
      // Convert SVG to React component using svgr
      let component = await transform(svgContent, { 
        ref: true, 
        titleProp: true
      }, { componentName })
      
      // Transform JSX to ensure compatibility
      let { code } = await babel.transformAsync(component, {
        plugins: [[require('@babel/plugin-transform-react-jsx'), { useBuiltIns: true, runtime: 'automatic' }]],
      })
      
      // Save as .jsx file (but keep the original SVG filename pattern)
      const jsxFileName = file.replace('.svg', '.jsx')
      const jsxPath = path.join(destDir, jsxFileName)
      await fs.writeFile(jsxPath, code, 'utf8')
    }
  }
}

async function main() {
  // Prefer packaging checkout: orig/ is upstream tailwindlabs/heroicons
  const upstreamOptimized = path.join(__dirname, '..', 'orig', 'optimized')
  let optimizedDir = upstreamOptimized
  try {
    await fs.access(optimizedDir)
  } catch {
    optimizedDir = path.join(__dirname, 'temp_heroicons', 'optimized')
  }

  console.log('Extracting heroicons from', optimizedDir, '→ data/{svg,jsx}/...')

  for (const [heroiconsPath, styleName] of Object.entries(iconMapping)) {
    const sourceDir = path.join(optimizedDir, heroiconsPath)

    try {
      await fs.access(sourceDir)
    } catch (err) {
      console.warn(`Warning: ${sourceDir} does not exist, skipping...`)
      continue
    }

    const svgDestDir = path.join(__dirname, '..', 'data', 'svg', styleName)
    console.log(`Copying SVG files from ${heroiconsPath} to data/svg/${styleName}...`)
    await copySvgFiles(sourceDir, svgDestDir)

    const jsxDestDir = path.join(__dirname, '..', 'data', 'jsx', styleName)
    console.log(`Converting SVG files from ${heroiconsPath} to data/jsx/${styleName}...`)
    await convertSvgToJsx(sourceDir, jsxDestDir)
  }

  console.log('Extraction complete!')
}

main().catch(console.error)

