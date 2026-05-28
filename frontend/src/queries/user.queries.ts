import { MaybeRefOrGetter } from "vue";

import { usersApi } from "@/api/users.api";
import { useListQuery } from "@/composables/useBaseQueries";
import { queryKeys } from "@/queries/queryKeys";
import { PaginatedUsers, UsersQueryParams } from "@/types/users";

export function useUsersQuery(params: MaybeRefOrGetter<UsersQueryParams>) {
  return useListQuery<PaginatedUsers, UsersQueryParams>(queryKeys.users, usersApi.getAll, params);
}
