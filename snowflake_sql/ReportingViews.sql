USE DATABASE INTERVIEW_DATA;

CREATE SCHEMA RPT_DW;

**********************************************************************************************************************************************************************

CREATE OR REPLACE VIEW INTERVIEW_DATA.RPT_DW.VW_CONTACT_ANALYSIS AS
SELECT
    dc.COMPANY_ID,
    dc.NAME AS company_name,
    dc.DOMAIN AS domain,
    dc.CREATEDAT AS company_created_at,
    dc.UPDATEDAT AS company_updated_at,
    dc.ARCHIVED,
    dc.CREATEDATE,
    dc.HS_LASTMODIFIEDDATE,
    dc.HS_OBJECT_ID,
    SUM(fcs.TOTAL_SPEND) AS total_spend,
    AVG(fcs.TOTAL_SPEND) AS avg_spend_per_transaction,
    COUNT(fcs.COMPANY_SPEND_ID) AS num_transactions,
    NTILE(5) OVER (ORDER BY SUM(fcs.TOTAL_SPEND) DESC) AS spend_quintile,
    DATE_TRUNC('month', fcs.DATE_ID) AS month,
    SUM(SUM(fcs.TOTAL_SPEND)) OVER (PARTITION BY dc.COMPANY_ID, DATE_TRUNC('month', fcs.DATE_ID)) AS monthly_spend
FROM
    INTERVIEW_DATA.DW.DIM_COMPANY dc
LEFT JOIN
    INTERVIEW_DATA.DW.FACT_COMPANY_SPEND fcs ON dc.COMPANY_ID = fcs.COMPANY_ID
GROUP BY
    dc.COMPANY_ID,
    dc.NAME,
    dc.DOMAIN,
    dc.CREATEDAT,
    dc.UPDATEDAT,
    dc.ARCHIVED,
    dc.CREATEDATE,
    dc.HS_LASTMODIFIEDDATE,
    dc.HS_OBJECT_ID,
    DATE_TRUNC('month', fcs.DATE_ID);

**********************************************************************************************************************************************************************

-- Comprehensive Company Analysis View
-- This view aggregates spending data at the company level and includes spend trends over time.

CREATE OR REPLACE VIEW INTERVIEW_DATA.RPT_DW.VW_COMPANY_ANALYSIS AS

SELECT
    dc.COMPANY_ID,
    dc.NAME AS company_name,
    dc.DOMAIN AS domain,
    dc.CREATEDAT AS company_created_at,
    dc.UPDATEDAT AS company_updated_at,
    dc.ARCHIVED,
    dc.CREATEDATE,
    dc.HS_LASTMODIFIEDDATE,
    dc.HS_OBJECT_ID,
    SUM(fcs.TOTAL_SPEND) AS total_spend,
    AVG(fcs.TOTAL_SPEND) AS avg_spend_per_transaction,
    COUNT(fcs.COMPANY_SPEND_ID) AS num_transactions,
    NTILE(5) OVER (ORDER BY SUM(fcs.TOTAL_SPEND) DESC) AS spend_quintile,
    DATE_TRUNC('month', fcs.DATE_ID) AS month,
    SUM(SUM(fcs.TOTAL_SPEND)) OVER (PARTITION BY dc.COMPANY_ID, DATE_TRUNC('month', fcs.DATE_ID)) AS monthly_spend
FROM
    INTERVIEW_DATA.DW.DIM_COMPANY dc
LEFT JOIN
    INTERVIEW_DATA.DW.FACT_COMPANY_SPEND fcs ON dc.COMPANY_ID = fcs.COMPANY_ID
GROUP BY
    dc.COMPANY_ID,
    dc.NAME,
    dc.DOMAIN,
    dc.CREATEDAT,
    dc.UPDATEDAT,
    dc.ARCHIVED,
    dc.CREATEDATE,
    dc.HS_LASTMODIFIEDDATE,
    dc.HS_OBJECT_ID,
    DATE_TRUNC('month', fcs.DATE_ID);

**********************************************************************************************************************************************************************

-- Comprehensive Team Performance Analysis View
-- This view aggregates transaction data by team and includes performance trends over time.


