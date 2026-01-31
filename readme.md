# 🧠 Enhanced Synthetic Chatroom

**Enhanced Synthetic Chatroom** is a full-stack, real-time discussion platform designed to simulate
high-fidelity social signals using synthetic data.
It combines a modern chat UI with a FastAPI backend and a smart synchronization engine that enables
incremental data updates, historical tracking, and realistic message streaming.

This project is ideal for:
- Synthetic social signal generation
- AI / agent testing environments
- Hackathons & demos
- Real-time feed simulations
- Backend-frontend system design showcases

---

## ✨ Key Features

- 💬 Modern Chat Interface (Slack / Discord style)
- 🔄 Delta-based Sync Engine (`/api/sync`)
- 🧪 Synthetic data simulation via JSON seeding
- 🗂 Channel-based discussions
- 🛠 Admin reset & control APIs
- 🌙 Dark mode optimized UI

---

## 🧱 Tech Stack

### Frontend
- React 18 (TypeScript)
- Vite
- Tailwind CSS
- Axios

### Backend
- FastAPI
- SQLite + SQLAlchemy
- Pydantic
- Uvicorn

---

## 📂 Project Structure
```text
enhanced_synthetic_chatroom/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── chatroom.db
│   └── history.json
├── frontend/
│   ├── src/
│   └── tailwind.config.ts
├── chat_data_1.json
├── seed_data.py
└── README.md
```

---

## 🧰 Prerequisites

- Node.js 18+
- Python 3.9+
- npm & pip

---

## ⚙️ Installation

### Backend

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic requests

### Frontend

cd frontend
npm install

---

## ▶️ Running the App

### Backend
uvicorn app.main:app --reload --port 8000

### Frontend
npm run dev

Frontend: http://localhost:3000  
Backend: http://127.0.0.1:8000

---

## 🔄 Sync API

GET /api/sync  
Returns only new posts/comments using history-based delta tracking.

---

## 📜 License

Open-source for demo, research, and educational use.

---

## 👤 Author

Ved Prakash  
https://github.com/Warrior-Ved
