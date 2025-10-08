<script setup lang="ts">
  import { ref } from "vue";
  import Button from "primevue/button";
  import Checkbox from 'primevue/checkbox';
  import CheckboxGroup from 'primevue/checkboxgroup';

  const res = ref(0);
  const pizza = ref<string[]>([]);


  const adder = () => {
    res.value++;
  };
</script>

<template>
  <div class="flex justify-center items-center">
    <h1 class="text-gray-500 my-8">Full Stack Project Template</h1>
  </div>

  <div class="flex flex-row justify-center items-center">
    <h1>{{ res }}</h1>
    <Button label="Button" severity="info" outlined class="text-gray-500 w-24 mx-8 my-4" @click="adder"/>
  </div>

  <!--  Specimen of PrimeVue buttons -->
  <div class="flex justify-center items-center my-8">
    <div class="flex w-1/2 justify-between">
      <Button label="Primary" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"/>
      <Button label="Secondary" severity="secondary" />
      <Button label="Success" severity="success" />
      <Button label="Info" severity="info" />
      <Button label="Warn" severity="warn" />
      <Button label="Help" severity="help" />
      <Button label="Danger" severity="danger" />
      <Button label="Contrast" severity="contrast" />
    </div>
  </div>

  <!--  Specimen of PrimeVue checkboxes -->
  <div class="card flex flex-wrap justify-center gap-4">
      <div class="flex items-center gap-2">
          <Checkbox v-model="pizza" inputId="ingredient1" name="pizza" value="Cheese" />
          <label for="ingredient1"> Cheese </label>
      </div>
      <div class="flex items-center gap-2">
          <Checkbox v-model="pizza" inputId="ingredient2" name="pizza" value="Mushroom" />
          <label for="ingredient2"> Mushroom </label>
      </div>
      <div class="flex items-center gap-2">
          <Checkbox v-model="pizza" inputId="ingredient3" name="pizza" value="Pepper" />
          <label for="ingredient3"> Pepper </label>
      </div>
      <div class="flex items-center gap-2">
          <Checkbox v-model="pizza" inputId="ingredient4" name="pizza" value="Onion" />
          <label for="ingredient4"> Onion </label>
      </div>
  </div>
</template>
