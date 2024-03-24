<script setup>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { ref, onMounted, watch, computed } from 'vue'

const userStore = useUserStore()
const conversations = ref([])
const activeConversation = ref({ messages: null })
const body = ref('')
const friends = ref([])

function setActiveConversation(conversation) {
  activeConversation.value = conversation
  getMessages()
}

function getMessages() {
  axios.get(`/api/chat/${activeConversation.value.id}/`).then(response => {
    activeConversation.value = response.data
  }).catch(error => {
    console.log(error);
  })
}

function getConversation() {
  axios.get('/api/chat/').then(response => {
    conversations.value = response.data

    if (!activeConversation.value.messages) {
      activeConversation.value = conversations.value[0]
    }

    getMessages()
  }).catch(error => {
    console.log(error);
  })
}

function submitForm() {
  axios.post(`/api/chat/send/${activeConversation.value.id}/`, {
    body: body.value
  }).then(response => {
    activeConversation.value.messages.push(response.data)
    body.value = ''
  }).catch(error => {
    console.log(error);
  })
}

function getFriends() {
  axios.get(`/api/friends/${userStore.user.id}/`).then(response => {
    friends.value = response.data.friends

    for (const i in conversations.value) {
      for (const iUser in conversations.value[i].users) {
        friends.value = friends.value.filter(
          friend => friend.id !== conversations.value[i].users[iUser].id
        )
      }
    }
  }).catch(error => {
    console.log('Error', error);
  })
}

function sendMessage(idFriend) {
  axios.get(`/api/chat/get-or-create/${idFriend}/`).then(response => {
    friends.value = friends.value.filter(friend => friend.id !== idFriend)
    getConversation()
    setActiveConversation(response.data)
  }).catch(error => {
    console.log('error', error)
  })
}

const friendsLength = computed(() => {
  return Object.keys(friends.value).length
})

onMounted(() => {
  getConversation()
  getFriends()
})

watch(() => conversations, () => {
  getConversation()
}, { immediate: true })

watch(() => friends, () => {
  getFriends()
}, { immediate: true })
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <div class="space-y-4">

          <div v-for="conversation in conversations" :key="conversation.id"
            @click="setActiveConversation(conversation)"
            class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <template v-for="user in conversation.users" :key="user.id">
                <template v-if="user.id !== userStore.user.id">
                  <img :src="user.get_avatar"
                    class="w-[40px] rounded-full cursor-pointer">
                  <p class="text-xs font-bold cursor-pointer">{{ user.name }}
                  </p>
                </template>
              </template>
            </div>
            <span class="text-xs text-gray-500">{{
            conversation.modified_at_formatted }}</span>
          </div>

          <hr v-if="friendsLength">
          <template v-for="friend in friends" :key="friend.id">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2"
                @click="sendMessage(friend.id)">
                <img :src="friend.get_avatar"
                  class="w-[40px] rounded-full cursor-pointer">
                <p class="text-xs font-bold cursor-pointer">{{ friend.name }}
                </p>
              </div>
            </div>
          </template>

        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg ">
        <div class="flex flex-col flex-grow p-4">


          <template v-for="message in activeConversation.messages"
            :key="message.id">
            <div v-if="message.created_by.id === userStore.user.id"
              class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
              <div>
                <div
                  class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                  <p class="text-sm">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none">
                  {{ message.created_at_formatted }} ago
                </span>
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img :src="message.created_by.get_avatar"
                  class="w-[40px] rounded-full">
              </div>
            </div>
            <div v-else class="flex w-full mt-2 space-x-3 max-w-md">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img :src="message.created_by.get_avatar"
                  class="w-[40px] rounded-full">
              </div>
              <div>
                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                  <p class="text-sm">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none">
                  {{ message.created_at_formatted }} ago
                </span>
              </div>
            </div>
          </template>

        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg">

        <form @submit.prevent="submitForm">
          <div class="p-4">
            <textarea v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg resize-none"
              placeholder="What do you want to say?"></textarea>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <button
              class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>