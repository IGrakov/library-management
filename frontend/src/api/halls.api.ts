import { axiosClient } from "@/api/client";
import { CreateOrUpdateHallPayload, Hall, HallQueryParams, PaginatedHalls } from "@/types/halls";

export const hallsApi = {
  getAll: async (params?: HallQueryParams): Promise<PaginatedHalls> => {
    const { data } = await axiosClient.get("/reference-value/list-hall/", {
      params,
    });

    return data;
  },

  getById: async (id: number): Promise<Hall> => {
    const { data } = await axiosClient.get(`/reference-value/manage-hall/${id}/`);

    return data;
  },

  create: async (payload: CreateOrUpdateHallPayload): Promise<Hall> => {
    const { data } = await axiosClient.post("/reference-value/add-hall/", payload);

    return data;
  },

  update: async (id: number, payload: Partial<CreateOrUpdateHallPayload>): Promise<Hall> => {
    const { data } = await axiosClient.patch(`/reference-value/manage-hall/${id}/`, payload);

    return data;
  },

  replace: async (id: number, payload: CreateOrUpdateHallPayload): Promise<Hall> => {
    const { data } = await axiosClient.put(`/reference-value/manage-hall/${id}/`, payload);

    return data;
  },

  delete: async (id: number): Promise<void> => {
    await axiosClient.delete(`/reference-value/manage-hall/${id}/`);
  },
};
