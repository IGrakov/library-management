export interface Language extends CreateLanguagePayload {
  id: number;
}

export interface PaginatedLanguages {
  count: number;
  next: string | null;
  previous: string | null;
  results: Language[];
}

export interface CreateLanguagePayload {
  name: string;
  two_letter_code: string;
  three_letter_code: string;
}

export type UpdateLanguagePayload = Partial<CreateLanguagePayload>;

export interface LanguageQueryParams {
  page?: number;
  page_size?: number;
  name?: string;
  two_letter_code?: string;
  three_letter_code?: string;
  sort?: string;
  ordering?: string;
}
