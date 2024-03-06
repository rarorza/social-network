<script setup>
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';

const toastStore = useToastStore()
const userStore = useUserStore()

const route = useRoute()
const router = useRouter()
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

function sendMessage() {
  axios.get(`/api/chat/get-or-create/${route.params.id}/`).then(response => {
    console.log('data', response.data);
    router.push('/messages')
  }).catch(error => {
    console.log('error', error)
  })
}

function logout() {
  userStore.removeToken()
  router.push('/login')
}
</script>

<template>
  <div class="main-left col-span-1">
    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
      <img src="https://i.pravatar.cc/300?img=12" class="mb-6 rounded-full">

      <p><strong>{{ props.user.name }}</strong></p>

      <div class="mt-6 flex space-x-8 justify-around">
        <RouterLink :to="{ name: 'friends', params: { id: props.user.id } }"
          class="text-xs text-gray-500">{{ props.user.friends_count }} friends
        </RouterLink>
        <p class="text-xs text-gray-500">{{ props.user.posts_count }} posts</p>
      </div>

      <div class="mt-6">
        <button v-if="userStore.user.id !== props.user.id"
          @click="sendFriendshipRequest"
          class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg">
          Follow
        </button>

        <button v-if="userStore.user.id !== props.user.id" @click="sendMessage"
          class="inline-block ml-4 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg">
          Message
        </button>

        <RouterLink :to="{ name: 'profileedit' }"
          v-if="userStore.user.id === props.user.id"
          class="inline-block mr-2 py-4 px-3 bg-gray-600 text-xs text-white rounded-lg">
          Edit
        </RouterLink>

        <button v-if="userStore.user.id === props.user.id" @click="logout"
          class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg">
          Log out
        </button>
      </div>
    </div>
  </div>
</template>