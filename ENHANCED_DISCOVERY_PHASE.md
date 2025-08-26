# Enhanced Discovery Phase for Threat Modeling

## Overview

The enhanced discovery phase significantly improves the Knowledge Retrieval and Semantic Analysis stages of the threat modeling process. This enhancement focuses on creating a self-learning system that adapts based on previous sessions and user feedback through the OpenWebUI chat interface.

## Key Enhancements

### 1. Advanced Discovery Architecture

#### **DiscoveryLearning Class**

- **Purpose**: Persistent learning from previous threat modeling sessions
- **Features**:
  - Tracks successful and failed queries for each asset type
  - Maintains learned patterns for improved asset identification
  - Stores user corrections and feedback
  - Calculates confidence scores for different discovery approaches

#### **EnhancedSemanticAnalyzer**

- **Purpose**: Advanced semantic analysis with confidence scoring
- **Features**:
  - Threagile schema-aligned property extraction
  - Confidence scoring for each discovered asset
  - Pattern-based learning from historical data
  - Missing property identification and suggestion generation

#### **DiscoveryPhaseProcessor**

- **Purpose**: Orchestrates the interactive discovery process
- **Features**:
  - Multi-round discovery with user clarification
  - Adaptive query generation based on learning
  - Real-time confidence assessment
  - Interactive feedback collection via OpenWebUI

### 2. Self-Learning Capabilities

#### **Query Pattern Learning**

```python
# Tracks successful query patterns
successful_queries = {
    "technical_assets": [
        "microservices containers kubernetes",
        "API gateway authentication services",
        "database servers data storage"
    ],
    "trust_boundaries": [
        "network segmentation security groups",
        "DMZ firewall perimeter"
    ]
}
```

#### **Asset Pattern Recognition**

- Learns from successfully identified assets
- Builds asset type-specific keyword vocabularies
- Improves extraction accuracy over time
- Reduces false positives through negative learning

#### **Confidence Scoring Algorithm**

```python
def _calculate_asset_confidence(self, line: str, keyword: str, asset_type: str) -> float:
    base_confidence = 0.5
    
    # Context indicators boost confidence
    if technical_indicators_present(line):
        base_confidence += 0.2
    
    # Historical success patterns
    if matches_successful_patterns(line, asset_type):
        base_confidence += 0.3
    
    # Avoid failed patterns
    if matches_failed_patterns(line, asset_type):
        base_confidence -= 0.2
    
    return clamp(base_confidence, 0.0, 1.0)
```

### 3. Interactive Discovery with User Feedback

#### **Clarification Request Generation**

The system automatically identifies low-confidence areas and generates specific clarification requests:

```text
I need some clarification to improve the threat model accuracy:

1. Technology stack details for the identified web services
2. Authentication mechanisms used between components
3. Data sensitivity levels for customer information processing

Please provide any additional information about these areas, or let me know if any of my assumptions are incorrect.
```

#### **User Feedback Integration**

- **Confirmation Learning**: When users confirm discoveries, patterns are reinforced
- **Correction Learning**: When users correct findings, failed patterns are recorded
- **Incremental Improvement**: Each session improves future discovery accuracy

### 4. Threagile Schema Alignment

#### **Comprehensive Property Discovery**

The enhanced system specifically looks for all Threagile-required properties:

**Technical Assets**:

- `type`, `usage`, `size`, `technology`
- `internet`, `machine`, `encryption`, `owner`
- `confidentiality`, `integrity`, `availability`
- `multi_tenant`, `redundant`, `custom_developed_parts`

**Data Assets**:

- `usage`, `origin`, `owner`, `quantity`
- CIA triad ratings with justifications

**Trust Boundaries**:

- `type`, `technical_assets_inside`, `trust_boundaries_nested`

**Communication Links**:

- `protocol`, `authentication`, `authorization`
- `vpn`, `ip_filtered`, `readonly`
- `data_assets_sent`, `data_assets_received`

#### **Missing Property Identification**

The system tracks which properties are missing and generates targeted discovery suggestions:

