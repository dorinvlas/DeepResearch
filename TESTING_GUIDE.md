# Testing Guide: DeepResearch Enhanced Threat Modeling Function

## Deployment and Testing Instructions

### Prerequisites

1. **OpenWebUI Running**: Ensure OpenWebUI is running on `localhost:3003`
   ```bash
   docker ps | grep open-webui
   ```

2. **Required Docker Images**: Ensure `ctm:local` is available for Threagile validation
   ```bash
   docker images | grep ctm
   ```

3. **Python Dependencies**: Install required packages
   ```bash
   pip install requests aiohttp pyyaml
   ```

### Step 1: Deploy the Function

1. **Run the deployment script**:
   ```bash
   python deploy_to_openwebui.py
   ```

2. **Alternative manual deployment** via curl:
   ```bash
   curl -X POST http://localhost:3003/api/v1/functions \
        -H "Content-Type: application/json" \
        -d @function_payload.json
   ```

### Step 2: Monitor OpenWebUI Logs

Open a terminal and start monitoring OpenWebUI logs:
```bash
docker logs -f open-webui
```

Look for log entries from our function:
- `DeepResearch-ThreatModeling` logger entries
- Function initialization messages
- Processing request logs
- Error messages with stack traces

### Step 3: Test Function Availability

1. **Check function list** via API:
   ```bash
   curl http://localhost:3003/api/v1/functions
   ```

2. **Look for our function** in the OpenWebUI interface:
   - Go to http://localhost:3003
   - Navigate to Functions section
   - Look for "DeepResearch Enhanced Threat Modeling"

### Step 4: Test Threat Modeling Functionality

#### Test Case 1: Basic Threat Modeling Query
```
Generate a threat model for my e-commerce web application
```

**Expected Response:**
- Function detects threat modeling keywords
- Displays discovery summary
- Shows architecture components discovered
- Generates Threagile YAML preview
- Provides learning summary

#### Test Case 2: Specific System Query
```
Create a Threagile analysis for a microservices-based payment system with API gateway
```

**Expected Response:**
- Enhanced discovery process triggered
- Multiple asset types identified
- Confidence scores displayed
- Validation status shown

#### Test Case 3: Non-Threat Modeling Query
```
Research the latest cybersecurity trends in 2024
```

**Expected Response:**
- Function detects this is NOT a threat modeling query
- Provides general research summary
- Explains current prototype limitations

### Step 5: Monitoring and Debugging

#### Log Patterns to Watch For

**Successful Function Execution:**
```
DeepResearch-ThreatModeling - INFO - DeepResearch Enhanced Threat Modeling Function initialized
DeepResearch-ThreatModeling - INFO - Processing request: Generate a threat model...
DeepResearch-ThreatModeling - INFO - Threat modeling request detected
DeepResearch-ThreatModeling - INFO - Starting enhanced threat modeling process
DeepResearch-ThreatModeling - INFO - Processing threat modeling with enhanced discovery
DeepResearch-ThreatModeling - INFO - Starting enhanced discovery process
DeepResearch-ThreatModeling - INFO - Threat modeling completed successfully
```

**Error Patterns:**
```
DeepResearch-ThreatModeling - ERROR - Error processing request: [error details]
DeepResearch-ThreatModeling - ERROR - Threat modeling failed: [error details]
```

#### Common Issues and Solutions

1. **Function Not Found Error**
   - Check if deployment was successful
   - Verify function ID matches: `deepresearch_threat_modeling`
   - Restart OpenWebUI if needed

2. **Import Errors**
   - Ensure all required packages are installed in OpenWebUI environment
   - Check Docker container has necessary Python packages

3. **Configuration Errors**
   - Verify valve parameters are set correctly
   - Check OpenWebUI base URL configuration
   - Ensure knowledge base ID is configured (if using)

### Step 6: Advanced Testing

#### Configuration Testing

1. **Enable Debug Mode**:
   - Set `DEBUG_MODE: true` in function valves
   - Set `LOG_LEVEL: "DEBUG"` for verbose logging

