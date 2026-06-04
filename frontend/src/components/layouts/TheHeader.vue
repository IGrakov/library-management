<script setup lang="ts">
import Button from "primevue/button";
import Menubar from "primevue/menubar";
import type { MenuItem } from "primevue/menuitem";
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

import AppBreadcrumb from "@/components/common/AppBreadcrumb.vue";
import { useAuthStore } from "@/stores/auth.store";

const route = useRoute();
const router = useRouter();

const authStore = useAuthStore();

const menuItems = computed<MenuItem[]>(() => {
  if (!authStore.isAuthenticated) {
    return [];
  }

  const menu: MenuItem[] = [
    {
      label: "Books",
      icon: "pi pi-book",

      class: route.path === "/books" ? "active-menu-item" : "",

      command: () => navigateTo("/books"),
    },
  ];

  if (["admin", "librarian"].includes(authStore.role ?? "")) {
    menu.push({
      label: "Users",
      icon: "pi pi-users",

      class: route.path === "/users" ? "active-menu-item" : "",

      command: () => navigateTo("/users"),
    });
  }

  if (["admin", "librarian"].includes(authStore.role ?? "")) {
    menu.push({
      label: "Reference Values",
      icon: "pi pi-list",
      items: [
        {
          label: "Halls",
          icon: "pi pi-building",

          class: route.path === "/halls" ? "active-menu-item" : "",

          command: () => navigateTo("/halls"),
        },
        {
          label: "Genres",
          icon: "pi pi-tags",

          class: route.path === "/genres" ? "active-menu-item" : "",

          command: () => navigateTo("/genres"),
        },
        {
          label: "Languages",
          icon: "pi pi-language",

          class: route.path === "/languages" ? "active-menu-item" : "",

          command: () => navigateTo("/languages"),
        },
        {
          label: "Authors",
          icon: "pi pi-pencil",

          class: route.path === "/authors" ? "active-menu-item" : "",

          command: () => navigateTo("/authors"),
        },
      ],
    });
  }

  return menu;
});

function navigateTo(path: string) {
  if (route.path !== path) {
    router.push(path);
  }
}

function logout() {
  authStore.logout();

  router.push("/login");
}
</script>

<template>
  <div class="m-4">
    <Menubar :model="menuItems">
      <template #end>
        <div class="flex items-center gap-2">
          <span v-if="authStore.user">
            {{ authStore.user.first_name }}
            {{ authStore.user.last_name }}
          </span>

          <Button v-if="authStore.isAuthenticated" label="Logout" icon="pi pi-sign-out" text @click="logout" />

          <template v-else>
            <Button label="Login" text @click="router.push('/login')" />

            <Button label="Register" text @click="router.push('/register')" />
          </template>
        </div>
      </template>
    </Menubar>
    <AppBreadcrumb />
  </div>
</template>
