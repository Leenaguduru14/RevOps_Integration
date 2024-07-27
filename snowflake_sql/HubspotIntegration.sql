USE DATABASE INTERVIEW_DATA;
CREATE SCHEMA DW_STAGE;

USE DATABASE INTERVIEW_DATA;
USE SCHEMA DW_STAGE;

-- CREATE STAGE HUBSPOT_STAGE;


-- PUT file:"F:\Github\Hubspot Integration - contacts.csv" @HUBSPOT_STAGE;

-- Created stages tried diff ways of direct intgeration with snowflake from Airbyte, Python connector, Snowsql to laod into satges but neither works because of Fiewwall



CREATE OR REPLACE TABLE DW_STAGE.CONTACTS (
    ID STRING PRIMARY KEY,
    CREATEDAT TIMESTAMP,
    UPDATEDAT TIMESTAMP,
    ARCHIVED BOOLEAN,
    CREATEDATE TIMESTAMP,
    EMAIL STRING,
    FIRSTNAME STRING,
    HS_OBJECT_ID STRING,
    LASTMODIFIEDDATE TIMESTAMP,
    LASTNAME STRING
);

COPY INTO "INTERVIEW_DATA"."DW_STAGE"."CONTACTS"
FROM '@"INTERVIEW_DATA"."DW_STAGE"."%CONTACTS"/__snowflake_temp_import_files__/'
FILES = ('contacts.csv')
FILE_FORMAT = (
    TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    DATE_FORMAT=AUTO,
    TIME_FORMAT=AUTO,
    TIMESTAMP_FORMAT=AUTO
)
ON_ERROR=ABORT_STATEMENT
PURGE=TRUE




CREATE OR REPLACE TABLE DW_STAGE.DEALS (
    ID STRING PRIMARY KEY,
    CREATEDAT TIMESTAMP,
    UPDATEDAT TIMESTAMP,
    ARCHIVED BOOLEAN,
    AMOUNT FLOAT,
    CLOSEDATE TIMESTAMP,
    CREATEDATE TIMESTAMP,
    DEALNAME STRING,
    DEALSTAGE STRING,
    HS_LASTMODIFIEDDATE TIMESTAMP,
    HS_OBJECT_ID STRING
);



COPY INTO "INTERVIEW_DATA"."DW_STAGE"."DEALS"
FROM '@"INTERVIEW_DATA"."DW_STAGE"."%DEALS"/__snowflake_temp_import_files__/'
FILES = ('deals.csv')
FILE_FORMAT = (
    TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    DATE_FORMAT=AUTO,
    TIME_FORMAT=AUTO,
    TIMESTAMP_FORMAT=AUTO
)
ON_ERROR=ABORT_STATEMENT
PURGE=TRUE


CREATE OR REPLACE TABLE DW_STAGE.COMPANIES (
    ID STRING PRIMARY KEY,
    CREATEDAT TIMESTAMP,
    UPDATEDAT TIMESTAMP,
    ARCHIVED BOOLEAN,
    CREATEDATE TIMESTAMP,
    DOMAIN STRING,
    HS_LASTMODIFIEDDATE TIMESTAMP,
    HS_OBJECT_ID STRING,
    NAME STRING
);


COPY INTO "INTERVIEW_DATA"."DW_STAGE"."COMPANIES"
FROM '@"INTERVIEW_DATA"."DW_STAGE"."%COMPANIES"/__snowflake_temp_import_files__/'
FILES = ('companies.csv')
FILE_FORMAT = (
    TYPE=CSV,
    SKIP_HEADER=1,
    FIELD_DELIMITER=',',
    TRIM_SPACE=FALSE,
    FIELD_OPTIONALLY_ENCLOSED_BY=NONE,
    REPLACE_INVALID_CHARACTERS=TRUE,
    DATE_FORMAT=AUTO,
    TIME_FORMAT=AUTO,
    TIMESTAMP_FORMAT=AUTO
)
ON_ERROR=ABORT_STATEMENT
PURGE=TRUE






