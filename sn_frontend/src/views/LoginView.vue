<script setup>
import { ref } from 'vue';
import FlashNotification from '@/components/FlashNotification.vue';

const form = ref({
  email: '',
  password: '',
})
const errors = ref([])
const classes = ref('')

function submitForm() {
  
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate.
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate.
        </p>
        <p class="font-bold">
          Don't have an account? <RouterLink :to="{ 'name': 'signup' }"
            class="underline">Click here</RouterLink> to
          create!
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>E-mail</label><br>
            <input v-model="form.email" type="email" placeholder="Your e-mail address"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>Password</label><br>
            <input v-model="form.password" type="password" placeholder="Your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <FlashNotification :errorsProps="errors" :classesProps="classes"/>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log
              in</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>