```python
missing_properties = {
    "technical_assets": ["encryption", "owner", "technology"],
    "data_assets": ["confidentiality", "origin"],
    "communication_links": ["authentication", "data_assets_sent"]
}

suggestions = [
    "Search for encryption methods and TLS/SSL usage for technical_assets",
    "Investigate data classification and sensitivity for data_assets",
    "Look for authentication mechanisms used by communication_links"
]
```

### 5. Adaptive Query Generation

#### **Multi-Template Discovery**

Enhanced discovery templates aligned with Threagile schema:

```python
discovery_templates = {
    "technical_assets": [
        "applications services components systems",
        "web servers application servers database servers",
        "microservices containers docker kubernetes pods",
        "API gateways load balancers reverse proxies",
        # ... more templates
    ],
    "trust_boundaries": [
        "network segmentation VLANs subnets",
        "firewalls security groups network policies",
        "DMZ demilitarized zones perimeter networks",
        # ... more templates
    ]
}
```

#### **Learning-Based Query Refinement**

- Incorporates successful patterns from previous sessions
- Avoids query patterns that have historically failed
- Adapts query complexity based on knowledge base response quality

### 6. Configuration and Tuning

#### **Enhanced Configuration Options**

```python
@dataclass
class ThreatModelingConfig:
    max_iterations: int = 5  # Increased for better discovery
    enable_user_feedback: bool = True
    confidence_threshold: float = 0.7
    max_clarification_rounds: int = 3
    learning_file: str = "threat_modeling_learning.pkl"
```

#### **Confidence Thresholds**

- **High Confidence (>0.8)**: Proceed without clarification
- **Medium Confidence (0.5-0.8)**: Optional clarification
- **Low Confidence (<0.5)**: Mandatory clarification or re-discovery

### 7. Integration with OpenWebUI

#### **Chat Interface Integration**

```python
async def _request_user_clarification(self, request: str, chat_interface) -> Optional[str]:
    """Request clarification from user via chat interface"""
    try:
        response = await chat_interface.send_message(request)
        return response
    except Exception as e:
        self.logger.error(f"Failed to request user clarification: {e}")
        return None
```

#### **Real-time Feedback Loop**

1. System performs initial discovery
2. Identifies low-confidence areas
3. Generates clarification request
4. Sends request through OpenWebUI chat
5. Processes user response
6. Updates discovery results
7. Learns patterns for future sessions

### 8. Performance Improvements

#### **Intelligent Deduplication**

- Removes duplicate discoveries across multiple queries
- Ranks results by confidence and relevance
- Consolidates similar assets into single entities

#### **Efficient Learning Storage**

- Persistent learning data using pickle serialization
- Configurable learning file location
- Automatic cleanup of outdated patterns

#### **Query Optimization**

- Limits query variations to prevent API overload
- Prioritizes high-success patterns from learning
- Balances exploration vs. exploitation

## Implementation Example

```python
# Initialize enhanced discovery
config = ThreatModelingConfig(
    enable_user_feedback=True,
    confidence_threshold=0.7,
    max_clarification_rounds=3
)

processor = DiscoveryPhaseProcessor(config)

# Perform interactive discovery
results = await processor.interactive_discovery(
    "threat model for e-commerce platform",
    chat_interface=openwebui_chat
)

# Results include:
# - Discovered assets with confidence scores
# - User interaction history
# - Learning updates applied
# - Suggestions for further investigation
```

## Benefits

1. **Improved Accuracy**: Learning from previous sessions and user feedback
2. **Comprehensive Coverage**: Threagile schema-aligned discovery ensures complete threat models
3. **User Engagement**: Interactive clarification keeps users involved in the discovery process
4. **Adaptive Intelligence**: System becomes more accurate over time
5. **Reduced Manual Effort**: Automated discovery with intelligent suggestions
6. **Quality Assurance**: Confidence scoring helps identify areas needing attention

## Future Enhancements

1. **NLP Integration**: Advanced natural language processing for better user feedback interpretation
2. **Vector Embeddings**: Semantic similarity for improved pattern matching
3. **Collaborative Learning**: Share learnings across multiple installations
4. **Visual Discovery**: Interactive diagrams for user validation
5. **Automated Testing**: Continuous validation of discovery accuracy
