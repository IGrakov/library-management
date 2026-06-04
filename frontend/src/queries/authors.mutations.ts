import { authorsApi } from "@/api/authors.api";
import { useCreateMutation, useDeleteMutation, useUpdateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import { Author, CreateAuthorPayload, UpdateAuthorPayload } from "@/types/authors";

export function useCreateAuthor() {
  return useCreateMutation<CreateAuthorPayload, Author>(queryKeys.authors, authorsApi.create);
}

export function useUpdateAuthor() {
  return useUpdateMutation<UpdateAuthorPayload, Author>(queryKeys.authors, authorsApi.update);
}

export function useDeleteAuthor() {
  return useDeleteMutation(queryKeys.authors, authorsApi.delete);
}