CREATE OR REPLACE VIEW INTERVIEW_DATA.RPT_DW.VW_TEAM_ANALYSIS AS
SELECT
    tm.TEAM_ID,
    tm.NAME AS team_name,
    tm.OWNER_ID,
    tm.CREATED_AT AS team_created_at,
    tm.UPDATED_AT AS team_updated_at,
    SUM(ft.TRANSACTION_AMOUNT) AS total_spend,
    AVG(ft.TRANSACTION_AMOUNT) AS avg_spend_per_transaction,
    COUNT(ft.TRANSACTION_ID) AS num_transactions,
    NTILE(5) OVER (ORDER BY SUM(ft.TRANSACTION_AMOUNT) DESC) AS spend_quintile,
    DATE_TRUNC('month', ft.DATE_ID) AS month,
    SUM(SUM(ft.TRANSACTION_AMOUNT)) OVER (PARTITION BY tm.TEAM_ID, DATE_TRUNC('month', ft.DATE_ID)) AS monthly_spend
FROM
    INTERVIEW_DATA.DW.DIM_TEAM tm
LEFT JOIN
    INTERVIEW_DATA.DW.FACT_TRANSACTIONS ft ON tm.TEAM_ID = ft.TEAM_ID
GROUP BY
    tm.TEAM_ID,
    tm.NAME,
    tm.OWNER_ID,
    tm.CREATED_AT,
    tm.UPDATED_AT,
    DATE_TRUNC('month', ft.DATE_ID);


**********************************************************************************************************************************************************************

--  Comprehensive Deal Analysis View
-- -This view provides detailed information on deals, their associated companies, and stages, including deal conversion rates and average time between stages

CREATE OR REPLACE VIEW INTERVIEW_DATA.RPT_DW.VW_DEAL_ANALYSIS AS
WITH StageCounts AS (
    SELECT 
        DEAL_STAGE,
        COUNT(DEAL_ID) AS num_deals
    FROM 
        INTERVIEW_DATA.DW.DIM_DEAL
    GROUP BY 
        DEAL_STAGE
),
DealDurations AS (
    SELECT 
        DEAL_ID,
        DEAL_STAGE,
        LAG(CLOSEDATE) OVER (PARTITION BY DEAL_ID ORDER BY DEAL_STAGE) AS prev_stage_date,
        CLOSEDATE,
        DATEDIFF('day', LAG(CLOSEDATE) OVER (PARTITION BY DEAL_ID ORDER BY DEAL_STAGE), CLOSEDATE) AS days_between_stages
    FROM 
        INTERVIEW_DATA.DW.DIM_DEAL
)
SELECT
    d.DEAL_ID,
    d.DEAL_NAME,
    d.DEAL_STAGE,
    d.AMOUNT,
    d.CLOSEDATE,
    d.CREATEDATE,
    d.HS_LASTMODIFIEDDATE,
    d.HS_OBJECT_ID,
    d.COMPANY_ID,
    dc.NAME AS company_name,
    dc.DOMAIN,
    dc.CREATEDAT AS company_created_at,
    dc.UPDATEDAT AS company_updated_at,
    dc.ARCHIVED,
    dc.CREATEDATE AS company_createdate,
    dc.HS_LASTMODIFIEDDATE AS company_last_modified_date,
    dc.HS_OBJECT_ID AS company_object_id,
    sc.num_deals,
    dd.days_between_stages,
    COALESCE(
        (SELECT 
            CAST(next_stage.num_deals AS FLOAT) / current_stage.num_deals 
         FROM 
            StageCounts current_stage
         LEFT JOIN 
            StageCounts next_stage ON current_stage.DEAL_STAGE + 1 = next_stage.DEAL_STAGE
         WHERE 
            current_stage.DEAL_STAGE = d.DEAL_STAGE
        ), 0) AS conversion_rate
FROM
    INTERVIEW_DATA.DW.DIM_DEAL d
LEFT JOIN
    INTERVIEW_DATA.DW.DIM_COMPANY dc ON d.COMPANY_ID = dc.COMPANY_ID
LEFT JOIN
    StageCounts sc ON d.DEAL_STAGE = sc.DEAL_STAGE
LEFT JOIN
    DealDurations dd ON d.DEAL_ID = dd.DEAL_ID AND d.DEAL_STAGE = dd.DEAL_STAGE;