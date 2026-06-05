<script setup lang="ts">
import { isAxiosError } from "axios";
import Button from "primevue/button";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

import BookForm from "@/components/books/BookForm.vue";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import { useBookFormLookups } from "@/composables/useBookFormLookups";
import { useForm } from "@/composables/useForm";
import { useCreateBook } from "@/queries/books.mutations";
import { AuthorOption } from "@/types/authors";
import { CreateBookPayload } from "@/types/books";

const router = useRouter();

const createBookMutation = useCreateBook();

const { fieldErrors, generalError, clearErrors, setBackendErrors } = useForm();

const { authorsSuggestions, languages, genres, onAuthorSearch } = useBookFormLookups();

const bookForm = reactive<CreateBookPayload>({
  title: "",
  author_ids: [],
  language_ids: [],
  genre_ids: [],
  published_date: null,
  pages: null,
  isbn: "",
  cover: null,
});

const selectedAuthors = ref<AuthorOption[]>([]);

async function onSubmit() {
  clearErrors();

  try {
    await createBookMutation.mutateAsync(bookForm);

    router.push("/books");
  } catch (error) {
    if (isAxiosError(error)) {
      setBackendErrors(error);
    } else {
      generalError.value = "Unexpected error occurred.";
    }
  }
}
</script>

<template>
  <DefaultLayout>
    <div class="card p-4 w-lg">
      <BookForm
        v-model="bookForm"
        v-model:selected-authors="selectedAuthors"
        :authors-suggestions="authorsSuggestions"
        :on-author-search="onAuthorSearch"
        :languages="languages"
        :genres="genres"
        :field-errors="fieldErrors"
        :general-error="generalError"
      />
      <div class="flex justify-center mt-8">
        <Button label="Create" severity="success" :loading="createBookMutation.isPending.value" @click="onSubmit" />
      </div>
    </div>
  </DefaultLayout>
</template>
