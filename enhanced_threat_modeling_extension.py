"""
Enhanced Threat Modeling Extension with Advanced Discovery Phase

This enhanced version focuses on improving the Knowledge Retrieval and Semantic Analysis stages
with self-improvement capabilities, user feedback integration, and comprehensive discovery
aligned with Threagile schema requirements.

Key Enhancements:
- Adaptive discovery phase with Threagile schema mapping
- Self-learning from previous threat modeling sessions
- User feedback integration via OpenWebUI chat interface
- Semantic analysis with confidence scoring
- Progressive knowledge refinement
- Interactive discovery with clarification requests
"""

import asyncio
import aiohttp
import json
import yaml
import subprocess
import tempfile
import os
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from pathlib import Path
import logging
from datetime import datetime
import pickle
from collections import defaultdict, Counter
import re

# Threagile schema URL for reference
THREAGILE_SCHEMA_URL = "https://github.com/Threagile/threagile/blob/master/support/schema.json"

@dataclass
class DiscoveryLearning:
    """Tracks learning from previous discovery sessions"""
    successful_queries: Dict[str, List[str]] = field(default_factory=dict)
    failed_queries: Dict[str, List[str]] = field(default_factory=dict)
    asset_patterns: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    user_corrections: List[Dict] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
    def save_to_file(self, filepath: str):
        """Save learning data to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'DiscoveryLearning':
        """Load learning data from file"""
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.PickleError):
            return cls()

@dataclass
class ThreatModelingConfig:
    """Enhanced configuration for threat modeling capabilities"""
    openwebui_base_url: str = "http://localhost:3003"
    knowledge_base_id: Optional[str] = None
    ctm_docker_image: str = "ctm:local"
    max_iterations: int = 5  # Increased for better discovery
    learning_file: str = "threat_modeling_learning.pkl"
    enable_user_feedback: bool = True
    confidence_threshold: float = 0.7
    max_clarification_rounds: int = 3
    
    # Enhanced discovery templates aligned with Threagile schema
    discovery_templates: Dict[str, List[str]] = field(default_factory=lambda: {
        "technical_assets": [
            "applications services components systems",
            "web servers application servers database servers",
            "microservices containers docker kubernetes pods",
            "API gateways load balancers reverse proxies",
            "mobile applications desktop applications clients",
            "authentication services identity providers",
            "monitoring logging security tools",
            "file systems storage systems databases"
        ],
        "trust_boundaries": [
            "network segmentation VLANs subnets",
            "firewalls security groups network policies",
            "DMZ demilitarized zones perimeter networks",
            "cloud regions availability zones",
            "container networks service meshes",
            "VPNs private networks public networks",
            "internal external boundaries",
            "security domains trust zones"
        ],
        "data_assets": [
            "personal data PII sensitive information",
            "customer data user data account information",
            "financial data payment information",
            "configuration data secrets credentials",
            "business data intellectual property",
            "audit logs security logs system logs",
            "backup data archived data",
            "session data cache data temporary files"
        ],
        "communication_links": [
            "HTTP HTTPS REST API calls",
            "gRPC GraphQL SOAP web services",
            "database connections SQL queries",
            "message queues pub/sub messaging",
            "file transfers FTP SFTP",
            "authentication flows OAuth SAML",
            "monitoring health checks",
            "backup replication synchronization"
        ],
        "shared_runtimes": [
            "container orchestration platforms",
            "serverless functions lambda",
            "virtual machines hypervisors",
            "application frameworks runtime environments",
            "shared libraries common dependencies",
            "operating systems base images"
        ]
    })

class EnhancedSemanticAnalyzer:
    """Advanced semantic analysis with confidence scoring and pattern learning"""
    
    def __init__(self, learning: DiscoveryLearning):
        self.learning = learning
        self.logger = logging.getLogger(__name__)
        
        # Threagile schema mappings for better extraction
        self.threagile_asset_properties = {
            "technical_assets": [
                "type", "usage", "size", "technology", "internet", "machine",
                "encryption", "owner", "confidentiality", "integrity", "availability",
                "justification_cia_rating", "multi_tenant", "redundant", "custom_developed_parts"
            ],
            "data_assets": [
                "usage", "origin", "owner", "quantity", "confidentiality", 
                "integrity", "availability", "justification_cia_rating"
            ],
            "trust_boundaries": [
                "type", "technical_assets_inside", "trust_boundaries_nested"
            ],
            "communication_links": [
                "target", "description", "protocol", "authentication", "authorization",
                "vpn", "ip_filtered", "readonly", "usage", "data_assets_sent", "data_assets_received"
            ]
        }
    
    def analyze_content_with_confidence(self, content: str, metadata: Dict) -> Dict[str, Any]:
        """Analyze content with confidence scoring"""
        analysis = {
            "technical_assets": [],
            "trust_boundaries": [],
            "data_assets": [],
            "communication_links": [],
            "shared_runtimes": [],
            "confidence_scores": {},
            "missing_properties": {},
            "suggestions": []
        }
        
        # Enhanced pattern matching with confidence
        for asset_type in ["technical_assets", "trust_boundaries", "data_assets", "communication_links"]:
            assets, confidence = self._extract_assets_with_confidence(content, metadata, asset_type)
            analysis[asset_type] = assets
            analysis["confidence_scores"][asset_type] = confidence
            
            # Check for missing Threagile properties
            missing = self._identify_missing_properties(assets, asset_type)
            if missing:
                analysis["missing_properties"][asset_type] = missing
                analysis["suggestions"].extend(self._generate_discovery_suggestions(asset_type, missing))
        
        return analysis
    
    def _extract_assets_with_confidence(self, content: str, metadata: Dict, asset_type: str) -> Tuple[List[Dict], float]:
        """Extract assets with confidence scoring"""
        assets = []
        confidence_scores = []
        
        # Use learned patterns if available
        learned_patterns = self.learning.asset_patterns.get(asset_type, set())
        
        if asset_type == "technical_assets":
            assets, scores = self._extract_technical_assets_enhanced(content, metadata, learned_patterns)
        elif asset_type == "trust_boundaries":
            assets, scores = self._extract_trust_boundaries_enhanced(content, metadata, learned_patterns)
        elif asset_type == "data_assets":
            assets, scores = self._extract_data_assets_enhanced(content, metadata, learned_patterns)
        elif asset_type == "communication_links":
            assets, scores = self._extract_communication_links_enhanced(content, metadata, learned_patterns)
        
        confidence_scores.extend(scores)
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        return assets, avg_confidence
    
    def _extract_technical_assets_enhanced(self, content: str, metadata: Dict, learned_patterns: Set[str]) -> Tuple[List[Dict], List[float]]:
        """Enhanced technical asset extraction with Threagile compliance"""
        assets = []
        confidence_scores = []
        
        # Enhanced keywords including learned patterns
        base_keywords = {
            "web_application": ["web app", "website", "web service", "webapp", "portal"],
            "process": ["service", "daemon", "worker", "processor", "handler"],
            "datastore": ["database", "db", "storage", "repository", "cache", "redis", "mongodb"],
            "external_entity": ["third-party", "external service", "vendor", "partner"],
            "load_balancer": ["load balancer", "lb", "proxy", "gateway", "ingress"],
            "container": ["docker", "container", "pod", "kubernetes", "k8s"]
        }
        
        # Add learned patterns
        for pattern in learned_patterns:
            for asset_type in base_keywords:
                if any(keyword in pattern.lower() for keyword in base_keywords[asset_type]):
                    base_keywords[asset_type].append(pattern)
        
        lines = content.split('\n')
        for line in lines:
            line_lower = line.lower()
            
            for asset_type, keywords in base_keywords.items():
                for keyword in keywords:
                    if keyword in line_lower:
                        asset = self._create_technical_asset(line, asset_type, metadata)
                        confidence = self._calculate_asset_confidence(line, keyword, asset_type)
                        
                        if confidence > 0.3:  # Only include if reasonably confident
                            assets.append(asset)
                            confidence_scores.append(confidence)
                        break
        
        return assets, confidence_scores
    
    def _create_technical_asset(self, description: str, asset_type: str, metadata: Dict) -> Dict:
        """Create Threagile-compliant technical asset"""
        asset_id = self._generate_id(description)
        
        # Base asset with Threagile required fields
        asset = {
            "id": asset_id,
            "description": description.strip(),
            "type": asset_type,
            "usage": "business",  # Default, should be refined
            "used_as_client_by_human": False,
            "out_of_scope": False,
            "justification_out_of_scope": "",
            "size": "component",
            "technology": self._infer_technology(description),
            "tags": self._extract_tags(description),
            "internet": self._infer_internet_exposure(description),
            "machine": self._infer_machine_type(description),
            "encryption": self._infer_encryption(description),
            "owner": self._infer_owner(description, metadata),
            "confidentiality": "internal",  # Default, should be refined
            "integrity": "important",
            "availability": "important",
            "justification_cia_rating": "Default rating - needs refinement",
            "multi_tenant": False,
            "redundant": False,
            "custom_developed_parts": True,
            "data_assets_processed": [],
            "data_assets_stored": [],
            "data_formats_accepted": [],
            "communication_links": {}
        }
        
        return asset
    
    def _infer_technology(self, description: str) -> str:
        """Infer technology from description"""
        desc_lower = description.lower()
        
        tech_mapping = {
            "web-service-rest": ["rest", "api", "http", "web service"],
            "web-application": ["web app", "website", "portal", "frontend"],
            "database": ["database", "db", "mysql", "postgresql", "mongodb"],
            "container": ["docker", "container", "kubernetes", "k8s"],
            "serverless": ["lambda", "function", "serverless"],
            "message-queue": ["queue", "kafka", "rabbitmq", "sqs"],
            "load-balancer": ["load balancer", "nginx", "apache", "haproxy"],
            "cache": ["redis", "memcache", "cache"]
        }
        
        for tech, keywords in tech_mapping.items():
            if any(keyword in desc_lower for keyword in keywords):
                return tech
        
        return "unknown-technology"
    
    def _calculate_asset_confidence(self, line: str, keyword: str, asset_type: str) -> float:
        """Calculate confidence score for asset extraction"""
        base_confidence = 0.5
        
        # Boost confidence based on context
        if any(indicator in line.lower() for indicator in ["service", "application", "system"]):
            base_confidence += 0.2
        
        # Boost if we have specific technical details
        if any(tech in line.lower() for tech in ["http", "api", "database", "server"]):
            base_confidence += 0.1
        
        # Check against learned successful patterns
        successful_patterns = self.learning.successful_queries.get(asset_type, [])
        if any(pattern.lower() in line.lower() for pattern in successful_patterns):
            base_confidence += 0.3
        
        # Penalize if similar to failed patterns
        failed_patterns = self.learning.failed_queries.get(asset_type, [])
        if any(pattern.lower() in line.lower() for pattern in failed_patterns):
            base_confidence -= 0.2
        
        return min(1.0, max(0.0, base_confidence))
    
    def _identify_missing_properties(self, assets: List[Dict], asset_type: str) -> List[str]:
        """Identify missing Threagile properties that need discovery"""
        if not assets:
            return []
        
        required_props = self.threagile_asset_properties.get(asset_type, [])
        missing_props = []
        
        for asset in assets:
            for prop in required_props:
                if prop not in asset or asset[prop] in ["unknown", "", None, []]:
                    if prop not in missing_props:
                        missing_props.append(prop)
        
        return missing_props
    
    def _generate_discovery_suggestions(self, asset_type: str, missing_properties: List[str]) -> List[str]:
        """Generate suggestions for additional discovery"""
        suggestions = []
        
        property_suggestions = {
            "technology": f"Search for technology stack, frameworks, or implementation details for {asset_type}",
            "authentication": f"Look for authentication mechanisms used by {asset_type}",
            "encryption": f"Investigate encryption methods and TLS/SSL usage for {asset_type}",
            "data_assets_processed": f"Identify what data flows through {asset_type}",
            "owner": f"Determine team or individual responsible for {asset_type}",
            "confidentiality": f"Assess sensitivity level of {asset_type}",
            "internet": f"Check if {asset_type} is internet-facing or internal only"
        }
        
        for prop in missing_properties:
            if prop in property_suggestions:
                suggestions.append(property_suggestions[prop])
        
        return suggestions

class DiscoveryPhaseProcessor:
    """Enhanced discovery phase with self-learning and user interaction"""
    
    def __init__(self, config: ThreatModelingConfig):
        self.config = config
        self.learning = DiscoveryLearning.load_from_file(config.learning_file)
        self.semantic_analyzer = EnhancedSemanticAnalyzer(self.learning)
        self.logger = logging.getLogger(__name__)
        self.session_data = {}
    
    async def interactive_discovery(self, initial_query: str, chat_interface=None) -> Dict[str, Any]:
        """Perform interactive discovery with user feedback"""
        discovery_results = {
            "iterations": [],
            "user_interactions": [],
            "final_architecture": {},
            "confidence_metrics": {},
            "learning_updates": {}
        }
        
        current_query = initial_query
        clarification_round = 0
        
        while clarification_round < self.config.max_clarification_rounds:
            iteration_data = await self._perform_discovery_iteration(current_query)
            discovery_results["iterations"].append(iteration_data)
            
            # Check if we need user clarification
            low_confidence_areas = self._identify_low_confidence_areas(iteration_data)
            
            if low_confidence_areas and self.config.enable_user_feedback and chat_interface:
                clarification_request = self._generate_clarification_request(low_confidence_areas)
                
                if clarification_request:
                    user_response = await self._request_user_clarification(
                        clarification_request, chat_interface
                    )
                    
                    if user_response:
                        discovery_results["user_interactions"].append({
                            "round": clarification_round + 1,
                            "request": clarification_request,
                            "response": user_response
                        })
                        
                        # Update discovery based on user feedback
                        current_query = self._refine_query_with_user_feedback(
                            current_query, user_response
                        )
                        
                        # Learn from user feedback
                        self._learn_from_user_feedback(user_response, iteration_data)
            
            # Check if we have sufficient confidence to proceed
            overall_confidence = self._calculate_overall_confidence(iteration_data)
            if overall_confidence >= self.config.confidence_threshold:
                break
            
            clarification_round += 1
        
        # Finalize results
        discovery_results["final_architecture"] = self._consolidate_discovery_results(
            discovery_results["iterations"]
        )
        discovery_results["confidence_metrics"] = self._calculate_final_confidence_metrics(
            discovery_results["iterations"]
        )
        
        # Save learning
        self.learning.save_to_file(self.config.learning_file)
        
        return discovery_results
    
    async def _perform_discovery_iteration(self, query: str) -> Dict[str, Any]:
        """Perform single discovery iteration with enhanced analysis"""
        iteration_data = {
            "query": query,
            "knowledge_results": [],
            "semantic_analysis": {},
            "discovered_assets": {},
            "confidence_scores": {},
            "missing_information": [],
            "suggested_followups": []
        }
        
        # Enhanced knowledge base queries using adaptive templates
        kb_results = await self._adaptive_knowledge_base_query(query)
        iteration_data["knowledge_results"] = kb_results
        
        # Enhanced semantic analysis
        semantic_analysis = self.semantic_analyzer.analyze_content_with_confidence(
            self._consolidate_content(kb_results), {}
        )
        iteration_data["semantic_analysis"] = semantic_analysis
        iteration_data["discovered_assets"] = self._extract_discovered_assets(semantic_analysis)
        iteration_data["confidence_scores"] = semantic_analysis["confidence_scores"]
        iteration_data["missing_information"] = semantic_analysis["missing_properties"]
        iteration_data["suggested_followups"] = semantic_analysis["suggestions"]
        
        return iteration_data
    
    async def _adaptive_knowledge_base_query(self, base_query: str) -> List[Dict]:
        """Adaptive knowledge base querying with learning"""
        all_results = []
        
        # Use successful query patterns from learning
        successful_patterns = []
        for asset_type, patterns in self.learning.successful_queries.items():
            successful_patterns.extend(patterns[:3])  # Top 3 successful patterns per type
        
        # Combine base query with discovery templates and learned patterns
        query_variations = [base_query]
        
        for asset_type, templates in self.config.discovery_templates.items():
            for template in templates[:2]:  # Top 2 templates per asset type
                query_variations.append(f"{base_query} {template}")
        
        # Add successful learned patterns
        for pattern in successful_patterns[:5]:  # Top 5 learned patterns
            query_variations.append(f"{base_query} {pattern}")
        
        # Execute queries
        for query in query_variations:
            results = await self._query_knowledge_base(query)
            all_results.extend(results)
            
            # Track query performance for learning
            if results:
                self._record_successful_query(query, len(results))
            else:
                self._record_failed_query(query)
        
        # Deduplicate and rank results
        return self._deduplicate_and_rank_results(all_results)
    
    def _generate_clarification_request(self, low_confidence_areas: List[str]) -> Optional[str]:
        """Generate user clarification request"""
        if not low_confidence_areas:
            return None
        
        request_parts = [
            "I need some clarification to improve the threat model accuracy:",
            ""
        ]
        
        for i, area in enumerate(low_confidence_areas[:3], 1):  # Limit to top 3
            request_parts.append(f"{i}. {area}")
        
        request_parts.extend([
            "",
            "Please provide any additional information about these areas, or let me know if any of my assumptions are incorrect."
        ])
        
        return "\n".join(request_parts)
    
    async def _request_user_clarification(self, request: str, chat_interface) -> Optional[str]:
        """Request clarification from user via chat interface"""
        try:
            # This would integrate with OpenWebUI chat interface
            # For now, we'll simulate the interface
            response = await chat_interface.send_message(request)
            return response
        except Exception as e:
            self.logger.error(f"Failed to request user clarification: {e}")
            return None
    
    def _learn_from_user_feedback(self, user_response: str, iteration_data: Dict):
        """Learn from user feedback to improve future discovery"""
        # Record user corrections
        correction = {
            "timestamp": datetime.now().isoformat(),
            "user_response": user_response,
            "context": iteration_data["query"],
            "discovered_assets": iteration_data["discovered_assets"]
        }
        self.learning.user_corrections.append(correction)
        
        # Extract patterns from user response
        response_lower = user_response.lower()
        
        # Look for confirmations and corrections
        if any(word in response_lower for word in ["yes", "correct", "right", "accurate"]):
            # User confirmed our findings - boost confidence in patterns
            for asset_type, assets in iteration_data["discovered_assets"].items():
                for asset in assets:
                    pattern = asset.get("description", "")
                    if pattern:
                        self.learning.asset_patterns[asset_type].add(pattern)
        
        elif any(word in response_lower for word in ["no", "wrong", "incorrect", "not"]):
            # User corrected our findings - record as failed pattern
            query = iteration_data["query"]
            for asset_type in iteration_data["discovered_assets"]:
                if asset_type not in self.learning.failed_queries:
                    self.learning.failed_queries[asset_type] = []
                self.learning.failed_queries[asset_type].append(query)
    
    def save_learning_data(self):
        """Save accumulated learning data"""
        self.learning.save_to_file(self.config.learning_file)
        self.logger.info(f"Learning data saved to {self.config.learning_file}")

# Enhanced main extension class
class EnhancedThreatModelingExtension:
    """Enhanced threat modeling extension with advanced discovery"""
    
    def __init__(self, pipe_instance, config: ThreatModelingConfig = None):
        self.pipe = pipe_instance
        self.config = config or ThreatModelingConfig()
        self.discovery_processor = DiscoveryPhaseProcessor(self.config)
        self.logger = logging.getLogger(__name__)
    
    async def process_threat_modeling_with_enhanced_discovery(
        self, query: str, user_valves: Dict = None, chat_interface=None
    ) -> Dict[str, Any]:
        """Process threat modeling with enhanced discovery phase"""
        
        try:
            # Enhanced discovery phase
            discovery_results = await self.discovery_processor.interactive_discovery(
                query, chat_interface
            )
            
            # Generate threat model from discovery results
            threat_model = await self._generate_threat_model_from_discovery(
                discovery_results
            )
            
            # Validate and refine
            validation_results = await self._validate_and_refine_model(threat_model)
            
            return {
                "success": True,
                "discovery_results": discovery_results,
                "threat_model": threat_model,
                "validation_results": validation_results,
                "confidence_metrics": discovery_results["confidence_metrics"],
                "learning_summary": self._generate_learning_summary()
            }
            
        except Exception as e:
            self.logger.error(f"Enhanced threat modeling failed: {e}")
            return {"error": f"Enhanced threat modeling failed: {str(e)}"}
    
    def _generate_learning_summary(self) -> Dict[str, Any]:
        """Generate summary of learning progress"""
        learning = self.discovery_processor.learning
        
        return {
            "total_successful_queries": sum(len(queries) for queries in learning.successful_queries.values()),
            "total_failed_queries": sum(len(queries) for queries in learning.failed_queries.values()),
            "learned_patterns": {
                asset_type: len(patterns) 
                for asset_type, patterns in learning.asset_patterns.items()
            },
            "user_corrections": len(learning.user_corrections),
            "confidence_improvements": learning.confidence_scores
        }

# Integration decorator with enhanced discovery
def extend_pipe_with_enhanced_threat_modeling(pipe_class):
    """Decorator to extend pipe with enhanced threat modeling"""
    
    original_pipe = pipe_class.pipe
    
    async def enhanced_discovery_pipe(self, user_message: str, model_id: str, messages: List[Dict], body: Dict) -> str:
        """Enhanced pipe with advanced discovery capabilities"""
        
        if any(keyword in user_message.lower() for keyword in ["threat model", "threagile", "security analysis"]):
            config = ThreatModelingConfig(
                openwebui_base_url=self.valves.get("openwebui_base_url", "http://localhost:3003"),
                knowledge_base_id=self.valves.get("knowledge_base_id"),
                max_iterations=self.valves.get("threat_modeling_iterations", 5),
                enable_user_feedback=self.valves.get("enable_user_feedback", True),
                confidence_threshold=self.valves.get("confidence_threshold", 0.7)
            )
            
            extension = EnhancedThreatModelingExtension(self, config)
            
            # Create chat interface for user interaction
            chat_interface = self._create_chat_interface()
            
            results = await extension.process_threat_modeling_with_enhanced_discovery(
                user_message, self.valves.__dict__, chat_interface
            )
            
            if results.get("success"):
                return self._format_enhanced_results(results)
            else:
                return f"Enhanced threat modeling failed: {results.get('error', 'Unknown error')}"
        
        return await original_pipe(self, user_message, model_id, messages, body)
    
    pipe_class.pipe = enhanced_discovery_pipe
    
    # Enhanced valves
    original_valves = pipe_class.Valves
    
    class EnhancedDiscoveryValves(original_valves):
        enhanced_discovery_enabled: bool = True
        enable_user_feedback: bool = True
        confidence_threshold: float = 0.7
        max_clarification_rounds: int = 3
        learning_file: str = "threat_modeling_learning.pkl"
    
    pipe_class.Valves = EnhancedDiscoveryValves
    
    return pipe_class
