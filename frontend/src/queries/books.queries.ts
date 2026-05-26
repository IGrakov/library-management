import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import { MaybeRefOrGetter, toValue } from "vue";

import { booksApi } from "@/api/books.api";
import { queryKeys } from "@/queries/queryKeys";
import { BooksQueryParams, PaginatedBooks } from "@/types/books";

export function useBooksQuery(params: MaybeRefOrGetter<BooksQueryParams>) {
  return useQuery<PaginatedBooks>({
    queryKey: [queryKeys.books, params],

    queryFn: () => booksApi.getAll(toValue(params)),

    placeholderData: keepPreviousData,

    staleTime: 1000 * 60 * 5, // 5 min cache
  });
}
