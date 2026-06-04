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
import { useCreateAuthor, useDeleteAuthor, useUpdateAuthor } from "@/queries/authors.mutations";
import { useAuthorsQuery } from "@/queries/authors.queries";
import { Author } from "@/types/authors";
import { ColumnConfig } from "@/types/table";

const { fieldErrors, generalError, clearErrors, setBackendErrors } = useForm();

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

const createAuthorMutation = useCreateAuthor();
const updateAuthorMutation = useUpdateAuthor();
const deleteAuthorMutation = useDeleteAuthor();

const confirm = useConfirm();

// Dialog state
const isDialogVisible = ref(false);

const editingAuthor = ref<Author | null>(null);

const firstName = ref("");
const middleName = ref("");
const lastName = ref("");

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
  firstName: "first_name",
  middleName: "middle_name",
  lastName: "last_name",
};

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  ...cleanedFilters.value,

  ordering: sortField.value ? `${sortOrder.value === "desc" ? "-" : ""}${sortField.value}` : undefined,
}));

// Query
const authorsQuery = useAuthorsQuery(queryParams);

// Flatten nested fields
const authors = computed(() =>
  (authorsQuery.data.value?.results ?? []).map((author) => ({
    ...author,

    firstName: author.first_name,
    middleName: author.middle_name,
    lastName: author.last_name,
  })),
);

// Define columns
const columns: ColumnConfig[] = [
  { field: "id", header: "Id" },
  { field: "lastName", header: "Last name" },
  { field: "firstName", header: "First name", sortable: false },
  { field: "middleName", header: "Middle name", sortable: false },
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
  editingAuthor.value = null;

  firstName.value = "";
  middleName.value = "";
  lastName.value = "";

  isDialogVisible.value = true;
}

function openEditDialog(author: Author) {
  clearErrors();
  editingAuthor.value = author;

  lastName.value = author.last_name;
  firstName.value = author.first_name;
  middleName.value = author.middle_name;

  isDialogVisible.value = true;
}

async function saveAuthor() {
  clearErrors();

  try {
    if (editingAuthor.value) {
      await updateAuthorMutation.mutateAsync({
        id: editingAuthor.value.id,

        payload: {
          first_name: firstName.value,
          middle_name: middleName.value,
          last_name: lastName.value,
        },
      });
    } else {
      await createAuthorMutation.mutateAsync({
        first_name: firstName.value,
        middle_name: middleName.value,
        last_name: lastName.value,
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

async function onDeleteAuthor(id: number) {
  confirm.require({
    message: "Are you sure you want to delete this author?",

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
      await deleteAuthorMutation.mutateAsync(id);
    },
  });
}
</script>

<template>
  <div class="card p-4">
    <!-- Filters -->
    <div class="flex justify-center gap-4 mb-4">
      <InputText v-model="nameFilter" placeholder="Filter by author name" class="border rounded p-1" />
      <Button icon="pi pi-plus" severity="success" @click="openCreateDialog" />
    </div>

    <BaseDataTable
      :rows="authors"
      :columns="columns"
      :loading="authorsQuery.isFetching.value"
      :total-records="authorsQuery.data.value?.count"
      :rows-per-page="rowsPerPage"
      :sort-field="sortField"
      :sort-order="sortOrder"
      @page="onPage"
      @sort="(event) => onSort(event, apiFieldMap)"
    >
      <template #body-actions="{ data }">
        <div class="flex gap-2 justify-center">
          <Button icon="pi pi-pencil" severity="info" text rounded @click="openEditDialog(data)" />

          <Button icon="pi pi-trash" severity="danger" text rounded @click="onDeleteAuthor(data.id)" />
        </div>
      </template>
    </BaseDataTable>
  </div>
  <BaseDialog
    v-model:visible="isDialogVisible"
    :title="editingAuthor ? 'Edit Author' : 'Create Author'"
    :submit-label="editingAuthor ? 'Save' : 'Create'"
    :loading="createAuthorMutation.isPending.value || updateAuthorMutation.isPending.value"
    @submit="saveAuthor"
  >
    <BaseFormField :error="fieldErrors.last_name">
      <InputText v-model="lastName" placeholder="Last name" />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.first_name">
      <InputText v-model="firstName" placeholder="First name" />
    </BaseFormField>

    <BaseFormField :error="fieldErrors.middle_name">
      <InputText v-model="middleName" placeholder="Middle name" />
    </BaseFormField>
  </BaseDialog>
  <ConfirmDialog />
</template>
