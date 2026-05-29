<script setup lang="ts">
import InputText from "primevue/inputtext";
import { computed, ref } from "vue";

import BaseDataTable from "@/components/common/BaseDataTable.vue";
import { useDataTable } from "@/composables/useDataTable";
import { useDebouncedFilters } from "@/composables/useDebouncedFilters";
import { useBooksQuery } from "@/queries/books.queries";
import { ColumnConfig } from "@/types/table";

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

// Filters
const titleFilter = ref("");
const authorFilter = ref("");
const languageFilter = ref("");
const genreFilter = ref("");
const isbnFilter = ref("");

// Debounced filtering
const { cleanedFilters } = useDebouncedFilters(
  {
    title: titleFilter,
    author: authorFilter,
    language: languageFilter,
    genre: genreFilter,
    isbn: isbnFilter,
  },
  {
    page,
    delay: 500,
  },
);

// Sort
const apiFieldMap: Record<string, string> = {
  title: "title",
  authorStr: "author",
  languageStr: "language",
  genreStr: "genre",
  publishedDate: "published_date",
  pages: "pages",
  isbn: "isbn",
  copiesCount: "copies_count",
};

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  ...cleanedFilters.value,

  ordering: sortField.value ? `${sortOrder.value === "desc" ? "-" : ""}${sortField.value}` : undefined,
}));

// Query
const booksQuery = useBooksQuery(queryParams);

// Flatten nested fields
const books = computed(() =>
  (booksQuery.data.value?.results ?? []).map((book) => ({
    ...book,

    authorStr: book.author.map((author) => `${author.first_name} ${author.last_name}`).join(", "),

    languageStr: book.language.map((language) => language.name).join(", "),

    genreStr: book.genre.map((genre) => genre.name).join(", "),

    publishedDate: book.published_date ? new Date(book.published_date).getFullYear() : null,

    copiesCount: book.copies_count,
  })),
);

// Define columns
const columns: ColumnConfig[] = [
  { field: "title", header: "Title" },
  { field: "authorStr", header: "Authors" },
  { field: "languageStr", header: "Languages" },
  { field: "genreStr", header: "Genres" },
  { field: "publishedDate", header: "Published" },
  { field: "pages", header: "Pages", align: "right", sortable: false },
  { field: "isbn", header: "ISBN", align: "right" },
  { field: "copiesCount", header: "Number of Copies", align: "right", sortable: false },
];
</script>

<template>
  <div class="card p-4">
    <!-- Filters -->
    <div class="flex justify-center gap-4 mb-4">
      <InputText v-model="titleFilter" placeholder="Filter by title" class="border rounded p-1" />
      <InputText v-model="authorFilter" placeholder="Filter by author" class="border rounded p-1" />
      <InputText v-model="languageFilter" placeholder="Filter by language" class="border rounded p-1" />
      <InputText v-model="genreFilter" placeholder="Filter by genre" class="border rounded p-1" />
      <InputText v-model="isbnFilter" placeholder="Filter by ISBN" class="border rounded p-1" />
    </div>

    <BaseDataTable
      :rows="books"
      :columns="columns"
      :loading="booksQuery.isFetching.value"
      :total-records="booksQuery.data.value?.count"
      :rows-per-page="rowsPerPage"
      :sort-field="sortField"
      :sort-order="sortOrder"
      @page="onPage"
      @sort="(event) => onSort(event, apiFieldMap)"
    />
  </div>
</template>
