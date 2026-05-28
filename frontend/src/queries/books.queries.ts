import { MaybeRefOrGetter } from "vue";

import { booksApi } from "@/api/books.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { Book, BooksQueryParams, PaginatedBooks } from "@/types/books";

export function useBooksQuery(params: MaybeRefOrGetter<BooksQueryParams>) {
  return useListQuery<PaginatedBooks, BooksQueryParams>(queryKeys.books, booksApi.getAll, params);
}

export function useBookQuery(id: number) {
  return useDetailQuery<Book>(queryKeys.books, booksApi.getById, id);
}
