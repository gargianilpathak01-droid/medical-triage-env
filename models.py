from pydantic import BaseModel

class PatientObservation(BaseModel):
    patient_id: str
    age: int
    symptoms: str
    vitals: str
    current_step: int
    max_steps: int

class TriageAction(BaseModel):
    urgency: str
    department: str

class TriageReward(BaseModel):
    value: float
    reason: str