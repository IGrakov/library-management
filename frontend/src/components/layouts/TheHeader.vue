<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRoute } from "vue-router";

import { useAuthStore } from "@/stores/auth.store";

const route = useRoute();

const authStore = useAuthStore();

const isAuthenticated = computed(() => !!authStore.token);

const isUsersPage = computed(() => route.name === "users");

const isBooksPage = computed(() => route.name === "books");

const isHallsPage = computed(() => route.name === "halls");

const isLoginPage = computed(() => route.name === "login");

const isRegisterPage = computed(() => route.name === "register");
</script>

<template>
  <header>
    <nav class="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <!-- Left side menu -->
        <div
          v-if="isAuthenticated"
          id="mobile-menu-2"
          class="hidden justify-between items-center w-full lg:flex lg:w-auto lg:order-1"
        >
          <ul class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
            <li>
              <RouterLink
                v-if="!isUsersPage"
                to="/users"
                class="block py-2 pr-4 pl-3 text-gray-700 hover:text-primary-700"
              >
                Users
              </RouterLink>
            </li>
            <li>
              <RouterLink
                v-if="!isBooksPage"
                to="/books"
                class="block py-2 pr-4 pl-3 text-gray-700 hover:text-primary-700"
              >
                Books
              </RouterLink>
            </li>
            <li>
              <RouterLink
                v-if="!isHallsPage"
                to="/halls"
                class="block py-2 pr-4 pl-3 text-gray-700 hover:text-primary-700"
              >
                Halls
              </RouterLink>
            </li>
          </ul>
        </div>
        <!-- Right side -->
        <div v-if="!isAuthenticated" class="flex items-center lg:order-2">
          <RouterLink
            v-if="!isLoginPage"
            to="/login"
            class="text-gray-800 dark:text-white hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800"
          >
            Log in
          </RouterLink>

          <RouterLink
            v-if="!isRegisterPage"
            to="/register"
            class="text-gray-800 dark:text-white hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800"
          >
            Register
          </RouterLink>
        </div>
      </div>
    </nav>
  </header>
</template>
