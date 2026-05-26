<script setup lang="ts">
import { computed, ref } from "vue";

import BaseDataTable from "@/components/common/BaseDataTable.vue";
import { useDataTable } from "@/composables/useDataTable";
import { useDebouncedFilters } from "@/composables/useDebouncedFilters";
import { useUsersQuery } from "@/queries/user.queries";
import { ColumnConfig } from "@/types/table";

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

// --- Filter state
const nameFilter = ref("");
const emailFilter = ref("");
const roleFilter = ref("");

// Debounced filtering
const { cleanedFilters } = useDebouncedFilters(
  {
    name: nameFilter,
    email: emailFilter,
    role: roleFilter,
  },
  {
    page,
    delay: 500,
  },
);

// --- Map DataTable columns to API fields
const apiFieldMap: Record<string, string> = {
  email: "email",
  nameStr: "last_name",
  role: "role",
};

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  ...cleanedFilters.value,

  ordering: sortField.value ? `${sortOrder.value === "desc" ? "-" : ""}${sortField.value}` : undefined,
}));

const usersQuery = useUsersQuery(queryParams);

const users = computed(() =>
  (usersQuery.data.value?.results ?? []).map((user) => ({
    ...user,
    nameStr: `${user.first_name} ${user.last_name}`,
  })),
);

// Define columns
const columns: ColumnConfig[] = [
  { field: "email", header: "Email" },
  { field: "nameStr", header: "Name" },
  { field: "role", header: "Role", sortable: false },
];
</script>

<template>
  <div class="card p-4">
    <!-- Filters -->
    <div class="flex justify-center gap-4 mb-4">
      <input v-model="emailFilter" placeholder="Filter by email" class="border rounded p-1" />
      <input v-model="nameFilter" placeholder="Filter by name" class="border rounded p-1" />
      <input v-model="roleFilter" placeholder="Filter by role" class="border rounded p-1" />
    </div>

    <BaseDataTable
      :rows="users"
      :columns="columns"
      :loading="usersQuery.isFetching.value"
      :total-records="usersQuery.data.value?.count"
      :rows-per-page="rowsPerPage"
      :sort-field="sortField"
      :sort-order="sortOrder"
      @page="onPage"
      @sort="(event) => onSort(event, apiFieldMap)"
    />
  </div>
</template>
