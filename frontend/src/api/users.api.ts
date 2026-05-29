import { axiosClient } from "@/api/client";
import { AuthUser, CreateUserPayload, PaginatedUsers, UserQueryParams } from "@/types/users";

export const usersApi = {
  getAll: async (params?: UserQueryParams): Promise<PaginatedUsers> => {
    const { data } = await axiosClient.get("/user/list/", {
      params,
    });
    return data;
  },

  create: async (payload: CreateUserPayload): Promise<AuthUser> => {
    const { data } = await axiosClient.post("/user/create/", payload);

    return data;
  },

  me: async (): Promise<AuthUser> => {
    const { data } = await axiosClient.get("/user/manage/");

    return data;
  },
};
