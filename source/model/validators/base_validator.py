from contextlib import contextmanager
from contextvars import ContextVar
from pydantic import BaseModel, model_validator, ValidationInfo
from typing import Any, Dict, Iterator

_init_context_var = ContextVar('_init_context_var', default=None)

@contextmanager
def init_context(value: Dict[str, Any]) -> Iterator[None]:
    token = _init_context_var.set(value)
    try:
        yield
    finally:
        _init_context_var.reset(token)

class BaseValidator(BaseModel):

    def __init__(self, check_fields_on_create = [], **data: Any):
        super().__init__(**data)
        self._check_fields_on_create = check_fields_on_create

    @model_validator(mode='after')
    def check_model(self, info: ValidationInfo) -> Any:
        if info.context is None: return self
        data = self.model_dump()

        if info.context.get('mode') == 'update':
            if all(value is None for value in data.values()):
                raise ValueError('at least one field must be provided')

        if info.context.get('mode') == 'create':
            errors = [f"{field} is required" for field in self._check_fields_on_create if data.get(field) is None]

            if errors:
                raise ValueError(" | ".join(errors))

        return self