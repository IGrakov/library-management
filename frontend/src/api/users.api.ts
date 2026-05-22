import { axiosClient } from "@/api/client";

import type { User, CreateUserPayload } from "@/types/users";

export const usersApi = {
  getAll: async (): Promise<User[]> => {
    const { data } = await axiosClient.get("/user/list/");

    return data;
  },

  create: async (payload: CreateUserPayload): Promise<User> => {
    const { data } = await axiosClient.post("/user/create/", payload);

    return data;
  },

  me: async (): Promise<User> => {
    const { data } = await axiosClient.get("/user/manage/");

    return data;
  },
};
