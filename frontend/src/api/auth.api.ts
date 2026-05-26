import { axiosClient } from "@/api/client";
import { LoginPayload, LoginResponse } from "@/types/users";

export const authApi = {
  login: async (payload: LoginPayload): Promise<LoginResponse> => {
    const { data } = await axiosClient.post("/user/token/", payload);

    return data;
  },
};
