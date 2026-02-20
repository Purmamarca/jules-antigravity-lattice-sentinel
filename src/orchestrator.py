from src.infrastructure.lattice_vault import LatticeVault
from src.services.jules_audit import JulesAudit
from src.domain.models import LatticeState

class AntigravityOrchestrator:
    def __init__(self, audit_service: JulesAudit):
        self.vault = LatticeVault()
        self.audit = audit_service
        self.status = "idle"
        self.deployed_stack = []

    async def deploy_lattice(self, node_ids, quantum_signature: str):
        print(f">>> STARTING AUDITED DEPLOYMENT (User: {quantum_signature}) <<<")
        
        # 1. Responsibility Alignment: Verify access BEFORE touching infrastructure
        if not await self.audit.verify_access(quantum_signature):
            self.status = "access_denied"
            return self.status

        self.status = "deploying"
        self.deployed_stack = []
        self.last_known_good_sync = self.vault.get_sync_status()
        
        try:
            for node_id in node_ids:
                await self.audit.record_event("NODE_DEPLOY_START", "PENDING", node_id, quantum_signature)
                
                await self.vault.deploy_node(node_id)
                self.deployed_stack.append(node_id)
                
                await self.audit.record_event("NODE_DEPLOY_SUCCESS", "ACTIVE", node_id, quantum_signature)
            
            self.status = "deployment_completed"
            self.vault.last_sync_point = f"Synced nodes: {', '.join(node_ids)}"
            await self.audit.record_event("LATTICE_SYNC_COMPLETE", "SUCCESS", quantum_signature=quantum_signature)
            return self.status
            
        except Exception as e:
            await self.audit.record_event("LATTICE_DEPLOY_FAILURE", "FAILED", quantum_signature=quantum_signature, details=str(e))
            self.status = "rolling_back"
            await self._rollback(quantum_signature)
            self.status = "rollback_completed"
            await self.audit.record_event("ROLLBACK_COMPLETE", "ROLLED_BACK", quantum_signature=quantum_signature)
            return self.status

    async def _rollback(self, quantum_signature: str):
        """Compensating transaction with Audit records"""
        while self.deployed_stack:
            node_id = self.deployed_stack.pop()
            await self.audit.record_event("NODE_ROLLBACK_START", "ROLLING_BACK", node_id, quantum_signature)
            await self.vault.rollback_node(node_id)
            await self.audit.record_event("NODE_ROLLBACK_SUCCESS", "ROLLED_BACK", node_id, quantum_signature)
