# 📘 CodeXR – AI Coding Assistant for AR/VR Developers

## 🚀 Overview  
**CodeXR** is an AI-powered coding assistant designed to help AR/VR developers working with **Unity, Unreal, and Shaders**.  
It accelerates development by:  

- 🔹 Breaking down queries into **step-by-step subtasks**  
- 🔹 Providing **ready-to-paste code snippets** (C#, C++, ShaderLab)  
- 🔹 Highlighting **gotchas and best practices**  
- 🔹 Linking to **official documentation** and tutorials  
- 🔹 Supporting **error debugging mode**  
- 🔹 Delivering **structured JSON outputs** for easy integration  

---

## 📂 Phased Development  

### **Phase 1 – Streamlit MVP**  
A demo assistant to validate feasibility.

#### Features  
- 🖊️ **Text-based input** (voice optional via Whisper)  
- 📑 **Context classification** (Unity / Unreal / Shader / General)  
- 🌐 **Web search grounding** (Bing/Serper API)  
- 🤖 **LLM processing** with Gemini-2.5, GPT-4o-mini, or StarCoder2  
- 📦 **JSON-validated responses** via Pydantic  

#### Example Execution  
1. Run Streamlit app:  
   ```bash
   streamlit run src/main.py
   ```
2. In the sidebar:  
   - Enter query: *“How do I add teleport locomotion in Unity VR?”*  
   - Choose LLM model → Submit  
3. Output will include:  
   - ✅ Subtasks  
   - ✅ Code snippet  
   - ✅ Gotchas / Best practices  
   - ✅ Difficulty rating  
   - ✅ Documentation link  
   - ✅ Raw JSON response  

---

### **Phase 2 – RAG-Lite & Debugging Mode**  
Enhances reliability with offline docs and log analysis.

#### Features  
1. **RAG-Lite Retriever**  
   - Indexes **Unity XR Toolkit docs, Unreal docs, Shader references**  
   - Fetches relevant offline content  
   - Reduces hallucinations and improves speed  

2. **Error Debugging Mode**  
   - Developers can **paste error logs**  
   - Assistant analyzes errors and suggests fixes  
   - Example:  
     ```
     Input: NullReferenceException: TeleportationProvider not set
     Output: Assign TeleportationProvider in the Inspector or via script
     ```  

#### Example Execution  
1. Build the docs index:  
   ```bash
   cd src
   python -m utils.docs_loader
   ```
   - Downloads & cleans Unity/Unreal/Shader docs  
   - Splits into chunks and builds FAISS index  

2. Run assistant with error logs:  
   - Paste logs in sidebar → Submit  
   - Output will show **debug explanation + suggested fix**  

3. Run assistant with coding query:  
   - Enter query: *“Which shader works best for AR occlusion?”*  
   - Response includes **retrieved docs + structured JSON**  

---

### **Phase 3 – VS Code Extension**  
Integrates CodeXR directly into the IDE.

#### Features  
- **Ask CodeXR** command (via Command Palette)  
- **Explain with CodeXR** (right-click error/code → explain)  
- **Side panel assistant** showing: subtasks, code, docs, best practices  
- **Insert snippet** into active editor  

#### Example Snippet Inserted:  
```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class TeleportSetup : MonoBehaviour
{
    public TeleportationProvider teleportationProvider;

    void Start()
    {
        if (teleportationProvider == null)
            Debug.LogError("TeleportationProvider not set");
    }
}
```

#### Example Execution  
1. Install dependencies:  
   ```bash
   npm install
   npm run compile
   ```

2. Run backend:  
   ```bash
   cd backend
   uvicorn server:app --reload --port 8000
   ```

3. Confirm FastAPI backend: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

4. Launch in VS Code:  
   - Press `F5` → Opens **Extension Development Host**  
   - Open file `test_snippet.cs`  
   - Run **Ask CodeXR** or highlight → **Explain with CodeXR**  

---

## ⚙️ Installation & Setup  

### Prerequisites  
- [Python 3.10+](https://www.python.org/)  
- [Node.js 18+](https://nodejs.org/)  
- [Streamlit](https://streamlit.io/)  
- [VS Code 1.103.0+](https://code.visualstudio.com/)  
- [FFmpeg](https://ffmpeg.org/) (for Whisper)  

### Clone the Repo  
```bash
git clone https://github.com/your-username/CodeXR.git
cd CodeXR
```

### Run Phase 1 (Streamlit)  
```bash
pip install -r requirements.txt
streamlit run src/main.py
```

### Run Phase 2 (Docs Loader for RAG)  
```bash
cd src
python -m utils.docs_loader
```

### Run Phase 3 (VS Code Extension)  
```bash
npm install
npm run compile
cd backend
uvicorn server:app --reload --port 8000
```

---

## ✅ Roadmap  
- [x] **Phase 1:** Streamlit MVP  
- [x] **Phase 2:** RAG-Lite + Debugging Mode  
- [x] **Phase 3:** VS Code Extension  
- [ ] **Phase 4:** Multi-turn chat inside panel  
- [ ] **Phase 5:** Context-aware debugging from entire project  

---

## 👨‍💻 Contributing  
Pull requests welcome. Run lint before committing:  
```bash
npm run lint
```

---

## 📜 License  
MIT License © 2025 CodeXR  
