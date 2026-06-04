<script setup lang="ts">
import AutoComplete from "primevue/autocomplete";
import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";
import MultiSelect from "primevue/multiselect";
import { ref, watch } from "vue";

import BaseFormField from "@/components/common/BaseFormField.vue";
import { AuthorOption } from "@/types/authors";

const props = defineProps<{
  authorsSuggestions: {
    id: number;
    full_name: string;
  }[];

  languages: {
    id: number;
    name: string;
  }[];

  genres: {
    id: number;
    name: string;
  }[];

  fieldErrors: Record<string, string>;
  generalError: string;

  onAuthorSearch: (query: string) => void;
}>();

const form = defineModel<{
  title: string;
  author_ids: number[];
  language_ids: number[];
  genre_ids: number[];
  published_date: string | null;
  pages: number | null;
  isbn: string;
  cover: string | null;
}>({ required: true });

const selectedAuthors = ref<AuthorOption[]>([]);

function handleAuthorSearch(event: { query: string }) {
  props.onAuthorSearch(event?.query ?? "");
}

watch(selectedAuthors, (authors: AuthorOption[]) => {
  form.value.author_ids = authors.map((author) => author.id);
});
</script>

<template>
  <div class="flex flex-col gap-4">
    <BaseFormField :error="fieldErrors.title">
      <InputText v-model="form.title" placeholder="Title" />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.author_ids">
      <AutoComplete
        v-model="selectedAuthors"
        :suggestions="authorsSuggestions"
        option-label="full_name"
        multiple
        @complete="handleAuthorSearch"
      />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.language_ids">
      <MultiSelect
        v-model="form.language_ids"
        :options="languages"
        option-label="name"
        option-value="id"
        filter
        placeholder="Languages"
      />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.genre_ids">
      <MultiSelect
        v-model="form.genre_ids"
        :options="genres"
        option-label="name"
        option-value="id"
        filter
        placeholder="Genres"
      />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.published_date">
      <InputText v-model="form.published_date" placeholder="Publication year" />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.pages">
      <InputNumber v-model="form.pages" placeholder="Number of pages" />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.isbn">
      <InputText v-model="form.isbn" placeholder="ISBN" />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.cover">
      <InputText v-model="form.cover" placeholder="Cover URL" />
    </BaseFormField>
  </div>
</template>
