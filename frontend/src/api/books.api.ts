import { axiosClient } from "@/api/client";
import { BookQueryParams, CreateBookPayload, DetailedBook, PaginatedBooks } from "@/types/books";

export const booksApi = {
  getAll: async (params?: BookQueryParams): Promise<PaginatedBooks> => {
    const { data } = await axiosClient.get("/book/list-book/", {
      params,
    });
    return data;
  },

  getById: async (id: number): Promise<DetailedBook> => {
    const { data } = await axiosClient.get(`/book/manage-book/${id}/`);
    return data;
  },

  create: async (payload: CreateBookPayload): Promise<DetailedBook> => {
    const { data } = await axiosClient.post("/book/create-book/", payload);
    return data;
  },

  update: async (id: number, payload: Partial<CreateBookPayload>): Promise<DetailedBook> => {
    const { data } = await axiosClient.patch(`/book/manage-book/${id}/`, payload);
    return data;
  },

  replace: async (id: number, payload: CreateBookPayload): Promise<DetailedBook> => {
    const { data } = await axiosClient.put(`/book/manage-book/${id}/`, payload);
    return data;
  },

  delete: async (id: number): Promise<void> => {
    await axiosClient.delete(`/book/manage-book/${id}/`);
  },
};
