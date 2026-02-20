from src.domain.models import LatticeState

class LatticeVault:
    def __init__(self):
        self.nodes = {}
        self.last_sync_point = "Initial State"

    async def deploy_node(self, node_id):
        print(f"[Vault] Deploying node: {node_id}")
        self.nodes[node_id] = LatticeState.PROVISIONING
        # In a real system, this would be an async cloud call
        self.nodes[node_id] = LatticeState.ACTIVE
        return True

    async def rollback_node(self, node_id):
        print(f"[Vault] Rolling back node: {node_id}")
        if node_id in self.nodes:
            del self.nodes[node_id]
        return True

    def get_sync_status(self):
        return self.last_sync_point
