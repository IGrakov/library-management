export interface Hall {
  id: number;
  name: string;
}

export interface PaginatedHalls {
  count: number;
  next: string | null;
  previous: string | null;
  results: Hall[];
}

export interface CreateOrUpdateHallPayload {
  name: string;
}

export interface HallsQueryParams {
  page?: number;
  page_size?: number;
  name?: string;
  sort?: string;
  ordering?: string;
}
