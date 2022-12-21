import fs from 'fs';

export default function CustomHotReload() {
  return {
    name: 'custom-hmr',
    enforce: 'pre',
    // HMR
    handleHotUpdate({ file }) {
      if (file.endsWith('.ftl')) {
        const data = fs.readFileSync('/workspace/src/translations/ftl.ts');
        if (data.toString() != '') {
          fs.writeFileSync('/workspace/src/translations/ftl.ts', data);
        }
      }
    },
  };
}
