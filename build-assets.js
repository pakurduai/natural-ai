const fs = require('fs');
const path = require('path');

const srcDir = __dirname;
const destDir = path.join(__dirname, 'www');

// Helper to recursively copy directories
function copyDirSync(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Clean and recreate destination directory
if (fs.existsSync(destDir)) {
  fs.rmSync(destDir, { recursive: true, force: true });
}
fs.mkdirSync(destDir, { recursive: true });

// Read all files in source directory
const files = fs.readdirSync(srcDir);

files.forEach(file => {
  const srcPath = path.join(srcDir, file);
  const stat = fs.statSync(srcPath);

  if (stat.isFile()) {
    const ext = path.extname(file).toLowerCase();
    const isWebFile = [
      '.html', '.css', '.js', '.json',
      '.png', '.jpg', '.jpeg', '.gif', '.svg',
      '.mp3', '.wav', '.ico'
    ].includes(ext);

    // Keep package.json and capacitor configs out of www
    const isCapacitorConfig = [
      'package.json', 'package-lock.json',
      'capacitor.config.json', 'capacitor.config.ts',
      'build-assets.js'
    ].includes(file);

    if (isWebFile && !isCapacitorConfig) {
      fs.copyFileSync(srcPath, path.join(destDir, file));
      console.log(`Copied file: ${file}`);
    }
  } else if (stat.isDirectory()) {
    // Copy specific directories that contain web assets
    if (file === 'audio') {
      copyDirSync(srcPath, path.join(destDir, file));
      console.log(`Copied directory: ${file}`);
    }
  }
});

console.log('Web assets build complete!');
