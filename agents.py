# backend/agents.py – Valencia Walker

import openai
import os

# Load API key securely from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_ai_agent(prompt: str, task_type: str = "general") -> str:
    # Define task-specific system message
    system_message = "You are an intelligent AI agent for digital twin development."

    if task_type == "motor_script":
        system_message = "You are a robotics programming assistant. Generate Python code to simulate or control a motor."
    elif task_type == "verify_circuit":
        system_message = "You are an electronics expert. Review and verify circuit connections and logic from user input."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
