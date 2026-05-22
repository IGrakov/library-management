<script setup lang="ts">
import { computed, ref } from "vue";

import type { DataTableSortEvent } from "primevue/datatable";

import Column from "primevue/column";
import DataTable from "primevue/datatable";

import { useBooksQuery } from "@/queries/books.queries";

// --- Pagination state
const page = ref(1);
const rowsPerPage = ref(10);

// --- Filter state
const titleFilter = ref("");
const authorFilter = ref("");
const languageFilter = ref("");
const genreFilter = ref("");
const isbnFilter = ref("");

const sortField = ref<string>();
const sortOrder = ref<"asc" | "desc">();
// const sortField = ref<string | keyof Book | ((item: Book) => string) | undefined>();
// const sortOrder = ref< "asc" | "desc" | undefined>("asc");

// --- Map DataTable columns to API fields
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

function onSort(event: DataTableSortEvent) {
  if (!event.sortField || event.sortOrder === 0) {
    sortField.value = undefined;
    sortOrder.value = undefined;
  } else {
    sortField.value = apiFieldMap[event.sortField as string];
    sortOrder.value = event.sortOrder === 1 ? "asc" : "desc";
  }
  page.value = 1;
}

// --- Handle DataTable page change
function onPage(event: { page: number; rows: number }) {
  page.value = event.page + 1; // PrimeVue pages are 0-indexed
  rowsPerPage.value = event.rows;
}

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  title: titleFilter.value || undefined,
  author: authorFilter.value || undefined,
  language: languageFilter.value || undefined,
  genre: genreFilter.value || undefined,
  isbn: isbnFilter.value || undefined,

  sort: sortField.value,
  order: sortOrder.value,
}));

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

const totalRecords = computed(() => booksQuery.data?.value?.count ?? 0);
const isLoading = computed(() => booksQuery.isFetching.value);
const isError = computed(() => booksQuery.isError.value);

// Define columns
const columns = [
  { field: "title", header: "Title", align: "left" },
  { field: "authorStr", header: "Authors", align: "left" },
  { field: "languageStr", header: "Languages", align: "left" },
  { field: "genreStr", header: "Genres", align: "left" },
  { field: "publishedDate", header: "Published", align: "left" },
  { field: "pages", header: "Pages", align: "right" },
  { field: "isbn", header: "ISBN", align: "right" },
  { field: "copiesCount", header: "Number of Copies", align: "right" },
];
</script>

<template>
  <div class="card p-4">
    <!-- Filters -->
    <div class="flex justify-center gap-4 mb-4">
      <input v-model="titleFilter" placeholder="Filter by title" class="border rounded p-1" />
      <input v-model="authorFilter" placeholder="Filter by author" class="border rounded p-1" />
      <input v-model="languageFilter" placeholder="Filter by language" class="border rounded p-1" />
      <input v-model="genreFilter" placeholder="Filter by genre" class="border rounded p-1" />
      <input v-model="isbnFilter" placeholder="Filter by ISBN" class="border rounded p-1" />
    </div>

    <div class="min-h-4/5 w-full">
      <DataTable
        :value="books"
        lazy
        paginator
        :rows="rowsPerPage"
        :total-records="totalRecords"
        :loading="isLoading"
        responsive-layout="scroll"
        sort-mode="multiple"
        class="mt-2"
        @page="onPage"
        @sort="onSort"
      >
        <Column
          v-for="col in columns"
          :key="col.field"
          :field="col.field"
          :header="col.header"
          :sortable="!!col.field"
          :pt="{
            columnHeaderContent: {
              class: 'justify-center',
            },
          }"
          :style="{ textAlign: col.align }"
        >
          <template #loading>
            <div class="h-4 bg-gray-200 rounded"></div>
          </template>
        </Column>
      </DataTable>
    </div>

    <div v-if="isError" class="text-red-600 mt-2">❌ Error loading books</div>
  </div>
</template>

<style scoped>
:deep(.p-datatable-thead > tr > th) {
  @apply text-center align-middle;
}
</style>
