import { createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/components/pages/LoginPage.vue";
import RegisterPage from "@/components/pages/RegisterPage.vue";
import UsersPage from "@/components/pages/UsersPage.vue";
import BookListPage from "@/components/pages/BookListPage.vue";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";

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
      component: UsersPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/books",
      name: "books",
      component: BookListPage,
    },
    {
      path: "/",
      name: "default",
      component: DefaultLayout,
    },
  ],
});

export default router;
