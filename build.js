import fs from 'fs';
import path from 'path';
import JavaScriptObfuscator from 'javascript-obfuscator';
import { minify } from 'html-minifier-terser';

const ignoreList = [
  'node_modules',
  'dist',
  '.git',
  '.github',
  'package.json',
  'package-lock.json',
  'vercel.json',
  'build.js',
  'vite.config.js',
  'api'
];

// ফাস্ট বিল্ডের জন্য অপ্টিমাইজড হিজিবিজি সেটিংস
const obfuscatorOptions = {
  compact: true,
  controlFlowFlattening: false, // এটি অফ করা হলো বিল্ড স্পিড ১০০ গুণ বাড়ানোর জন্য
  deadCodeInjection: false,     // এটি অফ করা হলো যাতে Vercel হ্যাং না করে
  debugProtection: true,
  debugProtectionInterval: 4000,
  disableConsoleOutput: true,
  identifierNamesGenerator: 'hexadecimal',
  log: false,
  numbersToExpressions: true,
  renameGlobals: true,
  selfDefending: true,
  simplify: true,
  splitStrings: true,
  stringArray: true,
  stringArrayCallsTransform: true,
  stringArrayEncoding: ['rc4'],
  stringArrayIndexShift: true,
  stringArrayRotate: true,
  stringArrayShuffle: true,
  stringArrayWrappersCount: 2,
  stringArrayWrappersChaining: true,
  stringArrayWrappersType: 'variable',
  stringArrayThreshold: 0.8,
  transformObjectKeys: true,
  unicodeEscapeSequence: true
};

function ensureDirectoryExistence(filePath) {
  const dirname = path.dirname(filePath);
  if (fs.existsSync(dirname)) return true;
  ensureDirectoryExistence(dirname);
  fs.mkdirSync(dirname);
}

async function processFile(sourcePath, destPath) {
  const ext = path.extname(sourcePath).toLowerCase();
  
  if (ext === '.html') {
    let content = fs.readFileSync(sourcePath, 'utf8');
    const scriptRegex = /(<script\b[^>]*>)([\s\S]*?)(<\/script>)/gi;
    
    content = content.replace(scriptRegex, (match, openTag, scriptContent, closeTag) => {
      if (/src\s*=/i.test(openTag)) return match;
      if (!scriptContent.trim()) return match;
      try {
        const obfuscated = JavaScriptObfuscator.obfuscate(scriptContent, obfuscatorOptions).getObfuscatedCode();
        return `${openTag}${obfuscated}${closeTag}`;
      } catch (err) {
        return match;
      }
    });

    try {
      content = await minify(content, {
        collapseWhitespace: true,
        removeComments: true,
        minifyCSS: true,
        minifyJS: false
      });
    } catch (err) {}
    fs.writeFileSync(destPath, content, 'utf8');
  } else if (ext === '.js') {
    const content = fs.readFileSync(sourcePath, 'utf8');
    try {
      const obfuscated = JavaScriptObfuscator.obfuscate(content, obfuscatorOptions).getObfuscatedCode();
      fs.writeFileSync(destPath, obfuscated, 'utf8');
    } catch (err) {
      fs.writeFileSync(destPath, content, 'utf8');
    }
  } else {
    fs.copyFileSync(sourcePath, destPath);
  }
}

async function walkAndProcess(currentDir, targetDir) {
  const files = fs.readdirSync(currentDir);
  for (const file of files) {
    if (ignoreList.includes(file)) continue;
    
    const sourcePath = path.join(currentDir, file);
    const destPath = path.join(targetDir, file);
    const stat = fs.statSync(sourcePath);
    
    if (stat.isDirectory()) {
      fs.mkdirSync(destPath, { recursive: true });
      await walkAndProcess(sourcePath, destPath);
    } else {
      ensureDirectoryExistence(destPath);
      await processFile(sourcePath, destPath);
    }
  }
}

async function start() {
  console.log('Starting optimized build process...');
  const distDir = path.join(process.cwd(), 'dist');
  
  if (fs.existsSync(distDir)) {
    fs.rmSync(distDir, { recursive: true, force: true });
  }
  fs.mkdirSync(distDir, { recursive: true });
  
  await walkAndProcess(process.cwd(), distDir);
  console.log('Build completed successfully!');
}

start().catch(err => {
  process.exit(1);
});

