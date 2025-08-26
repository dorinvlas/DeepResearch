# DeepResearch AI Agent Instructions

## Project Overview
DeepResearch is an advanced AI-powered research automation system implemented as an Open WebUI pipe. It performs comprehensive, iterative research (30-60 minutes) and generates detailed reports with verified citations. This is academic-quality analysis, not quick search.

**NEW: Enhanced Threat Modeling Extension** - The system now includes sophisticated automated Threagile YAML threat model generation with self-learning discovery capabilities, interactive user feedback integration, and comprehensive Threagile schema compliance.

## Core Architecture

### Open WebUI Pipe Implementation
- **Main File**: `pipe` - Single Python file containing the complete pipeline
- **Entry Point**: `Pipe` class implementing Open WebUI pipe interface
- **State Management**: `ResearchStateManager` for conversation isolation
- **Caching**: `EmbeddingCache` and `TransformationCache` for performance
- **Trajectory Tracking**: `TrajectoryAccumulator` for research direction

### Research Workflow Pipeline
1. **Query Processing**: Multi-query generation with semantic embeddings
2. **Outline Generation**: Interactive outline creation with user feedback
3. **Iterative Research**: Cycle-based research with semantic prioritization
4. **Content Management**: Sliding windows, compression, relevance penalties
5. **Report Synthesis**: Multi-stage generation (subsection → section → global editing)

### Key Classes and Components
- `Pipe.Valves`: Comprehensive configuration with 40+ parameters
- `ResearchStateManager`: Per-conversation state isolation
- `EmbeddingCache`: LRU cache for embedding API calls (10M max size)
- `TransformationCache`: Cache for semantic transformations (2.5M max size)
- `TrajectoryAccumulator`: Efficient research direction tracking

### Threat Modeling Extension Components
- `ThreatModelingExtension`: Main threat modeling orchestrator
- `ThreatModelingProcessor`: Knowledge base query and semantic analysis engine
- `DiscoveryLearning`: Persistent learning from discovery sessions
- `EnhancedSemanticAnalyzer`: Advanced semantic analysis with confidence scoring
- `DiscoveryPhaseProcessor`: Interactive discovery with user feedback
- `ThreatModelingConfig`: Comprehensive threat modeling configuration

## Configuration System

### Critical Valve Parameters
- `RESEARCH_MODEL`/`SYNTHESIS_MODEL`: Primary AI models (gemma3:12b/27b)
- `EMBEDDING_MODEL`: Semantic comparison (granite-embedding:30m)
- `MAX_CYCLES`/`MIN_CYCLES`: Research iteration limits (15/10)
- `MAX_RESULT_TOKENS`: Token limit per result (4000)
- `COMPRESSION_SETPOINT`: When compression engages (4000)
- `CHUNK_LEVEL`: Text chunking strategy (1=phrase, 2=sentence, 3=paragraph, 4+=multi-paragraph)

### Performance Tuning
- `TEMPERATURE`/`SYNTHESIS_TEMPERATURE`: Generation randomness (0.7/0.6)
- `THREAD_WORKERS`: Parallel processing (2 max recommended)
- `QUALITY_FILTER_ENABLED`: Result filtering toggle
- `STEPPED_SYNTHESIS_COMPRESSION`: Tiered compression for older results

### Search Integration
- `SEARCH_URL`: Web search endpoint (SearXNG recommended)
- `OLLAMA_URL`/`USE_AZURE_FOUNDRY`: AI model endpoints
- `HANDLE_PDFS`/`PDF_MAX_PAGES`: PDF processing (25 pages max)

