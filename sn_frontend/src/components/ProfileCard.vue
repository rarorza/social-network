<script setup>
import { useRoute } from 'vue-router';
import axios from 'axios'

const route = useRoute()
const props = defineProps({username: String})

function sendFriendshipRequest() {
  axios.post(`/api/friends/request/${route.params.id}/`).then(response => {
    console.log('data', response.data)
  }).catch(error => {
    console.log('error', error)
  })
}
</script>

<template>
  <div class="main-left col-span-1">
    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
      <img src="https://i.pravatar.cc/300?img=12" class="mb-6 rounded-full">

      <p><strong>{{ props.username }}</strong></p>

      <div class="mt-6 flex space-x-8 justify-around">
        <p class="text-xs text-gray-500">0 friends</p>
        <p class="text-xs text-gray-500">0 posts</p>
      </div>

      <div class="mt-6">
        <button @click="sendFriendshipRequest" class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg">Follow</button>
      </div>
    </div>
  </div>
</template>