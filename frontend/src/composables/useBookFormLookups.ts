import { computed, ref } from "vue";

import { useAuthorsLookupQuery } from "@/queries/authors.queries";
import { useGenresQuery } from "@/queries/genres.queries";
import { useLanguagesQuery } from "@/queries/languages.queries";

export function useBookFormLookups() {
  const authorSearch = ref("");

  const authorsLookupQuery = useAuthorsLookupQuery(
    computed(() => ({
      search: authorSearch.value,
    })),
    computed(() => authorSearch.value.trim().length >= 2),
  );

  const languagesQuery = useLanguagesQuery({
    page_size: 1000,
  });

  const genresQuery = useGenresQuery({
    page_size: 1000,
  });

  const authorsSuggestions = computed(() =>
    (authorsLookupQuery.data.value ?? []).map((a) => ({
      id: a.id,
      full_name: [a.last_name, a.first_name, a.middle_name].filter(Boolean).join(" "),
    })),
  );

  const languages = computed(() =>
    (languagesQuery.data.value?.results ?? []).map((language) => ({
      id: language.id,
      name: language.name,
    })),
  );

  const genres = computed(() =>
    (genresQuery.data.value?.results ?? []).map((genre) => ({
      id: genre.id,
      name: genre.name,
    })),
  );

  function onAuthorSearch(query: string) {
    authorSearch.value = query;
  }

  return {
    authorsSuggestions,
    languages,
    genres,
    onAuthorSearch,
  };
}
