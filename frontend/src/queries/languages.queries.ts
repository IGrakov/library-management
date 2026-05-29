import { MaybeRefOrGetter } from "vue";

import { languagesApi } from "@/api/languages.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { Language, LanguageQueryParams, PaginatedLanguages } from "@/types/languages";

export function useLanguagesQuery(params: MaybeRefOrGetter<LanguageQueryParams>) {
  return useListQuery<PaginatedLanguages, LanguageQueryParams>(queryKeys.languages, languagesApi.getAll, params);
}

export function useLanguageQuery(id: number) {
  return useDetailQuery<Language>(queryKeys.languages, languagesApi.getById, id);
}
