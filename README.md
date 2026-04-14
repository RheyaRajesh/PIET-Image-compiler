# 🎨 Piet Image Compiler

Welcome to the **Piet Image Compiler**, a full-stack web application that brings esoteric programming to life! 

[Piet](https://www.dangermouse.net/esoteric/piet.html) is a visual programming language where the code looks like abstract art. Programs are composed of blocks of color, and the interpreter navigates through these colors to execute logic. This compiler provides an interactive, beautiful interface to upload your Piet masterpieces, adjust codel sizes, and visually trace the execution step-by-step as it evaluates the code and outputs the results!

Be it "Hello World" or a complex algorithm, if it's painted correctly, it runs!

## 🚀 Features
- **Visual Uploads**: Upload your Piet programs as image files.
- **Adjustable Codel Size**: Easily scale your logical blocks to match upscaled or pixel-art images.
- **Smart Execution**: A robust backend written in Python automatically parses the hexagonal color grid to simulate the DP/CC traversal.
- **Interactive UI**: A vibrant, modern interface built with React and Tailwind CSS.
- **Debugging Trace**: See real-time operation steps like `push`, `add`, `out(char)` and the stack state as the program runs.

## 🛠️ Setup & Installation

To run this application locally, you will need two terminal windows: one to power the Python backend and one to serve the React frontend.

### 1. Start the Backend (FastAPI + Python)

Navigate to the `backend` directory, activate the environment, and start the server.

```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
*The backend will run on http://localhost:8000*

### 2. Start the Frontend (Vite + React)

Open a new terminal window, navigate to the `frontend` directory, and start the Vite development server.

```powershell
cd frontend
npm install
npm run dev
```
*The frontend will be available at http://localhost:5173*. Click the link in your terminal to open it in your browser!

---
*Happy Painting & Programming!*
