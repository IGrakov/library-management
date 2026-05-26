<script setup lang="ts">
import { refDebounced } from "@vueuse/core";
import { computed, ref, watch } from "vue";

import BaseDataTable from "@/components/common/BaseDataTable.vue";
import { useDataTable } from "@/composables/useDataTable";
import { useUsersQuery } from "@/queries/user.queries";
import { ColumnConfig } from "@/types/table";

const { page, rowsPerPage, sortField, sortOrder, onPage, onSort } = useDataTable();

// --- Filter state
const nameFilter = ref("");
const emailFilter = ref("");
const roleFilter = ref("");
const debouncedNameFilter = refDebounced(nameFilter, 500);
const debouncedEmailFilter = refDebounced(emailFilter, 500);
const debouncedRoleFilter = refDebounced(roleFilter, 500);

// --- Map DataTable columns to API fields
const apiFieldMap: Record<string, string> = {
  email: "email",
  nameStr: "last_name",
  role: "role",
};

const queryParams = computed(() => ({
  page: page.value,
  page_size: rowsPerPage.value,

  email: debouncedEmailFilter.value || undefined,
  name: debouncedNameFilter.value || undefined,
  role: debouncedRoleFilter.value || undefined,

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

watch(
  () => [debouncedNameFilter, debouncedEmailFilter, debouncedRoleFilter],
  () => {
    page.value = 1;
  },
);
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
