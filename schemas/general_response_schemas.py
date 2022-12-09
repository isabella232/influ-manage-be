from pydantic import BaseModel


class GeneralBoolResponseSchema(BaseModel):
    success: bool
