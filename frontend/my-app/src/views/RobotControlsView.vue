<script setup>
import { onBeforeUnmount, onMounted } from 'vue'
import { useWebsocketControls } from '../composables/useWebsocketControls'

const { startMovement, stopMovement } = useWebsocketControls()
const activeKeys = new Set()

const keyMap = {
  w: { direction: 'forward', component: 'chassis' },
  a: { direction: 'left', component: 'chassis' },
  s: { direction: 'backward', component: 'chassis' },
  d: { direction: 'right', component: 'chassis' },
  ArrowUp: { direction: 'forward', component: 'camera' },
  ArrowLeft: { direction: 'left', component: 'camera' },
  ArrowDown: { direction: 'backward', component: 'camera' },
  ArrowRight: { direction: 'right', component: 'camera' },
}

function press(direction, component) {
  startMovement(direction, 1, component)
}

function release(direction, component) {
  stopMovement(direction, component)
}

function shouldIgnoreKeyboardShortcut(event) {
  const target = event.target
  return (
    target instanceof HTMLElement &&
    (target.tagName === 'INPUT' ||
      target.tagName === 'TEXTAREA' ||
      target.isContentEditable)
  )
}

function handleKeyDown(event) {
  if (shouldIgnoreKeyboardShortcut(event)) {
    return
  }

  const binding = keyMap[event.key]

  if (!binding || event.repeat || activeKeys.has(event.key)) {
    return
  }

  event.preventDefault()
  activeKeys.add(event.key)
  press(binding.direction, binding.component)
}

function handleKeyUp(event) {
  const binding = keyMap[event.key]

  if (!binding) {
    return
  }

  event.preventDefault()
  activeKeys.delete(event.key)
  release(binding.direction, binding.component)
}

function handleWindowBlur() {
  for (const key of activeKeys) {
    const binding = keyMap[key]
    if (binding) {
      release(binding.direction, binding.component)
    }
  }

  activeKeys.clear()
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
  window.addEventListener('blur', handleWindowBlur)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
  window.removeEventListener('blur', handleWindowBlur)
})
</script>

<template>
  <section class="robot-controls">
    <h1>Robot Controls</h1>

    <!-- Dummy camera screen -->
    <div class="camera-shell">
      <div class="camera-feed">
        <span class="camera-label">Camera feed (dummy)</span>
      </div>
    </div>

    <div class="controls-row">
      <div>
        <h2>Chassis</h2>
        <div class="chassis-dpad">
          <button
            class="control-btn up"
            @pointerdown="press('forward', 'chassis')"
            @pointerup="release('forward', 'chassis')"
            @pointercancel="release('forward', 'chassis')"
            @pointerleave="release('forward', 'chassis')"
          >
            W
          </button>

          <button
            class="control-btn left"
            @pointerdown="press('left', 'chassis')"
            @pointerup="release('left', 'chassis')"
            @pointercancel="release('left', 'chassis')"
            @pointerleave="release('left', 'chassis')"
          >
            A
          </button>

          <button
            class="control-btn right"
            @pointerdown="press('right', 'chassis')"
            @pointerup="release('right', 'chassis')"
            @pointercancel="release('right', 'chassis')"
            @pointerleave="release('right', 'chassis')"
          >
            D
          </button>

          <button
            class="control-btn down"
            @pointerdown="press('backward', 'chassis')"
            @pointerup="release('backward', 'chassis')"
            @pointercancel="release('backward', 'chassis')"
            @pointerleave="release('backward', 'chassis')"
          >
            S
          </button>
        </div>
      </div>

      <div>
        <h2>Camera</h2>
        <div class="camera-dpad">
          <button
            class="control-btn up"
            @pointerdown="press('forward', 'camera')"
            @pointerup="release('forward', 'camera')"
            @pointercancel="release('forward', 'camera')"
            @pointerleave="release('forward', 'camera')"
          >
            ↑
          </button>

          <button
            class="control-btn left"
            @pointerdown="press('left', 'camera')"
            @pointerup="release('left', 'camera')"
            @pointercancel="release('left', 'camera')"
            @pointerleave="release('left', 'camera')"
          >
            ←
          </button>

          <button
            class="control-btn right"
            @pointerdown="press('right', 'camera')"
            @pointerup="release('right', 'camera')"
            @pointercancel="release('right', 'camera')"
            @pointerleave="release('right', 'camera')"
          >
            →
          </button>

          <button
            class="control-btn down"
            @pointerdown="press('backward', 'camera')"
            @pointerup="release('backward', 'camera')"
            @pointercancel="release('backward', 'camera')"
            @pointerleave="release('backward', 'camera')"
          >
            ↓
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.robot-controls {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem;
}

.camera-shell {
  margin: 1rem 0 2rem;
}

.camera-feed {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  background: linear-gradient(135deg, #1f2937, #111827);
  border: 2px solid #374151;
  display: grid;
  place-items: center;
}

.camera-label {
  color: #d1d5db;
  font-size: 1rem;
}

.controls-row {
  margin: 1.5rem auto 0;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 15rem;
  flex-wrap: wrap;
}

.chassis-dpad {
  margin: 0 auto;
  width: 260px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 72px 72px 72px;
  gap: 0.75rem;
  grid-template-areas:
    ". up ."
    "left . right"
    ". down .";
}

.camera-dpad {
  margin: 0 auto;
  width: 260px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 72px 72px 72px;
  gap: 0.75rem;
  grid-template-areas:
    ". up ."
    "left . right"
    ". down .";
}

.control-btn {
  font-size: 1.8rem;
  border: none;
  border-radius: 10px;
  background: #1f2937;
  color: white;
  cursor: pointer;
  user-select: none;
}

.control-btn:active {
  transform: scale(0.98);
  background: #111827;
}

.up { grid-area: up; }
.left { grid-area: left; }
.right { grid-area: right; }
.down { grid-area: down; }
</style>