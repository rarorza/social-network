<script setup>
import { ref, computed } from 'vue';
import { useToastStore } from '@/stores/toast';
import axios from 'axios';
import FlashNotification from '@/components/FlashNotification.vue';

const toastStore = useToastStore()

const form = ref({
  email: '',
  name: '',
  password1: '',
  password2: '',
})
const errors = ref([])
const classes = ref('')

function submitForm() {
  errors.value = []

  if (form.value.email === '') {
    errors.value.push('Your e-mail is missing')
  }
  if (form.value.name === '') {
    errors.value.push('Your name is missing')
  }
  if (form.value.password1 === '') {
    errors.value.push('Your password is missing')
  }
  if (form.value.password2 !== form.value.password1) {
    errors.value.push('The password does not match')
  }
  classes.value = 'bg-red-300'
  
  if (errorsLength.value === 0) {
    axios.post('/api/signup/', form.value).then(response => {
      if (response.data.message === 'success') {
        toastStore.showToast(
          5000,
          'The user is registered. Please log in',
          'bg-emerald-500'
        )
        form.value.email = ''
        form.value.name = ''
        form.value.password1 = ''
        form.value.password2 = ''
      } else {
        toastStore.showToast(
          5000,
          'Something went wrong. Please try again',
          'bg-red-300'
        )
      }
    }).catch(error => {
      console.log(error)
    })
  }
}

const errorsLength = computed(() => {
  // Workaround to return the length of errors ref
  return Object.keys(errors.value).length
})
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Sing in</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate.
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate.
        </p>
        <p class="font-bold">
          Already have an account? <RouterLink :to="{ 'name': 'login' }"
            class="underline">Click here</RouterLink> to log in!
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>Name</label><br>
            <input v-model="form.name" type="text" placeholder="Your full name"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>E-mail</label><br>
            <input v-model="form.email" type="email" placeholder="Your e-mail address"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>Password</label><br>
            <input v-model="form.password1" type="password" placeholder="Your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>Repeat password</label><br>
            <input v-model="form.password2" type="password" placeholder="Repeat your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <FlashNotification :errorsProps="errors" :classesProps="classes"/>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>