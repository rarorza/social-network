<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const notifications = ref([])

function getNotifications() {
  axios.get('/api/notifications/').then(response => {
    console.log(response.data)
    notifications.value = response.data
  }).catch(error => {
    console.log('Error: ', error)
  })
}

async function readNotification(notification) {
  await axios.post(`/api/notifications/read/${notification.id}/`).then(response => {
    console.log(response.data)

    if (notification.type_of_notification == 'post_like' || notification.type_of_notification == 'post_comment') {
      router.push({ name: 'post', params: { id: notification.post_id } })
    } else {
      router.push({ name: 'friends', params: { id: notification.created_for_id } })
    }
  }).catch(error => {
    console.log('Error: ', error)
  })
}

onMounted(() => {
  getNotifications()
})

const notificationsLength = computed(() => {
  return Object.keys(notifications.value).length
})
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="notification in notifications" :key="notification.id" v-if="notificationsLength">
        {{ notification.body }}

        <button class="underline" @click="readNotification(notification)">Read more</button>
      </div>
      <div v-else class="p-4 bg-white border border-gray-200 rounded-lg">
        <p>You don't have any notification.</p>
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
    </div>
  </div>
</template>