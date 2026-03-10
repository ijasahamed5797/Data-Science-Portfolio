# 📦 Supply Chain & Logistics Analytics Dashboard

<p align="center">

<img src="https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi&logoColor=black">
<img src="https://img.shields.io/badge/Data%20Modeling-Star%20Schema-blue">
<img src="https://img.shields.io/badge/DAX-Measures-green">
<img src="https://img.shields.io/badge/Business%20Analytics-Supply%20Chain-orange">

</p>

An **interactive Power BI analytics solution** designed to monitor and optimize supply chain operations across suppliers, inventory, logistics, and customer demand.

This dashboard enables stakeholders to **identify bottlenecks, analyze supplier performance, monitor inventory levels, and evaluate shipment efficiency** through real-time visual analytics.

---

# 📌 Business Problem

Modern supply chains generate large volumes of operational data, but many organizations struggle with **limited visibility into logistics performance and inventory dynamics**.

Key challenges faced by logistics teams included:

• Limited visibility into **delivery delays and route performance**
• Difficulty identifying **underperforming suppliers**
• Poor monitoring of **inventory levels across distribution centers**
• Lack of centralized analytics for **decision making**

Without a consolidated dashboard, decision-making relied on **manual reporting and fragmented data sources**.

---

# 🎯 Project Objective

The objective of this project was to build an **interactive supply chain intelligence dashboard** that allows business users to:

• Monitor logistics performance in real time
• Track supplier reliability and delivery efficiency
• Analyze inventory levels and stock movements
• Understand revenue contributions from customers
• Identify operational bottlenecks across the supply chain

---

# 🛠 Tools & Technologies

| Category         | Tools                           |
| ---------------- | ------------------------------- |
| BI Platform      | Power BI                        |
| Data Modeling    | Star Schema                     |
| Calculations     | DAX                             |
| Data Preparation | Power Query                     |
| Data Sources     | Structured operational datasets |

---

# 🧩 Data Model

The dashboard uses a **star schema model** consisting of:

Fact tables

* Shipments
* Orders
* Inventory movements

Dimension tables

* Suppliers
* Products
* Distribution centers
* Customers
* Time

This structure enables **efficient filtering, drill-down analysis, and KPI calculations**.

---

# 📊 Dashboard Overview

## Executive Overview

<img src="dashboard_overview.png" width="900">

Provides high-level KPIs including:

• Total shipments
• Delivery performance
• Inventory levels
• Logistics efficiency metrics

---

## Supplier Performance Analysis

<img src="supplier_analysis.png" width="900">

Analyzes supplier reliability by examining:

• delivery consistency
• lead time variability
• supplier contribution to total shipments

This helps identify **top-performing and underperforming suppliers**.

---

## Inventory Analytics

<img src="inventory_analytics.png" width="900">

Tracks inventory across distribution centers and highlights:

• stock shortages
• excess inventory
• seasonal demand patterns

Supports **inventory optimization and demand planning**.

---

## Shipment & Logistics Insights

<img src="shipment_logistics.png" width="900">

Analyzes shipment routes and logistics operations to detect:

• delivery delays
• route inefficiencies
• transportation performance trends

---

## Customer Revenue Analytics

<img src="customer_revenue.png" width="900">

Evaluates customer contribution to revenue by:

• region
• product category
• order frequency

Helps identify **high-value customers and demand trends**.

---

# 🔍 Key Insights Generated

Through the dashboard analysis, several operational insights were uncovered:

• Delivery delays were concentrated in specific shipping routes
• Certain distribution centers consistently showed **inventory imbalance**
• A small group of suppliers accounted for **major shipment volumes**
• Seasonal demand spikes influenced inventory requirements
• Customer revenue distribution revealed **key high-value regions**

---

# 📈 Business Impact

The dashboard enables supply chain managers to make **data-driven operational decisions**.

Potential impact includes:

• Reduction in inventory discrepancies (~15%)
• Improved supplier performance monitoring
• Faster detection of logistics bottlenecks
• Better demand forecasting and inventory planning

---

# 📁 Project Structure

```
Supply-Chain-Logistics-PowerBI
│
├ supply_chain_dashboard.pbix
├ dashboard_overview.png
├ supplier_analysis.png
├ inventory_analytics.png
├ shipment_logistics.png
├ customer_revenue.png
└ README.md
```

---

# 🚀 How to Use

1. Download the `.pbix` file from this repository
2. Open using **Microsoft Power BI Desktop**
3. Explore interactive filters and visualizations
4. Analyze supply chain KPIs across dashboards

---

# 💡 Future Improvements

• Integration with real-time logistics APIs
• Predictive analytics for delivery delays
• Demand forecasting models for inventory planning
• Automated alerts for supply chain anomalies

---

# 📌 Summary

This project demonstrates how **business intelligence tools like Power BI can transform raw operational data into actionable supply chain insights**.

The dashboard combines **data modeling, DAX calculations, and interactive visualization** to help organizations improve logistics efficiency and support strategic decision-making.
