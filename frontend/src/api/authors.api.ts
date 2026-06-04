import { axiosClient } from "@/api/client";
import {
  Author,
  AuthorLookupParams,
  AuthorQueryParams,
  CreateAuthorPayload,
  PaginatedAuthors,
  UpdateAuthorPayload,
} from "@/types/authors";

export const authorsApi = {
  getAll: async (params?: AuthorQueryParams): Promise<PaginatedAuthors> => {
    const { data } = await axiosClient.get("/reference-value/list-author/", {
      params,
    });

    return data;
  },

  getSelected: async (params?: AuthorLookupParams): Promise<Author[]> => {
    const { data } = await axiosClient.get("/reference-value/author-lookup/", {
      params,
    });

    return data;
  },

  getById: async (id: number): Promise<Author> => {
    const { data } = await axiosClient.get(`/reference-value/manage-author/${id}/`);

    return data;
  },

  create: async (payload: CreateAuthorPayload): Promise<Author> => {
    const { data } = await axiosClient.post("/reference-value/add-author/", payload);

    return data;
  },

  update: async (id: number, payload: UpdateAuthorPayload): Promise<Author> => {
    const { data } = await axiosClient.patch(`/reference-value/manage-author/${id}/`, payload);

    return data;
  },

  replace: async (id: number, payload: CreateAuthorPayload): Promise<Author> => {
    const { data } = await axiosClient.put(`/reference-value/manage-author/${id}/`, payload);

    return data;
  },

  delete: async (id: number): Promise<void> => {
    await axiosClient.delete(`/reference-value/manage-author/${id}/`);
  },
};
