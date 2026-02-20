import pytest
from unittest.mock import patch
from src.orchestrator import AntigravityOrchestrator
from src.services.jules_audit import JulesAudit
from src.infrastructure.lattice_vault import LatticeVault
from src.domain.models import LatticeState

@pytest.mark.asyncio
async def test_audit_verification():
    """
    Scenario: 'Audit Verification'.
    Validation:
    1. Run a failing deployment.
    2. Assert that Jules has a record of the failure.
    3. Assert that the record includes the 'Quantum-Signature' of the user.
    """
    audit_service = JulesAudit()
    orchestrator = AntigravityOrchestrator(audit_service)
    
    node_ids = ["node_alpha", "node_beta"]
    valid_signature = "GOOGLE_ANTIGRAVITY_SIG_001"
    
    # Simulate a failure during node_beta
    original_deploy = LatticeVault.deploy_node
    
    async def failing_deploy(vault_instance, node_id):
        if node_id == "node_beta":
            raise Exception("QuantumDeherenceFailure")
        return await original_deploy(vault_instance, node_id)

    with patch.object(LatticeVault, 'deploy_node', autospec=True, side_effect=failing_deploy):
        status = await orchestrator.deploy_lattice(node_ids, valid_signature)

    # Assertions
    assert status == "rollback_completed"
    
    # Verify Audit Trail
    logs = audit_service.get_logs()
    
    # Check for failure record
    failure_entries = [e for e in logs if e.action == "LATTICE_DEPLOY_FAILURE"]
    assert len(failure_entries) > 0, "Jules must have a record of the failure"
    assert failure_entries[0].quantum_signature == valid_signature, "Record must include the Quantum-Signature"
    assert "QuantumDeherenceFailure" in failure_entries[0].details

    # Check for rollback records
    rollback_entries = [e for e in logs if "ROLLBACK" in e.action]
    assert len(rollback_entries) > 0, "Audit must track the rollback process"
    
    print("\nVerified: Jules captured the failure and the identity signature.")
