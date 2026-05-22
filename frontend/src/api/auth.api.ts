import { axiosClient } from "@/api/client";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user_id: number;
}

export const authApi = {
  login: async (payload: LoginPayload): Promise<LoginResponse> => {
    const { data } = await axiosClient.post("/user/token/", payload);

    return data;
  },
};
