# Mini Project

Welcome to the **Mini Project** repository! Follow the steps below to set up and run the project on your local machine.

## 📌 Prerequisites

Ensure you have the following installed before proceeding:
- **Python 3.11** (Recommended: Install via [Anaconda](https://www.anaconda.com/))
- **Node.js** (Check installation with `node -v` and `npm -v`)
- **Git** (For cloning the repository)

## 🚀 Installation and Setup

### 1️⃣ Clone the Repository
```sh
 git clone https://github.com/Sandeepkandula2004/Mini_Project.git
 cd Mini_Project
```

### 2️⃣ Create and Activate a Virtual Environment
```sh
 conda create -p venv python==3.11 -y
```
Activate the environment:
- **Windows:**  
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux:**  
  ```sh
  source venv/bin/activate
  ```

### 3️⃣ Install Node.js (If Not Installed)
Download and install [Node.js](https://nodejs.org/), then ensure it’s added to your system path.

### 4️⃣ Install Node Dependencies
```sh
 cd my-react-app/my-react-app
 npm install
```

### 5️⃣ Install Python Dependencies
First, install **dlib** manually:
```sh
 pip install "<PATH_TO_DLIB_FILE>"
```
Make sure you replace `<PATH_TO_DLIB_FILE>` with the actual path.

Then, install other dependencies:
```sh
 pip install -r requirements.txt
```

## 🎯 Running the Project

Open **CMD (Not PowerShell)** and split it into two terminals:

### **Terminal 1: Start the Backend Server**
```sh
 cd backend
 python server.py
```

### **Terminal 2: Start the Frontend**
```sh
 cd my-react-app/src
 npm run dev
```

After running the frontend, a Vite development server will start, usually at:
```sh
 http://localhost:5734
```
Click on the link to access the application.

---

✅ **That's it! Your project should now be running successfully.** 🚀

