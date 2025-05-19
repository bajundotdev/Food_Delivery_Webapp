from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum

###################
# Admin Models
###################
@dataclass
class AdminLog:
    id: str
    admin_id: str
    action: str
    entity_type: str
    entity_id: str
    details: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    @staticmethod
    def log_action(admin_id: str, action: str, entity_type: str, entity_id: str, details: str = ""):
        """Log an admin action."""
        # Implementation needed
        pass