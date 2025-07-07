# 🌍 CityCatalyst Data Importer - User Stories

## 📋 Overview

The CityCatalyst Data Importer is an AI-powered tool that transforms raw environmental data into standardized greenhouse gas emission inventories following the Global Protocol for Community-Scale (GPC) standards.

---

## 👥 User Personas

### 🔬 **Dr. Elena Rodriguez** - Environmental Data Scientist

- **Role**: Climate researcher working with municipal emissions data
- **Goals**: Transform diverse city data sources into standardized GPC format for emissions reporting
- **Pain Points**: Manual data cleaning takes weeks, inconsistent data formats across cities

### 🏛️ **Marcus Thompson** - City Sustainability Manager

- **Role**: Municipal official responsible for carbon reporting
- **Goals**: Submit accurate emissions inventory to C40 Cities network
- **Pain Points**: Limited technical expertise, tight reporting deadlines

### 📊 **Sarah Kim** - Environmental Consultant

- **Role**: Processes emissions data for multiple clients
- **Goals**: Efficiently transform client data into reporting-ready format
- **Pain Points**: Each dataset requires custom processing, quality control is time-consuming

---

## 🔄 User Journey: From Raw Data to Standardized Emissions Inventory

### **Story 1: The Environmental Data Scientist** 🔬

**Workflow Visualization:**

```
📁 Raw CSV Data
    ↓
🚀 Launch Importer
    ↓
🤖 AI Data Cleaning
    ↓
📊 Environmental Field Extraction
    ↓
🎯 Activity Mapping
    ↓
📈 Methodology Assignment
    ↓
✅ Standardized GPC Dataset
```

**As Dr. Elena Rodriguez, I want to:**

#### 📥 **Step 1: Data Input**

> _"I have a CSV file with Buenos Aires energy consumption data that needs to be transformed into GPC format"_

**User Action:**

```bash
python transform_script.py --input-file buenos_aires_energy.csv --datasource-name "Buenos Aires Energy Ministry" --user-input "Municipal energy consumption data for residential and commercial sectors, 2015-2023"
```

**What happens:**

- 🔍 AI analyzes the raw data structure
- 📝 Creates initial data cleaning script
- 🧹 Normalizes column names and removes whitespace

---

#### 🔧 **Step 2: Smart Data Cleaning**

> _"The AI identifies and removes unnecessary columns while preserving emission-relevant data"_

**AI Agent Actions:**

- ❌ **Delete Columns Agent**: Removes irrelevant columns (e.g., internal IDs, administrative codes)
- 🏗️ **Data Types Agent**: Converts text numbers to numeric, standardizes date formats
- 📋 **Setup Agent**: Creates clean, normalized dataset structure

**Output:**

```
✅ Generated: 1_initially.py (Python script)
✅ Generated: 1_initially.csv (Cleaned data)
✅ Generated: 1_initially.md (AI reasoning documentation)
```

---

#### 🌍 **Step 3: Environmental Context Extraction**

> _"Multiple AI agents work together to extract standardized environmental fields"_

**Sequential AI Processing:**

1. **🏢 Datasource Agent**: `"Buenos Aires Energy Ministry"`
2. **📅 Year Agent**: Extracts `"2023"` from temporal data
3. **🎯 Actor Agent**: Identifies `"City of Buenos Aires"`
4. **🏭 Sector Agent**: Maps to `"Stationary Energy"`
5. **⚡ Sub-sector Agent**: Identifies `"Residential Buildings"`
6. **🎯 Scope Agent**: Assigns `"Scope 1"` or `"Scope 2"`
7. **📊 GPC Reference Agent**: Maps to `"I.1.1"` (residential energy)

**Workflow:**

```
Raw Data → 🤖 Datasource → 🤖 Year → 🤖 Actor → 🤖 Sector → 🤖 Sub-sector → 🤖 Scope → 🤖 GPC Ref → Structured Data
```

---

#### 🎯 **Step 4: Activity Data Mapping**

> _"AI maps energy consumption activities to standardized GPC categories"_

**AI Agents Extract:**

- 📋 **Activity Name**: `"Electricity consumption in residential buildings"`
- 📊 **Activity Value**: Numerical consumption data
- 📏 **Activity Unit**: `"MWh"` (standardized units)
- 🏗️ **Subcategories**: `"Single-family homes"`, `"Multi-family buildings"`

**Smart Mapping:**

```
Raw: "Residential Power Usage" → GPC: "Electricity consumption in residential buildings"
Raw: "kW/hour" → Standardized: "MWh"
```

---

#### 🔬 **Step 5: Methodology & Emission Factors**

> _"AI assigns appropriate calculation methodologies and emission factors"_

**Final Processing:**

- 📈 **Methodology Agent**: Assigns calculation approach (e.g., "Activity-based approach")
- ⚗️ **Emission Factor Agent**: Applies regional emission factors
- ✅ **Quality Check**: Validates data completeness and accuracy

---

### **Story 2: The City Sustainability Manager** 🏛️

**As Marcus Thompson, I want to:**

#### 🚀 **Quick Start with Human-in-the-Loop**

> _"I need to submit our emissions report next week, but I'm not sure about some data interpretations"_

**Enhanced Workflow with HITL:**

```bash
python transform_script.py --input-file city_transport_data.csv --datasource-name "City Transit Authority" --user-input "Public transportation emissions data" --hitl --verbose
```

**Interactive Process:**

1. 🤖 AI processes initial data cleaning
2. ⏸️ **HITL Checkpoint**: _"Should 'Bus Route 45' be classified as 'Public Transit' or 'Commercial Transport'?"_
3. 👤 **User Input**: _"Public Transit - it's part of our municipal system"_
4. ✅ AI continues with user guidance
5. 📋 Generates compliant GPC dataset

