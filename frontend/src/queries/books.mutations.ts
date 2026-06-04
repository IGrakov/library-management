import { booksApi } from "@/api/books.api";
import { useCreateMutation, useDeleteMutation, useUpdateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import { CreateBookPayload, DetailedBook } from "@/types/books";

export function useCreateBook() {
  return useCreateMutation<CreateBookPayload, DetailedBook>(queryKeys.books, booksApi.create);
}

export function useUpdateBook() {
  return useUpdateMutation<Partial<CreateBookPayload>, DetailedBook>(queryKeys.books, booksApi.update);
}

export function useDeleteBook() {
  return useDeleteMutation(queryKeys.books, booksApi.delete);
}
