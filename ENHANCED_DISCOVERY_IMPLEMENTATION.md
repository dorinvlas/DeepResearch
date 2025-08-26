# Implementation Guide: Enhanced Discovery Phase Integration

## Quick Start Integration

### 1. Basic Integration with Existing Pipe

Replace your existing threat modeling extension with the enhanced version:

```python
from enhanced_threat_modeling_extension import (
    EnhancedThreatModelingExtension,
    ThreatModelingConfig,
    extend_pipe_with_enhanced_threat_modeling
)

# Apply enhanced discovery to your existing pipe
@extend_pipe_with_enhanced_threat_modeling
class Pipe:
    # Your existing pipe implementation
    pass
```

### 2. Configuration Setup

Configure the enhanced discovery system through valve parameters:

```python
class Valves(BaseValves):
    # Existing valves...
    
    # Enhanced Discovery Configuration
    enhanced_discovery_enabled: bool = True
    enable_user_feedback: bool = True
    confidence_threshold: float = 0.7
    max_clarification_rounds: int = 3
    threat_modeling_iterations: int = 5
    learning_file: str = "threat_modeling_learning.pkl"
    
    # OpenWebUI Integration
    openwebui_base_url: str = "http://localhost:3003"
    knowledge_base_id: str = ""  # Your knowledge base ID
```

### 3. OpenWebUI Chat Interface Integration

The system requires integration with OpenWebUI's chat interface for user feedback:

```python
class ChatInterface:
    """Interface for OpenWebUI chat integration"""
    
    def __init__(self, pipe_instance):
        self.pipe = pipe_instance
    
    async def send_message(self, message: str) -> str:
        """Send message to user and wait for response"""
        # Implementation depends on OpenWebUI's event system
        # This is a simplified example
        
        # Emit message to user interface
        await self.pipe.__event_emitter__({
            "type": "message",
            "data": {
                "content": message,
                "role": "assistant",
                "requires_response": True
            }
        })
        
        # Wait for user response (implementation specific)
        # This would integrate with OpenWebUI's response handling
        return await self._wait_for_user_response()
    
    async def _wait_for_user_response(self) -> str:
        """Wait for user response through OpenWebUI"""
        # Implementation specific to OpenWebUI's event handling
        pass
```

## Progressive Implementation

### Phase 1: Basic Enhanced Discovery

Start with enhanced discovery without user feedback:

```python
config = ThreatModelingConfig(
    enhanced_discovery_enabled=True,
    enable_user_feedback=False,  # Start without feedback
    confidence_threshold=0.6,    # Lower threshold initially
    max_iterations=3
)
```

### Phase 2: Add Learning Capabilities

Enable learning from successful/failed patterns:

```python
config = ThreatModelingConfig(
    enhanced_discovery_enabled=True,
    enable_user_feedback=False,
    learning_file="threat_modeling_learning.pkl",
    confidence_threshold=0.7
)

# The system will automatically start learning patterns
```

### Phase 3: Enable User Feedback

Add interactive clarification with users:

```python
config = ThreatModelingConfig(
    enhanced_discovery_enabled=True,
    enable_user_feedback=True,
    max_clarification_rounds=2,  # Start with fewer rounds
    confidence_threshold=0.7
)
```

### Phase 4: Full Enhancement

Enable all advanced features:

```python
config = ThreatModelingConfig(
    enhanced_discovery_enabled=True,
    enable_user_feedback=True,
    max_clarification_rounds=3,
    confidence_threshold=0.8,    # Higher threshold for better quality
    max_iterations=5
)
```

## Customization Options

### Custom Discovery Templates

Add domain-specific discovery templates:

```python
custom_templates = {
    "technical_assets": [
        "microservices docker kubernetes containers",
        "API gateways service mesh istio",
        "databases postgresql mongodb redis",
        "web applications react angular vue",
        "mobile applications iOS android"
    ],
    "trust_boundaries": [
        "kubernetes namespaces service mesh",
        "cloud VPC subnets security groups",
        "DMZ internal network zones"
    ],
    "data_assets": [
        "user profiles customer data PII",
        "payment information credit cards",
        "session data authentication tokens",
        "configuration secrets environment variables"
    ]
}

config = ThreatModelingConfig(
    discovery_templates=custom_templates
)
```

### Custom Confidence Scoring

Implement domain-specific confidence scoring:

```python
class CustomSemanticAnalyzer(EnhancedSemanticAnalyzer):
    
    def _calculate_asset_confidence(self, line: str, keyword: str, asset_type: str) -> float:
        base_confidence = super()._calculate_asset_confidence(line, keyword, asset_type)
        
        # Add domain-specific confidence boosters
        if asset_type == "technical_assets":
            if any(tech in line.lower() for tech in ["kubernetes", "docker", "microservice"]):
                base_confidence += 0.1
        
        elif asset_type == "data_assets":
            if any(sensitivity in line.lower() for sensitivity in ["pii", "sensitive", "confidential"]):
                base_confidence += 0.2
        
        return min(1.0, base_confidence)
```

### Learning Data Management

Control how learning data is managed:

