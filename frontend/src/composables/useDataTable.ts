import type { DataTableSortEvent } from "primevue/datatable";
import { ref } from "vue";

export function useDataTable() {
  const page = ref(1);
  const rowsPerPage = ref(10);

  const sortField = ref<string>();
  const sortOrder = ref<"asc" | "desc">();

  function onPage(event: { page: number; rows: number }) {
    page.value = event.page + 1;
    rowsPerPage.value = event.rows;
  }

  function onSort(event: DataTableSortEvent, apiFieldMap: Record<string, string>) {
    if (!event.sortField || typeof event.sortField !== "string" || event.sortOrder === 0) {
      sortField.value = undefined;
      sortOrder.value = undefined;

      return;
    }

    sortField.value = apiFieldMap[event.sortField];
    sortOrder.value = event.sortOrder === 1 ? "asc" : "desc";

    page.value = 1;
  }

  return {
    page,
    rowsPerPage,

    sortField,
    sortOrder,

    onPage,
    onSort,
  };
}
