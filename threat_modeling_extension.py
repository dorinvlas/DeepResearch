"""
Threat Modeling Extension for DeepResearch Pipe

This extension adds automated Threagile YAML threat model generation capabilities
to the existing DeepResearch system, integrating with Open WebUI knowledge base
API and ctm:local Docker validation.

Key Features:
- Query Open WebUI knowledge base for architecture information
- Generate Threagile-compliant YAML threat models
- Validate generated models using ctm:local Docker container
- Iterative research approach for architecture interpretation
- Integration with existing DeepResearch semantic processing
"""

import asyncio
import aiohttp
import json
import yaml
import subprocess
import tempfile
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging

# Threagile schema URL for reference
THREAGILE_SCHEMA_URL = "https://github.com/Threagile/threagile/blob/master/support/schema.json"

@dataclass
class ThreatModelingConfig:
    """Configuration for threat modeling capabilities"""
    openwebui_base_url: str = "http://localhost:3003"
    knowledge_base_id: Optional[str] = None  # AAF knowledge base ID
    ctm_docker_image: str = "ctm:local"
    max_iterations: int = 3
    architecture_query_templates: List[str] = None
    
    def __post_init__(self):
        if self.architecture_query_templates is None:
            self.architecture_query_templates = [
                "system architecture components and data flows",
                "authentication and authorization mechanisms", 
                "data storage and processing elements",
                "external interfaces and communication protocols",
                "trust boundaries and security zones"
            ]

