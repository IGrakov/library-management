<script setup lang="ts" generic="T">
import Column from "primevue/column";
import type { DataTableSortEvent } from "primevue/datatable";
import DataTable from "primevue/datatable";

import { ColumnConfig } from "@/types/table";

defineProps<{
  rows: T[];
  columns: ColumnConfig[];

  loading?: boolean;
  totalRecords?: number;
  rowsPerPage?: number;
  sortField?: string;
  sortOrder?: "asc" | "desc";
}>();

const emit = defineEmits<{
  page: [{ page: number; rows: number }];
  sort: [DataTableSortEvent];
}>();
</script>

<template>
  <div class="flex justify-center">
    <div class="min-h-4/5 w-max">
      <DataTable
        :value="rows"
        lazy
        paginator
        :sort-field="sortField"
        :sort-order="sortOrder === 'asc' ? 1 : -1"
        :rows="rowsPerPage ?? 10"
        :total-records="totalRecords ?? 0"
        :loading="loading"
        responsive-layout="scroll"
        class="mt-2"
        @page="emit('page', $event)"
        @sort="emit('sort', $event)"
      >
        <Column
          v-for="col in columns"
          :key="col.field"
          :field="col.field"
          :header="col.header"
          :sortable="col.sortable ?? true"
          :style="{ textAlign: col.align ?? 'left' }"
          :pt="{
            columnHeaderContent: {
              class: 'justify-center',
            },
          }"
        >
          <template #body="{ data }">
            <slot :name="`body-${col.field}`" :data="data">
              {{ data[col.field] }}
            </slot>
          </template>

          <template #loading>
            <div class="h-4 bg-gray-200 rounded"></div>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<style scoped>
:deep(.p-datatable-thead > tr > th) {
  @apply text-center align-middle;
}
</style>
