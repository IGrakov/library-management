import type { QueryKey } from "@tanstack/vue-query";
import { useMutation, useQueryClient } from "@tanstack/vue-query";

export function useCreateMutation<TPayload, TResult>(
  queryKey: QueryKey,
  apiFn: (payload: TPayload) => Promise<TResult>,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: apiFn,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKey,
      });
    },
  });
}

export function useUpdateMutation<TPayload, TResult>(
  queryKey: QueryKey,
  apiFn: (id: number, payload: TPayload) => Promise<TResult>,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: TPayload }) => apiFn(id, payload),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKey,
      });
    },
  });
}

export function useDeleteMutation(queryKey: QueryKey, apiFn: (id: number) => Promise<void>) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: apiFn,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKey,
      });
    },
  });
}
