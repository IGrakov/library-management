import { createRouter, createWebHistory } from "vue-router";

import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import BookListPage from "@/components/pages/BookListPage.vue";
import GenreListPage from "@/components/pages/GenreListPage.vue";
import HallListPage from "@/components/pages/HallListPage.vue";
import LanguageListPage from "@/components/pages/LanguageListPage.vue";
import LoginPage from "@/components/pages/LoginPage.vue";
import RegisterPage from "@/components/pages/RegisterPage.vue";
import UserListPage from "@/components/pages/UserListPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: LoginPage,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/users",
      name: "users",
      component: UserListPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/books",
      name: "books",
      component: BookListPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/halls",
      name: "halls",
      component: HallListPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/genres",
      name: "genres",
      component: GenreListPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/languages",
      name: "languages",
      component: LanguageListPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/",
      name: "default",
      component: DefaultLayout,
    },
  ],
});

export default router;
