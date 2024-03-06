<script setup>
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import FlashNotification from '@/components/FlashNotification.vue';
import { ref, computed } from 'vue';
import router from '@/router';

const toastStore = useToastStore()
const userStore = useUserStore()

const form = ref({
  email: userStore.user.email,
  name: userStore.user.name,
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
  classes.value = 'bg-red-300'
  console.log('Hello');

  
  if (errorsLength.value === 0) {
    axios.post('/api/profile/edit/', form.value).then(response => {
      if (response.data.message === 'information updated') {
        toastStore.showToast(
          5000,
          'The information was saved',
          'bg-emerald-500'
        )
        userStore.setUserInfo({
          id: userStore.user.id,
          name: form.value.name,
          email: form.value.email,
        })

        router.back()
      } else {
        toastStore.showToast(
          5000,
          `${response.data.message}. Please try again.`,
          'bg-red-300'
        )
      }
    }).catch(error => {
      console.log(error)
    })
  }
}

const errorsLength = computed(() => {
  return Object.keys(errors.value).length
})
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

    <div class="col-start-2">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h2 class="text-xl">Edit Profile</h2>
        <hr class="py-4">
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
          <FlashNotification :errorsProps="errors" :classesProps="classes"/>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>