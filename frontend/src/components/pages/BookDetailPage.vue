<script setup lang="ts">
import { useRoute } from "vue-router";

import BookDetails from "@/components/books/BookDetails.vue";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import { useBookQuery } from "@/queries/books.queries";

const route = useRoute();

const bookId = Number(route.params.id);

const bookQuery = useBookQuery(bookId);
</script>

<template>
  <DefaultLayout>
    <div class="card p-4 w-lg">
      <BookDetails v-if="bookQuery.data.value" :book="bookQuery.data.value" />
    </div>
  </DefaultLayout>
</template>
