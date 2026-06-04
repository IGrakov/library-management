<script setup lang="ts">
import Button from "primevue/button";
import ConfirmDialog from "primevue/confirmdialog";
import InputText from "primevue/inputtext";
import { useConfirm } from "primevue/useconfirm";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import BaseDataTable from "@/components/common/BaseDataTable.vue";
import { useDataTable } from "@/composables/useDataTable";
import { useDebouncedFilters } from "@/composables/useDebouncedFilters";
import { useDeleteBook } from "@/queries/books.mutations";
import { useBooksQuery } from "@/queries/books.queries";
import { useAuthStore } from "@/stores/auth.store";
import { Book } from "@/types/books";
import { ColumnConfig } from "@/types/table";

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

const authStore = useAuthStore();
const router = useRouter();

const deleteBookMutation = useDeleteBook();

const confirm = useConfirm();

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
  {
    field: "actions",
    header: "",
    sortable: false,
    align: "center",
  },
];

function onCreateBook() {
  router.push("/books/create");
}

function onEditBook(book: Book) {
  router.push(`/books/${book.id}/edit`);
}

function onDeleteBook(id: number) {
  confirm.require({
    message: "Are you sure you want to delete this book?",

    header: "Delete Confirmation",

    icon: "pi pi-exclamation-triangle",

    rejectProps: {
      label: "Cancel",
      severity: "secondary",
      outlined: true,
    },

    acceptProps: {
      label: "Delete",
      severity: "danger",
    },

    accept: async () => {
      await deleteBookMutation.mutateAsync(id);
    },
  });
}
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
      <Button v-show="authStore.canCreateOrDeleteBook" icon="pi pi-plus" severity="success" @click="onCreateBook" />
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
    >
      <template #body-title="{ data }">
        <Button
          :label="data.title"
          text
          severity="secondary"
          class="p-0 hover:!bg-transparent hover:underline"
          @click="router.push(`/books/${data.id}`)"
        />
      </template>
      <template #body-actions="{ data }">
        <div class="flex gap-2 justify-center">
          <Button
            v-show="authStore.canEditBook"
            icon="pi pi-pencil"
            severity="info"
            text
            rounded
            @click="onEditBook(data)"
          />
          <Button
            v-show="authStore.canCreateOrDeleteBook"
            icon="pi pi-trash"
            severity="danger"
            text
            rounded
            @click="onDeleteBook(data.id)"
          />
        </div>
      </template>
    </BaseDataTable>
    <ConfirmDialog />
  </div>
</template>