class ThreatModelingProcessor:
    """Processes threat modeling requests using Open WebUI knowledge base"""
    
    def __init__(self, config: ThreatModelingConfig, headers: Dict[str, str] = None):
        self.config = config
        self.headers = headers or {}
        self.logger = logging.getLogger(__name__)
        
    async def query_knowledge_base(self, query: str, collection_name: str = None) -> List[Dict]:
        """Query Open WebUI knowledge base for architecture information"""
        
        endpoint = f"{self.config.openwebui_base_url}/api/v1/retrieval/query/collection"
        
        payload = {
            "collection_names": [collection_name] if collection_name else ["default"],
            "query": query,
            "k": 10,  # Top-K results
            "k_reranker": 5,  # Reranker top-K
            "r": 0.7,  # Relevance threshold
            "hybrid": True,  # Use hybrid search
            "hybrid_bm25_weight": 0.5
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    json=payload,
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("results", [])
                    else:
                        self.logger.error(f"Knowledge base query failed: {response.status}")
                        return []
        except Exception as e:
            self.logger.error(f"Error querying knowledge base: {e}")
            return []
    
    async def extract_architecture_components(self, knowledge_results: List[Dict]) -> Dict[str, Any]:
        """Extract architecture components from knowledge base results"""
        
        architecture_data = {
            "technical_assets": [],
            "trust_boundaries": [],
            "shared_runtimes": [],
            "data_assets": [],
            "communication_links": [],
            "risk_categories": [],
            "individual_risk_categories": [],
            "threats": []
        }
        
        # Process knowledge results to extract structured architecture data
        for result in knowledge_results:
            content = result.get("content", "")
            metadata = result.get("metadata", {})
            
            # Use semantic analysis to categorize content
            if self._contains_asset_keywords(content):
                asset = self._extract_technical_asset(content, metadata)
                if asset:
                    architecture_data["technical_assets"].append(asset)
            
            if self._contains_boundary_keywords(content):
                boundary = self._extract_trust_boundary(content, metadata)
                if boundary:
                    architecture_data["trust_boundaries"].append(boundary)
            
            if self._contains_data_keywords(content):
                data_asset = self._extract_data_asset(content, metadata)
                if data_asset:
                    architecture_data["data_assets"].append(data_asset)
            
            if self._contains_communication_keywords(content):
                comm_link = self._extract_communication_link(content, metadata)
                if comm_link:
                    architecture_data["communication_links"].append(comm_link)
        
        return architecture_data
    
    def _contains_asset_keywords(self, content: str) -> bool:
        """Check if content describes technical assets"""
        keywords = [
            "service", "server", "database", "application", "component",
            "microservice", "api", "web", "mobile", "client", "system"
        ]
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)
    
    def _contains_boundary_keywords(self, content: str) -> bool:
        """Check if content describes trust boundaries"""
        keywords = [
            "network", "dmz", "firewall", "subnet", "zone", "boundary",
            "perimeter", "internal", "external", "public", "private"
        ]
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)
    
    def _contains_data_keywords(self, content: str) -> bool:
        """Check if content describes data assets"""
        keywords = [
            "data", "information", "records", "files", "documents",
            "pii", "sensitive", "confidential", "personal", "customer"
        ]
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)
    
    def _contains_communication_keywords(self, content: str) -> bool:
        """Check if content describes communication links"""
        keywords = [
            "api call", "http", "https", "rest", "soap", "grpc",
            "communication", "connection", "flow", "protocol", "transfer"
        ]
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)
    
    def _extract_technical_asset(self, content: str, metadata: Dict) -> Optional[Dict]:
        """Extract technical asset from content"""
        # Simplified extraction - would be enhanced with NLP
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ["service", "server", "application"]):
                # Extract asset name and properties
                asset_id = self._generate_id(line)
                return {
                    "id": asset_id,
                    "description": line.strip(),
                    "type": "process",  # Default type
                    "usage": "business",
                    "used_as_client_by_human": False,
                    "out_of_scope": False,
                    "justification_out_of_scope": "",
                    "size": "component",
                    "technology": "unknown",
                    "tags": [],
                    "internet": False,
                    "machine": "virtual",
                    "encryption": "none",
                    "owner": "unknown",
                    "confidentiality": "internal",
                    "integrity": "important",
                    "availability": "important",
                    "justification_cia_rating": "Default rating based on business usage"
                }
        return None
    
    def _extract_trust_boundary(self, content: str, metadata: Dict) -> Optional[Dict]:
        """Extract trust boundary from content"""
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ["network", "zone", "boundary"]):
                boundary_id = self._generate_id(line)
                return {
                    "id": boundary_id,
                    "description": line.strip(),
                    "type": "network-cloud-security-group",
                    "tags": [],
                    "technical_assets_inside": [],
                    "trust_boundaries_nested": []
                }
        return None
    
    def _extract_data_asset(self, content: str, metadata: Dict) -> Optional[Dict]:
        """Extract data asset from content"""
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ["data", "information", "records"]):
                data_id = self._generate_id(line)
                return {
                    "id": data_id,
                    "description": line.strip(),
                    "usage": "business",
                    "tags": [],
                    "origin": "unknown",
                    "owner": "unknown",
                    "quantity": "normal",
                    "confidentiality": "internal",
                    "integrity": "important",
                    "availability": "important",
                    "justification_cia_rating": "Default rating for business data"
                }
        return None
    
    def _extract_communication_link(self, content: str, metadata: Dict) -> Optional[Dict]:
        """Extract communication link from content"""
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ["api", "http", "communication"]):
                link_id = self._generate_id(line)
                return {
                    "id": link_id,
                    "source_id": "unknown",
                    "target_id": "unknown",
                    "description": line.strip(),
                    "protocol": "https",
                    "authentication": "none",
                    "authorization": "none",
                    "tags": [],
                    "vpn": False,
                    "ip_filtered": False,
                    "readonly": False,
                    "usage": "business",
                    "data_assets_sent": [],
                    "data_assets_received": []
                }
        return None
    
    def _generate_id(self, text: str) -> str:
        """Generate valid ID from text"""
        import re
        # Convert to lowercase, replace spaces and special chars with underscores
        id_text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        id_text = re.sub(r'\s+', '_', id_text.strip())
        return id_text[:50] if id_text else "unknown_asset"
    
    async def generate_threagile_yaml(self, architecture_data: Dict[str, Any], project_name: str = "Generated Threat Model") -> str:
        """Generate Threagile-compliant YAML from architecture data"""
        
        threagile_model = {
            "threagile_version": "1.0.0",
            "title": project_name,
            "date": "2024-01-01",  # Would use actual date
            "author": {
                "name": "DeepResearch Threat Modeling",
                "homepage": "Generated by DeepResearch AI"
            },
            "contributors": [],
            "management_summary_comment": "Automatically generated threat model from architecture analysis",
            "business_criticality": "important",
            "business_overview": {
                "description": "System analyzed for threat modeling",
                "images": []
            },
            "technical_overview": {
                "description": "Technical architecture extracted from knowledge base",
                "images": []
            },
            "questions": {},
            "abuse_cases": {},
            "security_requirements": {},
            "tags_available": [],
            "data_assets": {asset["id"]: asset for asset in architecture_data.get("data_assets", [])},
            "technical_assets": {asset["id"]: asset for asset in architecture_data.get("technical_assets", [])},
            "trust_boundaries": {boundary["id"]: boundary for boundary in architecture_data.get("trust_boundaries", [])},
            "shared_runtimes": {},
            "individual_risk_categories": {},
            "risk_tracking": {},
            "diagram_tweak_nodesep": 1,
            "diagram_tweak_ranksep": 1
        }
        
        # Add communication links
        for link in architecture_data.get("communication_links", []):
            source_id = link["source_id"]
            if source_id in threagile_model["technical_assets"]:
                if "communication_links" not in threagile_model["technical_assets"][source_id]:
                    threagile_model["technical_assets"][source_id]["communication_links"] = {}
                threagile_model["technical_assets"][source_id]["communication_links"][link["id"]] = {
                    "target": link["target_id"],
                    "description": link["description"],
                    "protocol": link["protocol"],
                    "authentication": link["authentication"],
                    "authorization": link["authorization"],
                    "tags": link["tags"],
                    "vpn": link["vpn"],
                    "ip_filtered": link["ip_filtered"],
                    "readonly": link["readonly"],
                    "usage": link["usage"],
                    "data_assets_sent": link["data_assets_sent"],
                    "data_assets_received": link["data_assets_received"]
                }
        
        return yaml.dump(threagile_model, default_flow_style=False, sort_keys=False)
    
    async def validate_with_ctm_local(self, yaml_content: str) -> Tuple[bool, str]:
        """Validate Threagile YAML using ctm:local Docker container"""
        
        try:
            # Create temporary file for YAML content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
                temp_file.write(yaml_content)
                temp_path = temp_file.name
            
            # Run ctm:local validation
            cmd = [
                "docker", "run", "--rm",
                "-v", f"{temp_path}:/tmp/model.yaml",
                self.config.ctm_docker_image,
                "validate", "/tmp/model.yaml"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Cleanup
            os.unlink(temp_path)
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        
        except subprocess.TimeoutExpired:
            return False, "Validation timeout"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    async def iterative_threat_modeling(self, initial_query: str, max_iterations: int = None) -> Dict[str, Any]:
        """Perform iterative threat modeling research cycle"""
        
        if max_iterations is None:
            max_iterations = self.config.max_iterations
        
        results = {
            "iterations": [],
            "final_model": None,
            "validation_results": [],
            "architecture_data": {}
        }
        
        current_query = initial_query
        
        for iteration in range(max_iterations):
            iteration_data = {
                "iteration": iteration + 1,
                "query": current_query,
                "knowledge_results": [],
                "architecture_extracted": {},
                "yaml_generated": "",
                "validation_passed": False,
                "validation_message": ""
            }
            
            # Query knowledge base with current query
            for template in self.config.architecture_query_templates:
                query = f"{current_query} {template}"
                kb_results = await self.query_knowledge_base(query)
                iteration_data["knowledge_results"].extend(kb_results)
            
            # Extract architecture components
            architecture_data = await self.extract_architecture_components(
                iteration_data["knowledge_results"]
            )
            iteration_data["architecture_extracted"] = architecture_data
            
            # Generate Threagile YAML
            yaml_content = await self.generate_threagile_yaml(
                architecture_data,
                f"Threat Model - Iteration {iteration + 1}"
            )
            iteration_data["yaml_generated"] = yaml_content
            
            # Validate with ctm:local
            is_valid, validation_msg = await self.validate_with_ctm_local(yaml_content)
            iteration_data["validation_passed"] = is_valid
            iteration_data["validation_message"] = validation_msg
            
            results["iterations"].append(iteration_data)
            
            if is_valid:
                results["final_model"] = yaml_content
                results["architecture_data"] = architecture_data
                break
            else:
                # Refine query based on validation errors
                current_query = self._refine_query_from_validation(current_query, validation_msg)
        
        return results
    
    def _refine_query_from_validation(self, original_query: str, validation_error: str) -> str:
        """Refine query based on validation errors"""
        
        # Basic refinement logic - would be enhanced with AI analysis
        if "technical_assets" in validation_error.lower():
            return f"{original_query} technical components systems services"
        elif "trust_boundaries" in validation_error.lower():
            return f"{original_query} network boundaries security zones"
        elif "data_assets" in validation_error.lower():
            return f"{original_query} data information assets storage"
        elif "communication" in validation_error.lower():
            return f"{original_query} communication links protocols APIs"
        else:
            return f"{original_query} detailed architecture specification"

class ThreatModelingExtension:
    """Main extension class for integrating threat modeling with DeepResearch"""
    
    def __init__(self, pipe_instance, config: ThreatModelingConfig = None):
        self.pipe = pipe_instance
        self.config = config or ThreatModelingConfig()
        self.processor = ThreatModelingProcessor(self.config)
        self.logger = logging.getLogger(__name__)
    
    async def process_threat_modeling_query(self, query: str, user_valves: Dict = None) -> Dict[str, Any]:
        """Main entry point for threat modeling queries"""
        
        try:
            # Check if this is a threat modeling request
            if not self._is_threat_modeling_query(query):
                return {"error": "Not a threat modeling query"}
            
            # Extract system/architecture name from query
            system_name = self._extract_system_name(query)
            
            # Perform iterative threat modeling
            results = await self.processor.iterative_threat_modeling(
                f"threat model for {system_name}",
                max_iterations=user_valves.get("threat_modeling_iterations", 3) if user_valves else 3
            )
            
            # Format results for display
            formatted_results = self._format_results(results)
            
            return {
                "success": True,
                "system_name": system_name,
                "threat_model": results.get("final_model"),
                "iterations": len(results["iterations"]),
                "validation_passed": any(iter_data["validation_passed"] for iter_data in results["iterations"]),
                "formatted_output": formatted_results
            }
            
        except Exception as e:
            self.logger.error(f"Threat modeling error: {e}")
            return {"error": f"Threat modeling failed: {str(e)}"}
    
    def _is_threat_modeling_query(self, query: str) -> bool:
        """Check if query is requesting threat modeling"""
        threat_keywords = [
            "threat model", "threagile", "security analysis", "risk assessment",
            "threat assessment", "security threats", "vulnerability analysis"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in threat_keywords)
    
    def _extract_system_name(self, query: str) -> str:
        """Extract system/application name from query"""
        # Simple extraction - would be enhanced with NLP
        words = query.split()
        
        # Look for patterns like "threat model for X" or "threagile for X"
        for i, word in enumerate(words):
            if word.lower() in ["for", "of"] and i + 1 < len(words):
                return " ".join(words[i+1:i+3])  # Take next 1-2 words
        
        return "Unknown System"
    
    def _format_results(self, results: Dict[str, Any]) -> str:
        """Format threat modeling results for display"""
        
        output = []
        output.append("# Automated Threat Modeling Results\n")
        
        if results.get("final_model"):
            output.append("## ✅ Threat Model Successfully Generated\n")
            output.append(f"**Iterations Required:** {len(results['iterations'])}\n")
            
            # Show architecture summary
            arch_data = results.get("architecture_data", {})
            output.append("## Architecture Components Identified:\n")
            output.append(f"- **Technical Assets:** {len(arch_data.get('technical_assets', []))}")
            output.append(f"- **Trust Boundaries:** {len(arch_data.get('trust_boundaries', []))}")
            output.append(f"- **Data Assets:** {len(arch_data.get('data_assets', []))}")
            output.append(f"- **Communication Links:** {len(arch_data.get('communication_links', []))}\n")
            
            # Show final YAML (truncated)
            yaml_content = results["final_model"]
            output.append("## Generated Threagile YAML:\n")
            output.append("```yaml")
            output.append(yaml_content[:1000] + "..." if len(yaml_content) > 1000 else yaml_content)
            output.append("```\n")
            
        else:
            output.append("## ❌ Threat Model Generation Failed\n")
            output.append(f"**Iterations Attempted:** {len(results['iterations'])}\n")
            
            # Show validation errors
            output.append("## Validation Errors:\n")
            for i, iteration in enumerate(results["iterations"]):
                output.append(f"**Iteration {i+1}:** {iteration['validation_message']}")
        
        return "\n".join(output)

# Integration with existing Pipe class
def extend_pipe_with_threat_modeling(pipe_class):
    """Decorator to extend existing Pipe class with threat modeling capabilities"""
    
    original_pipe = pipe_class.pipe
    
    async def enhanced_pipe(self, user_message: str, model_id: str, messages: List[Dict], body: Dict) -> str:
        """Enhanced pipe method with threat modeling support"""
        
        # Check if this is a threat modeling request
        if any(keyword in user_message.lower() for keyword in ["threat model", "threagile"]):
            # Initialize threat modeling extension
            config = ThreatModelingConfig(
                openwebui_base_url=self.valves.get("openwebui_base_url", "http://localhost:3003"),
                knowledge_base_id=self.valves.get("knowledge_base_id"),
                max_iterations=self.valves.get("threat_modeling_iterations", 3)
            )
            
            extension = ThreatModelingExtension(self, config)
            
            # Process threat modeling request
            results = await extension.process_threat_modeling_query(user_message, self.valves.__dict__)
            
            if results.get("success"):
                return results["formatted_output"]
            else:
                return f"Threat modeling failed: {results.get('error', 'Unknown error')}"
        
        # Fall back to original pipe for non-threat modeling queries
        return await original_pipe(self, user_message, model_id, messages, body)
    
    # Replace pipe method
    pipe_class.pipe = enhanced_pipe
    
    # Add threat modeling valves
    original_valves = pipe_class.Valves
    
    class EnhancedValves(original_valves):
        threat_modeling_enabled: bool = True
        threat_modeling_iterations: int = 3
        openwebui_base_url: str = "http://localhost:3003"
        knowledge_base_id: str = ""
        ctm_docker_image: str = "ctm:local"
    
    pipe_class.Valves = EnhancedValves
    
    return pipe_class

# Example usage:
# @extend_pipe_with_threat_modeling
# class Pipe:
#     # ... existing Pipe implementation
