<script setup lang="ts">
import Button from "primevue/button";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import Password from "primevue/password";
import Select from "primevue/select";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import { useCreateUser } from "@/queries/user.mutations";

const router = useRouter();

const createUserMutation = useCreateUser();

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const firstName = ref("");
const lastName = ref("");
const role = ref("");

const roleOptions = [
  {
    label: "Reader",
    value: "Reader",
  },
  {
    label: "Librarian",
    value: "Librarian",
  },
];

const errorMessage = ref("");

const passwordsMatch = computed(() => password.value === confirmPassword.value);

async function onSubmit() {
  errorMessage.value = "";

  if (!passwordsMatch.value) {
    errorMessage.value = "Passwords do not match";

    return;
  }

  try {
    await createUserMutation.mutateAsync({
      email: email.value,
      password: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      role: role.value,
    });

    // clear form
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    firstName.value = "";
    lastName.value = "";
    role.value = "";

    await router.push("/login");
  } catch (error) {
    console.error(error);

    errorMessage.value = "Failed to create user";
  }
}
</script>

<template>
  <DefaultLayout>
    <Card class="max-w-xl mx-auto p-6">
      <template #content>
        <form class="flex justify-center flex-col gap-4" @submit.prevent="onSubmit">
          <div class="flex flex-col gap-1">
            <InputText
              v-model="firstName"
              name="first-name"
              type="text"
              placeholder="First Name"
              class="border p-2 rounded"
            />
          </div>
          <div class="flex flex-col gap-1">
            <InputText
              v-model="lastName"
              name="last-name"
              type="text"
              placeholder="Last Name"
              class="border p-2 rounded"
            />
          </div>
          <div class="flex flex-col gap-1">
            <InputText
              v-model="email"
              name="email"
              type="text"
              placeholder="Email"
              class="border p-2 rounded"
              required
            />
          </div>
          <div class="flex flex-col gap-1">
            <Password v-model="password" name="password" placeholder="Password" :feedback="false" fluid required />
          </div>
          <div class="flex flex-col gap-1">
            <Password
              v-model="confirmPassword"
              name="confirm-password"
              placeholder="Confirm Password"
              :feedback="false"
              fluid
              required
            />
          </div>
          <Select
            v-model="role"
            :options="roleOptions"
            option-label="label"
            option-value="value"
            placeholder="Select Role"
            class="w-full"
            required
          />
          <Message v-if="errorMessage" severity="error">
            {{ errorMessage }}
          </Message>
          <Button
            type="submit"
            variant="outlined"
            severity="info"
            label="Submit"
            class="mt-6"
            :loading="createUserMutation.isPending.value"
          />
        </form>
      </template>
    </Card>
  </DefaultLayout>
</template>
