<script setup>
const props = defineProps({
  likes: Number,
  dislikes: Number,
})

const emit = defineEmits(['like', 'dislike', 'reset'])
</script>

<template>
  <h1>👍 Likes: {{ props.likes }}</h1>
  <h1>👎 Dislikes: {{ props.dislikes }}</h1>
  <button @click="emit('like')">Like</button>
  <button @click="emit('dislike')">Dislike</button>
  <button @click="emit('reset')">Reset</button>
</template>