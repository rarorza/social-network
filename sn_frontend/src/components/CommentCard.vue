<script setup>
const props = defineProps({ comment: Object })
</script>

<template>
  <div class="mb-6 flex items-center justify-between">
    <div class="flex items-center space-x-6">
      <RouterLink :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">
        <img src="https://i.pravatar.cc/300?img=12" class="w-[40px] rounded-full">
      </RouterLink>

      <RouterLink :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">
        <p><strong>{{ comment.created_by.name }}</strong></p>
      </RouterLink>
    </div>

    <p class="text-gray-600">{{ comment.created_at_formatted }} ago</p>
  </div>

  <p>{{ comment.body }}</p>
</template>