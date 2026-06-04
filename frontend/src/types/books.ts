import { Author } from "@/types/authors";
import { Genre } from "@/types/genres";
import { Language } from "@/types/languages";

export interface BaseBook {
  title: string;
  author: Author[];
  language: Language[];
  genre: Genre[];
  published_date: string | null;
  pages: number | null;
  isbn: string;
}

export interface Book extends BaseBook {
  id: number;
  copies_count: number;
}

export interface DetailedBook extends BaseBook {
  id: number;
  cover: string | null;
}

export interface PaginatedBooks {
  count: number;
  next: string | null;
  previous: string | null;
  results: Book[];
}

export interface CreateBookPayload {
  title: string;
  author_ids: number[];
  language_ids: number[];
  genre_ids: number[];
  published_date: string | null;
  pages: number | null;
  isbn: string;
  cover: string | null;
}

export type UpdateBookPayload = Partial<CreateBookPayload>;

export interface BookQueryParams {
  page?: number;
  page_size?: number;
  title?: string;
  author?: string;
  language?: string;
  genre?: string;
  isbn?: string;
  sort?: string;
  ordering?: string;
}