2. **Test Different Confidence Thresholds**:
   - Modify `CONFIDENCE_THRESHOLD` (0.5, 0.7, 0.9)
   - Observe how it affects discovery behavior

3. **Test Learning Persistence**:
   - Run multiple threat modeling sessions
   - Check if `/tmp/threat_modeling_learning.pkl` is created
   - Verify learning data persists between sessions

#### Performance Testing

1. **Response Time Testing**:
   ```bash
   time curl -X POST http://localhost:3003/api/v1/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Generate threat model for web app", "function": "deepresearch_threat_modeling"}'
   ```

2. **Concurrent Request Testing**:
   ```bash
   # Run multiple parallel requests
   for i in {1..3}; do
     curl -X POST http://localhost:3003/api/v1/chat \
          -H "Content-Type: application/json" \
          -d "{\"message\": \"Threat model test $i\", \"function\": \"deepresearch_threat_modeling\"}" &
   done
   wait
   ```

### Step 7: Validation Testing

#### Threagile YAML Validation

1. **Extract generated YAML** from function response
2. **Save to file**: `test_threat_model.yaml`
3. **Validate with ctm:local**:
   ```bash
   docker run --rm -v $(pwd)/test_threat_model.yaml:/tmp/model.yaml ctm:local validate /tmp/model.yaml
   ```

#### Knowledge Base Integration Testing

1. **Prepare test knowledge base** in OpenWebUI
2. **Add architecture documentation**
3. **Set `KNOWLEDGE_BASE_ID` in function configuration**
4. **Test knowledge base queries**

### Troubleshooting Commands

#### Check OpenWebUI Status
```bash
docker ps | grep open-webui
docker logs open-webui | tail -50
```

#### Check Function Registration
```bash
curl -s http://localhost:3003/api/v1/functions | jq '.[] | select(.id=="deepresearch_threat_modeling")'
```

#### Test Function Directly
```bash
curl -X POST http://localhost:3003/api/v1/functions/deepresearch_threat_modeling/invoke \
     -H "Content-Type: application/json" \
     -d '{"message": "test threat model", "context": {}}'
```

#### Debug Learning File
```bash
ls -la /tmp/threat_modeling_learning.pkl
python3 -c "import pickle; print(pickle.load(open('/tmp/threat_modeling_learning.pkl', 'rb')))"
```

### Expected Test Results

#### Successful Threat Modeling Response Format:
```markdown
# 🔒 Enhanced Threat Modeling Results

## 📊 Discovery Summary
- **Iterations**: 1
- **User Interactions**: 0
- **Overall Confidence**: 0.75

## 🏗️ Architecture Components Discovered
- **Technical Assets**: 1
- **Trust Boundaries**: 1
- **Data Assets**: 1
- **Communication Links**: 0

## ✅ Validation Status
- **Threagile YAML**: Valid
- **Docker Validation**: Passed

## 🧠 Learning Summary
- **Successful Queries**: 5
- **Failed Queries**: 1
- **Learned Patterns**: 5
- **User Corrections**: 0

## 📋 Generated Threagile YAML (Preview)
```yaml
threagile_version: 1.0.0
title: Generated Threat Model - Prototype
...
```

## 🎯 Next Steps
1. Review the discovered architecture components
2. Validate the generated Threagile YAML
3. Refine any low-confidence findings
4. Deploy the threat model using ctm:local
```

### Success Criteria

✅ **Function Deploys Successfully**: No errors during deployment
✅ **Function Appears in OpenWebUI**: Visible in functions list
✅ **Threat Modeling Detection Works**: Correctly identifies threat modeling queries
✅ **Response Generation**: Produces properly formatted threat modeling results
✅ **Logging Works**: Clear log entries in OpenWebUI logs
✅ **Error Handling**: Graceful error handling with informative messages
✅ **Configuration**: Valve parameters work correctly
✅ **Learning Persistence**: Learning data persists between sessions

This prototype validates the core threat modeling functionality and provides a foundation for the full enhanced discovery implementation.
