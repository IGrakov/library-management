export interface Book extends CreateBookPayload {
  id: number;
  copies_count: number;
}

export interface PaginatedBooks {
  count: number;
  next: string | null;
  previous: string | null;
  results: Book[];
}

export interface CreateBookPayload {
  title: string;
  author: { first_name: string; last_name: string }[];
  language: { name: string }[];
  genre: { name: string }[];
  published_date: string;
  pages: number;
}

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
