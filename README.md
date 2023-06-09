# training-datawarehouse-restaurant-inspection



## Table of Contents

- [Introduction](#Introduction)
- [Data modelling](#Datamodelling)
- [High-level design](#Highleveldesign)
- [Dashboard](#Dashboard)
- [Reference](#Reference)

## Introduction
Restaurant inspection involves the assessment of food establishments to ensure they comply with health and safety regulations. Inspections are conducted by regulatory bodies to evaluate various factors such as cleanliness, food handling practices, sanitation, and compliance with food safety standards. The collected inspection data provides valuable insights into the overall quality and compliance of restaurants.

Applying Restaurant Inspection in a Data Warehouse:

1. Data Integration:
    - Extract: We will extract restaurant inspection data from various sources such as government databases, API feeds, or CSV files. Azure Synapse can be used to automate and schedule data extraction processes.
    - Transform: The extracted data will undergo transformations to standardize formats, clean inconsistencies, and enrich with additional information if required. Azure Data Factory or Azure Synapse can be leveraged for data transformation tasks.
    - Load: The transformed data will be loaded into the data warehouse for further processing and analysis. Azure Synapse Analytics can serve as our data warehouse storage solution.
2. Data Modeling:
    - Designing Dimensional Model: We will design a dimensional model to represent restaurant inspection data effectively. Dimensions such as time, location, cuisine, and inspection type can be identified, along with fact tables representing inspection details.
    - Establishing Relationships: Relationships between dimension and fact tables will be defined to enable data analysis and querying. This will allow us to slice and dice the data based on various dimensions.
3. Data Processing and Analysis:
    - Aggregating Data: We can aggregate inspection data at different levels of granularity (e.g., daily, monthly, by location, or cuisine) to facilitate trend analysis and reporting.
    - Performing Advanced Analytics: Azure Synapse can be utilized to perform advanced analytics on the inspection data. Techniques like predictive modeling or anomaly detection can help identify patterns, trends, and potential risks in restaurant inspections.
    - Generating Reports and Dashboards: Power BI can be integrated with the data warehouse to create interactive dashboards and reports. These visualizations will enable stakeholders to monitor inspection results, identify areas of improvement, and make data-driven decisions.

## Data modelling
In this project, we are utilizing dimensional data modeling for the batching workload. Dimensional data modeling is a technique specifically designed to create databases that enable efficient data analysis and reporting.

Within dimensional data modeling, we organize the data into two primary types of tables: fact tables and dimension tables.

Fact tables store numerical and measurable data, often referred to as metrics or measures, representing business events or transactions. These tables typically contain quantitative data that organizations analyze, such as sales figures, quantities, or durations. Fact tables serve as the central point for analysis and are associated with specific business processes or events. In this project, we have one fact tables:'fact_restaurant_inspection_violations.'

fact_restaurant_inspection:

- This table contains information about restaurant inspections.
- Columns:
    - inspection_key: Unique identifier for each inspection.
    - inspection_date_key: Foreign key referencing the DimDate table for the inspection date.
    - inspection_type_key: Foreign key referencing the DimInspectionType table for the inspection type.
    - cuisine_description_key: Foreign key referencing the DimCuisine table for the cuisine description.
    - borough_key: Foreign key referencing the DimAddress table for the borough.
    - count_of_restaurant: Count of restaurants inspected.
    - created_date: Date when the inspection information was created.

Dimension tables provide context and descriptive information about the data in the fact tables (fact_restaurant_inspection_violations). They contain attributes or characteristics that help categorize, filter, and provide context to the metrics in the fact tables. For this project, we have nine dimension tables.

1. DimRestaurantPlaces:
    - This table contains information about restaurants.
    - Columns:
        - restaurant_key: Unique identifier for each restaurant.
        - restaurant_id: Identifier for the restaurant.
        - restaurant_name: Name of the restaurant.
        - phone: Phone number of the restaurant.
        - address_key: Foreign key referencing the DimAddress table for the restaurant's address.
        - cuisine_description_key: Foreign key referencing the DimCuisine table for the cuisine description.
        - created_date: Date when the restaurant information was created.
        - end_date: Date when the restaurant information is no longer valid.
        - is_current: Flag indicating if the restaurant information is current.
        - batch_id: Identifier for the batch of data.
2. DimCuisine:
    - This table contains information about cuisines.
    - Columns:
        - cuisine_description_key: Unique identifier for each cuisine description.
        - cuisine_description: Description of the cuisine.
        - created_date: Date when the cuisine information was created.
3. DimDate:
    - This table contains information about dates.
    - Columns:
        - date_key: Unique identifier for each date.
        - date_id: Date value.
        - day_of_month: Day of the month.
        - day_of_week: Day of the week.
        - day_name: Name of the day.
        - month_of_year: Month of the year.
        - month_name: Name of the month.
        - quarter: Quarter of the year.
        - year: Year.
4. DimAddress:
    - This table contains information about addresses.
    - Columns:
        - address_key: Unique identifier for each address.
        - boro: Borough of the address.
        - building: Building number.
        - street: Street name.
        - zipcode: ZIP code.
        - latitude: Latitude coordinate.
        - longitude: Longitude coordinate.
        - community_board: Community board number.
        - council_district: Council district number.
        - created_date: Date when the address information was created.
5. DimViolation:
    - This table contains information about violations.
    - Columns:
        - violation_key: Unique identifier for each violation.
        - violation_id: Identifier for the violation.
        - violation_description: Description of the violation.
        - created_date: Date when the violation information was created.
        - end_date: Date when the violation information is no longer valid.
        - is_current: Flag indicating if the violation information is current.
6. DimInspectionAction:
    - This table contains information about inspection actions.
    - Columns:
        - inspection_action_key: Unique identifier for each inspection action.
        - inspection_action: Action taken during an inspection.
        - created_date: Date when the inspection action information was created.
7. DimInspectionType:
    - This table contains information about inspection types.
    - Columns:
        - inspection_type_key: Unique identifier for each inspection type.
        - inspection_type: Type of inspection.
        - created_date: Date when the inspection type information was created.
8. DimInspectionGrade:
    - This table contains information about inspection grades.
    - Columns:
        - inspection_grade_key: Unique identifier for each inspection grade.
        - inspection_grade: Grade assigned during an inspection.
        - created_date: Date when the inspection grade information was created.
9. DimCriticalFlag:
    - This table contains information about critical flags.
    - Columns:
        - critical_flag_key: Unique identifier for each critical flag.
        - critical_flag: Flag indicating the criticality of an inspection.
        - created_date: Date when the critical flag information was created.

Each dimension table serves as a lookup table providing additional information about specific attributes related to the restaurant inspections. These tables can be joined with the fact table (fact_restaurant_inspection_violations).
## High-level design
![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/4526638a-68b2-4c5d-9890-9dc9d72f40c5)
In this system, we have three data sources, including both streaming and batching methods: SQL Server, internal data streaming system, and an API. All of these sources are located within our on-premises system.

For the batching workload, we will be working with two data sources: SQL Server and the API. To transform and store the data efficiently, we will leverage Azure Synapse and utilize Azure Data Lake for data storage.

Regarding the streaming workload, we will ingest data into Azure EventHub from our internal data streaming system. To process and analyze this streaming data, we will employ Azure Streaming Analytics and Analytic services.

Once the data is transformed, the resulting data will be stored in Azure Synapse Dedicated. Users will have the ability to connect to Synapse using Power BI, enabling them to query and analyze the data seamlessly.
## Dashboard

##Reference
http://www1.nyc.gov/site/doh/services/restaurant-grades.page
https://azure.microsoft.com/en-au/products/synapse-analytics/
https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/

