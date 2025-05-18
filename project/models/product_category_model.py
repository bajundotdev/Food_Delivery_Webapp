from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum


#####################
# Enums             #
#####################

class ProductCategory(Enum):
    MAIN_COURSE = "Main"