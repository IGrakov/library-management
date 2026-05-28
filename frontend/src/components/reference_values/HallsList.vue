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
import { useCreateHall, useDeleteHall, useUpdateHall } from "@/queries/halls.mutations";
import { useHallsQuery } from "@/queries/halls.queries";
import { Hall } from "@/types/halls";
import { ColumnConfig } from "@/types/table";

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

const createHallMutation = useCreateHall();
const updateHallMutation = useUpdateHall();
const deleteHallMutation = useDeleteHall();

const confirm = useConfirm();

// Dialog state
const isDialogVisible = ref(false);

const editingHall = ref<Hall | null>(null);

const hallName = ref("");

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

const hallsQuery = useHallsQuery(queryParams);

// Flatten nested fields
const halls = computed(() =>
  (hallsQuery.data.value?.results ?? []).map((hall) => ({
    ...hall,
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
  editingHall.value = null;

  hallName.value = "";

  isDialogVisible.value = true;
}

function openEditDialog(hall: Hall) {
  editingHall.value = hall;

  hallName.value = hall.name;

  isDialogVisible.value = true;
}

async function saveHall() {
  if (editingHall.value) {
    await updateHallMutation.mutateAsync({
      id: editingHall.value.id,

      payload: {
        name: hallName.value,
      },
    });
  } else {
    await createHallMutation.mutateAsync({
      name: hallName.value,
    });
  }

  isDialogVisible.value = false;
}

async function onDeleteHall(id: number) {
  confirm.require({
    message: "Are you sure you want to delete this hall?",

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
      await deleteHallMutation.mutateAsync(id);
    },
  });
}
</script>

<template>
  <div class="card p-4">
    <div class="flex justify-center gap-4 mb-4">
      <input v-model="nameFilter" placeholder="Filter by hall name" class="border rounded p-1" />
      <Button icon="pi pi-plus" severity="success" @click="openCreateDialog" />
    </div>

    <BaseDataTable
      :rows="halls"
      :columns="columns"
      :loading="hallsQuery.isFetching.value"
      :total-records="hallsQuery.data.value?.count"
      :rows-per-page="rowsPerPage"
      :sort-field="sortField"
      :sort-order="sortOrder"
      @page="onPage"
      @sort="(event) => onSort(event, apiFieldMap)"
    >
      <template #body-actions="{ data }">
        <div class="flex gap-2 justify-center">
          <Button icon="pi pi-pencil" severity="info" text rounded @click="openEditDialog(data)" />

          <Button icon="pi pi-trash" severity="danger" text rounded @click="onDeleteHall(data.id)" />
        </div>
      </template>
    </BaseDataTable>
  </div>
  <Dialog v-model:visible="isDialogVisible" modal :header="editingHall ? 'Edit Hall' : 'Create Hall'" class="w-sm">
    <div class="flex flex-col gap-4">
      <InputText v-model="hallName" placeholder="Hall name" />

      <div class="flex justify-end gap-2">
        <Button label="Cancel" severity="secondary" @click="isDialogVisible = false" />

        <Button
          :label="editingHall ? 'Save' : 'Create'"
          :severity="editingHall ? 'info' : 'success'"
          :loading="createHallMutation.isPending.value || updateHallMutation.isPending.value"
          @click="saveHall"
        />
      </div>
    </div>
  </Dialog>
  <ConfirmDialog />
</template>
