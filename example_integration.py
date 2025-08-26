"""
Example Integration of Threat Modeling Extension with DeepResearch Pipe

This file demonstrates how to integrate the automated threat modeling capabilities
with your existing DeepResearch Open WebUI pipe implementation.
"""

from typing import List
from pydantic import BaseModel

# Import the threat modeling extension
from threat_modeling_extension import extend_pipe_with_threat_modeling

# Apply the decorator to extend your existing Pipe class
@extend_pipe_with_threat_modeling
class Pipe:
    class Valves(BaseModel):
        # Existing DeepResearch valves (truncated for brevity)
        ENABLE_STARTER_SEARCHES: bool = True
        NUM_STARTER_SEARCHES: int = 4
        SEARXNG_URL: str = ""
        # ... other existing valves ...
        
        # NEW: Threat modeling valves (automatically added by extension)
        threat_modeling_enabled: bool = True
        threat_modeling_iterations: int = 3
        openwebui_base_url: str = "http://localhost:3003"
        knowledge_base_id: str = ""
        ctm_docker_image: str = "ctm:local"

    def __init__(self):
        self.type = "manifold"
        self.valves = self.Valves()
        # ... existing initialization code ...

    async def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> str:
        """
        Enhanced pipe method with threat modeling support.
        
        The extension automatically detects threat modeling queries and handles them,
        while falling back to the original DeepResearch functionality for other queries.
        """
        
        # The @extend_pipe_with_threat_modeling decorator automatically:
        # 1. Detects threat modeling keywords in user_message
        # 2. Initializes threat modeling processor if detected
        # 3. Processes threat modeling requests
        # 4. Falls back to original pipe() method for non-threat modeling queries
        
        # Original DeepResearch implementation continues here for non-threat modeling queries
        if self.valves.ENABLE_STARTER_SEARCHES:
            # ... existing DeepResearch logic ...
            pass
        
        # The extension handles the routing automatically
        # No changes needed to existing code!

# Example usage scenarios:

# 1. Regular DeepResearch query (unchanged behavior):
# "Analyze the latest developments in quantum computing"

# 2. Threat modeling query (new functionality):
# "Generate a threat model for our customer portal system"
# "Create a Threagile analysis for the payment processing API"
# "Perform threat modeling for the mobile banking application"

# 3. Mixed queries work seamlessly:
# User can alternate between research queries and threat modeling requests
# in the same conversation session

# Configuration examples for different environments:

# Development environment
development_config = {
    "threat_modeling_enabled": True,
    "threat_modeling_iterations": 2,  # Faster for testing
    "openwebui_base_url": "http://localhost:3003",
    "knowledge_base_id": "dev_architecture_kb",
    "ctm_docker_image": "ctm:local"
}

# Production environment
production_config = {
    "threat_modeling_enabled": True,
    "threat_modeling_iterations": 5,  # More thorough analysis
    "openwebui_base_url": "https://openwebui.company.com",
    "knowledge_base_id": "prod_architecture_kb",
    "ctm_docker_image": "threagile:latest"
}

# Testing environment (threat modeling disabled)
testing_config = {
    "threat_modeling_enabled": False,
    "threat_modeling_iterations": 1,
    "openwebui_base_url": "http://test-openwebui:3003",
    "knowledge_base_id": "test_kb",
    "ctm_docker_image": "ctm:test"
}