**Benefits:**

- 🎯 Domain expertise combined with AI efficiency
- ✅ Confidence in classification decisions
- 📝 Audit trail of all decisions

---

### **Story 3: The Environmental Consultant** 📊

**As Sarah Kim, I want to:**

#### 🔄 **Batch Processing Multiple Clients**

> _"I have emissions data from 5 different cities, each with unique formats"_

**Multi-City Workflow:**

**City 1 - Mexico City:**

```bash
python transform_script.py --input-file mexico_city_waste.csv --datasource-name "Mexico City Waste Management" --user-input "Solid waste emissions data including landfill and composting facilities"
```

**City 2 - Lagos:**

```bash
python transform_script.py --input-file lagos_energy.csv --datasource-name "Lagos State Energy Board" --user-input "Commercial and industrial energy consumption data"
```

**Consistent Output Structure:**

```
📁 generated/
├── 🏙️ mexico_city/
│   ├── 📊 final_output.csv (GPC-compliant)
│   ├── 🐍 final_output.py (Reusable script)
│   └── 📝 final_output.md (Documentation)
└── 🏙️ lagos/
    ├── 📊 final_output.csv (GPC-compliant)
    ├── 🐍 final_output.py (Reusable script)
    └── 📝 final_output.md (Documentation)
```

---

## 🎯 Key User Benefits

### ⚡ **Speed & Efficiency**

- **Before**: 2-3 weeks manual processing per dataset
- **After**: 30 minutes automated transformation
- **Time Saved**: 95% reduction in processing time

### 🎯 **Accuracy & Standardization**

- **Consistent GPC Mapping**: Automated classification using standard protocols
- **Quality Assurance**: AI validates data completeness and logical consistency
- **Audit Trail**: Complete documentation of all transformation decisions

### 🔄 **Reproducibility**

- **Generated Scripts**: Reusable Python code for similar datasets
- **Version Control**: Track changes and improvements over time
- **Documentation**: AI-generated explanations for all decisions

### 🤝 **Human-AI Collaboration**

- **Domain Expertise**: Human knowledge guides AI decisions
- **Iterative Improvement**: Learn from user feedback
- **Confidence Building**: Transparent decision-making process

---

## 📈 Success Metrics

### 📊 **Quantitative Results**

- ⚡ **Processing Time**: From weeks to minutes
- 🎯 **Accuracy Rate**: 95%+ correct GPC classifications
- 🔄 **Reusability**: Generated scripts work on similar datasets
- 📝 **Documentation**: 100% of decisions documented

### 😊 **User Satisfaction**

- 🎓 **Learning Curve**: Minimal technical knowledge required
- 🔍 **Transparency**: Clear explanations for all AI decisions
- 🤝 **Collaboration**: Effective human-AI teamwork
- ✅ **Confidence**: Trust in automated results

---

## 🛠️ Technical Architecture

### 🤖 **AI Agent Pipeline**

```
📥 Input CSV → 🧹 Cleaning Agents → 🌍 Environmental Agents → 🎯 Activity Agents → 📈 Methodology Agents → 📊 GPC Output
```

### 🔄 **Workflow Stages**

#### **Phase 1: Data Preparation** 🧹

- **Setup Agent**: Load and normalize data
- **Delete Columns Agent**: Remove irrelevant fields
- **Data Types Agent**: Standardize formats
- **HITL Checkpoint**: User validation

#### **Phase 2: Environmental Context** 🌍

- **Datasource Extraction**: Identify data source
- **Temporal Extraction**: Extract emission years
- **Geographic Extraction**: Identify reporting entity
- **Sector Classification**: Map to GPC sectors
- **Scope Assignment**: Classify emission scopes

#### **Phase 3: Activity Mapping** 🎯

- **Activity Identification**: Map to GPC activities
- **Value Extraction**: Quantify activity data
- **Unit Standardization**: Convert to standard units
- **Subcategory Assignment**: Detailed classifications

#### **Phase 4: Methodology & Factors** 📈

- **Methodology Assignment**: Select calculation approach
- **Emission Factor Application**: Apply regional factors
- **Quality Validation**: Final accuracy checks

---

## 🎪 Example Transformations

### **Before Transformation** ❌

```csv
ID,Facility_Name,Year,Consumption_KWH,Type
1,"Downtown Office",2023,125000,"Commercial"
2,"Shopping Mall A",2023,890000,"Retail"
```

### **After Transformation** ✅

```csv
datasource_name,emissions_year,actor_name,sector,sub_sector,scope,gpc_refno,activity_name,activity_value,activity_unit,activity_subcategory_1,methodology_name
"City Energy Authority",2023,"City of Toronto","Stationary Energy","Commercial Buildings","Scope 2","I.2.1","Electricity consumption in commercial buildings",125000,"MWh","Office Buildings","Activity-based approach"
"City Energy Authority",2023,"City of Toronto","Stationary Energy","Commercial Buildings","Scope 2","I.2.1","Electricity consumption in commercial buildings",890000,"MWh","Retail Buildings","Activity-based approach"
```

---

## 🎯 Next Steps for Users

### 🚀 **Getting Started**

1. **Prepare Data**: Clean CSV with environmental/emissions data
2. **Run Command**: Use transform script with appropriate flags
3. **Review Output**: Check generated scripts and documentation
4. **Iterate**: Use HITL mode for complex datasets

### 📚 **Advanced Usage**

- **Custom Mappings**: Extend activity and methodology mappings
- **Batch Processing**: Process multiple datasets efficiently
- **Integration**: Incorporate into existing reporting workflows
- **Quality Control**: Validate outputs against known benchmarks

---

_Built for environmental professionals who need to transform diverse emissions data into standardized, reporting-ready formats quickly and accurately._ 🌍✨