```python
from enhanced_threat_modeling_extension import DiscoveryLearning

# Load existing learning data
learning = DiscoveryLearning.load_from_file("custom_learning.pkl")

# Add custom successful patterns
learning.successful_queries["technical_assets"].extend([
    "kubernetes pods services deployments",
    "microservices REST APIs gRPC"
])

# Add failed patterns to avoid
learning.failed_queries["trust_boundaries"].extend([
    "generic network description"
])

# Save updated learning data
learning.save_to_file("custom_learning.pkl")
```

## Testing and Validation

### Unit Testing Discovery Components

```python
import pytest
from enhanced_threat_modeling_extension import (
    DiscoveryPhaseProcessor,
    ThreatModelingConfig
)

@pytest.mark.asyncio
async def test_discovery_processor():
    config = ThreatModelingConfig(
        enable_user_feedback=False,
        confidence_threshold=0.5
    )
    
    processor = DiscoveryPhaseProcessor(config)
    
    # Test discovery with sample query
    results = await processor.interactive_discovery(
        "e-commerce platform with microservices"
    )
    
    assert "technical_assets" in results["final_architecture"]
    assert len(results["iterations"]) > 0
    assert "confidence_metrics" in results
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_full_threat_modeling_workflow():
    config = ThreatModelingConfig(
        enhanced_discovery_enabled=True,
        enable_user_feedback=False,
        max_iterations=2
    )
    
    extension = EnhancedThreatModelingExtension(None, config)
    
    results = await extension.process_threat_modeling_with_enhanced_discovery(
        "threat model for online banking system"
    )
    
    assert results["success"] is True
    assert "discovery_results" in results
    assert "threat_model" in results
    assert "confidence_metrics" in results
```

## Performance Optimization

### Learning Data Cleanup

Periodically clean up learning data to maintain performance:

```python
def cleanup_learning_data(learning_file: str, max_patterns: int = 1000):
    """Clean up learning data to maintain performance"""
    learning = DiscoveryLearning.load_from_file(learning_file)
    
    # Keep only top performing patterns
    for asset_type in learning.successful_queries:
        if len(learning.successful_queries[asset_type]) > max_patterns:
            # Sort by usage frequency and keep top patterns
            patterns = learning.successful_queries[asset_type]
            learning.successful_queries[asset_type] = patterns[:max_patterns]
    
    # Remove old user corrections (keep last 100)
    if len(learning.user_corrections) > 100:
        learning.user_corrections = learning.user_corrections[-100:]
    
    learning.save_to_file(learning_file)
```

### Confidence Threshold Tuning

Monitor and adjust confidence thresholds based on results:

```python
def analyze_confidence_performance(results_history: List[Dict]):
    """Analyze confidence scoring performance"""
    
    confidence_accuracy = []
    
    for result in results_history:
        for iteration in result["discovery_results"]["iterations"]:
            for asset_type, confidence in iteration["confidence_scores"].items():
                # Compare confidence vs. actual validation success
                validation_success = iteration.get("validation_passed", False)
                confidence_accuracy.append((confidence, validation_success))
    
    # Calculate optimal threshold
    optimal_threshold = calculate_optimal_threshold(confidence_accuracy)
    
    return {
        "current_accuracy": calculate_accuracy(confidence_accuracy),
        "recommended_threshold": optimal_threshold,
        "total_samples": len(confidence_accuracy)
    }
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Learning File Corruption

```python
try:
    learning = DiscoveryLearning.load_from_file("threat_modeling_learning.pkl")
except (FileNotFoundError, pickle.PickleError):
    print("Learning file corrupted or missing, creating new one")
    learning = DiscoveryLearning()
    learning.save_to_file("threat_modeling_learning.pkl")
```

#### 2. Low Confidence Scores

If confidence scores are consistently low:

- Lower the confidence threshold temporarily
- Add more specific discovery templates
- Review and improve keyword matching
- Check if knowledge base has sufficient relevant content

#### 3. OpenWebUI Integration Issues

```python
class FallbackChatInterface:
    """Fallback when OpenWebUI integration fails"""
    
    async def send_message(self, message: str) -> str:
        # Log the message instead of sending to user
        logger.info(f"Would ask user: {message}")
        
        # Return default response to continue processing
        return "Please proceed with current findings"
```

## Monitoring and Analytics

### Discovery Performance Metrics

```python
def generate_discovery_metrics(results: Dict) -> Dict:
    """Generate metrics for discovery performance"""
    
    metrics = {
        "discovery_efficiency": {
            "avg_iterations": len(results["discovery_results"]["iterations"]),
            "avg_confidence": calculate_avg_confidence(results),
            "user_interactions": len(results["discovery_results"]["user_interactions"])
        },
        "asset_coverage": {
            "technical_assets": len(results["discovery_results"]["final_architecture"].get("technical_assets", [])),
            "trust_boundaries": len(results["discovery_results"]["final_architecture"].get("trust_boundaries", [])),
            "data_assets": len(results["discovery_results"]["final_architecture"].get("data_assets", [])),
            "communication_links": len(results["discovery_results"]["final_architecture"].get("communication_links", []))
        },
        "quality_indicators": {
            "validation_success": results["validation_results"].get("success", False),
            "learning_improvements": len(results["learning_summary"]["learned_patterns"])
        }
    }
    
    return metrics
```

This implementation guide provides a comprehensive approach to integrating the enhanced discovery phase into your existing threat modeling system, with options for gradual adoption and customization based on your specific needs.
