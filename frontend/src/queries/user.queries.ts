import { MaybeRefOrGetter } from "vue";

import { usersApi } from "@/api/users.api";
import { useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { PaginatedUsers, UserQueryParams } from "@/types/users";

export function useUsersQuery(params: MaybeRefOrGetter<UserQueryParams>) {
  return useListQuery<PaginatedUsers, UserQueryParams>(queryKeys.users, usersApi.getAll, params);
}
