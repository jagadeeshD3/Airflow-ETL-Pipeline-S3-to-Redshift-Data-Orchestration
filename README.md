# 🚀 Airflow ETL Pipeline: S3 to Redshift Data Orchestration

![Airflow](https://img.shields.io/badge/Apache%20Airflow-3.0+-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Astro](https://img.shields.io/badge/Astro%20CLI-Enabled-FF5D01?style=for-the-badge&logo=astronomer&logoColor=white)

> An end-to-end ETL pipeline orchestrated with Apache Airflow 3.0, demonstrating automated data ingestion from S3 to AWS Redshift using modern best practices and the TaskFlow API.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [DAG Workflows](#dag-workflows)
- [Configuration](#configuration)
- [Usage](#usage)
- [Monitoring & Troubleshooting](#monitoring--troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project demonstrates a production-ready ETL (Extract, Transform, Load) pipeline built with **Apache Airflow 3.0** and deployed using **Astronomer's Astro CLI**. The pipeline automates the generation of fake order data, uploads it to Amazon S3, and loads it into AWS Redshift for analytics.

### What This Project Does

1. **Generates** synthetic order data using the Faker library
2. **Extracts** data and uploads CSV files to Amazon S3
3. **Loads** data from S3 into AWS Redshift staging tables
4. **Orchestrates** the entire workflow with fault-tolerant task dependencies
5. **Monitors** pipeline execution through Airflow's web UI

## 🏗️ Architecture

![Airflow ETL Pipeline Architecture](docs/images/architecture.png)

### Pipeline Overview

The pipeline follows a four-stage automated ETL process orchestrated by Apache Airflow:

| Stage | Component | Description |
|-------|-----------|-------------|
| **1. Generate Fake Data** | Faker Library | Synthesizes realistic order data with customer info, products, pricing |
| **2. Upload to S3** | Amazon S3 | Stores CSV files in data lake with timestamped filenames |
| **3. Load to Redshift** | AWS Redshift | Copies data to staging tables using optimized COPY command |
| **4. Analytics & Reports** | Insights & BI | Data ready for analysis, dashboards, and business intelligence |

### ETL Workflow

```mermaid
graph LR
    A[Apache Airflow<br/>Astro CLI] -->|Orchestrate| B[Generate Fake Data]
    B -->|Faker Library| C[Synthetic Order Data]
    C -->|CSV Export| D[Upload to S3]
    D -->|Amazon S3<br/>CSV Files| E[Load to Redshift]
    E -->|AWS Redshift<br/>Staging Tables| F[Analytics & Reports<br/>Insights & BI]
    
    style A fill:#017CEE,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#569A31,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#FF9900,stroke:#333,stroke-width:2px,color:#fff
    style F fill:#4A90E2,stroke:#333,stroke-width:2px,color:#fff
```

### Technical Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Apache Airflow (Astro CLI)                   │
│                      Orchestrate Workflow                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────────┐
         │  Stage 1: Extract (Generate Fake Data)   │
         │  ─────────────────────────────────────    │
         │  • Faker Library generates orders         │
         │  • Pandas DataFrame transformation        │
         │  • 20 synthetic order records             │
         └───────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────────┐
         │  Stage 2: Load to S3 (Upload to S3)      │
         │  ────────────────────────────────────     │
         │  • Convert DataFrame to CSV               │
         │  • Upload to S3 bucket                    │
         │  • Path: incoming_data/orders/*.csv       │
         └───────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────────┐
         │  Stage 3: Load (Copy to Redshift)        │
         │  ──────────────────────────────────       │
         │  • S3ToRedshiftOperator                   │
         │  • COPY command execution                 │
         │  • Load to staging.stg_orders             │
         └───────────────────────────────────────────┘
                                 │
                                 ▼
         ┌───────────────────────────────────────────┐
         │  Stage 4: Analytics Ready                 │
         │  ─────────────────────────────            │
         │  • Data available for BI tools            │
         │  • Ready for transformations (dbt)        │
         │  • Insights & reporting enabled           │
         └───────────────────────────────────────────┘
```

## ✨ Features

- ✅ **Modern Airflow 3.0** with TaskFlow API and decorators
- ✅ **Astronomer Astro CLI** for local development
- ✅ **AWS Integration** with S3 and Redshift
- ✅ **Synthetic Data Generation** using Faker library
- ✅ **Idempotent Pipeline** with proper error handling
- ✅ **XCom for Task Communication** (no manual pulls needed)
- ✅ **Modular & Scalable** architecture
- ✅ **Docker-based Deployment** for consistency
- ✅ **Configurable Scheduling** (daily, hourly, cron)

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Apache Airflow 3.0** | Workflow orchestration |
| **Astronomer Astro CLI** | Local Airflow development |
| **AWS S3** | Data lake storage |
| **AWS Redshift** | Cloud data warehouse |
| **Python 3.8+** | Programming language |
| **Faker** | Synthetic data generation |
| **Pandas** | Data manipulation |
| **Docker** | Containerization |

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Docker Desktop** (running)
- **Astronomer Astro CLI** ([Installation Guide](https://docs.astronomer.io/astro/cli/install-cli))
- **AWS Account** with:
  - S3 bucket created
  - Redshift cluster/serverless configured
  - IAM credentials with appropriate permissions
- **Git** (for cloning the repository)

### AWS Permissions Required

Your AWS IAM user/role needs:
- `s3:PutObject`, `s3:GetObject` for S3
- `redshift:DescribeClusters`, `redshift-data:ExecuteStatement` for Redshift

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/airflow-s3-redshift-etl.git
cd airflow-s3-redshift-etl
```

### 2. Initialize Astro Project

```bash
# Initialize Astro (if not already done)
astro dev init

# This creates the necessary project structure
```

### 3. Install Dependencies

The dependencies are defined in `requirements.txt`:

```bash
# Dependencies will be installed automatically when you start Astro
# Verify your requirements.txt includes:
# - apache-airflow-providers-amazon
# - faker
# - pandas
```

### 4. Configure AWS Connections

#### Option A: Using Airflow UI (Recommended)

1. Start Airflow: `astro dev start`
2. Navigate to: `http://localhost:8080`
3. Login with: `admin` / `admin`
4. Go to **Admin → Connections**

**Create AWS Connection:**
- **Connection ID**: `aws_default`
- **Connection Type**: `Amazon Web Services`
- **AWS Access Key ID**: Your AWS access key
- **AWS Secret Access Key**: Your AWS secret key
- **Region Name**: `us-east-1` (or your region)

**Create Redshift Connection:**
- **Connection ID**: `redshift_conn`
- **Connection Type**: `Amazon Redshift`
- **Host**: Your Redshift endpoint
- **Database**: `staging` (or your database name)
- **Schema**: `public`
- **Login**: Your Redshift username
- **Password**: Your Redshift password
- **Port**: `5439`

#### Option B: Using Environment Variables

Add to `.env` file (not committed to Git):

```env
AIRFLOW_CONN_AWS_DEFAULT=aws://YOUR_ACCESS_KEY:YOUR_SECRET_KEY@?region_name=us-east-1
AIRFLOW_CONN_REDSHIFT_CONN=redshift://username:password@your-cluster.region.redshift.amazonaws.com:5439/staging
```

### 5. Update DAG Configuration

Edit `dags/redshift_pipeline_airflow3.py`:

```python
S3_BUCKET = 'your-actual-bucket-name'
REDSHIFT_SCHEMA = 'public'  # or 'staging'
REDSHIFT_STAGING_TABLE = 'stg_orders'
```

### 6. Create Redshift Table

Run this SQL in your Redshift query editor:

```sql
CREATE TABLE IF NOT EXISTS public.stg_orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR(50),
    product_id INTEGER,
    quantity INTEGER,
    price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    cdc_timestamp TIMESTAMP
);
```

### 7. Start Airflow

```bash
# Start the Airflow environment
astro dev start

# Stop when done
astro dev stop

# View logs
astro dev logs
```

## 📁 Project Structure

```
airflow-s3-redshift-etl/
├── dags/
│   ├── redshift_pipeline_airflow3.py    # Main ETL DAG
│   └── snowflake_query_dag_airflow3.py  # Snowflake example DAG
├── include/
│   └── helper_functions.py              # Utility functions (optional)
├── tests/
│   └── test_dags.py                     # DAG validation tests
├── plugins/
│   └── custom_operators/                # Custom operators (if any)
├── Dockerfile                           # Astro-generated Dockerfile
├── requirements.txt                     # Python dependencies
├── packages.txt                         # OS-level packages
├── airflow_settings.yaml               # Airflow configurations
├── .env                                # Environment variables (not in Git)
├── .gitignore
└── README.md
```

## 🔄 DAG Workflows

### 1. Redshift ETL Pipeline

**DAG ID**: `extract_and_load_data_to_redshift`

**Schedule**: Daily (`@daily`)

**Tasks**:
1. **start** → Empty operator marking workflow start
2. **generate_and_upload_to_s3** → Generates 20 fake orders and uploads CSV to S3
3. **copy_to_redshift** → Copies S3 data to Redshift using COPY command
4. **end** → Empty operator marking workflow completion

**Key Features**:
- Uses TaskFlow API for seamless data passing
- Automatic XCom handling between tasks
- Fault-tolerant with retries configured

### 2. Snowflake Incremental Load (Bonus)

**DAG ID**: `snowflake_incremental_load`

**Schedule**: Daily (`@daily`)

**Tasks**:
1. **start** → Workflow start marker
2. **incremental_load** → Executes Snowflake stored procedure
3. **end** → Workflow completion marker

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (never commit this):

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Redshift Configuration
REDSHIFT_HOST=your-cluster.region.redshift.amazonaws.com
REDSHIFT_DB=staging
REDSHIFT_USER=admin
REDSHIFT_PASSWORD=your_password

# S3 Configuration
S3_BUCKET=your-bucket-name
```

### Airflow Variables (Optional)

Set via UI: **Admin → Variables**

```json
{
  "s3_bucket": "your-bucket-name",
  "redshift_schema": "public",
  "num_rows": 20
}
```

## 🎮 Usage

### Running the Pipeline

1. **Access Airflow UI**: Navigate to `http://localhost:8080`
2. **Enable DAG**: Toggle the DAG switch to ON
3. **Trigger Manually**: Click the "Play" button or wait for scheduled run
4. **Monitor Progress**: Watch task colors change (gray → yellow → green)

### Viewing Logs

```bash
# All logs
astro dev logs

# Specific task logs
astro dev logs -f  # Follow mode

# Or via UI: Click task → View Logs
```

### Validating Data

**Check S3:**
```bash
aws s3 ls s3://your-bucket-name/incoming_data/orders/
```

**Check Redshift:**
```sql
SELECT COUNT(*) FROM public.stg_orders;
SELECT * FROM public.stg_orders LIMIT 10;
```

## 🐛 Monitoring & Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Connection timeout** | Verify AWS credentials and Redshift security groups |
| **Import errors** | Run `astro dev restart` to reload dependencies |
| **DAG not appearing** | Check syntax errors: `astro dev parse` |
| **S3 access denied** | Verify IAM permissions for S3 bucket |
| **Redshift COPY fails** | Check table schema matches CSV columns |

### Health Checks

```bash
# Validate DAGs
astro dev parse

# Test connections
astro dev bash
airflow connections test aws_default
airflow connections test redshift_conn
```

### Debugging

Enable detailed logging in `airflow_settings.yaml`:

```yaml
logging:
  logging_level: DEBUG
```

## 📊 Sample Output

**Generated Data (CSV)**:
```csv
order_id,customer_id,order_date,status,product_id,quantity,price,total_amount,cdc_timestamp
1,742,2024-03-15,SHIPPED,45,3,125.50,376.50,2024-03-20 10:30:45
2,231,2024-03-16,CREATED,12,1,450.00,450.00,2024-03-20 10:30:45
```

**Redshift Table**:
```sql
SELECT * FROM public.stg_orders LIMIT 3;

 order_id | customer_id | order_date | status    | product_id | quantity | price  | total_amount
----------|-------------|------------|-----------|------------|----------|--------|-------------
    1     |     742     | 2024-03-15 | SHIPPED   |     45     |    3     | 125.50 |   376.50
    2     |     231     | 2024-03-16 | CREATED   |     12     |    1     | 450.00 |   450.00
```



## 🙏 Acknowledgments

- [Apache Airflow](https://airflow.apache.org/) - Workflow orchestration platform
- [Astronomer](https://www.astronomer.io/) - Astro CLI for local development
- [Faker](https://faker.readthedocs.io/) - Synthetic data generation
- Inspired by real-world data engineering patterns


---

⭐ **Star this repo** if you found it helpful!

🚀 **Happy Data Engineering!**