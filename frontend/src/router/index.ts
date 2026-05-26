import { createRouter, createWebHistory } from "vue-router";

import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import BookListPage from "@/components/pages/BookListPage.vue";
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
      path: "/",
      name: "default",
      component: DefaultLayout,
    },
  ],
});

export default router;
