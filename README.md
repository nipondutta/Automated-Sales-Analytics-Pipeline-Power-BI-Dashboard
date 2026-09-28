# Automated Sales Analytics Pipeline & Power BI Dashboard

An end-to-end automated sales analytics project that demonstrates how raw sales data can be extracted, transformed, loaded into PostgreSQL, and visualized through an interactive Power BI dashboard.

The project simulates a real-world data pipeline where new sales data is periodically generated, processed through an ETL pipeline, stored in PostgreSQL, and made available for business reporting.

---

## 📌 Project Overview

This project demonstrates a complete data analytics workflow:

```text
Data Source
     ↓
Python ETL Pipeline
     ↓
Extract
     ↓
Transform
     ↓
Load
     ↓
PostgreSQL
     ↓
SQL Views / Analytics Layer
     ↓
Power BI
     ↓
Interactive Dashboard
```

The pipeline can be automated using **Windows Task Scheduler**, allowing new data to be processed at predefined intervals.

The project focuses on:

* Data extraction
* Data cleaning and transformation
* PostgreSQL database management
* SQL analytics
* ETL pipeline development
* Data quality handling
* Pipeline logging
* Power BI dashboard development
* DAX measures
* Pipeline automation

---

# 🎯 Business Objective

The objective is to build a sales analytics system that allows a business to monitor:

* Total sales
* Total orders
* Total customers
* Average Order Value
* Sales trends over time
* Sales by product category
* Sales by state
* Top-performing products
* Customer sales performance
* Order status
* Quantity sold

The pipeline is designed so that when new sales data becomes available, it can automatically process and load the new records into PostgreSQL.

---

# 🛠️ Tech Stack

| Technology             | Purpose                   |
| ---------------------- | ------------------------- |
| Python                 | ETL pipeline              |
| Pandas                 | Data transformation       |
| NumPy                  | Data processing           |
| Faker                  | Simulated data generation |
| SQLAlchemy             | Database connectivity     |
| psycopg2               | PostgreSQL driver         |
| PostgreSQL             | Data storage              |
| pgAdmin                | Database management       |
| SQL                    | Data analysis and views   |
| Power BI               | Data visualization        |
| DAX                    | Business metrics          |
| Windows Task Scheduler | Pipeline automation       |
| Git                    | Version control           |
| GitHub                 | Project hosting           |

---

# 📂 Project Structure

```text
automated-sales-bi/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── pipeline/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── config/
│   └── config.py
│
├── logs/
│
├── powerbi/
│   └── SalesDashboard.pbix
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run_pipeline.bat
```

> `.env`, `.venv`, generated data, and logs should be excluded from GitHub using `.gitignore`.

---

# 🔄 ETL Pipeline

## 1. Extract

The extraction layer simulates incoming sales data using Python and Faker.

The pipeline generates:

* Customers
* Products
* Orders
* Order Items

The generated raw data is stored as CSV files in:

```text
data/raw/
```

Example:

```text
customers.csv
products.csv
orders.csv
order_items.csv
```

---

## 2. Transform

The transformation layer cleans and validates the extracted data.

### Customer transformations

* Remove duplicate customer IDs
* Convert signup dates to datetime
* Remove records with missing customer IDs
* Remove records with missing customer names

### Product transformations

* Remove duplicate product IDs
* Convert prices to numeric values
* Remove invalid negative prices

### Order transformations

* Remove duplicate order IDs
* Convert order dates to datetime
* Validate order status
* Remove records with missing customer IDs

Valid order statuses:

```text
Completed
Pending
Cancelled
```

### Order Item transformations

* Convert quantity to numeric
* Convert unit price to numeric
* Remove duplicate order items
* Remove invalid quantities
* Remove negative prices

---

# 🗄️ PostgreSQL Database

The processed data is loaded into PostgreSQL.

The database contains the following tables:

```text
customers
products
orders
order_items
pipeline_metadata
```

### Customers

| Column        | Description                |
| ------------- | -------------------------- |
| customer_id   | Unique customer identifier |
| customer_name | Customer name              |
| city          | Customer city              |
| state         | Customer state             |
| signup_date   | Customer signup date       |

### Products

| Column       | Description               |
| ------------ | ------------------------- |
| product_id   | Unique product identifier |
| product_name | Product name              |
| category     | Product category          |
| price        | Product price             |

### Orders

| Column      | Description             |
| ----------- | ----------------------- |
| order_id    | Unique order identifier |
| customer_id | Customer identifier     |
| order_date  | Date of order           |
| status      | Order status            |
| updated_at  | Last update timestamp   |

### Order Items

