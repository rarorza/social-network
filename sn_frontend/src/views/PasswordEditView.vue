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
  old_password: '',
  new_password1: '',
  new_password2: '',
})

const errors = ref([])
const classes = ref('')

function submitForm() {
  errors.value = []
  classes.value = 'bg-red-300'

  if (form.value.old_password === '') {
    errors.value.push('Your old password is missing')
  }
  if (form.value.password1 === '') {
    errors.value.push('Your password is missing')
  }
  if (form.value.password2 !== form.value.password1) {
    errors.value.push('The password does not match')
  }

  if (errorsLength.value === 0) {
    let formData = new FormData()
    formData.append('old_password', form.value.old_password)
    formData.append('new_password1', form.value.new_password1)
    formData.append('new_password2', form.value.new_password2)

    axios.post('/api/profile/edit/password/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    }).then(response => {
      if (response.data.message === 'success') {
        toastStore.showToast(
          5000,
          'The information was saved',
          'bg-emerald-500'
        )
        router.push(`/profile/${userStore.user.id}`)
      } else {
        toastStore.showToast(
          5000,
          `${response.data.message}. Please try again.`,
          'bg-red-300'
        )

        const messages = JSON.parse(response.data.message)
        for (const key in messages) {
          errors.value.push(messages[key][0].message)
        }
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
        <h2 class="text-xl">Change your password</h2>
        <hr class="py-4">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>Old Password</label><br>
            <input v-model="form.old_password" type="password" placeholder="Your old password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>New password</label><br>
            <input v-model="form.new_password1" type="password" placeholder="Your new password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <div>
            <label>Repeat password</label><br>
            <input v-model="form.new_password2" type="password" placeholder="Repeat your new password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <FlashNotification :errorsProps="errors" :classesProps="classes" />
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