import { ref, watch } from 'vue'

const likes = ref(Number(localStorage.getItem('likes')) || 0)
const dislikes = ref(Number(localStorage.getItem('dislikes')) || 0)

function like() {
  likes.value++
}

function dislike() {
  dislikes.value++
}

function resetCounts() {
  likes.value = 0
  dislikes.value = 0
}

watch(likes, (newValue) => {
  localStorage.setItem('likes', newValue)
})

watch(dislikes, (newValue) => {
  localStorage.setItem('dislikes', newValue)
})

export function useLikes() {
  return {
    likes,
    dislikes,
    like,
    dislike,
    resetCounts,
  }
}