| Column        | Description                  |
| ------------- | ---------------------------- |
| order_item_id | Unique order item identifier |
| order_id      | Order identifier             |
| product_id    | Product identifier           |
| quantity      | Quantity purchased           |
| unit_price    | Price per unit               |

---

# 📊 SQL Analytics Layer

A SQL view named `sales_summary` combines the transactional tables.

```sql
CREATE OR REPLACE VIEW sales_summary AS
SELECT
    o.order_id,
    o.order_date,
    o.status,
    o.customer_id,
    c.customer_name,
    c.city,
    c.state,
    p.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS sales_amount
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
INNER JOIN products p
    ON oi.product_id = p.product_id;
```

Additional analytical views include:

```text
monthly_sales
category_sales
customer_sales
```

These views provide a reporting layer between PostgreSQL and Power BI.

---

# 📈 Power BI Dashboard

The Power BI dashboard connects to PostgreSQL and provides an interactive view of sales performance.

## KPI Cards

The dashboard contains KPIs such as:

* Total Sales
* Total Orders
* Total Customers
* Total Quantity
* Average Order Value

### Total Sales

```DAX
Total Sales =
CALCULATE(
    SUM(sales_summary[sales_amount]),
    sales_summary[status] = "Completed"
)
```

### Total Orders

```DAX
Total Orders =
CALCULATE(
    DISTINCTCOUNT(sales_summary[order_id]),
    sales_summary[status] = "Completed"
)
```

### Total Customers

```DAX
Total Customers =
CALCULATE(
    DISTINCTCOUNT(sales_summary[customer_id]),
    sales_summary[status] = "Completed"
)
```

### Total Quantity

```DAX
Total Quantity =
CALCULATE(
    SUM(sales_summary[quantity]),
    sales_summary[status] = "Completed"
)
```

### Average Order Value

```DAX
Average Order Value =
DIVIDE(
    [Total Sales],
    [Total Orders]
)
```

---

# 📊 Dashboard Visualizations

The dashboard includes analysis such as:

### Sales Trend

A line chart showing:

```text
Month → Total Sales
```

### Category Performance

A bar chart showing:

```text
Category → Total Sales
```

### Geographic Analysis

Sales performance by:

```text
State
```

### Product Performance

A table showing:

* Product
* Category
* Quantity
* Sales

### Filters / Slicers

Users can filter the dashboard using:

* Order Date
* State
* Category
* Order Status

---

# ⚙️ Pipeline Automation

The pipeline can be automated using Windows Task Scheduler.

A batch file is used to execute the Python pipeline:

```bat
@echo off

cd /d "YOUR_PROJECT_PATH"

call .venv\Scripts\activate

python pipeline\pipeline.py

echo Pipeline execution completed.
```

The scheduled workflow becomes:

```text
Windows Task Scheduler
          ↓
run_pipeline.bat
          ↓
pipeline.py
          ↓
Extract
          ↓
Transform
          ↓
Load
          ↓
PostgreSQL
```

The pipeline can be configured to run periodically, for example every 30 minutes.

---

# 📝 Pipeline Logging

Pipeline execution is logged in:

```text
logs/pipeline.log
```

The logs record:

* Pipeline start
* Pipeline completion
* Extraction status
* Transformation status
* Database loading status
* Number of records loaded
* Pipeline failures

Example:

```text
PIPELINE STARTED
Starting extraction...
Extraction completed.
Starting transformation...
Transformation completed.
Starting database load...
Customers loaded: 0
Products loaded: 0
Orders loaded: 100
Order items loaded: 200
PIPELINE COMPLETED SUCCESSFULLY
```

---

# 🔐 Environment Configuration

Database credentials are stored in a `.env` file.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Automated_Sales_Analytics_Pipeline
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file should **never be committed to GitHub**.

---

# 🚫 Git Security

The `.gitignore` file should include:

```gitignore
# Virtual environment
.venv/
venv/
env/

# Environment variables
.env

# Python cache
__pycache__/
*.py[cod]

# Logs
logs/
*.log

# Generated raw data
data/raw/*.csv
data/processed/*.csv

# Jupyter
.ipynb_checkpoints/

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Power BI temporary files
*.pbit
~$*.pbix
---

# 🚀 Installation & Setup

## Prerequisites

Install the following:

* Python 3.x
* PostgreSQL
* pgAdmin
* Power BI Desktop
* Git

---

# 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/automated-sales-bi.git
```

Navigate into the project:

```bash
cd automated-sales-bi
```

---

# 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Create PostgreSQL Database

Open pgAdmin and create:

```text
Automated_Sales_Analytics_Pipeline
```

Then execute:

```text
sql/schema.sql
```

> **Warning:** `schema.sql` contains `DROP TABLE IF EXISTS` statements. Do not execute it against a database containing data that you want to keep.

---

