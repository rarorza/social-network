<script setup>
const props = defineProps({username: String})
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
    </div>
  </div>
</template>