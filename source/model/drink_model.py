from datetime import datetime
from typing import Any, Optional

from source.model.validators.base_validator import BaseValidator

class Drink(BaseValidator):

    def __init__(self, **data: Any):
        super().__init__(check_fields_on_create=['ml', 'person_id'], **data)
        
    ml: int
    id: Optional[str] = None
    drinked_at: Optional[datetime] = None
    person_id: str