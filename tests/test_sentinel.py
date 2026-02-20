import pytest
from src.security.models import UserContext, LatticeState, AccessClearance
from src.security.exceptions import SecurityPolicyViolation
from src.security.sentinel import Sentinel

def test_reject_generic_dictionary_context():
    """
    Test that the Sentinel rejects a generic dictionary as a security context.
    This enforces the 'Type Sovereignty' rule.
    """
    sentinel = Sentinel()
    generic_context = {"user_id": "123", "clearance": "STANDARD"}
    lattice_state = LatticeState.STANDARD

    with pytest.raises(SecurityPolicyViolation) as excinfo:
        sentinel.validate_request(generic_context, lattice_state)

    assert "Invalid context type" in str(excinfo.value)

def test_accept_valid_user_context():
    """
    Test that the Sentinel accepts a valid UserContext.
    """
    sentinel = Sentinel()
    user_context = UserContext(user_id="user-123", clearance=AccessClearance.STANDARD)
    lattice_state = LatticeState.STANDARD

    # Should not raise exception
    sentinel.validate_request(user_context, lattice_state)

def test_block_access_locked_vault_without_quantum_safe():
    """
    Test that access is blocked when LatticeState is LOCKED_VAULT and clearance is not QUANTUM_SAFE.
    """
    sentinel = Sentinel()
    user_context = UserContext(user_id="user-123", clearance=AccessClearance.STANDARD)
    lattice_state = LatticeState.LOCKED_VAULT

    with pytest.raises(SecurityPolicyViolation) as excinfo:
        sentinel.validate_request(user_context, lattice_state)

    assert "Access Denied: Quantum Safe clearance required for Locked Vault" in str(excinfo.value)

def test_allow_access_locked_vault_with_quantum_safe():
    """
    Test that access is allowed when LatticeState is LOCKED_VAULT and clearance is QUANTUM_SAFE.
    """
    sentinel = Sentinel()
    user_context = UserContext(user_id="user-quantum", clearance=AccessClearance.QUANTUM_SAFE)
    lattice_state = LatticeState.LOCKED_VAULT

    # Should not raise exception
    sentinel.validate_request(user_context, lattice_state)
