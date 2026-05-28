import { usersApi } from "@/api/users.api";
import { useCreateMutation } from "@/composables/useBaseMutations";
import { queryKeys } from "@/queries/queryKeys";
import { AuthUser, CreateUserPayload } from "@/types/users";

export function useCreateUser() {
  return useCreateMutation<CreateUserPayload, AuthUser>(queryKeys.users, usersApi.create);
}
