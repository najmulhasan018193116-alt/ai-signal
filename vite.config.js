import { defineConfig } from 'vite';
import javascriptObfuscator from 'vite-plugin-javascript-obfuscator';
import { resolve, extname } from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// এই ফাংশনটি আপনার প্রজেক্টের সব HTML ফাইল (যেমন: gfuhg, admin-panel ইত্যাদি) অটোমেটিক খুঁজে বের করবে
const getHtmlInputs = () => {
  const inputs = {};
  const files = fs.readdirSync(__dirname);
  files.forEach(file => {
    if (extname(file) === '.html') {
      const name = file.replace('.html', '');
      inputs[name] = resolve(__dirname, file);
    }
  });
  return inputs;
};

export default defineConfig({
  plugins: [
    javascriptObfuscator({
      compact: true,
      controlFlowFlattening: false, // Vercel-এর ফ্রি সার্ভারে দ্রুত বিল্ড করার জন্য এটি false রাখা হয়েছে
      deadCodeInjection: false,
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
    })
  ],
  build: {
    minify: 'terser',
    rollupOptions: {
      input: getHtmlInputs() // সব পেজ একসাথে বিল্ড হবে, কোনো 404 আসবে না
    },
    outDir: 'dist'
  }
});
 
