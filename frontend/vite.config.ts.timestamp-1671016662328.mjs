// vite.config.ts
import react from "file:///workspace/.yarn/__virtual__/@vitejs-plugin-react-virtual-8c372023b7/2/home/node/.yarn/berry/cache/@vitejs-plugin-react-npm-2.2.0-a43e4127d1-9.zip/node_modules/@vitejs/plugin-react/dist/index.mjs";
import { visualizer } from "file:///workspace/.yarn/__virtual__/rollup-plugin-visualizer-virtual-204dd13248/2/home/node/.yarn/berry/cache/rollup-plugin-visualizer-npm-5.8.3-7aab3ac46d-9.zip/node_modules/rollup-plugin-visualizer/dist/plugin/index.js";
import { URL, fileURLToPath } from "url";
import { defineConfig } from "file:///workspace/.yarn/__virtual__/vite-virtual-dd80a7df83/2/home/node/.yarn/berry/cache/vite-npm-3.2.2-b6065be34d-9.zip/node_modules/vite/dist/node/index.js";

// plugins/ftlHotReload.ts
import fs from "fs";
function CustomHotReload() {
  return {
    name: "custom-hmr",
    enforce: "pre",
    handleHotUpdate({ file }) {
      if (file.endsWith(".ftl")) {
        const data = fs.readFileSync("/workspace/src/translations/ftl.ts");
        fs.writeFileSync("/workspace/src/translations/ftl.ts", data);
      }
    }
  };
}

// plugins/ftlDynamicLoad.ts
import fs2 from "fs";
var fileRegex = /\.ftl$/;
var translationsContents = {};
function FTLDynamicLoad() {
  return {
    name: "custom-bundler",
    enforce: "pre",
    async resolveId(source, importer, options) {
      const id = await this.resolve(source, importer, {
        skipSelf: true,
        ...options
      });
      if (fileRegex.test(id.id)) {
        const fileName = id.id.replace(/^.*[\\\/]/, "").split(".")[0];
        return { id: `${fileName}.ftl`, external: true };
      }
    },
    async load(id) {
      if (fileRegex.test(id)) {
        const fileName = id.replace(/^.*[\\\/]/, "").split(".")[0];
        const fileContent = await fs2.promises.readFile(id, "utf8");
        translationsContents[fileName] += fileContent;
        return `
                import { Bundles } from "@/translations/ftl.ts";
                import { FluentResource } from '@fluent/bundle';


                if ("${fileName}" in Bundles) {
                    Bundles["${fileName}"].addResource(new FluentResource("${fileContent}"))

                } else {
                    throw Error("No language in Bundles matches the filename ${fileName}")
                }
              `;
      }
    }
  };
}

