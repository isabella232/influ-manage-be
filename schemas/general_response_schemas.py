from typing import Union
import datetime
from pydantic import BaseModel


class GeneralBoolResponseSchema(BaseModel):
    success: bool