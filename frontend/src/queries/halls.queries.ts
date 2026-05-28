import { MaybeRefOrGetter } from "vue";

import { hallsApi } from "@/api/halls.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import type { Hall, HallsQueryParams, PaginatedHalls } from "@/types/halls";

export function useHallsQuery(params: MaybeRefOrGetter<HallsQueryParams>) {
  return useListQuery<PaginatedHalls, HallsQueryParams>(queryKeys.halls, hallsApi.getAll, params);
}

export function useHallQuery(id: number) {
  return useDetailQuery<Hall>(queryKeys.halls, hallsApi.getById, id);
}
