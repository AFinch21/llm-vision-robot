let websocket
let reconnectTimer

function getWebsocketUrl() {
  if (import.meta.env.VITE_WEBSOCKET_URL) {
    return import.meta.env.VITE_WEBSOCKET_URL
  }

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'

  // During Vite development the backend normally runs separately on port 8000.
  // In production FastAPI serves the built frontend, so use the current origin.
  const host = import.meta.env.DEV
    ? `${window.location.hostname}:8000`
    : window.location.host

  return `${protocol}//${host}/ws`
}

function connect() {
  if (
    websocket?.readyState === WebSocket.OPEN ||
    websocket?.readyState === WebSocket.CONNECTING
  ) {
    return
  }

  websocket = new WebSocket(getWebsocketUrl())

  websocket.addEventListener('close', () => {
    window.clearTimeout(reconnectTimer)
    reconnectTimer = window.setTimeout(connect, 1000)
  })

  websocket.addEventListener('error', () => {
    websocket.close()
  })
}

connect()



function startMovement(direction, distance, component) {
  const message = {
    type: 'start_movement',
    component,
    direction,
    distance,
  }

  console.log('Sending start movement message:', message)

  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(message))
  }
}

function stopMovement(direction, component) {
  const message = {
    type: 'stop_movement',
    component,
    direction
  }

  console.log('Sending stop movement message:', message)

  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(message))
  }
}

export function useWebsocketControls() {
  return {
    startMovement,
    stopMovement,
  }
}
