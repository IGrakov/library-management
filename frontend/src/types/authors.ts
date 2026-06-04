export interface Author extends CreateAuthorPayload {
  id: number;
}

export interface PaginatedAuthors {
  count: number;
  next: string | null;
  previous: string | null;
  results: Author[];
}

export interface CreateAuthorPayload {
  last_name: string;
  first_name: string;
  middle_name: string;
}

export type UpdateAuthorPayload = Partial<CreateAuthorPayload>;

export interface AuthorQueryParams {
  page?: number;
  page_size?: number;
  name?: string;
  sort?: string;
  ordering?: string;
}

export interface AuthorLookupParams {
  search?: string;
}

export type AuthorOption = {
  id: number;
  full_name: string;
};
