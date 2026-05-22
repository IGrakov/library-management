<script setup lang="ts">
import { useQuery } from "@tanstack/vue-query";
import { usersApi } from "@/api/users.api";

const usersQuery = useQuery({
  queryKey: ["users"],

  queryFn: usersApi.getAll,
});
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Users</h1>

    <div v-for="user in usersQuery.data.value" :key="user.id">
      {{ user.firstName }}
      {{ user.lastName }}
    </div>
  </div>
</template>
