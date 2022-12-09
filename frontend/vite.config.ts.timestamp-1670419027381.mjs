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

// vite.config.ts
var __vite_injected_original_import_meta_url = "file:///workspace/vite.config.ts";
var vite_config_default = defineConfig({
  plugins: [react(), visualizer({ template: "sunburst" }), CustomHotReload()],
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
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiLCAicGx1Z2lucy9mdGxIb3RSZWxvYWQudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvd29ya3NwYWNlXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvd29ya3NwYWNlL3ZpdGUuY29uZmlnLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy93b3Jrc3BhY2Uvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgcmVhY3QgZnJvbSAnQHZpdGVqcy9wbHVnaW4tcmVhY3QnO1xuaW1wb3J0IHsgdmlzdWFsaXplciB9IGZyb20gJ3JvbGx1cC1wbHVnaW4tdmlzdWFsaXplcic7XG5pbXBvcnQgeyBVUkwsIGZpbGVVUkxUb1BhdGggfSBmcm9tICd1cmwnO1xuaW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSAndml0ZSc7XG5cbmltcG9ydCBDdXN0b21Ib3RSZWxvYWQgZnJvbSAnLi9wbHVnaW5zL2Z0bEhvdFJlbG9hZCc7XG5cbi8vIGh0dHBzOi8vdml0ZWpzLmRldi9jb25maWcvXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xuICBwbHVnaW5zOiBbcmVhY3QoKSwgdmlzdWFsaXplcih7IHRlbXBsYXRlOiAnc3VuYnVyc3QnIH0pLCBDdXN0b21Ib3RSZWxvYWQoKV0sXG4gIGJ1aWxkOiB7XG4gICAgcm9sbHVwT3B0aW9uczoge1xuICAgICAgb3V0cHV0OiB7XG4gICAgICAgIG1hbnVhbENodW5rczoge1xuICAgICAgICAgIGFqdjogWydhanYnXSxcbiAgICAgICAgfSxcbiAgICAgIH0sXG4gICAgfSxcbiAgfSxcbiAgY3NzOiB7XG4gICAgbW9kdWxlczoge1xuICAgICAgZ2VuZXJhdGVTY29wZWROYW1lOiAnW2xvY2FsXS1baGFzaDpiYXNlNjQ6NV0nLFxuICAgICAgbG9jYWxzQ29udmVudGlvbjogJ2NhbWVsQ2FzZU9ubHknLFxuICAgIH0sXG4gIH0sXG4gIHNlcnZlcjoge1xuICAgIGZzOiB7XG4gICAgICBhbGxvdzogWycuLiddLFxuICAgIH0sXG4gIH0sXG4gIHJlc29sdmU6IHtcbiAgICBhbGlhczoge1xuICAgICAgJ0AvJzogYCR7ZmlsZVVSTFRvUGF0aChuZXcgVVJMKCcuL3NyYycsIGltcG9ydC5tZXRhLnVybCkpfS9gLFxuICAgIH0sXG4gIH0sXG59KTtcbiIsICJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiL3dvcmtzcGFjZS9wbHVnaW5zXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvd29ya3NwYWNlL3BsdWdpbnMvZnRsSG90UmVsb2FkLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy93b3Jrc3BhY2UvcGx1Z2lucy9mdGxIb3RSZWxvYWQudHNcIjtpbXBvcnQgZnMgZnJvbSAnZnMnO1xuXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBDdXN0b21Ib3RSZWxvYWQoKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ2N1c3RvbS1obXInLFxuICAgIGVuZm9yY2U6ICdwcmUnLFxuICAgIC8vIEhNUlxuICAgIGhhbmRsZUhvdFVwZGF0ZSh7IGZpbGUgfSkge1xuICAgICAgaWYgKGZpbGUuZW5kc1dpdGgoJy5mdGwnKSkge1xuICAgICAgICBjb25zdCBkYXRhID0gZnMucmVhZEZpbGVTeW5jKCcvd29ya3NwYWNlL3NyYy90cmFuc2xhdGlvbnMvZnRsLnRzJyk7XG4gICAgICAgIGZzLndyaXRlRmlsZVN5bmMoJy93b3Jrc3BhY2Uvc3JjL3RyYW5zbGF0aW9ucy9mdGwudHMnLCBkYXRhKTtcbiAgICAgIH1cbiAgICB9LFxuICB9O1xufVxuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUFnTixPQUFPLFdBQVc7QUFDbE8sU0FBUyxrQkFBa0I7QUFDM0IsU0FBUyxLQUFLLHFCQUFxQjtBQUNuQyxTQUFTLG9CQUFvQjs7O0FDSDZNLE9BQU8sUUFBUTtBQUUxTyxTQUFSLGtCQUFtQztBQUN4QyxTQUFPO0FBQUEsSUFDTCxNQUFNO0FBQUEsSUFDTixTQUFTO0FBQUEsSUFFVCxnQkFBZ0IsRUFBRSxLQUFLLEdBQUc7QUFDeEIsVUFBSSxLQUFLLFNBQVMsTUFBTSxHQUFHO0FBQ3pCLGNBQU0sT0FBTyxHQUFHLGFBQWEsb0NBQW9DO0FBQ2pFLFdBQUcsY0FBYyxzQ0FBc0MsSUFBSTtBQUFBLE1BQzdEO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFDRjs7O0FEZDRILElBQU0sMkNBQTJDO0FBUTdLLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVMsQ0FBQyxNQUFNLEdBQUcsV0FBVyxFQUFFLFVBQVUsV0FBVyxDQUFDLEdBQUcsZ0JBQWdCLENBQUM7QUFBQSxFQUMxRSxPQUFPO0FBQUEsSUFDTCxlQUFlO0FBQUEsTUFDYixRQUFRO0FBQUEsUUFDTixjQUFjO0FBQUEsVUFDWixLQUFLLENBQUMsS0FBSztBQUFBLFFBQ2I7QUFBQSxNQUNGO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFBQSxFQUNBLEtBQUs7QUFBQSxJQUNILFNBQVM7QUFBQSxNQUNQLG9CQUFvQjtBQUFBLE1BQ3BCLGtCQUFrQjtBQUFBLElBQ3BCO0FBQUEsRUFDRjtBQUFBLEVBQ0EsUUFBUTtBQUFBLElBQ04sSUFBSTtBQUFBLE1BQ0YsT0FBTyxDQUFDLElBQUk7QUFBQSxJQUNkO0FBQUEsRUFDRjtBQUFBLEVBQ0EsU0FBUztBQUFBLElBQ1AsT0FBTztBQUFBLE1BQ0wsTUFBTSxHQUFHLGNBQWMsSUFBSSxJQUFJLFNBQVMsd0NBQWUsQ0FBQztBQUFBLElBQzFEO0FBQUEsRUFDRjtBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
