import { useMutation, useQueryClient } from "@tanstack/vue-query";

import { booksApi } from "@/api/books.api";
import { queryKeys } from "@/queries/queryKeys";

export function useCreateBook() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: booksApi.create,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: queryKeys.books,
      });
    },
  });
}
