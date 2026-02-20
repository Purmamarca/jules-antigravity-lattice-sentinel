from enum import Enum, auto
from dataclasses import dataclass

class LatticeState(Enum):
    """Represents the security state of the Lattice."""
    STANDARD = auto()
    LOCKED_VAULT = auto()

class AccessClearance(Enum):
    """Represents the security clearance level of a user."""
    STANDARD = auto()
    QUANTUM_SAFE = auto()

@dataclass(frozen=True)
class UserContext:
    """Represents the security context of a user."""
    user_id: str
    clearance: AccessClearance
