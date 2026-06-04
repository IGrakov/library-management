<script setup lang="ts">
import { isAxiosError } from "axios";
import Button from "primevue/button";
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import BookForm from "@/components/books/BookForm.vue";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import { useForm } from "@/composables/useForm";
import { useAuthorsLookupQuery } from "@/queries/authors.queries";
import { useCreateBook } from "@/queries/books.mutations";
import { useGenresQuery } from "@/queries/genres.queries";
import { useLanguagesQuery } from "@/queries/languages.queries";
import { CreateBookPayload } from "@/types/books";

const router = useRouter();

const createBookMutation = useCreateBook();

const { fieldErrors, generalError, clearErrors, setBackendErrors } = useForm();

const languagesQuery = useLanguagesQuery({
  page_size: 1000,
});

const genresQuery = useGenresQuery({
  page_size: 1000,
});

const authorSearch = ref("");

const authorsLookupQuery = useAuthorsLookupQuery(
  computed(() => ({
    search: authorSearch.value,
  })),
  computed(() => authorSearch.value.trim().length >= 2),
);

function onAuthorSearch(query: string) {
  authorSearch.value = query;
}

const authorsSuggestions = computed(() =>
  (authorsLookupQuery.data.value ?? []).map((a) => ({
    id: a.id,
    full_name: [a.last_name, a.first_name, a.middle_name].filter(Boolean).join(" "),
  })),
);

const languages = computed(() =>
  (languagesQuery.data.value?.results ?? []).map((language) => ({
    id: language.id,
    name: language.name,
  })),
);

const genres = computed(() =>
  (genresQuery.data.value?.results ?? []).map((genre) => ({
    id: genre.id,
    name: genre.name,
  })),
);

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
