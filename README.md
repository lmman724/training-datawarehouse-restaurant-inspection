# training-datawarehouse-restaurant-inspection



## Table of Contents

- [Introduction](#Introduction)
- [Data modelling](#Datamodelling)
- [High-level design](#Highleveldesign)
- [Data transformation](#DataTransformation)
- [Dashboard](#Dashboard)
- [Reference](#Reference)

## Introduction
Restaurant inspection involves the assessment of food establishments to ensure they comply with health and safety regulations. Inspections are conducted by regulatory bodies to evaluate various factors such as cleanliness, food handling practices, sanitation, and compliance with food safety standards. The collected inspection data provides valuable insights into the overall quality and compliance of restaurants.

About data: http://www1.nyc.gov/site/doh/services/restaurant-grades.page

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

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/bf94ec34-a74d-4ab0-a0ee-10f9fa9c930d)

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

## Data transformation

We have full progress pipelines in Azure Synapse

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/135b9e08-c142-4d26-b30c-f11d8aec2125)

Raw ---> Bronze: We use Synapse SparkPool

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/814b02f4-0047-4474-963c-20b00a1a2956)

Bronze ---> Stage

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/fa38c56d-ec82-476e-a1b5-e9eb3718c1ce)

Stage ---> each of dim table

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/d524f74b-50cc-4d14-8534-c989ed5f94f3)

Example: DimVolation, DimAddress

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/6d8e770c-4fa1-46d3-b260-3d9b972c587d)

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/fc008a87-5ece-4de1-a2af-137abb8f3991)

Fact table: FactRestaurant and FactRestaurantVolation

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/b9c900c7-2390-4f79-8909-1671dcaabef2)

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/2fe48ac3-4209-444b-ae8a-4f135639b452)

## Dashboard

The dashboard aims to provide valuable insights and analysis of restaurant inspections in New York City. It focuses on two key components:

Top Restaurants:

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/b7816268-1bd6-49a7-9385-6250d60534c3)

This section highlights the top-performing restaurants based on their inspection scores or grades.
The dashboard identifies and recognizes establishments that consistently maintain high standards.
Users can easily identify the restaurants that have excelled in maintaining cleanliness and adhering to food safety regulations.

Overall Restaurant Grades:

This section presents a visual representation of restaurant grades across different areas of New York City.
Users can explore the distribution of grades through interactive charts, such as bar charts or maps.
It offers a comprehensive overview of how restaurants are performing in various neighborhoods or boroughs.
This information helps consumers make informed choices about dining options based on the overall hygiene and compliance standards.

![image](https://github.com/lmman724/training-datawarehouse-restaurant-inspection/assets/70752409/756fc84c-3b67-4f31-af14-0bcb53395fa3)

The dashboard provides comprehensive trend analysis and performance evaluation of restaurant inspections in New York City. It focuses on two key areas:

Trend Analysis:

This section showcases the trends in inspection scores or violation counts over time.
Users can visualize and analyze the data to identify any improvements or patterns in compliance.
It enables stakeholders to gain insights into the overall performance of restaurants in terms of maintaining hygiene and following food safety regulations.
Users can track the progress of inspection scores or violation counts and identify areas that require attention or further improvement.
Inspector Performance:

This section evaluates the performance of inspectors by analyzing their inspection outcomes.
Users can assess and compare the findings of different inspectors to identify any variations or discrepancies in their evaluations.
It provides insights into the consistency and accuracy of inspection reports.
This information is valuable for identifying training needs, ensuring standardization in inspection processes, and enhancing overall quality control.

## Reference
http://www1.nyc.gov/site/doh/services/restaurant-grades.page
https://azure.microsoft.com/en-au/products/synapse-analytics/
https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/

