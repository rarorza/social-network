<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
</script>

<template>
  <Navbar />
  <main class="px-8 py-6 bg-gray-100 min-h-screen">
    <RouterView />
  </main>
</template>

<style scoped></style>
