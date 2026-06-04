import type { QueryKey } from "@tanstack/vue-query";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import { computed, MaybeRefOrGetter, toValue } from "vue";

export function useListQuery<TData, TParams>(
  queryKey: QueryKey,
  apiFn: (params?: TParams) => Promise<TData>,
  params: MaybeRefOrGetter<TParams>,
  enabled: MaybeRefOrGetter<boolean> = true,
) {
  return useQuery<TData>({
    queryKey: computed(() => [...queryKey, toValue(params)]),

    queryFn: () => apiFn(toValue(params)),

    enabled,

    placeholderData: keepPreviousData,

    staleTime: 1000 * 60 * 5,
  });
}

export function useDetailQuery<TData>(
  queryKey: QueryKey,
  apiFn: (id: number) => Promise<TData>,
  id: MaybeRefOrGetter<number>,
) {
  return useQuery<TData>({
    queryKey: [...queryKey, id],

    queryFn: () => apiFn(toValue(id)),

    enabled: !!toValue(id),

    staleTime: 1000 * 60 * 5,
  });
}
