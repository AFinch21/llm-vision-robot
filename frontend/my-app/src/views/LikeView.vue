<script setup>
import LikeCounter from '../components/LikeCounter.vue'
import { useLikes } from '../composables/useLikes'

const { likes, dislikes, like, dislike, resetCounts } = useLikes()
</script>

<template>
  <LikeCounter
    :likes="likes"
    :dislikes="dislikes"
    @like="like"
    @dislike="dislike"
    @reset="resetCounts"
  />
</template>