// eslint.config.js

// import { FlatCompat } from "@eslint/eslintrc";
// import path from "path";
// import { fileURLToPath } from "url";
//
// import js from "@eslint/js";
// import ts from "@typescript-eslint/eslint-plugin";
// import tsParser from "@typescript-eslint/parser";
// import vue from "eslint-plugin-vue";
// import importPlugin from "eslint-plugin-import";
// import prettier from "eslint-config-prettier";
//
// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);
// const compat = new FlatCompat({ baseDirectory: __dirname });
//
// export default [
//   // === Base config for JS, TS, and Vue ===
//   {
//     files: ["**/*.{js,ts,vue}"],
//     ignores: ["node_modules/**", "dist/**"],
//
//     languageOptions: {
//       parser: tsParser,
//       parserOptions: {
//         ecmaVersion: "latest",
//         sourceType: "module",
//         extraFileExtensions: [".vue"],
//       },
//       globals: {
//         console: "readonly",
//         window: "readonly",
//         document: "readonly",
//       },
//     },
//
//     plugins: {
//       vue,
//       import: importPlugin,
//       "@typescript-eslint": ts,
//     },
//
//     rules: {
//       // --- General JS rules ---
//       "no-console": ["warn", { allow: ["warn", "error", "debug"] }],
//       curly: "error",
//       "no-empty": "error",
//       eqeqeq: "error",
//
//       // --- Imports ---
//       "import/newline-after-import": ["error", { count: 1 }],
//       "import/default": "error",
//       "import/no-relative-packages": "error",
//
//       // --- JSDoc enforcement ---
//       // "require-jsdoc": [
//       //   "error",
//       //   {
//       //     require: {
//       //       FunctionDeclaration: true,
//       //       MethodDefinition: true,
//       //       ClassDeclaration: false,
//       //       ArrowFunctionExpression: false,
//       //       FunctionExpression: false,
//       //     },
//       //   },
//       // ],
//
//       // --- Class member formatting ---
//       "lines-between-class-members": [
//         "error",
//         { enforce: [{ blankLine: "always", prev: "*", next: "method" }] },
//       ],
//
//       // --- Vue 3 rules ---
//       "vue/max-attributes-per-line": "off",
//       "vue/singleline-html-element-content-newline": "off",
//       "vue/attribute-hyphenation": ["error", "always", { ignore: ["viewBox"] }],
//       "vue/no-reserved-component-names": [
//         "error",
//         {
//           disallowVueBuiltInComponents: true,
//           disallowVue3BuiltInComponents: true,
//         },
//       ],
//       "vue/no-static-inline-styles": "error",
//       "vue/multi-word-component-names": "off",
//       "vue/prop-name-casing": "off",
//       "vue/require-explicit-emits": "error",
//       "vue/match-component-file-name": [
//         "error",
//         { extensions: ["vue"], shouldMatchCase: false },
//       ],
//       "vue/eqeqeq": "error",
//       "vue/component-api-style": ["error", ["script-setup", "composition"]],
//       "vue/define-macros-order": [
//         "error",
//         { order: ["defineOptions", "defineProps", "defineEmits", "defineSlots"] },
//       ],
//       "vue/define-props-declaration": ["error", "type-based"],
//       "vue/html-button-has-type": ["error", { button: true, submit: true, reset: true }],
//       "vue/html-comment-indent": "error",
//       "vue/match-component-import-name": "error",
//       "vue/next-tick-style": ["error", "promise"],
//       "vue/no-duplicate-attr-inheritance": "error",
//       "vue/no-empty-component-block": "error",
//       "vue/no-multiple-objects-in-class": "error",
//       "vue/no-ref-object-destructure": "error",
//       "vue/no-setup-props-reactivity-loss": "error",
//       "vue/no-required-prop-with-default": "error",
//       "vue/no-template-target-blank": "error",
//       "vue/no-undef-properties": "error",
//       "vue/no-unused-refs": "error",
//       "vue/no-useless-mustaches": "error",
//       "vue/no-useless-v-bind": "error",
//       "vue/padding-line-between-blocks": "error",
//       "vue/prefer-define-options": "error",
//       "vue/prefer-separate-static-class": "error",
//       "vue/prefer-true-attribute-shorthand": "error",
//       "vue/require-macro-variable-name": [
//         "error",
//         {
//           defineProps: "props",
//           defineEmits: "emit",
//           defineSlots: "slots",
//           useSlots: "slots",
//           useAttrs: "attrs",
//         },
//       ],
//       "vue/html-comment-content-spacing": ["error", "always"],
//
//       // --- TypeScript-specific ---
//       "no-redeclare": "off",
//       "@typescript-eslint/no-redeclare": "error",
//       "no-unused-vars": "off",
//       "@typescript-eslint/no-unused-vars": [
//         "error",
//         {
//           vars: "local",
//           args: "none",
//           ignoreRestSiblings: false,
//         },
//       ],
//     },
//   },
//
//   // === TypeScript-only parsing (fixes “Unexpected token : / interface”) ===
//   {
//     files: ["**/*.ts", "**/*.tsx"],
//     languageOptions: {
//       parser: tsParser,
//       parserOptions: {
//         project: "./tsconfig.json",
//         ecmaVersion: "latest",
//         sourceType: "module",
//       },
//     },
//     plugins: {
//       "@typescript-eslint": ts,
//     },
//     rules: {
//       ...ts.configs.recommended.rules,
//     },
//   },
//
//   // === Test, API, and factory overrides ===
//   {
//     files: [
//       "*.spec.ts",
//       "src/api/urls/*.ts",
//       "test/utils/factories/**/*.ts",
//       "src/api/client/**/*.ts",
//     ],
//     rules: {
//       "require-jsdoc": "off",
//     },
//   },
//
//   // === HTML files override ===
//   {
//     files: ["*.html"],
//     rules: {
//       "vue/comment-directive": "off",
//     },
//   },
//
//   // === Extend recommended configs ===
//   js.configs.recommended,
//   ...compat.extends("plugin:vue/vue3-recommended"),
//   ...compat.extends("prettier"),
//   prettier,
// ];

