from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException

import models
import schemas
from libs.dependencies import Utils, UtilsObject

router = APIRouter()
