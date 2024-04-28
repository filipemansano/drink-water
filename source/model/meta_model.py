from typing import Any, Optional
from source.enum.meta_period_enum import MetaPeriodEnum

from source.model.validators.base_validator import BaseValidator

class Meta(BaseValidator):

    def __init__(self, **data: Any):
        super().__init__(check_fields_on_create=['quantity', 'period'], **data)

    id: Optional[str] = None
    quantity: Optional[float] = None
    period: Optional[MetaPeriodEnum] = None