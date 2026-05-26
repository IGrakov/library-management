import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { authApi } from "@/api/auth.api";
import { AuthUser } from "@/types/users";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(window.localStorage.getItem("access_token"));

  const user = ref<AuthUser | null>(JSON.parse(window.localStorage.getItem("user") || "null"));

  const isAuthenticated = computed(() => !!token.value);

  const role = computed(() => user.value?.role);

  async function login(email: string, password: string) {
    const response = await authApi.login({
      email,
      password,
    });

    token.value = response.token;
    user.value = response.user;

    window.localStorage.setItem("access_token", response.token);

    window.localStorage.setItem("user", JSON.stringify(response.user));
  }

  function logout() {
    token.value = null;
    user.value = null;

    window.localStorage.removeItem("access_token");
    window.localStorage.removeItem("user");
  }

  return {
    token,
    user,
    role,
    isAuthenticated,

    login,
    logout,
  };
});
