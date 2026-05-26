import js from "@eslint/js";
import ts from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import prettier from "eslint-config-prettier";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import vue from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";

/**
 * Minimal, stable ESLint flat config for Vue 3 + TS + Vite.
 * Works with ESLint v9+, Vue 3.5+, Vite 5+.
 */
export default [
  js.configs.recommended,

  ...vue.configs["flat/recommended"],

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
      "simple-import-sort": simpleImportSort,
    },

    rules: {
      ...ts.configs.recommended.rules,
      ...prettier.rules,

      // --- JS/TS best practices ---
      "no-console": ["warn", { allow: ["warn", "error"] }],
      eqeqeq: "error",

      // --- TS-specific ---
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": ["error", { vars: "all", args: "none", ignoreRestSiblings: true }],

      "simple-import-sort/imports": "error",
      "simple-import-sort/exports": "error",

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
