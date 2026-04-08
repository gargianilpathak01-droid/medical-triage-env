import random
from models import PatientObservation, TriageReward

# Easy patients - clear cut, obvious symptoms
EASY_PATIENTS = [
    {"id": "e1", "age": 45, "symptoms": "Chest pain, shortness of breath, sweating", "vitals": "BP: 160/100, HR: 110, O2: 94%", "urgency": "critical", "department": "ER", "hint": "classic heart attack symptoms"},
    {"id": "e2", "age": 32, "symptoms": "Mild fever, sore throat, cough", "vitals": "BP: 120/80, HR: 78, O2: 98%", "urgency": "normal", "department": "GP", "hint": "common cold"},
    {"id": "e3", "age": 28, "symptoms": "Broken arm after fall, severe pain", "vitals": "BP: 125/82, HR: 88, O2: 99%", "urgency": "urgent", "department": "orthopedics", "hint": "clear fracture"},
    {"id": "e4", "age": 70, "symptoms": "Severe abdominal pain, vomiting blood", "vitals": "BP: 90/60, HR: 120, O2: 93%", "urgency": "critical", "department": "ER", "hint": "GI bleed"},
    {"id": "e5", "age": 22, "symptoms": "Anxiety, panic attacks, unable to sleep", "vitals": "BP: 118/76, HR: 92, O2: 99%", "urgency": "normal", "department": "psychiatry", "hint": "mental health"},
    {"id": "e6", "age": 55, "symptoms": "Irregular heartbeat, dizziness, fatigue", "vitals": "BP: 140/90, HR: 55, O2: 97%", "urgency": "urgent", "department": "cardiology", "hint": "arrhythmia"},
    {"id": "e7", "age": 40, "symptoms": "Lower back pain for 2 weeks, mild", "vitals": "BP: 122/80, HR: 72, O2: 99%", "urgency": "low", "department": "orthopedics", "hint": "chronic back pain"},
    {"id": "e8", "age": 67, "symptoms": "Sudden severe headache and confusion", "vitals": "BP: 180/120, HR: 95, O2: 96%", "urgency": "critical", "department": "neurology", "hint": "possible stroke"},
]

# Medium patients - overlapping symptoms, requires more reasoning
MEDIUM_PATIENTS = [
    {"id": "m1", "age": 58, "symptoms": "Chest tightness, jaw pain, mild nausea", "vitals": "BP: 145/95, HR: 98, O2: 96%", "urgency": "critical", "department": "ER", "hint": "atypical heart attack - easy to miss"},
    {"id": "m2", "age": 35, "symptoms": "Severe headache, neck stiffness, fever 39C", "vitals": "BP: 130/85, HR: 105, O2: 97%", "urgency": "critical", "department": "ER", "hint": "possible meningitis"},
    {"id": "m3", "age": 62, "symptoms": "Shortness of breath, swollen ankles, fatigue", "vitals": "BP: 155/95, HR: 88, O2: 95%", "urgency": "urgent", "department": "cardiology", "hint": "heart failure, not obvious"},
    {"id": "m4", "age": 29, "symptoms": "Sudden vision loss in one eye, no pain", "vitals": "BP: 118/75, HR: 72, O2: 99%", "urgency": "urgent", "department": "neurology", "hint": "could be MS or retinal detachment"},
    {"id": "m5", "age": 45, "symptoms": "Right shoulder pain, fever, jaundice", "vitals": "BP: 128/82, HR: 95, O2: 98%", "urgency": "urgent", "department": "ER", "hint": "gallbladder, referred pain confuses"},
    {"id": "m6", "age": 71, "symptoms": "Confusion, mild fever, frequent urination", "vitals": "BP: 135/85, HR: 88, O2: 97%", "urgency": "urgent", "department": "ER", "hint": "UTI causing delirium in elderly"},
    {"id": "m7", "age": 38, "symptoms": "Palpitations, weight loss, heat intolerance", "vitals": "BP: 138/88, HR: 118, O2: 98%", "urgency": "urgent", "department": "cardiology", "hint": "hyperthyroidism"},
    {"id": "m8", "age": 50, "symptoms": "Persistent cough, night sweats, weight loss", "vitals": "BP: 122/78, HR: 82, O2: 96%", "urgency": "urgent", "department": "ER", "hint": "TB or cancer - needs workup"},
]

# Hard patients - ambiguous, multiple conditions, time pressure
HARD_PATIENTS = [
    {"id": "h1", "age": 55, "symptoms": "Back pain radiating to legs, mild confusion, recent fall", "vitals": "BP: 168/102, HR: 92, O2: 96%", "urgency": "critical", "department": "neurology", "hint": "spinal cord compression + hypertensive encephalopathy"},
    {"id": "h2", "age": 42, "symptoms": "Chest pain, fever 38.5C, productive cough, sweating", "vitals": "BP: 105/70, HR: 115, O2: 92%", "urgency": "critical", "department": "ER", "hint": "septic pneumonia masking as cardiac"},
    {"id": "h3", "age": 68, "symptoms": "Sudden behavioral change, mild headache, history of anticoagulants", "vitals": "BP: 175/110, HR: 78, O2: 97%", "urgency": "critical", "department": "neurology", "hint": "subdural hematoma - anticoagulants clue"},
    {"id": "h4", "age": 33, "symptoms": "Abdominal pain, missed period, dizziness on standing", "vitals": "BP: 98/65, HR: 122, O2: 98%", "urgency": "critical", "department": "ER", "hint": "ectopic pregnancy - easily missed"},
    {"id": "h5", "age": 60, "symptoms": "Fatigue, muscle weakness, constipation, depression", "vitals": "BP: 148/92, HR: 58, O2: 98%", "urgency": "urgent", "department": "ER", "hint": "hypercalcemia - vague symptoms"},
    {"id": "h6", "age": 48, "symptoms": "Knee pain, fever, recent dental procedure", "vitals": "BP: 132/84, HR: 102, O2: 99%", "urgency": "urgent", "department": "ER", "hint": "septic arthritis from dental bacteremia"},
    {"id": "h7", "age": 77, "symptoms": "Falls x3 this week, mild confusion, on multiple medications", "vitals": "BP: 142/88 sitting 112/70 standing, HR: 82, O2: 97%", "urgency": "urgent", "department": "ER", "hint": "polypharmacy causing orthostatic hypotension"},
    {"id": "h8", "age": 25, "symptoms": "Severe fatigue, joint pain, facial rash after sun exposure", "vitals": "BP: 128/82, HR: 88, O2: 98%", "urgency": "urgent", "department": "ER", "hint": "lupus flare - autoimmune, easy to miss in young"},
]

