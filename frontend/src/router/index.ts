import { createRouter, createWebHistory } from "vue-router";

import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import AuthorListPage from "@/components/pages/AuthorListPage.vue";
import BookCreatePage from "@/components/pages/BookCreatePage.vue";
import BookDetailPage from "@/components/pages/BookDetailPage.vue";
import BookEditPage from "@/components/pages/BookEditPage.vue";
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
      meta: {
        breadcrumb: [{ label: "Login" }],
      },
    },
    {
      path: "/register",
      name: "register",
      component: RegisterPage,
      meta: {
        breadcrumb: [{ label: "Register" }],
        requiresAuth: true,
      },
    },
    {
      path: "/users",
      name: "users",
      component: UserListPage,
      meta: {
        breadcrumb: [{ label: "Users" }],
        requiresAuth: true,
      },
    },
    {
      path: "/books",
      name: "books",
      component: BookListPage,
      meta: {
        breadcrumb: [{ label: "Books" }],
        requiresAuth: true,
      },
    },
    {
      path: "/books/create",
      name: "book-create",
      component: BookCreatePage,
      meta: {
        breadcrumb: [{ label: "Books", to: "/books" }, { label: "Create" }],
        requiresAuth: true,
      },
    },
    {
      path: "/books/:id",
      name: "book-detail",
      component: BookDetailPage,
      meta: {
        breadcrumb: [{ label: "Books", to: "/books" }, { label: "Details" }],
        requiresAuth: true,
      },
    },
    {
      path: "/books/:id/edit",
      name: "book-edit",
      component: BookEditPage,
      meta: {
        breadcrumb: [{ label: "Books", to: "/books" }, { label: "Edit" }],
        requiresAuth: true,
      },
    },
    {
      path: "/halls",
      name: "halls",
      component: HallListPage,
      meta: {
        breadcrumb: [{ label: "Reference Values" }, { label: "Halls" }],
        requiresAuth: true,
      },
    },
    {
      path: "/genres",
      name: "genres",
      component: GenreListPage,
      meta: {
        breadcrumb: [{ label: "Reference Values" }, { label: "Genres" }],
        requiresAuth: true,
      },
    },
    {
      path: "/languages",
      name: "languages",
      component: LanguageListPage,
      meta: {
        breadcrumb: [{ label: "Reference Values" }, { label: "Languages" }],
        requiresAuth: true,
      },
    },
    {
      path: "/authors",
      name: "authors",
      component: AuthorListPage,
      meta: {
        breadcrumb: [{ label: "Reference Values" }, { label: "Authors" }],
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
