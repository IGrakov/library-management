import { MaybeRefOrGetter } from "vue";

import { hallsApi } from "@/api/halls.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import type { Hall, HallQueryParams, PaginatedHalls } from "@/types/halls";

export function useHallsQuery(params: MaybeRefOrGetter<HallQueryParams>) {
  return useListQuery<PaginatedHalls, HallQueryParams>(queryKeys.halls, hallsApi.getAll, params);
}

export function useHallQuery(id: number) {
  return useDetailQuery<Hall>(queryKeys.halls, hallsApi.getById, id);
}