# Urgency severity mapping for partial credit
URGENCY_SEVERITY = {"critical": 4, "urgent": 3, "normal": 2, "low": 1}

# Department similarity mapping for partial credit
DEPARTMENT_GROUPS = {
    "ER": ["ER", "cardiology", "neurology"],
    "cardiology": ["cardiology", "ER"],
    "neurology": ["neurology", "ER"],
    "orthopedics": ["orthopedics", "ER"],
    "GP": ["GP", "psychiatry"],
    "psychiatry": ["psychiatry", "GP"],
}


class MedicalTriageEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.step_count = 0
        self.max_steps = {"easy": 5, "medium": 7, "hard": 10}[task]
        self.score = 0.0
        self.current_patient = None
        self.patient_pool = {"easy": EASY_PATIENTS, "medium": MEDIUM_PATIENTS, "hard": HARD_PATIENTS}[task]
        self.used_patients = []

    def reset(self):
        self.step_count = 0
        self.score = 0.0
        self.used_patients = []
        self._pick_new_patient()
        return self._make_obs()

    def _pick_new_patient(self):
        available = [p for p in self.patient_pool if p["id"] not in self.used_patients]
        if not available:
            self.used_patients = []
            available = self.patient_pool
        self.current_patient = random.choice(available)
        self.used_patients.append(self.current_patient["id"])

    def _make_obs(self):
        return PatientObservation(
            patient_id=self.current_patient["id"],
            age=self.current_patient["age"],
            symptoms=self.current_patient["symptoms"],
            vitals=self.current_patient["vitals"],
            current_step=self.step_count,
            max_steps=self.max_steps
        )

    def _calculate_reward(self, action):
        correct_urgency = self.current_patient["urgency"]
        correct_dept = self.current_patient["department"]

        urgency_correct = action.urgency == correct_urgency
        dept_correct = action.department == correct_dept

        # Perfect score
        if urgency_correct and dept_correct:
            # Bonus for critical patients correctly identified early
            if correct_urgency == "critical" and self.step_count <= 2:
                reward = 1.0
                reason = "Perfect triage! Critical patient correctly identified early."
            else:
                reward = 1.0
                reason = "Perfect triage! Correct urgency and department."

        # Partial: both wrong but urgency is close
        elif urgency_correct and not dept_correct:
            # Check if department is in related group
            related = DEPARTMENT_GROUPS.get(correct_dept, [correct_dept])
            if action.department in related:
                reward = 0.6
                reason = f"Correct urgency, department close but should be {correct_dept}."
            else:
                reward = 0.4
                reason = f"Correct urgency but wrong department. Should be {correct_dept}."

        elif not urgency_correct and dept_correct:
            # Penalize more if urgency is dangerously wrong (e.g. critical marked as low)
            correct_severity = URGENCY_SEVERITY[correct_urgency]
            given_severity = URGENCY_SEVERITY.get(action.urgency, 0)
            severity_diff = abs(correct_severity - given_severity)
            if severity_diff >= 3:
                reward = 0.1
                reason = f"Correct department but dangerously wrong urgency! Should be {correct_urgency}."
            elif severity_diff == 2:
                reward = 0.25
                reason = f"Correct department but urgency too far off. Should be {correct_urgency}."
            else:
                reward = 0.4
                reason = f"Correct department but urgency slightly off. Should be {correct_urgency}."

        else:
            # Both wrong - check how wrong
            correct_severity = URGENCY_SEVERITY[correct_urgency]
            given_severity = URGENCY_SEVERITY.get(action.urgency, 0)
            severity_diff = abs(correct_severity - given_severity)
            related = DEPARTMENT_GROUPS.get(correct_dept, [correct_dept])

            if severity_diff == 0 and action.department in related:
                reward = 0.3
                reason = "Close but both slightly off."
            elif severity_diff >= 3:
                reward = 0.0
                reason = f"Dangerous misclassification! Should be {correct_urgency} → {correct_dept}."
            else:
                reward = 0.1
                reason = f"Incorrect triage. Should be {correct_urgency} → {correct_dept}."

        return reward, reason

    def step(self, action):
        self.step_count += 1
        reward, reason = self._calculate_reward(action)
        self.score += reward
        done = self.step_count >= self.max_steps
        if not done:
            self._pick_new_patient()
        obs = self._make_obs()
        return obs, TriageReward(value=reward, reason=reason), done, {}

    def state(self):
        return {
            "task": self.task,
            "step": self.step_count,
            "score": round(self.score, 2),
            "max_steps": self.max_steps,
            "avg_score": round(self.score / self.step_count, 2) if self.step_count > 0 else 0.0,
            "current_patient_id": self.current_patient["id"] if self.current_patient else None
        }
