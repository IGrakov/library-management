export interface BaseUser {
  email: string;
  first_name: string;
  last_name: string;
  role: string;
}

export interface AuthUser extends BaseUser {
  id: number;
}

export interface CreateUserPayload extends BaseUser {
  password: string;
}

export type UpdateUserPayload = Partial<CreateUserPayload>;

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: AuthUser;
}

export interface PaginatedUsers {
  count: number;
  next: string | null;
  previous: string | null;
  results: AuthUser[];
}

export interface UsersQueryParams {
  page?: number;
  page_size?: number;
  name?: string;
  email?: string;
  role?: string;
  sort?: string;
  order?: "asc" | "desc";
}
