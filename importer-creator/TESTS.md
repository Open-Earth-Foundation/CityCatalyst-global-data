# Comprehensive Test Plan for CityCatalyst Importer-Creator

## Overview

This document outlines a comprehensive testing strategy for the importer-creator system using pytest. The plan is organized into three main categories:

1. **Individual Agent Tests** - Testing each agent in isolation
2. **Integration Tests** - Testing agent workflows and system interactions
3. **Function-by-Function Tests** - Testing utility functions and helper methods

## Test Structure

```
tests/
├── conftest.py                     # Shared fixtures and test configuration
├── unit/
│   ├── agents/
│   │   ├── test_initial_script_agents.py
│   │   ├── test_step_2_agents.py
│   │   ├── test_step_3_agents.py
│   │   ├── test_step_4_agents.py
│   │   └── test_hitl_agent.py
│   ├── utils/
│   │   ├── test_agent_creation.py
│   │   ├── test_agent_factory.py
│   │   ├── test_config_loader.py
│   │   ├── test_token_calculator.py
│   │   ├── test_vectorstore_utils.py
│   │   ├── test_data_processing_utils.py
│   │   └── test_prompt_creation.py
│   ├── state/
│   │   └── test_agent_state.py
│   └── workflow/
│       └── test_graph_definition.py
├── integration/
│   ├── test_workflow_end_to_end.py
│   ├── test_step_sequences.py
│   ├── test_hitl_workflows.py
│   └── test_error_handling.py
├── fixtures/
│   ├── sample_data/
│   │   ├── clean_csv_file.csv
│   │   ├── messy_csv_file.csv
│   │   ├── special_chars_csv.csv
│   │   └── edge_cases_csv.csv
│   └── expected_outputs/
│       ├── expected_initial_script.py
│       ├── expected_step2_output.csv
│       └── expected_final_output.csv
└── performance/
    ├── test_token_consumption.py
    ├── test_memory_usage.py
    └── test_execution_time.py
```

---

## 1. Individual Agent Tests

### 1.1 Initial Script Agents (`test_initial_script_agents.py`)

#### 1.1.1 Setup Agent Tests

- **Test input validation**

  - Valid CSV file path
  - Invalid/non-existent file path
  - Corrupted CSV file
  - Empty CSV file
  - CSV with various encodings (UTF-8, UTF-16, Latin-1)

- **Test CSV loading and processing**

  - Different separators (comma, semicolon, tab)
  - Files with/without headers
  - Files with missing values
  - Files with special characters
  - Large files (performance impact)

- **Test state management**
  - Proper state initialization
  - State updates after processing
  - Error state handling

#### 1.1.2 Delete Columns Agent Tests

- **Test column identification logic**

  - Identify empty columns
  - Identify columns with only NaN values
  - Identify columns with single unique value
  - Preserve necessary columns

- **Test column deletion scenarios**
  - Delete multiple empty columns
  - Handle case where no columns need deletion
  - Preserve data integrity after deletion
  - Update metadata correctly

#### 1.1.3 Data Types Agent Tests

- **Test data type detection**

  - Numeric columns (int, float)
  - String columns
  - Date/datetime columns
  - Boolean columns
  - Mixed type columns

- **Test data type conversion**
  - Safe type conversion
  - Handle conversion errors
  - Preserve data accuracy
  - Generate appropriate code

#### 1.1.4 Create Final Output Agent Tests

- **Test output generation**

  - Python script generation
  - CSV file creation
  - Markdown reasoning file
  - File encoding validation

- **Test code quality**
  - Syntax validation
  - Executable code generation
  - Proper import statements
  - Code documentation

#### 1.1.5 HITL Agent Initial Script Tests

- **Test human interaction**
  - Feedback collection
  - State update based on feedback
  - Continue/retry logic
  - Timeout handling

### 1.2 Step 2 Agents (`test_step_2_agents.py`)

#### 1.2.1 Extract Datasource Name Agent Tests

- **Test extraction logic**
  - Extract from user input
  - Extract from file metadata
  - Handle missing datasource information
  - Validate extracted datasource names

#### 1.2.2 Extract Emissions Year Agent Tests

- **Test year extraction patterns**
  - 4-digit years (2020, 2021)
  - Year ranges (2020-2022)
  - Multiple years in dataset
  - Missing year information

#### 1.2.3 Extract Actor Name Agent Tests

- **Test actor identification**
  - Government entities
  - Private companies
  - NGOs
  - Mixed actor types

#### 1.2.4 Extract Sector/Sub-sector Agent Tests

- **Test sector classification**
  - Energy sector
  - Transportation sector
  - Waste sector
  - Industrial processes
  - Cross-sector data

#### 1.2.5 Extract Scope Agent Tests

- **Test scope classification**
  - Scope 1 emissions
  - Scope 2 emissions
  - Scope 3 emissions
  - Mixed scopes

#### 1.2.6 Extract GPC RefNo Agent Tests

