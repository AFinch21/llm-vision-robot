const websocket = new WebSocket('ws://localhost:8000/ws')



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