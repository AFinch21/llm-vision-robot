# 🚀 Robot System (Final Plan)

## 🧩 Frontend (Vue + Vite SPA)

- **Tech**: Vue 3 + Vite  
- **Type**: Single Page App (SPA)  
- **Responsibility**:
  - UI (buttons, camera view, controls)
  - Routing (`/`, `/control`, etc.)
  - WebSocket client

👉 Loads **once**, then updates dynamically without reloads  

---

## ⚙️ Backend (Jetson Nano)

- **Tech**: FastAPI (or Node — your choice)  
- **Responsibility**:
  - WebSocket server → robot control  
  - REST endpoints → optional (auth, config, etc.)  
  - GPIO + hardware control  
  - Camera stream  

---

## 🔌 Communication

- **Protocol**: WebSocket ✅  
- **Pattern**:
