from src.security.models import UserContext, LatticeState, AccessClearance
from src.security.exceptions import SecurityPolicyViolation
from src.security.logger import SecurityReasonCode, log_security_event

class Sentinel:
    def validate_request(self, context, lattice_state):
        """
        Validates the request context and lattice state.
        Enforces Type Sovereignty: Reject generic dictionaries.
        Enforces Quantum-Safe: Require QUANTUM_SAFE clearance for LOCKED_VAULT state.
        """
        if not isinstance(context, UserContext):
            msg = f"Invalid context type: Expected UserContext, got {type(context).__name__}"
            log_security_event(SecurityReasonCode.TYPE_VIOLATION, msg)
            raise SecurityPolicyViolation(msg)

        if not isinstance(lattice_state, LatticeState):
            msg = f"Invalid lattice state type: Expected LatticeState, got {type(lattice_state).__name__}"
            log_security_event(SecurityReasonCode.TYPE_VIOLATION, msg)
            raise SecurityPolicyViolation(msg)

        if lattice_state == LatticeState.LOCKED_VAULT:
            if context.clearance != AccessClearance.QUANTUM_SAFE:
                msg = "Access Denied: Quantum Safe clearance required for Locked Vault"
                log_security_event(SecurityReasonCode.ACCESS_DENIED_LOCKED_VAULT, msg)
                raise SecurityPolicyViolation(msg)

        log_security_event(SecurityReasonCode.ACCESS_GRANTED, f"Access granted for user {context.user_id}")
