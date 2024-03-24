<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'

const trends = ref([])

function getTrends() {
  axios.get('/api/posts/trends/').then(response => {
    console.log('response:', response.data);
    trends.value = response.data
  }).catch(error => {
    console.log('error:', error);
  })
}

const trendsLength = computed(() => {
  return Object.keys(trends.value).length
})

onMounted(() => {
  getTrends()
})
</script>

<template>
  <template v-if="trendsLength">
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
      <h3 class="mb-6 text-xl">Trends</h3>

      <div class="space-y-4">
        <div v-for="trend in trends" :key="trend.id"
          class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <p class="text-xs">
              <strong>{{ trend.hashtag }}</strong><br>
              <span class="text-gray-500">{{ trend.occurrences }} posts</span>
            </p>
          </div>
          <RouterLink :to="{ name: 'trends', params: { id: trend.hashtag } }"
            class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">
            Explore
          </RouterLink>
        </div>
      </div>

    </div>
  </template>
</template>