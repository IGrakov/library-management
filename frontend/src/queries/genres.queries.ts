import { MaybeRefOrGetter } from "vue";

import { genresApi } from "@/api/genres.api";
import { useDetailQuery, useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { Genre, GenreQueryParams, PaginatedGenres } from "@/types/genres";

export function useGenresQuery(params: MaybeRefOrGetter<GenreQueryParams>) {
  return useListQuery<PaginatedGenres, GenreQueryParams>(queryKeys.genres, genresApi.getAll, params);
}

export function useGenreQuery(id: number) {
  return useDetailQuery<Genre>(queryKeys.genres, genresApi.getById, id);
}
