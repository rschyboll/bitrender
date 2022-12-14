import fs from 'fs';
import { Plugin } from 'vite';

const fileRegex = /\.ftl$/;

export default function FTLDynamicLoad(): Plugin {
  return {
    name: 'custom-bundler',
    enforce: 'post',

    async load(id: string) {
      if (fileRegex.test(id)) {
        const fileName = id.replace(/^.*[\\\/]/, '').split('.')[0];

        const fileContent = await fs.promises.readFile(id, 'utf8');

        return `
                import { Bundles } from "@/translations/ftl.ts";
                import { FluentResource } from '@fluent/bundle';


                if ("${fileName}" in Bundles) {
                    Bundles["${fileName}"].addResource(new FluentResource(\`${fileContent}\`))

                } else {
                    throw Error("No language in Bundles matches the filename ${fileName}")
                }
              `;
      }
    },
  };
}
