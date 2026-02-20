from models import LatticeState
from infrastructure.lattice_vault import LatticeVault

class AntigravityOrchestrator:
    def __init__(self):
        self.vault = LatticeVault()
        self.status = "idle"
        self.deployed_stack = []

    async def deploy_lattice(self, node_ids):
        print(">>> INITIALIZING ATOMIC LATTICE DEPLOYMENT <<<")
        self.status = "deploying"
        self.deployed_stack = []
        
        # Capture current sync point as "Last Known Good"
        self.last_known_good_sync = self.vault.get_sync_status()
        
        try:
            for node_id in node_ids:
                print(f"Orchestrating deployment for {node_id}...")
                await self.vault.deploy_node(node_id)
                self.deployed_stack.append(node_id)
            
            self.status = "deployment_completed"
            # If successful, we update the sync point
            self.vault.last_sync_point = f"Synced nodes: {', '.join(node_ids)}"
            return self.status
            
        except Exception as e:
            print(f"!!! CRITICAL FAILURE: {str(e)} !!!")
            self.status = "rolling_back"
            await self._rollback()
            self.status = "rollback_completed"
            print(f"System stabilized at: {self.last_known_good_sync}")
            return self.status

    async def _rollback(self):
        """Compensating transaction (Saga Pattern)"""
        while self.deployed_stack:
            node_id = self.deployed_stack.pop()
            await self.vault.rollback_node(node_id)
        print("Rollback sequence finished.")
