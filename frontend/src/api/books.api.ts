import { axiosClient } from "@/api/client";
import { Book, BookQueryParams, CreateBookPayload, PaginatedBooks } from "@/types/books";

export const booksApi = {
  getAll: async (params?: BookQueryParams): Promise<PaginatedBooks> => {
    const { data } = await axiosClient.get("/book/list-book/", {
      params,
    });
    return data;
  },

  getById: async (id: number): Promise<Book> => {
    const { data } = await axiosClient.get(`/book/${id}/`);
    return data;
  },

  create: async (payload: CreateBookPayload): Promise<Book> => {
    const { data } = await axiosClient.post("/book/create-book/", payload);

    return data;
  },
};
