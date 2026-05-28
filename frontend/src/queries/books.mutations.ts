import { booksApi } from "@/api/books.api";
import { useCreateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import { Book, CreateBookPayload } from "@/types/books";

export function useCreateBook() {
  return useCreateMutation<CreateBookPayload, Book>(queryKeys.books, booksApi.create);
}
