import { genresApi } from "@/api/genres.api";
import { useCreateMutation, useDeleteMutation, useUpdateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import { CreateOrUpdateGenrePayload, Genre } from "@/types/genres";

export function useCreateGenre() {
  return useCreateMutation<CreateOrUpdateGenrePayload, Genre>(queryKeys.genres, genresApi.create);
}

export function useUpdateGenre() {
  return useUpdateMutation<CreateOrUpdateGenrePayload, Genre>(queryKeys.genres, genresApi.update);
}

export function useDeleteGenre() {
  return useDeleteMutation(queryKeys.genres, genresApi.delete);
}
