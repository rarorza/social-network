<script setup>
import axios from 'axios'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { useUserStore } from '@/stores/user'

const props = defineProps({ post: Object })
const emit = defineEmits(['deletePost', 'reportPost'])
const userStore = useUserStore()

function likePost(id) {
  axios.post(`/api/posts/like/${id}/`).then(response => {
    if (response.data.message == 'like created') {
      props.post.likes_count += 1
    }
  }).catch(error => {
    console.log('error', error)
  })
}

function deletePostEmit(id) {
  emit('deletePost', id)
}

function reportPostEmit(id) {
  emit('reportPost', id)
}
</script>

<template>
  <div class="mb-6 flex items-center justify-between">
    <div class="flex items-center space-x-6">
      <RouterLink
        :to="{ name: 'profile', params: { 'id': post.created_by.id } }">
        <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full">
      </RouterLink>

      <RouterLink
        :to="{ name: 'profile', params: { 'id': post.created_by.id } }">
        <p><strong>{{ post.created_by.name }}</strong></p>
      </RouterLink>
    </div>

    <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
  </div>

  <p>{{ post.body }}</p>
  <template v-if="post.attachments.length">
    <img v-for="image in post.attachments" :key="image.id"
      :src="image.get_image" class="w-full mb-4 rounded-xl">
  </template>

  <div class="my-6 flex justify-between">
    <div class="flex space-x-6">
      <div class="flex items-center space-x-2 cursor-pointer"
        @click="likePost(post.id)">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
          </path>
        </svg>

        <span class="text-gray-500 text-xs">{{ post.likes_count }} likes</span>
      </div>

      <RouterLink :to="{ name: 'post', params: { id: post.id } }"
        class="flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
          </path>
        </svg>

        <span class="text-gray-500 text-xs">{{ post.comments_count }}
          comments</span>
      </RouterLink>

      <div v-if="post.is_private"
        class="flex items-center space-x-2 text-gray-500 text-xs">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
        </svg>
        <span>Is private</span>
      </div>
    </div>
    
    <Menu as="div" class="relative inline-block text-left">
      <MenuButton
        class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
          </path>
        </svg>
      </MenuButton>

      <transition enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95">
        <MenuItems
          class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
          <div class="py-1">
            <MenuItem v-if="post.created_by.id === userStore.user.id" v-slot="{ active }" @click="deletePostEmit(post.id)">
            <span
              :class="[active ? 'bg-gray-100 text-gray-900 cursor-pointer' : 'text-gray-700', 'block px-4 py-2 text-sm']">Delete post</span>
            </MenuItem>
            <MenuItem v-slot="{ active }" @click="reportPostEmit(post.id)">
            <span
              :class="[active ? 'bg-gray-100 text-gray-900 cursor-pointer' : 'text-gray-700', 'block px-4 py-2 text-sm']">Report post</span>
            </MenuItem>
          </div>
        </MenuItems>
      </transition>
    </Menu>
  </div>
</template>