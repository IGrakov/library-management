import { ComputedRef, MaybeRefOrGetter } from "vue";

import { authorsApi } from "@/api/authors.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { Author, AuthorLookupParams, AuthorQueryParams, PaginatedAuthors } from "@/types/authors";

export function useAuthorsQuery(params: MaybeRefOrGetter<AuthorQueryParams>) {
  return useListQuery<PaginatedAuthors, AuthorQueryParams>(queryKeys.authors, authorsApi.getAll, params);
}

export function useAuthorsLookupQuery(params: MaybeRefOrGetter<AuthorLookupParams>, enabled: ComputedRef<boolean>) {
  return useListQuery<Author[], AuthorLookupParams>(queryKeys.authors, authorsApi.getSelected, params, enabled);
}

export function useAuthorQuery(id: number) {
  return useDetailQuery<Author>(queryKeys.authors, authorsApi.getById, id);
}
