import logging
from enum import Enum

class SecurityReasonCode(Enum):
    TYPE_VIOLATION = "SEC-001"
    POLICY_VIOLATION = "SEC-002"
    ACCESS_DENIED_LOCKED_VAULT = "SEC-003"
    ACCESS_GRANTED = "SEC-100"

logger = logging.getLogger("JulesSentinel")
logger.addHandler(logging.NullHandler())  # Prevent "No handler found" warning

def log_security_event(reason_code: SecurityReasonCode, message: str, level: int = logging.INFO):
    """Logs a security event with a specific reason code."""
    logger.log(level, f"[{reason_code.value}] {message}")