// vite.config.ts
var __vite_injected_original_import_meta_url = "file:///workspace/vite.config.ts";
var vite_config_default = defineConfig({
  plugins: [react(), visualizer({ template: "sunburst" }), CustomHotReload(), FTLDynamicLoad()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          ajv: ["ajv"]
        }
      }
    }
  },
  css: {
    modules: {
      generateScopedName: "[local]-[hash:base64:5]",
      localsConvention: "camelCaseOnly"
    }
  },
  server: {
    fs: {
      allow: [".."]
    }
  },
  resolve: {
    alias: {
      "@/": `${fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url))}/`
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiLCAicGx1Z2lucy9mdGxIb3RSZWxvYWQudHMiLCAicGx1Z2lucy9mdGxEeW5hbWljTG9hZC50cyJdLAogICJzb3VyY2VzQ29udGVudCI6IFsiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIi93b3Jrc3BhY2VcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi93b3Jrc3BhY2Uvdml0ZS5jb25maWcudHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL3dvcmtzcGFjZS92aXRlLmNvbmZpZy50c1wiO2ltcG9ydCByZWFjdCBmcm9tICdAdml0ZWpzL3BsdWdpbi1yZWFjdCc7XG5pbXBvcnQgeyB2aXN1YWxpemVyIH0gZnJvbSAncm9sbHVwLXBsdWdpbi12aXN1YWxpemVyJztcbmltcG9ydCB7IFVSTCwgZmlsZVVSTFRvUGF0aCB9IGZyb20gJ3VybCc7XG5pbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJztcblxuaW1wb3J0IEN1c3RvbUhvdFJlbG9hZCBmcm9tICcuL3BsdWdpbnMvZnRsSG90UmVsb2FkJztcbmltcG9ydCBGVExEeW5hbWljTG9hZCBmcm9tICcuL3BsdWdpbnMvZnRsRHluYW1pY0xvYWQnO1xuXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcGx1Z2luczogW3JlYWN0KCksIHZpc3VhbGl6ZXIoeyB0ZW1wbGF0ZTogJ3N1bmJ1cnN0JyB9KSwgQ3VzdG9tSG90UmVsb2FkKCksIEZUTER5bmFtaWNMb2FkKCldLFxuICBidWlsZDoge1xuICAgIHJvbGx1cE9wdGlvbnM6IHtcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBtYW51YWxDaHVua3M6IHtcbiAgICAgICAgICBhanY6IFsnYWp2J10sXG4gICAgICAgIH0sXG4gICAgICB9LFxuICAgIH0sXG4gIH0sXG4gIGNzczoge1xuICAgIG1vZHVsZXM6IHtcbiAgICAgIGdlbmVyYXRlU2NvcGVkTmFtZTogJ1tsb2NhbF0tW2hhc2g6YmFzZTY0OjVdJyxcbiAgICAgIGxvY2Fsc0NvbnZlbnRpb246ICdjYW1lbENhc2VPbmx5JyxcbiAgICB9LFxuICB9LFxuICBzZXJ2ZXI6IHtcbiAgICBmczoge1xuICAgICAgYWxsb3c6IFsnLi4nXSxcbiAgICB9LFxuICB9LFxuICByZXNvbHZlOiB7XG4gICAgYWxpYXM6IHtcbiAgICAgICdALyc6IGAke2ZpbGVVUkxUb1BhdGgobmV3IFVSTCgnLi9zcmMnLCBpbXBvcnQubWV0YS51cmwpKX0vYCxcbiAgICB9LFxuICB9LFxufSk7XG4iLCAiY29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2Rpcm5hbWUgPSBcIi93b3Jrc3BhY2UvcGx1Z2luc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiL3dvcmtzcGFjZS9wbHVnaW5zL2Z0bEhvdFJlbG9hZC50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vd29ya3NwYWNlL3BsdWdpbnMvZnRsSG90UmVsb2FkLnRzXCI7aW1wb3J0IGZzIGZyb20gJ2ZzJztcblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gQ3VzdG9tSG90UmVsb2FkKCkge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdjdXN0b20taG1yJyxcbiAgICBlbmZvcmNlOiAncHJlJyxcbiAgICAvLyBITVJcbiAgICBoYW5kbGVIb3RVcGRhdGUoeyBmaWxlIH0pIHtcbiAgICAgIGlmIChmaWxlLmVuZHNXaXRoKCcuZnRsJykpIHtcbiAgICAgICAgY29uc3QgZGF0YSA9IGZzLnJlYWRGaWxlU3luYygnL3dvcmtzcGFjZS9zcmMvdHJhbnNsYXRpb25zL2Z0bC50cycpO1xuICAgICAgICBmcy53cml0ZUZpbGVTeW5jKCcvd29ya3NwYWNlL3NyYy90cmFuc2xhdGlvbnMvZnRsLnRzJywgZGF0YSk7XG4gICAgICB9XG4gICAgfSxcbiAgfTtcbn1cbiIsICJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiL3dvcmtzcGFjZS9wbHVnaW5zXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvd29ya3NwYWNlL3BsdWdpbnMvZnRsRHluYW1pY0xvYWQudHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL3dvcmtzcGFjZS9wbHVnaW5zL2Z0bER5bmFtaWNMb2FkLnRzXCI7aW1wb3J0IGZzIGZyb20gJ2ZzJztcbmltcG9ydCB7IFBsdWdpbiB9IGZyb20gJ3ZpdGUnO1xuXG5jb25zdCBmaWxlUmVnZXggPSAvXFwuZnRsJC87XG5jb25zdCBvdXRwdXRGaWxlID0gJ3RyYW5zbGF0aW9ucy5qcyc7XG5cbmNvbnN0IHRyYW5zbGF0aW9uc0NvbnRlbnRzOiBSZWNvcmQ8c3RyaW5nLCBzdHJpbmc+ID0ge307XG5cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIEZUTER5bmFtaWNMb2FkKCk6IFBsdWdpbiB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ2N1c3RvbS1idW5kbGVyJyxcbiAgICBlbmZvcmNlOiAncHJlJyxcbiAgICAvLyBITVJcbiAgICBhc3luYyByZXNvbHZlSWQoc291cmNlLCBpbXBvcnRlciwgb3B0aW9ucykge1xuICAgICAgY29uc3QgaWQgPSBhd2FpdCB0aGlzLnJlc29sdmUoc291cmNlLCBpbXBvcnRlciwge1xuICAgICAgICBza2lwU2VsZjogdHJ1ZSxcbiAgICAgICAgLi4ub3B0aW9ucyxcbiAgICAgIH0pO1xuICAgICAgaWYgKGZpbGVSZWdleC50ZXN0KGlkLmlkKSkge1xuICAgICAgICBjb25zdCBmaWxlTmFtZSA9IGlkLmlkLnJlcGxhY2UoL14uKltcXFxcXFwvXS8sICcnKS5zcGxpdCgnLicpWzBdO1xuICAgICAgICByZXR1cm4geyBpZDogYCR7ZmlsZU5hbWV9LmZ0bGAsIGV4dGVybmFsOiB0cnVlIH07XG4gICAgICB9XG4gICAgfSxcblxuICAgIGFzeW5jIGxvYWQoaWQ6IHN0cmluZykge1xuICAgICAgaWYgKGZpbGVSZWdleC50ZXN0KGlkKSkge1xuICAgICAgICBjb25zdCBmaWxlTmFtZSA9IGlkLnJlcGxhY2UoL14uKltcXFxcXFwvXS8sICcnKS5zcGxpdCgnLicpWzBdO1xuXG4gICAgICAgIGNvbnN0IGZpbGVDb250ZW50ID0gYXdhaXQgZnMucHJvbWlzZXMucmVhZEZpbGUoaWQsICd1dGY4Jyk7XG5cbiAgICAgICAgdHJhbnNsYXRpb25zQ29udGVudHNbZmlsZU5hbWVdICs9IGZpbGVDb250ZW50O1xuICAgICAgICByZXR1cm4gYFxuICAgICAgICAgICAgICAgIGltcG9ydCB7IEJ1bmRsZXMgfSBmcm9tIFwiQC90cmFuc2xhdGlvbnMvZnRsLnRzXCI7XG4gICAgICAgICAgICAgICAgaW1wb3J0IHsgRmx1ZW50UmVzb3VyY2UgfSBmcm9tICdAZmx1ZW50L2J1bmRsZSc7XG5cblxuICAgICAgICAgICAgICAgIGlmIChcIiR7ZmlsZU5hbWV9XCIgaW4gQnVuZGxlcykge1xuICAgICAgICAgICAgICAgICAgICBCdW5kbGVzW1wiJHtmaWxlTmFtZX1cIl0uYWRkUmVzb3VyY2UobmV3IEZsdWVudFJlc291cmNlKFwiJHtmaWxlQ29udGVudH1cIikpXG5cbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICB0aHJvdyBFcnJvcihcIk5vIGxhbmd1YWdlIGluIEJ1bmRsZXMgbWF0Y2hlcyB0aGUgZmlsZW5hbWUgJHtmaWxlTmFtZX1cIilcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIGA7XG4gICAgICB9XG4gICAgfSxcbiAgfTtcbn1cbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBZ04sT0FBTyxXQUFXO0FBQ2xPLFNBQVMsa0JBQWtCO0FBQzNC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
