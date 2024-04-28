from pydantic import BaseModel
from source.model.person_model import Meta
from datetime import datetime

class MetaHistory(BaseModel):
    details: Meta
    person_id: str
    start_at: datetime
    end_at: datetime
    ml_dring: float
    ml_drink_left: float
    achieved: bool