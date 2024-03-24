<script setup>
import axios from 'axios'
import { ref, computed, onMounted} from 'vue'

const users = ref([])

function getFriendSuggestions() {
  axios.get('/api/friends/suggestions/').then(response => {
    users.value = response.data
  }).catch(error => {
    console.log('Error: ', error)
  })
}

const usersLength = computed(() => {
  return Object.keys(users.value).length
})


onMounted(() => {
  getFriendSuggestions()
})
</script>

<template>
  <template v-if="usersLength">
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
      <h3 class="mb-6 text-xl">People you may know</h3>
      
      <div class="space-y-4">
        <div v-for="user in users" :key="user.id" class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <img :src="user.get_avatar"
            class="w-[40px] rounded-full">
            
            <p class="text-xs"><strong>{{ user.name }}</strong></p>
          </div>
          
          <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }"
          class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</RouterLink>
        </div>
      </div>
    </div>
  </template>
</template>