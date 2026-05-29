import type { AxiosError } from "axios";
import { ref } from "vue";

export type BackendErrors = Record<string, string[]> | { detail: string };

export function useForm() {
  const fieldErrors = ref<Record<string, string>>({});
  const generalError = ref("");

  function clearErrors() {
    fieldErrors.value = {};
    generalError.value = "";
  }

  function setBackendErrors(error: AxiosError<BackendErrors>) {
    clearErrors();

    const status = error?.response?.status;
    const data: BackendErrors | undefined = error?.response?.data;

    if (!data) {
      return;
    }

    // Validation errors (DRF serializer)
    if (status === 400 && data) {
      fieldErrors.value = Object.fromEntries(
        Object.entries(data).map(([field, messages]) => [
          field,
          Array.isArray(messages) ? messages.join(" ") : String(messages),
        ]),
      );

      return;
    }

    // Permission
    if (status === 403) {
      generalError.value = "You do not have permission to perform this action.";

      return;
    }

    // Not found
    if (status === 404) {
      generalError.value = "The requested object was not found.";

      return;
    }

    // Server error
    if (status && status >= 500) {
      generalError.value = "Unexpected server error. Please try again later.";

      return;
    }

    // Network / fallback
    generalError.value = "Unexpected error occurred.";
  }

  return {
    fieldErrors,
    generalError,

    clearErrors,
    setBackendErrors,
  };
}
