from datetime import datetime
from typing import Any, List, Optional, Union
from pydantic import SecretStr, ValidationInfo, field_validator, model_validator
from source.enum.gender_enum import GenderEnum
from source.model.meta_model import Meta
from source.model.validators.base_validator import BaseValidator

class Person(BaseValidator):

    def __init__(self, **data: Any):
        super().__init__(check_fields_on_create=['name', 'age', 'weight', 'gender', 'password', 'email'], **data)

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[SecretStr] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    gender: Optional[GenderEnum] = None
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    meta: Optional[List[Meta]] = None
    
    @field_validator('age', 'weight')
    @classmethod
    def double(cls, v: Union[int, float, None], info: ValidationInfo) -> str:
        if info.context is None: return v
        if info.context == 'update' and v is None:
            return v
        
        if v is None or v <= 0:
            raise ValueError('must be greater than 0')
        return v