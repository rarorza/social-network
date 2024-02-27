<script setup>
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { ref, onMounted } from 'vue'

const userStore = useUserStore()
const conversations = ref([])
const activeConversation = ref({})
const body = ref('')

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
    console.log('getConversation', response.data);

    if (conversations.value) {
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
  }).catch(error => {
    console.log(error);
  })
}

onMounted(() => {
  getConversation()
})
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
              <img src="https://i.pravatar.cc/300?img=43"
                class="w-[40px] rounded-full">
              <p v-for="user in conversation.users" :key="user.id"
                class="text-xs font-bold">
                <template v-if="user.id !== userStore.user.id">{{ user.name
                }}</template>
              </p>
            </div>
            <span class="text-xs text-gray-500">{{
              conversation.modified_at_formatted }}</span>
          </div>

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
                <img src="https://i.pravatar.cc/300?img=43"
                  class="w-[40px] rounded-full">
              </div>
            </div>
            <div v-else class="flex w-full mt-2 space-x-3 max-w-md">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img src="https://i.pravatar.cc/300?img=12"
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