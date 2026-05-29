<script setup lang="ts">
import { isAxiosError } from "axios";
import Button from "primevue/button";
import ConfirmDialog from "primevue/confirmdialog";
import InputText from "primevue/inputtext";
import { useConfirm } from "primevue/useconfirm";
import { computed, ref } from "vue";

import BaseDataTable from "@/components/common/BaseDataTable.vue";
import BaseDialog from "@/components/common/BaseDialog.vue";
import BaseFormField from "@/components/common/BaseFormField.vue";
import { useDataTable } from "@/composables/useDataTable";
import { useDebouncedFilters } from "@/composables/useDebouncedFilters";
import { useForm } from "@/composables/useForm";
import { useCreateGenre, useDeleteGenre, useUpdateGenre } from "@/queries/genres.mutations";
import { useGenresQuery } from "@/queries/genres.queries";
import { Genre } from "@/types/genres";
import { ColumnConfig } from "@/types/table";

const { fieldErrors, generalError, clearErrors, setBackendErrors } = useForm();

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

const createGenreMutation = useCreateGenre();
const updateGenreMutation = useUpdateGenre();
const deleteGenreMutation = useDeleteGenre();

const confirm = useConfirm();

// Dialog state
const isDialogVisible = ref(false);

const editingGenre = ref<Genre | null>(null);

const genreName = ref("");

// Filters
const nameFilter = ref("");

// Debounced filtering
const { cleanedFilters } = useDebouncedFilters(
  {
    name: nameFilter,
  },
  {
    page,
    delay: 500,
  },
);

// Sorting
const apiFieldMap: Record<string, string> = {
  id: "id",
  name: "name",
};

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  ...cleanedFilters.value,

  ordering: sortField.value ? `${sortOrder.value === "desc" ? "-" : ""}${sortField.value}` : undefined,
}));

// Query
const genresQuery = useGenresQuery(queryParams);

// Flatten nested fields
const genres = computed(() =>
  (genresQuery.data.value?.results ?? []).map((genre) => ({
    ...genre,
  })),
);

// Define columns
const columns: ColumnConfig[] = [
  { field: "id", header: "Id" },
  { field: "name", header: "Name" },
  {
    field: "actions",
    header: "",
    sortable: false,
    align: "center",
  },
];

// Create / Edit
function openCreateDialog() {
  clearErrors();
  editingGenre.value = null;

  genreName.value = "";

  isDialogVisible.value = true;
}

function openEditDialog(genre: Genre) {
  clearErrors();
  editingGenre.value = genre;

  genreName.value = genre.name;

  isDialogVisible.value = true;
}

async function saveGenre() {
  clearErrors();

  try {
    if (editingGenre.value) {
      await updateGenreMutation.mutateAsync({
        id: editingGenre.value.id,

        payload: {
          name: genreName.value,
        },
      });
    } else {
      await createGenreMutation.mutateAsync({
        name: genreName.value,
      });
    }

    isDialogVisible.value = false;
  } catch (error) {
    if (isAxiosError(error)) {
      setBackendErrors(error);
    } else {
      generalError.value = "Unexpected error occurred.";
    }
  }
}

async function onDeleteGenre(id: number) {
  confirm.require({
    message: "Are you sure you want to delete this genre?",

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
      await deleteGenreMutation.mutateAsync(id);
    },
  });
}
</script>

<template>
  <div class="card p-4">
    <!-- Filters -->
    <div class="flex justify-center gap-4 mb-4">
      <InputText v-model="nameFilter" placeholder="Filter by genre name" class="border rounded p-1" />
      <Button icon="pi pi-plus" severity="success" @click="openCreateDialog" />
    </div>

    <BaseDataTable
      :rows="genres"
      :columns="columns"
      :loading="genresQuery.isFetching.value"
      :total-records="genresQuery.data.value?.count"
      :rows-per-page="rowsPerPage"
      :sort-field="sortField"
      :sort-order="sortOrder"
      @page="onPage"
      @sort="(event) => onSort(event, apiFieldMap)"
    >
      <template #body-actions="{ data }">
        <div class="flex gap-2 justify-center">
          <Button icon="pi pi-pencil" severity="info" text rounded @click="openEditDialog(data)" />

          <Button icon="pi pi-trash" severity="danger" text rounded @click="onDeleteGenre(data.id)" />
        </div>
      </template>
    </BaseDataTable>
  </div>
  <BaseDialog
    v-model:visible="isDialogVisible"
    :title="editingGenre ? 'Edit Genre' : 'Create Genre'"
    :submit-label="editingGenre ? 'Save' : 'Create'"
    :loading="createGenreMutation.isPending.value || updateGenreMutation.isPending.value"
    @submit="saveGenre"
  >
    <BaseFormField :error="fieldErrors.name">
      <InputText v-model="genreName" placeholder="Genre name" />
    </BaseFormField>
  </BaseDialog>
  <ConfirmDialog />
</template>
