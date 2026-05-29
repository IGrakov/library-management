import { axiosClient } from "@/api/client";
import { CreateOrUpdateGenrePayload, Genre, GenreQueryParams, PaginatedGenres } from "@/types/genres";

export const genresApi = {
  getAll: async (params?: GenreQueryParams): Promise<PaginatedGenres> => {
    const { data } = await axiosClient.get("/reference-value/list-genre/", {
      params,
    });

    return data;
  },

  getById: async (id: number): Promise<Genre> => {
    const { data } = await axiosClient.get(`/reference-value/manage-genre/${id}/`);

    return data;
  },

  create: async (payload: CreateOrUpdateGenrePayload): Promise<Genre> => {
    const { data } = await axiosClient.post("/reference-value/add-genre/", payload);

    return data;
  },

  update: async (id: number, payload: Partial<CreateOrUpdateGenrePayload>): Promise<Genre> => {
    const { data } = await axiosClient.patch(`/reference-value/manage-genre/${id}/`, payload);

    return data;
  },

  replace: async (id: number, payload: CreateOrUpdateGenrePayload): Promise<Genre> => {
    const { data } = await axiosClient.put(`/reference-value/manage-genre/${id}/`, payload);

    return data;
  },

  delete: async (id: number): Promise<void> => {
    await axiosClient.delete(`/reference-value/manage-genre/${id}/`);
  },
};
