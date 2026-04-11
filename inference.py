import os
import json
import requests
from openai import OpenAI

ENV_URL = os.environ.get("ENV_URL", "https://gargianilpathak01-medical-triage-env.hf.space")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.2-3B-Instruct")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api-inference.huggingface.co/v1")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def call_llm(patient_info: dict) -> dict:
    prompt = f"""You are an expert emergency room triage doctor. Analyze this patient and respond ONLY with valid JSON.

Patient:
- Age: {patient_info.get('age')}
- Symptoms: {patient_info.get('symptoms')}
- Vitals: {patient_info.get('vitals')}

Respond ONLY with this JSON format:
{{"urgency": "critical|urgent|normal|low", "department": "ER|cardiology|neurology|orthopedics|GP|psychiatry"}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.1,
    )
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def run_episode(task: str = "easy"):
    print(f"[START] task={task} model={MODEL_NAME}", flush=True)

    res = requests.post(f"{ENV_URL}/reset", params={"task": task})
    obs = res.json()
    print(f"[START] episode_reset patient_id={obs.get('patient_id')} step=0", flush=True)

    done = False
    step = 0
    total_reward = 0.0

    while not done:
        step += 1
        try:
            action = call_llm(obs)
        except Exception as e:
            print(f"[STEP] step={step} error={e}", flush=True)
            action = {"urgency": "urgent", "department": "ER"}

        print(f"[STEP] step={step} patient_id={obs.get('patient_id')} urgency={action.get('urgency')} department={action.get('department')}", flush=True)

        res = requests.post(f"{ENV_URL}/step", json=action)
        result = res.json()

        reward = result.get("reward", {}).get("value", 0.5)
        reason = result.get("reward", {}).get("reason", "")
        total_reward += reward
        done = result.get("done", True)
        obs = result.get("observation", {})

        print(f"[STEP] step={step} reward={reward} reason={reason} done={done}", flush=True)

    state_res = requests.get(f"{ENV_URL}/state")
    state = state_res.json()
    avg_score = state.get("avg_score", round(total_reward / step, 2) if step > 0 else 0.5)

    normalized = max(0.01, min(0.99, round(total_reward / step, 2) if step > 0 else 0.5))
    print(f"[END] task={task} steps={step} total_reward={normalized} avg_score={avg_score}", flush=True)
    return normalized

if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_episode(task)