# 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Automated_Sales_Analytics_Pipeline
DB_USER=postgres
DB_PASSWORD=your_password
```

---

# 6. Run the Pipeline

From the project root:

```powershell
python pipeline\pipeline.py
```

The pipeline will:

```text
Extract data
      ↓
Transform data
      ↓
Load data
      ↓
PostgreSQL
```

---

# 7. Verify Data in PostgreSQL

Open pgAdmin and run:

```sql
SELECT COUNT(*) FROM customers;

SELECT COUNT(*) FROM products;

SELECT COUNT(*) FROM orders;

SELECT COUNT(*) FROM order_items;
```

Check the analytical view:

```sql
SELECT *
FROM sales_summary
LIMIT 20;
```

Check monthly sales:

```sql
SELECT *
FROM monthly_sales;
```

---

# 8. Connect Power BI

Open Power BI Desktop.

Navigate to:

```text
Home
→ Get Data
→ PostgreSQL database
```

Use:

```text
Server:
localhost

Port:
5432

Database:
Automated_Sales_Analytics_Pipeline
```

Select:

```text
sales_summary
```

Load the data into Power BI.

---

# 🔄 Data Refresh Workflow

When the automated pipeline runs:

```text
New Data
   ↓
Python ETL
   ↓
PostgreSQL Updated
   ↓
Power BI Refresh
   ↓
Updated Dashboard
```

For the local portfolio implementation, Power BI Desktop requires a manual **Refresh** after PostgreSQL has been updated.

A fully unattended production implementation would typically use Power BI Service or another cloud-based BI/data platform with scheduled or event-driven refresh.

---

# 🧪 Data Quality Checks

The transformation layer performs basic data quality checks including:

* Duplicate detection
* Missing ID detection
* Invalid status detection
* Invalid quantity detection
* Negative price detection
* Date conversion
* Numeric type validation

This prevents common data-quality issues from reaching the analytics layer.

---

# 📌 Key Features

### Automated ETL

The pipeline automatically performs:

```text
Extract → Transform → Load
```

### Incremental Order Loading

The pipeline checks the existing maximum `order_id` in PostgreSQL and generates subsequent order IDs.

Example:

```text
Existing maximum order_id = 500

Next pipeline run:

Starting order_id = 501
```

This prevents previously loaded orders from being inserted again.

### Duplicate Prevention

Before inserting records, the load layer checks existing IDs.

This helps prevent duplicate:

* Customers
* Products
* Orders
* Order Items

### Error Logging

Pipeline failures are captured in:

```text
logs/pipeline.log
```

---

# 📊 Example Business Questions

The dashboard can answer questions such as:

1. What is the total completed sales?
2. How many orders were completed?
3. Which product categories generate the most revenue?
4. Which states generate the highest sales?
5. Which products have the highest sales?
6. What is the average order value?
7. How are sales changing over time?
8. How many customers have placed completed orders?
9. How much quantity has been sold?
10. What percentage of orders are completed, pending, or cancelled?

---

# 🏗️ Production Architecture

The current project uses a local environment for demonstration and portfolio purposes.

A production implementation could follow:

```text
        Data Sources
             ↓
     Cloud Data Pipeline
             ↓
      Data Lake / Storage
             ↓
       Data Warehouse
             ↓
      Transformation Layer
             ↓
     Power BI Semantic Model
             ↓
      Power BI Dashboard
---

# 📚 Skills Demonstrated

This project demonstrates practical experience in:

### Data Analytics

* Exploratory analysis
* KPI development
* Business metrics
* Data validation
* Data quality

### SQL

* Joins
* Aggregations
* Views
* Date functions
* GROUP BY
* Analytical queries

### Python

* Pandas
* Data processing
* ETL development
* File handling
* Environment variables
* Logging
* Database integration

### PostgreSQL

* Relational database design
* Primary keys
* Foreign keys
* Constraints
* Views
* SQL analytics

### Power BI

* PostgreSQL connectivity
* Data modeling
* DAX
* KPI cards
* Interactive dashboards
* Filters and slicers
* Data visualization

### Automation

* ETL automation
* Windows Task Scheduler
* Batch scripting
* Pipeline logging

---

# 👨‍💻 Author

**Nipon Kumar Dutta**

Data Analyst

Interested in:

* Data Analytics
* SQL
* Python
* Power BI
* Data Engineering
* Business Intelligence

---

# ⭐ Project Purpose

This project was developed as a portfolio project to demonstrate an end-to-end analytics workflow rather than only a static Power BI dashboard.

It combines:

```text
Python
+
SQL
+
PostgreSQL
+
ETL
+
Power BI
+
DAX
+
Automation
```

to demonstrate how raw data can be transformed into an automated business intelligence solution.
