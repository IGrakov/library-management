import { useMutation } from "@tanstack/vue-query";

import { usersApi } from "@/api/users.api";

export function useCreateUser() {
  return useMutation({
    mutationFn: usersApi.create,
  });
}
