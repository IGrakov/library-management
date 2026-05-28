import { hallsApi } from "@/api/halls.api";
import { useCreateMutation, useDeleteMutation, useUpdateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import type { CreateOrUpdateHallPayload, Hall } from "@/types/halls";

export function useCreateHall() {
  return useCreateMutation<CreateOrUpdateHallPayload, Hall>(queryKeys.halls, hallsApi.create);
}

export function useUpdateHall() {
  return useUpdateMutation<CreateOrUpdateHallPayload, Hall>(queryKeys.halls, hallsApi.update);
}

export function useDeleteHall() {
  return useDeleteMutation(queryKeys.halls, hallsApi.delete);
}
