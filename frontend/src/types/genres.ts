export interface Genre {
  id: number;
  name: string;
}

export interface PaginatedGenres {
  count: number;
  next: string | null;
  previous: string | null;
  results: Genre[];
}

export interface CreateOrUpdateGenrePayload {
  name: string;
}

export interface GenreQueryParams {
  page?: number;
  page_size?: number;
  name?: string;
  sort?: string;
  ordering?: string;
}