### Threat Modeling Configuration
- `THREAT_MODELING_ENABLED`: Enable/disable threat modeling capabilities
- `OPENWEBUI_BASE_URL`: OpenWebUI API endpoint (default: http://localhost:3003)
- `KNOWLEDGE_BASE_ID`: Target knowledge base for architecture discovery
- `CTM_DOCKER_IMAGE`: ctm:local Docker image for Threagile validation
- `THREAT_MODELING_ITERATIONS`: Maximum discovery iterations (default: 5)
- `CONFIDENCE_THRESHOLD`: Minimum confidence for proceeding (default: 0.7)
- `ENABLE_USER_FEEDBACK`: Interactive clarification via OpenWebUI chat
- `MAX_CLARIFICATION_ROUNDS`: Maximum user interaction rounds (default: 3)
- `LEARNING_FILE`: Persistent learning data storage file

## AI Agent Architecture

### Primary AI Agents

#### **1. DeepResearch Core Agent**
- **Purpose**: Comprehensive research automation and report generation
- **Models**: gemma3:12b (research), gemma3:27b (synthesis), granite-embedding:30m (semantic)
- **Capabilities**: 
  - Multi-cycle iterative research with semantic prioritization
  - Preference direction vector (PDV) learning from user feedback
  - Advanced content compression with eigendecomposition
  - Citation verification and bibliography generation

#### **2. Enhanced Threat Modeling Agent**
- **Purpose**: Automated Threagile YAML threat model generation with self-learning
- **Components**: Multiple specialized sub-agents working in concert
- **Capabilities**:
  - Architecture discovery from knowledge bases
  - Interactive user clarification via OpenWebUI chat
  - Confidence-scored asset extraction
  - Learning pattern recognition and adaptation

### Threat Modeling Sub-Agents

#### **Discovery Intelligence Agent**
- **Class**: `DiscoveryPhaseProcessor`
- **Function**: Orchestrates multi-round architecture discovery
- **Learning**: Persistent pattern recognition from successful/failed discoveries
- **Interaction**: Real-time clarification requests via OpenWebUI chat interface

#### **Semantic Analysis Agent**
- **Class**: `EnhancedSemanticAnalyzer`
- **Function**: Asset extraction with confidence scoring and Threagile alignment
- **Intelligence**: Context-aware classification using learned vocabularies
- **Output**: Structured architecture data with missing property identification

#### **Learning Management Agent**
- **Class**: `DiscoveryLearning`
- **Function**: Persistent learning across threat modeling sessions
- **Data**: Successful/failed query patterns, user corrections, confidence scores
- **Evolution**: Continuous improvement of discovery accuracy and relevance

#### **Validation Orchestration Agent**
- **Function**: Docker integration for Threagile YAML validation
- **Process**: ctm:local container management and error interpretation
- **Feedback**: Validation error analysis for iterative improvement

### Agent Interaction Patterns

#### **Research Cycle Coordination**
```python
# Multi-agent research workflow
1. Query processing → Embedding generation (Core Agent)
2. Topic prioritization → Semantic analysis (Core Agent)
3. Search execution → Content extraction (Core Agent)
4. Compression and analysis → State updates (Core Agent)
5. Threat model detection → Extension activation (Routing Agent)
6. Discovery phase → Multi-agent collaboration (Threat Modeling Agents)
7. Synthesis generation → Final report (Core Agent)
```

#### **Threat Modeling Agent Collaboration**
```python
# Enhanced discovery workflow
1. Query classification → Discovery Intelligence Agent
2. Knowledge base queries → Adaptive template generation
3. Content analysis → Semantic Analysis Agent
4. Confidence assessment → Missing property identification
5. User clarification → Interactive feedback processing
6. Pattern learning → Learning Management Agent
7. YAML generation → Threagile compliance validation
8. Docker validation → Validation Orchestration Agent
9. Iterative refinement → Multi-agent coordination
```

### Agent Communication Protocols

#### **State Sharing**
- **ResearchStateManager**: Maintains conversation isolation across agents
- **Shared Memory**: EmbeddingCache and TransformationCache for performance
- **Context Preservation**: Trajectory accumulation across research cycles

#### **Learning Synchronization**
- **Pattern Sharing**: Discovery patterns shared between semantic analysis and learning agents
- **Confidence Calibration**: Cross-agent validation of confidence scoring accuracy
- **User Feedback Integration**: Learning agent processes feedback for all sub-agents

#### **Error Handling and Fallbacks**
- **Graceful Degradation**: Agents continue operation when dependencies fail
- **Fallback Strategies**: Alternative processing paths when primary agents unavailable
- **Recovery Mechanisms**: Automatic retry and error recovery protocols

## Semantic Processing Architecture

### Embedding System
- **Caching Strategy**: Text hash keys, LRU eviction, hit/miss tracking
- **Batch Processing**: Sequential embedding generation for efficiency
- **Vocabulary Integration**: 10k word vocabulary for semantic analysis
- **Transformation Pipeline**: Eigendecomposition-based semantic transformations

### Content Compression
- `compress_content_with_local_similarity()`: Local context awareness
- `compress_content_with_eigendecomposition()`: Advanced semantic compression
- `apply_stepped_compression()`: Age-based tiered compression
- `handle_repeated_content()`: Sliding window for repeats

### Research Direction
- **Preference Direction Vector (PDV)**: User preference modeling
- **Research Dimensions**: Semantic space tracking with coverage metrics
- **Gap Vector**: Identifies under-researched areas
- **Trajectory Accumulator**: Maintains research momentum across cycles

### Threat Modeling Semantic Processing
- **Discovery Learning**: Persistent learning from successful/failed discovery patterns
- **Asset Pattern Recognition**: Builds vocabularies from confirmed discoveries
- **Confidence Scoring**: AI-driven assessment of discovery quality with 0.0-1.0 scoring
- **Threagile Schema Alignment**: Property extraction aligned with Threagile requirements
- **Interactive Clarification**: Real-time user feedback integration via OpenWebUI chat
- **Adaptive Query Generation**: Learning-enhanced query templates for knowledge base

## Development Patterns

### State Management
```python
# Always use state manager for conversation isolation
state = self.get_state()
self.update_state("key", value)
```

### Embedding Workflows
```python
# Cache-aware embedding generation
embedding = await self.get_embedding(text)
transformed = await self.get_transformed_embedding(text, transformation)
```

### Threat Modeling Workflows
```python
# Enhanced discovery with learning
discovery_results = await self.discovery_processor.interactive_discovery(query, chat_interface)
# Threagile YAML generation
yaml_content = await self.generate_threagile_yaml(architecture_data, project_name)
# Docker validation
is_valid, msg = await self.validate_with_ctm_local(yaml_content)
```

### Content Processing
```python
# Multi-level text chunking
chunks = self.chunk_text(content)
# Semantic compression with context
compressed = await self.compress_content_with_local_similarity(content, query_embedding)
```

### Error Handling
- Graceful degradation for embedding failures
- Archive.org fallback for blocked sources
- PDF processing with page limits
- Rate limiting with exponential backoff

## Key Workflows

### Research Cycle
1. **Topic Prioritization**: `rank_topics_by_research_priority()`
2. **Query Generation**: `improved_query_generation()` with semantic context
3. **Search Processing**: `process_query()` with result filtering
4. **Content Extraction**: URL fetching with anti-blocking measures
5. **Semantic Analysis**: Similarity calculation and compression
6. **State Updates**: Dimension coverage and trajectory tracking

### Synthesis Pipeline
1. **Outline Generation**: `generate_synthesis_outline()` based on coverage
2. **Section Building**: `generate_section_content_with_citations()`
3. **Citation Verification**: `verify_citations()` against source content
4. **Global Review**: `review_synthesis()` for coherence
5. **Bibliography**: Formatted source list with verification status

### User Interaction
- **Outline Feedback**: `process_user_outline_feedback()` with NLP parsing
- **Interactive Research**: Real-time status updates via event emitters
- **Preference Learning**: PDV calculation from user choices

### Threat Modeling Workflow
1. **Query Classification**: Identify threat modeling requests using keyword detection
2. **Enhanced Discovery Phase**: Multi-round discovery with adaptive templates
3. **Knowledge Base Queries**: OpenWebUI API integration with hybrid search
4. **Semantic Analysis**: Asset extraction with confidence scoring and Threagile alignment
5. **User Clarification**: Interactive feedback via OpenWebUI chat for low-confidence areas
6. **Threagile Generation**: Standards-compliant YAML with complete property coverage
7. **Docker Validation**: ctm:local container validation with error feedback
8. **Learning Integration**: Pattern learning from successful/failed discoveries
9. **Iterative Refinement**: Multi-iteration improvement until validation success

## Performance Considerations

### Memory Management
- Embedding cache: 10M items, LRU eviction
- Transformation cache: 2.5M items
- State isolation per conversation
- Token counting and compression triggers

### Optimization Strategies
- Sequential processing to avoid overwhelming APIs
- Cache hit rate monitoring (log via `cache.stats()`)
- Adaptive token limits based on relevance scores
- Stepped compression for older results

### Rate Limiting
- Domain-specific delays for academic sources
- User-agent rotation and header management
- Archive.org fallback for blocked content
- Exponential backoff for failed requests

## Integration Points

### Open WebUI Interface
- `pipe()` method: Main entry point with event emitters
- `__event_emitter__`: Status updates to UI
- `__event_call__`: Direct API calls to Open WebUI
- `__user__`/`__model__`: Context from Open WebUI

### External Dependencies
- **Ollama/Azure**: AI model inference
- **SearXNG**: Web search (configurable endpoint)
- **Archive.org**: Fallback content source
- **PDF Processing**: PyPDF2/pdfplumber for document extraction

### Threat Modeling Dependencies
- **OpenWebUI API**: Knowledge base access via REST endpoints
- **ctm:local Docker**: Threagile YAML validation container
- **aiohttp**: Async HTTP client for knowledge base queries
- **PyYAML**: YAML generation and parsing for Threagile models
- **pickle**: Persistent learning data serialization

### Model Requirements
- Primary: gemma3:12b/27b for research/synthesis
- Embedding: granite-embedding:30m for semantic analysis
- Quality Filter: gemma3:4b for result filtering

## File Patterns and Structure
- `pipe`: Main Python implementation (single file)
- `gemma3-12b-prompt`: AI model system prompt configuration
- `why`: Example philosophical research output
- `granite30m mit 10k.gz`: Large dataset archive
- Research exports: `research_export_[query]_[timestamp].txt`

### Threat Modeling Extension Files
- `threat_modeling_extension.py`: Basic threat modeling implementation
- `enhanced_threat_modeling_extension.py`: Enhanced discovery with self-learning
- `THREAT_MODELING_INTEGRATION.md`: Integration documentation
- `ENHANCED_DISCOVERY_PHASE.md`: Technical discovery documentation
- `ENHANCED_DISCOVERY_IMPLEMENTATION.md`: Implementation guide
- `ENHANCED_DISCOVERY_SUMMARY.md`: Executive summary
- `threat_modeling_learning.pkl`: Persistent learning data storage

## Critical Implementation Notes
- **No async/await in main pipe()**: Open WebUI compatibility
- **State isolation crucial**: Multiple conversations must not interfere
- **Cache management**: Monitor hit rates, implement LRU eviction
- **Error resilience**: Graceful degradation when APIs fail
- **Token awareness**: Track and optimize for model context limits

### Threat Modeling Implementation Notes
- **Discovery Learning Persistence**: Use pickle for learning data across sessions
- **OpenWebUI Chat Integration**: Leverage `__event_emitter__` for user clarification
- **Confidence Threshold Tuning**: Start with 0.7, adjust based on validation success
- **Docker Container Management**: Ensure ctm:local image availability for validation
- **Knowledge Base Access**: Requires proper OpenWebUI API authentication headers
- **Threagile Schema Compliance**: All generated YAML must validate against official schema
- **Learning Data Cleanup**: Periodically clean learning files to maintain performance
- **Interactive Feedback Handling**: Graceful fallback when user interaction fails

### Advanced Configuration Examples
```python
# Enhanced threat modeling valve configuration
class EnhancedValves(BaseValves):
    # Core DeepResearch settings
    RESEARCH_MODEL: str = "gemma3:12b"
    SYNTHESIS_MODEL: str = "gemma3:27b"
    EMBEDDING_MODEL: str = "granite-embedding:30m"
    
    # Threat modeling extensions
    THREAT_MODELING_ENABLED: bool = True
    ENHANCED_DISCOVERY_ENABLED: bool = True
    OPENWEBUI_BASE_URL: str = "http://localhost:3003"
    KNOWLEDGE_BASE_ID: str = ""
    CTM_DOCKER_IMAGE: str = "ctm:local"
    
    # Discovery configuration
    CONFIDENCE_THRESHOLD: float = 0.7
    MAX_CLARIFICATION_ROUNDS: int = 3
    ENABLE_USER_FEEDBACK: bool = True
    LEARNING_FILE: str = "threat_modeling_learning.pkl"
    THREAT_MODELING_ITERATIONS: int = 5
```

### Discovery Phase Technical Details
- **Multi-Template Querying**: Uses 8+ templates per asset type for comprehensive discovery
- **Confidence Algorithm**: Combines keyword matching, context analysis, and historical patterns
- **Pattern Learning**: Tracks query success rates and builds asset-specific vocabularies
- **User Feedback Integration**: Processes natural language responses to improve accuracy
- **Adaptive Query Generation**: Refines queries based on validation feedback and user input
- **Threagile Property Mapping**: Ensures all required properties are discovered for each asset type

### Integration Patterns
```python
# Decorator pattern for threat modeling extension
@extend_pipe_with_enhanced_threat_modeling
class Pipe:
    # Existing DeepResearch implementation
    pass

# Manual integration approach
extension = EnhancedThreatModelingExtension(pipe_instance, config)
results = await extension.process_threat_modeling_with_enhanced_discovery(query, valves, chat_interface)
```
