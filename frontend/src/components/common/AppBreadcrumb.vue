<script setup lang="ts">
import Breadcrumb from "primevue/breadcrumb";
import { MenuItem } from "primevue/menuitem";
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const home: MenuItem = {
  label: "Home",
  icon: "pi pi-home",
  to: "/",
};

const breadcrumbs = computed<MenuItem[]>(() => {
  return (route.meta.breadcrumb as MenuItem[]) ?? [];
});
</script>

<template>
  <Breadcrumb :home="home" :model="breadcrumbs">
    <template #item="{ item, props }">
      <router-link v-if="item.to" v-slot="{ href, navigate }" :to="item.to" custom>
        <a :href="href" v-bind="props.action" @click="navigate">
          {{ item.label }}
        </a>
      </router-link>
      <span v-else v-bind="props.action">
        {{ item.label }}
      </span>
    </template>
  </Breadcrumb>
</template>
