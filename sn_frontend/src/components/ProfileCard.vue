<script setup>
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';

const toastStore = useToastStore()

const route = useRoute()
const props = defineProps({ user: Object })

function sendFriendshipRequest() {
  axios.post(`/api/friends/${route.params.id}/request/`).then(response => {
    console.log('data', response.data)
    if (response.data.message == 'request already sent') {
      toastStore.showToast(
        5000,
        'The request has already been sent!',
        'bg-red-300'
      )
    } else {
      toastStore.showToast(
        5000,
        'The request was sent!',
        'bg-emerald-300'
      )
    }
  }).catch(error => {
    console.log('error', error)
  })
}
</script>

<template>
  <div class="main-left col-span-1">
    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
      <img src="https://i.pravatar.cc/300?img=12" class="mb-6 rounded-full">

      <p><strong>{{ props.user.name }}</strong></p>

      <div class="mt-6 flex space-x-8 justify-around">
        <RouterLink :to="{ name: 'friends', params: props.user.id }"
          class="text-xs text-gray-500">{{ props.user.friends_count }} friends
        </RouterLink>
        <p class="text-xs text-gray-500">0 posts</p>
      </div>

      <div class="mt-6">
        <button @click="sendFriendshipRequest"
          class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg">Follow</button>
      </div>
    </div>
</div></template>