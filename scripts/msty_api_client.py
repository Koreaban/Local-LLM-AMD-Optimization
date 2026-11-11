import requests
import json
import time

def generate_code():
    api_url = "http://localhost:11434/v1/chat/completions"
    
    payload = {
        "model": "qwen2.5-coder:7b",
        "messages": [
            {
                "role": "system", 
                "content": "You are a Senior Systems Engineer. Write thread-safe, production-ready code."
            },
            {
                "role": "user", 
                "content": "Write a simple async task worker pool in Python."
            }
        ],
        "temperature": 0.4,
        "max_tokens": 1024
    }

    headers = {"Content-Type": "application/json"}

    print("[*] Sending request to local Qwen 2.5 backend...")
    start_time = time.time()

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result['choices'][0]['message']['content']
        
        execution_time = time.time() - start_time
        print(f"[+] Generation successful! Time taken: {execution_time:.2f} seconds\n")
        print("--- GENERATED CODE ---\n")
        print(generated_text)
        
    except requests.exceptions.ConnectionError:
        print("[!] Error: Cannot connect to the local LLM server. Is Msty Studio running?")
    except Exception as e:
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    generate_code()