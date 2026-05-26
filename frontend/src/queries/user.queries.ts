import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import { MaybeRefOrGetter, toValue } from "vue";

import { usersApi } from "@/api/users.api";
import { queryKeys } from "@/queries/queryKeys";
import { PaginatedUsers, UsersQueryParams } from "@/types/users";

export function useUsersQuery(params: MaybeRefOrGetter<UsersQueryParams>) {
  return useQuery<PaginatedUsers>({
    queryKey: [queryKeys.users, params],

    queryFn: () => usersApi.getAll(toValue(params)),

    placeholderData: keepPreviousData,

    staleTime: 1000 * 60 * 5, // 5 min cache
  });
}
