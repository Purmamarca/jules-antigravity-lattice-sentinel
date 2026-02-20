import pytest
from unittest.mock import patch
from src.orchestrator import AntigravityOrchestrator
from src.services.jules_audit import JulesAudit
from src.infrastructure.lattice_vault import LatticeVault

@pytest.mark.asyncio
async def test_access_denied_alignment():
    """
    Goal: Ensure that the LatticeVault is NOT touched if Jules denies access.
    """
    audit_service = JulesAudit()
    orchestrator = AntigravityOrchestrator(audit_service)
    
    invalid_signature = "UNAUTHORIZED_USER_999"
    node_ids = ["protected_node"]
    
    # We'll spy on the vault to ensure no methods are called
    with patch.object(LatticeVault, 'deploy_node', return_value=True) as mock_deploy:
        status = await orchestrator.deploy_lattice(node_ids, invalid_signature)
        
    assert status == "access_denied"
    mock_deploy.assert_not_called(), "LatticeVault must NOT be touched if access is denied"
    
    # Verify rejection in audit logs
    logs = audit_service.get_logs()
    denied_entries = [e for e in logs if e.action == "ACCESS_DENIED"]
    assert len(denied_entries) >= 1, "Audit must record the unauthorized access attempt"
    assert denied_entries[0].quantum_signature == invalid_signature
