import { languagesApi } from "@/api/languages.api";
import { useCreateMutation, useDeleteMutation, useUpdateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import { CreateLanguagePayload, Language, UpdateLanguagePayload } from "@/types/languages";

export function useCreateLanguage() {
  return useCreateMutation<CreateLanguagePayload, Language>(queryKeys.languages, languagesApi.create);
}

export function useUpdateLanguage() {
  return useUpdateMutation<UpdateLanguagePayload, Language>(queryKeys.languages, languagesApi.update);
}

export function useDeleteLanguage() {
  return useDeleteMutation(queryKeys.languages, languagesApi.delete);
}
