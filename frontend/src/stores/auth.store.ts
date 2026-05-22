import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { authApi } from "@/api/auth.api";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem("access_token"));

  const userId = ref<number | null>(Number(localStorage.getItem("user_id")));

  const isAuthenticated = computed(() => !!token.value);

  async function login(email: string, password: string) {
    const response = await authApi.login({
      email,
      password,
    });

    token.value = response.token;
    userId.value = response.user_id;

    localStorage.setItem("access_token", response.token);

    localStorage.setItem("user_id", String(response.user_id));
  }

  function logout() {
    token.value = null;
    userId.value = null;

    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
  }

  return {
    token,
    userId,
    isAuthenticated,

    login,
    logout,
  };
});
