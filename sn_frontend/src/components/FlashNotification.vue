<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  errorsProps: Array,
  classesProps: String,
})
</script>

<template>
  <div v-if="$props.errorsProps.length > 0">
    <div :class="`${$props.classesProps} text-white rounded-lg p-6`">
      <p v-for="error in $props.errorsProps" :key="error">{{ error }}</p>
    </div>
  </div>
</template>