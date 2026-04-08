---
title: Medical Triage RL Env
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
short_description: Medical triage RL environment for Meta PyTorch Hackathon
---

# 🏥 Medical Triage RL Environment

An RL environment where AI agents learn to make emergency room triage decisions. Built for the **Meta PyTorch OpenEnv Hackathon**.

## 🎯 Problem
Triage errors in emergency rooms cost lives. This environment trains AI agents to correctly assess patient urgency and route them to the right department.

## 🔁 How It Works
1. Patient arrives with symptoms + vitals
2. Agent observes the patient state
3. Agent decides: urgency level + department
4. Environment scores the decision
5. Agent learns over many episodes

## 📊 Reward Function
| Score | Meaning |
|-------|---------|
| 1.0 | Perfect — correct urgency + department |
| 0.6 | Correct urgency, close department |
| 0.4 | One correct, one slightly off |
| 0.1 | Dangerous misclassification |
| 0.0 | Critical patient marked as low |

## 🏋️ Task Difficulty
| Task | Patients | Description |
|------|----------|-------------|
| easy | 8 | Clear-cut symptoms, obvious decisions |
| medium | 8 | Overlapping symptoms, requires reasoning |
| hard | 8 | Ambiguous, multiple conditions, tricky vitals |

## 🔌 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/reset?task=easy` | Start new episode |
| POST | `/step` | Submit triage action |
| GET | `/state` | Current environment state |

## 💊 Action Space
```json
{
  "urgency": "critical | urgent | normal | low",
  "department": "ER | cardiology | neurology | orthopedics | GP | psychiatry"
}
```

## 🧠 Observation Space
- Patient age + symptoms
- Vital signs (BP, HR, O2)
- Current step + max steps

## 🛠 Tech Stack
FastAPI · Pydantic · OpenEnv · Hugging Face Spaces · Docker