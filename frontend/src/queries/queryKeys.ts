export const queryKeys = {
  books: ["books"] as const,
  book: (id: number) => ["book", id] as const,
  users: ["users"] as const,
  user: (id: number) => ["user", id] as const,
  languages: ["languages"] as const,
  language: (id: number) => ["language", id] as const,
  authors: ["authors"] as const,
  author: (id: number) => ["author", id] as const,
  genres: ["genres"] as const,
  genre: (id: number) => ["genre", id] as const,
  halls: ["halls"] as const,
  hall: (id: number) => ["hall", id] as const,
};