- **Test GPC reference matching**
  - Valid GPC references
  - Invalid references
  - Partial matches
  - Multiple possible matches

### 1.3 Step 3 Agents (`test_step_3_agents.py`)

#### 1.3.1 Extract Activity Name Agent Tests

- **Test activity identification**
  - Energy consumption activities
  - Transportation activities
  - Waste generation activities
  - Industrial activities

#### 1.3.2 Extract Activity Value Agent Tests

- **Test value extraction**
  - Numeric values
  - Values with units
  - Range values
  - Missing values

#### 1.3.3 Extract Activity Unit Agent Tests

- **Test unit standardization**
  - Common units (kg, tonnes, MWh)
  - Unit conversion needs
  - Inconsistent unit formats
  - Missing units

#### 1.3.4 Extract Activity Subcategory Agents Tests

- **Test subcategory classification**
  - Primary subcategories
  - Secondary subcategories
  - Nested classifications
  - Ambiguous cases

### 1.4 Step 4 Agents (`test_step_4_agents.py`)

#### 1.4.1 Extract Methodology Name Agent Tests

- **Test methodology identification**
  - IPCC methodologies
  - Custom methodologies
  - Regional methodologies
  - Method matching accuracy

#### 1.4.2 Get Emission Factor Value Agent Tests

- **Test emission factor retrieval**
  - Database lookups
  - Default values
  - Regional factors
  - Factor validation

### 1.5 HITL Agent Tests (`test_hitl_agent.py`)

#### 1.5.1 General HITL Functionality Tests

- **Test interaction patterns**
  - User feedback collection
  - State preservation
  - Workflow continuation
  - Error recovery

---

## 2. Integration Tests

### 2.1 End-to-End Workflow Tests (`test_workflow_end_to_end.py`)

#### 2.1.1 Complete Pipeline Tests

- **Test full workflow execution**
  - Initial script → Step 2 → Step 3 → Step 4
  - With HITL enabled/disabled
  - With different input file types
  - With various configuration settings

#### 2.1.2 Error Recovery Tests

- **Test resilience**
  - Agent failure recovery
  - Partial workflow completion
  - State persistence across failures
  - Rollback mechanisms

### 2.2 Step Sequence Tests (`test_step_sequences.py`)

#### 2.2.1 Sequential Agent Execution

- **Test agent chains**
  - Initial script agent sequence
  - Step 2 agent sequence
  - Step 3 agent sequence
  - Cross-step data flow

#### 2.2.2 State Propagation Tests

- **Test data flow**
  - State updates between agents
  - Data consistency
  - State validation
  - Memory management

### 2.3 HITL Workflow Tests (`test_hitl_workflows.py`)

#### 2.3.1 Human-in-the-Loop Integration

- **Test HITL scenarios**
  - User approval workflows
  - Feedback incorporation
  - Workflow branching
  - Timeout handling

### 2.4 Error Handling Tests (`test_error_handling.py`)

#### 2.4.1 System Error Scenarios

- **Test error conditions**
  - Invalid input handling
  - API failures
  - File system errors
  - Memory limitations

---

## 3. Function-by-Function Tests

### 3.1 Agent Creation Tests (`test_agent_creation.py`)

#### 3.1.1 Agent Factory Functions

- **Test agent instantiation**
  - `create_structured_output_agent()`
  - `create_coding_agent()`
  - `create_extraction_agent()`
  - Agent configuration validation

#### 3.1.2 Agent Configuration Tests

- **Test configuration handling**
  - Model selection
  - Temperature settings
  - Token limits
  - Timeout configurations

### 3.2 Agent Factory Tests (`test_agent_factory.py`)

#### 3.2.1 Factory Pattern Tests

- **Test factory methods**
  - `get_structured_output_agent()`
  - `get_coding_agent()`
  - `get_extraction_agent()`
  - Singleton behavior

### 3.3 Config Loader Tests (`test_config_loader.py`)

#### 3.3.1 Configuration Loading

- **Test config operations**
  - YAML file loading
  - Environment variable handling
  - Default value fallbacks
  - Validation logic

#### 3.3.2 Model Configuration Tests

- **Test model settings**
  - Model name resolution
  - API endpoint configuration
  - Authentication handling
  - Rate limiting settings

### 3.4 Token Calculator Tests (`test_token_calculator.py`)

#### 3.4.1 Token Counting Functions

- **Test token calculations**
  - `count_tokens()`
  - `estimate_cost()`
  - `track_usage()`
  - Model-specific counting

#### 3.4.2 Cost Estimation Tests

- **Test cost calculations**
  - Input token costs
  - Output token costs
  - Model-specific pricing
  - Usage tracking

### 3.5 Vectorstore Utils Tests (`test_vectorstore_utils.py`)

#### 3.5.1 Vectorstore Operations

- **Test vectorstore functions**
  - `create_vectorstore()`
  - `load_vectorstore()`
  - Document embedding
  - Similarity search

