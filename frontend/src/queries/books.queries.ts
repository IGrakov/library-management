import { MaybeRefOrGetter } from "vue";

import { booksApi } from "@/api/books.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { BookQueryParams, DetailedBook, PaginatedBooks } from "@/types/books";

export function useBooksQuery(params: MaybeRefOrGetter<BookQueryParams>) {
  return useListQuery<PaginatedBooks, BookQueryParams>(queryKeys.books, booksApi.getAll, params);
}

export function useBookQuery(id: number) {
  return useDetailQuery<DetailedBook>(queryKeys.books, booksApi.getById, id);
}
