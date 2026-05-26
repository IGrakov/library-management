import { refDebounced } from "@vueuse/core";
import { computed, Ref, watch } from "vue";

type Filters = Record<string, Ref<string>>;

interface UseDebouncedFiltersOptions {
  delay?: number;
  page?: Ref<number>;
}

export function useDebouncedFilters(filters: Filters, options: UseDebouncedFiltersOptions = {}) {
  const { delay = 500, page } = options;

  // Create debounced refs
  const debouncedFilters = Object.fromEntries(
    Object.entries(filters).map(([key, value]) => [key, refDebounced(value, delay)]),
  ) as Record<string, Ref<string>>;

  // Reset pagination when filters change
  if (page) {
    watch(Object.values(debouncedFilters), () => {
      page.value = 1;
    });
  }

  // Clean empty values for API query params
  const cleanedFilters = computed(() =>
    Object.fromEntries(
      Object.entries(debouncedFilters)
        .filter(([, value]) => value.value)
        .map(([key, value]) => [key, value.value]),
    ),
  );

  return {
    debouncedFilters,
    cleanedFilters,
  };
}