#### 3.5.2 Retriever Tests

- **Test retrieval functions**
  - Document retrieval
  - Similarity scoring
  - Context filtering
  - Performance optimization

### 3.6 Data Processing Utils Tests (`test_data_processing_utils.py`)

#### 3.6.1 File Processing Functions

- **Test file operations**
  - `load_csv_file()`
  - `save_csv_file()`
  - `validate_file_format()`
  - Encoding handling

#### 3.6.2 Data Validation Functions

- **Test validation logic**
  - `validate_dataframe()`
  - `check_data_quality()`
  - `identify_issues()`
  - Error reporting

### 3.7 Prompt Creation Tests (`test_prompt_creation.py`)

#### 3.7.1 Prompt Generation Functions

- **Test prompt creation**
  - `create_prompt()`
  - `create_descriptive_stats_prompt()`
  - Template rendering
  - Variable substitution

#### 3.7.2 Prompt Optimization Tests

- **Test prompt quality**
  - Token efficiency
  - Context relevance
  - Response quality
  - Template validation

### 3.8 Agent State Tests (`test_agent_state.py`)

#### 3.8.1 State Management Functions

- **Test state operations**
  - State initialization
  - State updates
  - State validation
  - Type checking

#### 3.8.2 Data Structure Tests

- **Test state structure**
  - Required fields
  - Optional fields
  - Type annotations
  - Serialization

### 3.9 Graph Definition Tests (`test_graph_definition.py`)

#### 3.9.1 Workflow Graph Functions

- **Test graph operations**
  - `create_workflow()`
  - Node addition
  - Edge creation
  - Conditional routing

#### 3.9.2 Graph Validation Tests

- **Test graph integrity**
  - Node connectivity
  - Cycle detection
  - Dead ends
  - Entry/exit points

---

## 4. Performance Tests

### 4.1 Token Consumption Tests (`test_token_consumption.py`)

#### 4.1.1 Token Usage Monitoring

- **Test token efficiency**
  - Per-agent token usage
  - Workflow total consumption
  - Optimization opportunities
  - Cost analysis

### 4.2 Memory Usage Tests (`test_memory_usage.py`)

#### 4.2.1 Memory Management

- **Test memory efficiency**
  - Memory leaks
  - Peak memory usage
  - Garbage collection
  - Large file handling

### 4.3 Execution Time Tests (`test_execution_time.py`)

#### 4.3.1 Performance Benchmarks

- **Test execution speed**
  - Per-agent timing
  - End-to-end timing
  - Bottleneck identification
  - Performance regression

---

## 5. Test Implementation Guidelines

### 5.1 Test Data Management

- **Use realistic test data**
  - Anonymized real datasets
  - Edge case scenarios
  - Various data quality levels
  - Different domain contexts

### 5.2 Mocking Strategy

- **Mock external dependencies**
  - API calls to OpenRouter
  - File system operations
  - Database connections
  - Network requests

### 5.3 Assertion Patterns

- **Comprehensive validation**
  - Output format validation
  - Data integrity checks
  - Performance assertions
  - Error condition verification

### 5.4 Test Organization

- **Logical grouping**
  - Test by functionality
  - Test by agent type
  - Test by workflow step
  - Test by error scenario

### 5.5 CI/CD Integration

- **Automated testing**
  - Pre-commit hooks
  - Pull request validation
  - Nightly regression tests
  - Performance monitoring

---

## 6. Special Considerations

### 6.1 AI Model Testing

- **Handle AI uncertainty**
  - Response variability
  - Model hallucinations
  - Context limitations
  - Deterministic testing approaches

### 6.2 File System Testing

- **Cross-platform compatibility**
  - Windows path handling
  - Unix path handling
  - Permission management
  - Temporary file cleanup

### 6.3 Configuration Testing

- **Environment variations**
  - Development vs. production
  - Different API keys
  - Model availability
  - Rate limiting

### 6.4 Error Simulation

- **Controlled failure testing**
  - Network failures
  - API rate limits
  - Invalid responses
  - Resource exhaustion

---

## 7. Test Execution Strategy

### 7.1 Test Categories

- **Unit Tests**: Fast, isolated, no external dependencies
- **Integration Tests**: Medium speed, test component interactions
- **End-to-End Tests**: Slower, test complete workflows
- **Performance Tests**: Long-running, resource monitoring

### 7.2 Test Prioritization

1. **Critical Path Tests**: Core workflow functionality
2. **Error Handling Tests**: System resilience
3. **Performance Tests**: Scalability validation
4. **Edge Case Tests**: Boundary condition handling

### 7.3 Test Environment Setup

- **Development**: Local testing with mocked dependencies
- **Staging**: Integration testing with real APIs (rate-limited)
- **Production**: Monitoring and regression testing

This comprehensive test plan ensures thorough coverage of the importer-creator system, from individual functions to complete workflows, with special attention to AI-specific challenges and real-world deployment scenarios.

