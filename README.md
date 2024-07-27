# RevOps Integration

## Overview
This project integrates Hubspot data sources into a unified data warehouse for reporting and analysis. It includes scripts for data extraction, transformation, and loading , as well as SQL views for reporting.

## Project Structure
- `src/`: Contains the source code for data extraction and transformation.
- `datamodel/`: Contains SQL scripts for creating views and other database objects.
- `README.md`: This file.
- [`README_SF.md`](README_Snowflake.md): Detailed documentation for Snowflake.
- `Dockerfile`: Dockerfile to build the project image.
- `docker-compose.yml`: Docker Compose file to set up services including Airflow.
- `dags/`: Directory for Airflow DAGs.

## Setup Instructions
1. **Clone the Repository**:
    ```sh
    git clone 
    cd RevOps_Integration
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
### Running Locally
1. **Run Main Script**:
    ```sh
    python src/main.py
    ```

    This script will generate a CSV file with the extracted data.

2. **Run SQL Scripts**:
    - Use Snowflake SQL client to run the scripts in the `sql/` directory, which will load the generated CSV file into Snowflake.

### Running with Docker

1. **Build Docker Image**:
    ```sh
    docker-compose build
    ```

2. **Initialize Airflow Database and Create Admin User**:
    ```sh
    docker-compose run --rm airflow-init
    ```

3. **Start Docker Containers**:
    ```sh
    docker-compose up -d
    ```

4. **Access Airflow**:
    Open your browser and go to `http://localhost:8080`. Use the credentials `admin/admin` to log in.

### Checking Logs

1. **View Logs for Webserver**:
    ```sh
    docker-compose logs webserver
    ```

2. **View Logs for Scheduler**:
    ```sh
    docker-compose logs scheduler
    ```

3. **View Logs for Postgres**:
    ```sh
    docker-compose logs postgres
    ```

### Stopping and Removing Containers

1. **Stop Docker Containers**:
    ```sh
    docker-compose down
    ```

2. **Remove All Containers, Networks, and Volumes**:
    ```sh
    docker-compose down -v
    ```

## Docker and Airflow Orchestration

- A Docker image has been created to containerize the project.



## Automation Attempts During Development

### Airbyte Integration
- Attempted to automate the data pipeline using Airbyte, which already has a source connector for HubSpot.
- Encountered issues with Snowflake authentication, preventing the Airbyte user from authenticating.
- Airbyte could be a great solution with less maintenance, as it can control incremental and full overwrite streams.

### Snowflake Python Connector
- Considered using the Snowflake Python connector to automate the full idempotent data pipeline.

## Current Approach
- The current approach uses minimal automation but includes an Airflow DAG as a placeholder to run the scripts as a DAG and automate the Snowflake part.


## Conclusion and Architectural Decisions

### Data Warehouse Design
- Structured the data warehouse in a star schema to optimize querying and reporting.

### Automation Strategy
- The current approach uses Docker and Airflow as a placeholder for future automation enhancements.

### Reporting Layer

By leveraging the structured data warehouse and the reporting layer, RunPod can significantly enhance its visibility into the sales pipeline and customer spending patterns, leading to better decision-making and improved sales performance.

This document outlines the structure, relationships, steps, and decisions involved in the data integration project, ensuring clarity and ease of understanding for anyone working with the data model.