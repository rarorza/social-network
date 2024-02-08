<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
import ToastNotification from './components/ToastNotification.vue';
</script>

<template>
  <Navbar />
  
  <main class="px-8 py-6 bg-gray-100 min-h-screen">
    <RouterView />
  </main>

  <ToastNotification />
</template>

<style scoped></style>
