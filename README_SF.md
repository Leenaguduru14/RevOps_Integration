# RunPod Data Warehouse Project

## Overview

This project aims to integrate data from HubSpot and our Business Logic Database (Snowflake) to improve visibility into the sales pipeline and customer spending patterns. The integration involves creating a comprehensive data warehouse that enables efficient querying and reporting.

## Data Model

### Schema Structure

1. **DW_STAGE**: Staging area for raw data imported from HubSpot.
2. **DW**: Core data warehouse containing fact and dimension tables.
3. **RPT_DW**: Reporting layer with views tailored for specific business analyses and reporting.

### Data Flow

1. **DW_STAGE**: Raw data from HubSpot is imported into staging tables.
2. **DW**: Fact and dimension tables are created from the staging tables to form the core data warehouse.
3. **RPT_DW**: Reporting views are created from the fact and dimension tables for business analysis.

## Relationships

### Fact Tables

1. **FACT_TRANSACTIONS**:
   - Links to `DIM_USER` via `USER_ID`
   - Links to `DIM_TEAM` via `TEAM_ID`
   - Links to `DIM_DATE` via `DATE_ID`

2. **FACT_COMPANY_SPEND**:
   - Links to `DIM_COMPANY` via `COMPANY_ID`
   - Links to `DIM_DATE` via `DATE_ID`

### Dimension Tables

1. **DIM_USER**: Contains user details.
2. **DIM_COMPANY**: Contains company details.
3. **DIM_TEAM**: Contains team details.
4. **DIM_DATE**: Contains date details.
5. **DIM_DEAL**: Contains deal details.

## Data Model Explanation

### DW_STAGE Schema

The `DW_STAGE` schema holds the raw data imported from HubSpot. This data is then transformed and loaded into the core data warehouse (`DW`).

### DW Schema

The `DW` schema forms the core of the data warehouse. It contains the following tables:

1. **Fact Tables**:
   - `FACT_TRANSACTIONS`: Stores transaction data linked to users, teams, and dates.
   - `FACT_COMPANY_SPEND`: Stores company spending data linked to companies and dates.

2. **Dimension Tables**:
   - `DIM_USER`: Stores user details.
   - `DIM_COMPANY`: Stores company details.
   - `DIM_TEAM`: Stores team details.
   - `DIM_DATE`: Stores date details.
   - `DIM_DEAL`: Stores deal details.

### RPT_DW Schema

The `RPT_DW` schema is designed for reporting purposes. It contains views that aggregate and analyze data from the `DW` schema to provide insights into customer behavior, company spending patterns, deal performance, and team effectiveness.

## Views in RPT_DW

1. **VW_CONTACT_ANALYSIS**:
   - Provides comprehensive contact analysis, including lifetime spend and associated company details.

2. **VW_COMPANY_ANALYSIS**:
   - Aggregates spending data at the company level and includes spend trends over time.

3. **VW_DEAL_ANALYSIS**:
   - Provides detailed deal performance information, including deal stages, conversion rates, and average time between stages.

4. **VW_TEAM_ANALYSIS**:
   - Aggregates transaction data by team and includes performance trends over time.


## Setup and Running Instructions

1. **Set up Snowflake**:
   - Log in to your Snowflake instance and create the necessary schemas: `DW_STAGE`, `DW`, and `RPT_DW`.

2. **Load Data into DW_STAGE**:
   - Use the `PUT` command in Snowflake to upload raw data files to the `DW_STAGE` schema.

3. **Create Fact and Dimension Tables in DW**:
   - Execute the provided SQL scripts to create the fact and dimension tables in the `DW` schema.

4. **Create Reporting Views in RPT_DW**:
   - Execute the provided SQL scripts to create the views in the `RPT_DW` schema for reporting purposes.

## Assumptions

- The raw data from HubSpot is accurately formatted and uploaded to `DW_STAGE`.
- Snowflake instance is properly configured and accessible.
- The provided SQL scripts are executed in the correct sequence.

## Conclusion

This README provides a high-level overview of the data model, relationships, and data flow for the RunPod RevOps Data Integration Project. By following the setup and running instructions, you can integrate data from HubSpot and Snowflake to improve visibility into the sales pipeline and customer spending patterns, ultimately enhancing business decision-making.
