from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import PatientObservation, TriageAction
from environment import MedicalTriageEnv

app = FastAPI(title="Medical Triage RL Environment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

envs = {}

@app.get("/")
def root():
    return {"message": "Medical Triage RL Environment", "status": "running"}

@app.post("/reset")
def reset(task: str = "easy"):
    env = MedicalTriageEnv(task=task)
    envs["default"] = env
    obs = env.reset()
    return obs

@app.post("/step")
def step(action: TriageAction):
    env = envs.get("default")
    if not env:
        return {"error": "Call /reset first"}
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.get("/state")
def state():
    env = envs.get("default")
    if not env:
        return {"error": "Call /reset first"}
    return env.state()