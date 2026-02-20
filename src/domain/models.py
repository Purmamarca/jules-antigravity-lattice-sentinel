from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

class LatticeState(Enum):
    PENDING = "pending"
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"
    SYNCED = "synced"

@dataclass
class AuditEntry:
    timestamp: str
    action: str
    status: str
    node_id: Optional[str] = None
    quantum_signature: Optional[str] = None
    details: Optional[str] = None

@dataclass
class AuditTrail:
    entries: List[AuditEntry] = field(default_factory=list)

    def add_entry(self, action: str, status: str, node_id: Optional[str] = None, quantum_signature: Optional[str] = None, details: Optional[str] = None):
        entry = AuditEntry(
            timestamp=datetime.utcnow().isoformat(),
            action=action,
            status=status,
            node_id=node_id,
            quantum_signature=quantum_signature,
            details=details
        )
        self.entries.append(entry)
        return entry
