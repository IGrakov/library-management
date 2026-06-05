import { Hall } from "@/types/halls";

export interface BookCopy {
  id: number;
  uid: string;
  hall: Hall;
}

export interface BookCopyQueryParams {
  page?: number;
  page_size?: number;
  uid?: string;
  sort?: string;
  ordering?: string;
}