// eslint.config.js
import js from "@eslint/js";
import ts from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import vue from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";
import prettier from "eslint-config-prettier";

/**
 * Minimal, stable ESLint flat config for Vue 3 + TS + Vite.
 * Works with ESLint v9+, Vue 3.5+, Vite 5+.
 */
export default [
  js.configs.recommended,
  {
    files: ["**/*.{vue,ts,js}"],
    ignores: ["dist/**", "node_modules/**", "**/*.d.ts"],

    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsParser, // delegate <script lang="ts">
        ecmaVersion: "latest",
        sourceType: "module",
        extraFileExtensions: [".vue"],
      },
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly",
      },
    },

    plugins: {
      vue,
      "@typescript-eslint": ts,
    },

    rules: {
      ...vue.configs["vue3-recommended"].rules,
      ...ts.configs.recommended.rules,
      ...prettier.rules,

      // --- JS/TS best practices ---
      "no-console": ["warn", { allow: ["warn", "error"] }],
      eqeqeq: "error",

      // --- TS-specific ---
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": ["error", { vars: "all", args: "none", ignoreRestSiblings: true }],

      // --- Vue adjustments ---
      "vue/html-indent": ["error", 2],
      "vue/max-attributes-per-line": "off",
      "vue/singleline-html-element-content-newline": "off",
      "vue/attribute-hyphenation": ["error", "always", { ignore: ["viewBox"] }],
      "vue/no-reserved-component-names": [
        "error",
        {
          disallowVueBuiltInComponents: true,
          disallowVue3BuiltInComponents: true,
        },
      ],
      "vue/no-static-inline-styles": "error",
      "vue/multi-word-component-names": "off",
      "vue/prop-name-casing": "off",
      "vue/require-explicit-emits": "error",
      "vue/match-component-file-name": ["error", { extensions: ["vue"], shouldMatchCase: false }],
      "vue/eqeqeq": "error",
      "vue/component-api-style": ["error", ["script-setup", "composition"]],
      "vue/define-macros-order": ["error", { order: ["defineOptions", "defineProps", "defineEmits", "defineSlots"] }],
      "vue/define-props-declaration": ["error", "type-based"],
      "vue/html-button-has-type": ["error", { button: true, submit: true, reset: true }],
      "vue/html-comment-indent": "error",
      "vue/match-component-import-name": "error",
      "vue/next-tick-style": ["error", "promise"],
      "vue/no-duplicate-attr-inheritance": "error",
      "vue/no-empty-component-block": "error",
      "vue/no-multiple-objects-in-class": "error",
      "vue/no-ref-object-destructure": "error",
      "vue/no-setup-props-reactivity-loss": "error",
      "vue/no-required-prop-with-default": "error",
      "vue/no-template-target-blank": "error",
      "vue/no-undef-properties": "error",
      "vue/no-unused-refs": "error",
      "vue/no-useless-mustaches": "error",
      "vue/no-useless-v-bind": "error",
      "vue/padding-line-between-blocks": "error",
      "vue/prefer-define-options": "error",
      "vue/prefer-separate-static-class": "error",
      "vue/prefer-true-attribute-shorthand": "error",
      "vue/require-macro-variable-name": [
        "error",
        {
          defineProps: "props",
          defineEmits: "emit",
          defineSlots: "slots",
          useSlots: "slots",
          useAttrs: "attrs",
        },
      ],
      "vue/html-comment-content-spacing": ["error", "always"],
    },
  },
  prettier,
];
