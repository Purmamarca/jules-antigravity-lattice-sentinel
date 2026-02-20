import pytest
from unittest.mock import patch
from src.orchestrator import AntigravityOrchestrator
from src.domain.models import LatticeState
from src.infrastructure.lattice_vault import LatticeVault
from src.services.jules_audit import JulesAudit

@pytest.mark.asyncio
async def test_lattice_deployment_atomicity():
    """
    Scenario:
    1. Start a deployment of 3 new lattice nodes.
    2. Successfully deploy node 1 and node 2.
    3. Simulate a 'SystemFailure' during node 3.
    
    Assertion:
    - The LatticeState must NOT show node 1 and 2 as 'active'.
    - The AntigravityOrchestrator must return a 'rollback_completed' status.
    - The system must remain at the 'Last Known Good Sync' point.
    """
    audit_service = JulesAudit()
    orchestrator = AntigravityOrchestrator(audit_service)
    node_ids = ["node_1", "node_2", "node_3"]
    valid_signature = "GOOGLE_ANTIGRAVITY_SIG_001"
    
    # We'll patch LatticeVault.deploy_node to fail on node_3.
    original_deploy = LatticeVault.deploy_node
    
    async def side_effect(vault_instance, node_id):
        if node_id == "node_3":
            raise Exception("SystemFailure")
        return await original_deploy(vault_instance, node_id)

    with patch.object(LatticeVault, 'deploy_node', autospec=True, side_effect=side_effect):
        status = await orchestrator.deploy_lattice(node_ids, valid_signature)

    # 1. Verify rollback: node 1 and 2 should NOT be active
    for node_id in ["node_1", "node_2"]:
        state = orchestrator.vault.nodes.get(node_id)
        assert state != LatticeState.ACTIVE, f"{node_id} should not be ACTIVE after failure"

    # 2. Verify orchestrator status
    assert status == "rollback_completed"
    
    # 3. Verify the system remains at the 'Last Known Good Sync' point
    assert orchestrator.vault.get_sync_status() == "Initial State"
    # Ensure no residual data remains in the vault for failed/rolled back nodes
    assert len(orchestrator.vault.nodes) == 0
