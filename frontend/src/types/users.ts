export interface User {
  id: number;
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: string;
}

export interface CreateUserPayload extends Omit<User, "id"> {}

export interface UpdateUserPayload extends Partial<User> {}
