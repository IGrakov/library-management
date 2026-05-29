import { axiosClient } from "@/api/client";
import {
  CreateLanguagePayload,
  Language,
  LanguageQueryParams,
  PaginatedLanguages,
  UpdateLanguagePayload,
} from "@/types/languages";

export const languagesApi = {
  getAll: async (params?: LanguageQueryParams): Promise<PaginatedLanguages> => {
    const { data } = await axiosClient.get("/reference-value/list-language/", {
      params,
    });

    return data;
  },

  getById: async (id: number): Promise<Language> => {
    const { data } = await axiosClient.get(`/reference-value/manage-language/${id}/`);

    return data;
  },

  create: async (payload: CreateLanguagePayload): Promise<Language> => {
    const { data } = await axiosClient.post("/reference-value/add-language/", payload);

    return data;
  },

  update: async (id: number, payload: UpdateLanguagePayload): Promise<Language> => {
    const { data } = await axiosClient.patch(`/reference-value/manage-language/${id}/`, payload);

    return data;
  },

  replace: async (id: number, payload: CreateLanguagePayload): Promise<Language> => {
    const { data } = await axiosClient.put(`/reference-value/manage-language/${id}/`, payload);

    return data;
  },

  delete: async (id: number): Promise<void> => {
    await axiosClient.delete(`/reference-value/manage-language/${id}/`);
  },
};
