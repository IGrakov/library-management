<script setup lang="ts">
import Button from "primevue/button";
import ConfirmDialog from "primevue/confirmdialog";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import { useConfirm } from "primevue/useconfirm";
import { computed, ref } from "vue";

import BaseDataTable from "@/components/common/BaseDataTable.vue";
import { useDataTable } from "@/composables/useDataTable";
import { useDebouncedFilters } from "@/composables/useDebouncedFilters";
import { useCreateLanguage, useDeleteLanguage, useUpdateLanguage } from "@/queries/languages.mutations";
import { useLanguagesQuery } from "@/queries/languages.queries";
import { Language } from "@/types/languages";
import { ColumnConfig } from "@/types/table";

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

const createLanguageMutation = useCreateLanguage();
const updateLanguageMutation = useUpdateLanguage();
const deleteLanguageMutation = useDeleteLanguage();

const confirm = useConfirm();

// Dialog state
const isDialogVisible = ref(false);

const editingLanguage = ref<Language | null>(null);

const languageName = ref("");
const threeLetterCodeRef = ref("");
const twoLetterCodeRef = ref("");

// Filters
const nameFilter = ref("");
const codeFilter = ref("");

// Debounced filtering
const { cleanedFilters } = useDebouncedFilters(
  {
    name: nameFilter,
    code: codeFilter,
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
  threeLetterCode: "three_letter_code",
  twoLetterCode: "two_letter_code",
};

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  ...cleanedFilters.value,

  ordering: sortField.value ? `${sortOrder.value === "desc" ? "-" : ""}${sortField.value}` : undefined,
}));

// Query
const languagesQuery = useLanguagesQuery(queryParams);

// Flatten nested fields
const languages = computed(() =>
  (languagesQuery.data.value?.results ?? []).map((language) => ({
    ...language,

    threeLetterCode: language.three_letter_code,
    twoLetterCode: language.two_letter_code,
  })),
);

// Define columns
const columns: ColumnConfig[] = [
  { field: "id", header: "Id" },
  { field: "name", header: "Name" },
  { field: "threeLetterCode", header: "3 letter code" },
  { field: "twoLetterCode", header: "2 letter code" },
  {
    field: "actions",
    header: "",
    sortable: false,
    align: "center",
  },
];

// Create / Edit
function openCreateDialog() {
  editingLanguage.value = null;

  languageName.value = "";
  threeLetterCodeRef.value = "";
  twoLetterCodeRef.value = "";

  isDialogVisible.value = true;
}

function openEditDialog(language: Language) {
  editingLanguage.value = language;

  languageName.value = language.name;
  threeLetterCodeRef.value = language.three_letter_code;
  twoLetterCodeRef.value = language.two_letter_code;

  isDialogVisible.value = true;
}

async function saveLanguage() {
  if (editingLanguage.value) {
    await updateLanguageMutation.mutateAsync({
      id: editingLanguage.value.id,

      payload: {
        name: languageName.value,
        three_letter_code: threeLetterCodeRef.value,
        two_letter_code: twoLetterCodeRef.value,
      },
    });
  } else {
    await createLanguageMutation.mutateAsync({
      name: languageName.value,
      three_letter_code: threeLetterCodeRef.value,
      two_letter_code: twoLetterCodeRef.value,
    });
  }

  isDialogVisible.value = false;
}

async function onDeleteLanguage(id: number) {
  confirm.require({
    message: "Are you sure you want to delete this language?",

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
      await deleteLanguageMutation.mutateAsync(id);
    },
  });
}
</script>

<template>
  <div class="card p-4">
    <!-- Filters -->
    <div class="flex justify-center gap-4 mb-4">
      <InputText v-model="nameFilter" placeholder="Filter by language name" class="border rounded p-1" />
      <InputText v-model="codeFilter" placeholder="Filter by language code" class="border rounded p-1" />
      <Button icon="pi pi-plus" severity="success" @click="openCreateDialog" />
    </div>

    <BaseDataTable
      :rows="languages"
      :columns="columns"
      :loading="languagesQuery.isFetching.value"
      :total-records="languagesQuery.data.value?.count"
      :rows-per-page="rowsPerPage"
      :sort-field="sortField"
      :sort-order="sortOrder"
      @page="onPage"
      @sort="(event) => onSort(event, apiFieldMap)"
    >
      <template #body-actions="{ data }">
        <div class="flex gap-2 justify-center">
          <Button icon="pi pi-pencil" severity="info" text rounded @click="openEditDialog(data)" />

          <Button icon="pi pi-trash" severity="danger" text rounded @click="onDeleteLanguage(data.id)" />
        </div>
      </template>
    </BaseDataTable>
  </div>
  <Dialog
    v-model:visible="isDialogVisible"
    modal
    :header="editingLanguage ? 'Edit Language' : 'Create Language'"
    class="w-sm"
  >
    <div class="flex flex-col gap-4">
      <InputText v-model="languageName" placeholder="Language name" />
      <InputText v-model="threeLetterCodeRef" placeholder="Language three letter code" />
      <InputText v-model="twoLetterCodeRef" placeholder="Language two letter code" />

      <div class="flex justify-end gap-2">
        <Button label="Cancel" severity="secondary" @click="isDialogVisible = false" />

        <Button
          :label="editingLanguage ? 'Save' : 'Create'"
          :severity="editingLanguage ? 'info' : 'success'"
          :loading="createLanguageMutation.isPending.value || updateLanguageMutation.isPending.value"
          @click="saveLanguage"
        />
      </div>
    </div>
  </Dialog>
  <ConfirmDialog />
</template>
