from typing import Any, Optional

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    loc: list[str]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[list[ErrorDetail]] = None
    meta: Optional[dict[str, Any]] = None
