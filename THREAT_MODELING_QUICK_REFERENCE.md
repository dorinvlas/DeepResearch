# Threat Modeling Quick Reference

## Installation

1. Copy `threat_modeling_extension.py` to your pipe directory
2. Install dependencies: `pip install aiohttp pyyaml`
3. Build ctm:local Docker image
4. Apply decorator to your Pipe class

## Usage

### Trigger Threat Modeling

Use these keywords in your queries:

- "threat model"
- "threagile"
- "security analysis"
- "risk assessment"
- "threat assessment"
- "security threats"
- "vulnerability analysis"

### Example Queries

```text
Generate a threat model for the customer portal
Create a Threagile analysis for the payment API
Perform threat modeling for our e-commerce system
Security analysis of the mobile banking app
```

## Configuration

### Essential Valves

- `threat_modeling_enabled`: Enable/disable feature
- `openwebui_base_url`: Your Open WebUI instance URL
- `knowledge_base_id`: Target knowledge base (optional)

### Optional Valves

- `threat_modeling_iterations`: Max analysis cycles (default: 3)
- `ctm_docker_image`: Docker image for validation (default: ctm:local)

## Prerequisites

### Knowledge Base Content

Ensure your knowledge base contains:

- System architecture diagrams
- Component descriptions
- Data flow documentation
- Security requirements
- Network topology information

### Docker Setup

```bash
# Build ctm:local image
git clone https://github.com/Threagile/threagile.git
cd threagile
docker build -t ctm:local .
```

## Expected Output

1. **Architecture Analysis**: Extracted components and boundaries
2. **Iteration Summary**: Number of research cycles performed
3. **Validation Status**: ctm:local validation results
4. **Threagile YAML**: Generated threat model (if successful)
5. **Error Details**: Validation errors (if failed)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No knowledge base results | Check knowledge base content and ID |
| Docker validation fails | Verify ctm:local image and Docker access |
| API connection errors | Check Open WebUI URL and authentication |
| Empty threat model | Improve architecture documentation |

## Integration Pattern

```python
from threat_modeling_extension import extend_pipe_with_threat_modeling

@extend_pipe_with_threat_modeling
class Pipe:
    # Your existing implementation
    pass
```

## API Endpoints Used

- `POST /api/v1/retrieval/query/collection` - Query knowledge base
- `GET /api/v1/knowledge` - List knowledge bases

## File Structure

```text
your-pipe/
├── pipe (your main pipe file)
├── threat_modeling_extension.py
├── example_integration.py
└── THREAT_MODELING_INTEGRATION.md
```
