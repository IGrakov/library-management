<script setup lang="ts">
import { isAxiosError } from "axios";
import Button from "primevue/button";
import { computed, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import BookForm from "@/components/books/BookForm.vue";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import { useForm } from "@/composables/useForm";
import { useAuthorsLookupQuery } from "@/queries/authors.queries";
import { useUpdateBook } from "@/queries/books.mutations";
import { useBookQuery } from "@/queries/books.queries";
import { useGenresQuery } from "@/queries/genres.queries";
import { useLanguagesQuery } from "@/queries/languages.queries";
import { AuthorOption } from "@/types/authors";
import { CreateBookPayload } from "@/types/books";

const router = useRouter();
const route = useRoute();

const updateBookMutation = useUpdateBook();

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

const bookId = Number(route.params.id);

const bookQuery = useBookQuery(bookId);

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
    await updateBookMutation.mutateAsync({
      id: bookId,
      payload: bookForm,
    });

    router.push("/books");
  } catch (error) {
    if (isAxiosError(error)) {
      setBackendErrors(error);
    } else {
      generalError.value = "Unexpected error occurred.";
    }
  }
}

watch(
  () => bookQuery.data.value,
  (book) => {
    if (!book) {
      return;
    }

    bookForm.title = book.title;
    bookForm.author_ids = book.author.map((a) => a.id);
    bookForm.language_ids = book.language.map((l) => l.id);
    bookForm.genre_ids = book.genre.map((g) => g.id);
    bookForm.published_date = book.published_date;
    bookForm.pages = book.pages;
    bookForm.isbn = book.isbn;
    bookForm.cover = book.cover;

    selectedAuthors.value = book.author.map((author) => ({
      id: author.id,
      full_name: [author.last_name, author.first_name, author.middle_name].filter(Boolean).join(" "),
    }));
  },
  { immediate: true },
);
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
        <Button label="Update" severity="success" :loading="updateBookMutation.isPending.value" @click="onSubmit" />
      </div>
    </div>
  </DefaultLayout>
</template>
