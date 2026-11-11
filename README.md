# Local LLM Infrastructure & Optimization on AMD (RX 7600)

## 📌 Project Overview
An infrastructure and hardware optimization project focused on deploying and running large local language models (specifically Qwen 2.5 Coder 7B/8B) on consumer-grade AMD hardware. 

The primary goal of this project was to overcome AMD's historical bottlenecks in AI workloads, managing the strict **8GB VRAM limitation** of the Radeon RX 7600, while maintaining high generation speeds and eliminating logic hallucinations for complex asynchronous Python/C++ code generation.

## ⚙️ Tech Stack & Hardware
* **Hardware:** AMD Ryzen 5 7600X, 32GB DDR5 RAM, AMD Radeon RX 7600 (8GB VRAM)
* **OS Environment:** Windows 11 / Kali Linux (Dual-Boot Setup)
* **LLM Backend:** Ollama / LLaMA.cpp (Vulkan API)
* **Client & Models:** Msty Studio, Qwen 2.5 Coder (7B), Python (REST API Client)

---

## 🛠️ Challenges & Troubleshooting

### 1. VRAM Overflow & GPU Layer Optimization
* **Problem:** Loading an entire 7B/8B model strictly into the GPU's 8GB VRAM caused memory overflow. The backend automatically offloaded layers to the slower system RAM, causing generation speeds to bottleneck at `~10 tokens/sec`.
* **Solution:** Precision tuning of the `GPU Layers` parameter for the **Vulkan backend**. Through stress testing, I found the optimal balance at **28–30 layers**. This kept the active context strictly within the 8GB VRAM limit, eliminating RAM fallback and skyrocketing generation speed to a stable **40–50 tokens/sec**.

### 2. Cyrillic Path Encoding Crash (Backend Failure)
* **Problem:** Fatal backend crash during model initialization (`server_exited exit code 1`, `DirectFile error 3`).
* **Root Cause:** Local backends are highly sensitive to character encoding. The Windows user profile path contained Cyrillic characters, breaking the system's ability to parse manifests and load `.gguf` / `blob` weight files correctly.
* **Solution:** Reconfigured the workspace and model storage directories to a strict ASCII-compliant path at the root of the drive (e.g., `C:\LLM_Models\`), resolving the fatal initialization crash.

### 3. Mitigating Architectural Hallucinations & Logic Errors
* **Problem:** Without strict system prompts and at default temperatures, the model suffered from severe logic degradation. When tested with a logic riddle ("I have branches, but no leaves..."), the model hallucinated absurd answers like "a snake" or overcomplicated it to "a linked list" instead of the correct programmatic concept.
* **Evidence:**
  
  *(See how the model hallucinated a biological snake or over-engineered a linked list before prompt optimization)*
  ![Hallucination 1: Linked List](images/hallucination_linked_list.png)
  ![Hallucination 2: Snake](images/hallucination_snake.png)

* **Solution:** 
  * Decreased the `Temperature` parameter to **0.4** for highly deterministic, logic-based outputs.
  * Engineered a strict **System Prompt** enforcing a "Senior Systems Engineer" persona, prioritizing thread-safety and shared state logic.

---

## 🚀 API Client & Final Benchmark
To interact with the optimized local Ollama backend, I developed a lightweight Python API client (`scripts/msty_api_client.py`). It enforces the optimized parameters over a local REST API connection (`http://localhost:11434`).

**Final Stress Test:**
I requested the model to generate a thread-safe, asynchronous task worker pool in Python (`asyncio`).

**Results:**
The optimized backend successfully generated production-ready, OOP-compliant code in just **18.29 seconds** without hitting VRAM bottlenecks.

```text
PS C:\Local-LLM-AMD-Optimization> python -u "c:\Local-LLM-AMD-Optimization\scripts\msty_api_client.py"
[*] Sending request to local Qwen 2.5 backend...
[+] Generation successful! Time taken: 18.29 seconds

--- GENERATED CODE ---
# (Thread-safe Async Task Worker Pool successfully generated)