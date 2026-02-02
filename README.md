# V2V-BIAS Safety Lab

A Web-Based Data Analytics Platform for Bias, Privacy, and Safety Auditing in V2V Systems

# Overview

- V2V-BIAS Safety Lab is a web-based analytical auditing platform designed to evaluate dataset bias, privacy risks, and safety concerns in Vehicle-to-Vehicle (V2V) communication systems.

- The platform enables users to upload real-world datasets, perform preprocessing and exploratory data analysis, detect bias patterns, audit sensitive information, and run scenario-based safety simulations, with a specific focus on Vulnerable Road Users (VRUs) such as pedestrians and cyclists.

- This project emphasizes Responsible AI, transparency, and fairness in data-driven intelligent transportation systems.

# Problem Statement

- Datasets used in autonomous and V2V systems may unintentionally contain:

- Bias due to class imbalance or skewed distributions

- Privacy risks caused by sensitive or identifiable attributes

- Safety risks when deployed without proper scenario evaluation

- This project addresses these challenges by providing a pre-deployment analytical auditing framework.

# Key Features & Analytics
## 1. Data Ingestion & Preprocessing

- Upload CSV datasets

- Preview dataset structure

- Identify missing values and data types

- Clean and export processed datasets

## 2. Bias Detection & Analysis

- Class imbalance analysis

- Skewness and numeric bias detection

- Outlier identification

- Composite Bias Score to quantify dataset fairness

## 3. Privacy Audit

- Detection of sensitive and potentially identifiable attributes

- Privacy exposure assessment

- Risk-level classification (Safe / Exposed)

## 4. Safety Simulation Engine

- Scenario-based simulations using parameters such as:

- Vehicle speed

- Distance to VRU

- Weather conditions

- Lighting conditions

- Risk scoring and collision likelihood estimation

- Focus on pedestrian and cyclist safety

## 5. Interactive Dashboards

- Visual summaries of bias, risk, and dataset distributions

- Charts for collision risk, environment conditions, and vehicle types

- Insight-driven visualization for decision support

# Tech Stack

- Backend: Python, FastAPI

- Data Analytics: Pandas, NumPy

- Frontend: HTML, CSS, JavaScript

- Visualization: Chart.js

# Architecture / Workflow

- Dataset Upload

- Data Preprocessing & Summary

- Bias Detection & Scoring

- Privacy Audit

- Safety Simulation

- Dashboard Visualization

# Project Structure

## Backend:
- main.py – Entry point of the FastAPI application
- routers/data_ingestion.py – Handles dataset upload and validation
- routers/preprocessing.py – Performs data cleaning and summarization
- routers/bias.py – Bias detection and analysis
- routers/privacy.py – Privacy audit and PII detection
- routers/simulation.py – Collision risk simulation logic
- routers/dashboard.py – Dashboard statistics and visual metrics

## Frontend:
- home.html – Main web interface of V2V-BIAS Safety Lab
- styles.css – Dark-themed UI styling
- home.js – Frontend logic and API integration

## Datasets:
- vru.csv – Sample V2V dataset used for analysis

## Documentation:
- README.md – Project documentation

# Sample Outputs
<img width="1916" height="697" alt="Screenshot 2025-12-13 223051" src="https://github.com/user-attachments/assets/6fe8a0dc-3c45-4dae-bfcb-8188c1ce4f2f" />

<img width="1919" height="924" alt="Screenshot 2025-12-13 223631" src="https://github.com/user-attachments/assets/55b37318-3121-4b2a-a453-0fac94609469" />

<img width="1919" height="988" alt="Screenshot 2025-12-13 224226" src="https://github.com/user-attachments/assets/1ec0df84-b500-4145-b7c5-08fccfa203ff" />

<img width="1919" height="1017" alt="Screenshot 2025-12-13 225504" src="https://github.com/user-attachments/assets/d317437f-f1db-4b28-881e-711177b80951" />

<img width="1919" height="732" alt="Screenshot 2025-12-13 230338" src="https://github.com/user-attachments/assets/679fa30f-4a8f-4543-8185-043dd64b635d" />

<img width="1919" height="901" alt="Screenshot 2025-12-13 230548" src="https://github.com/user-attachments/assets/431d50ec-346d-48e7-ba25-c4feb5a05f38" />

<img width="1919" height="977" alt="Screenshot 2025-12-13 230816" src="https://github.com/user-attachments/assets/43ead11e-95f6-4065-96e4-dff85182700f" />

# How to Run the Project

## Prerequisites

- Python 3.8+

- pip

## Steps

- Clone the repository
git clone https://github.com/NiranjaniC/V2V-BIAS-Safety-Lab.git

- Navigate to backend
cd V2V-BIAS-Safety-Lab/backend

- Install dependencies
pip install -r requirements.txt

- Run FastAPI server
uvicorn main:app --reload

- Open the frontend (index.html) in a browser

- Access backend APIs via http://127.0.0.1:8000

# Skills Demonstrated

- Data Analytics & Exploratory Data Analysis (EDA)

- Statistical Reasoning & Metric Design

- Ethical / Responsible AI Evaluation

- Scenario-Based Risk Analysis

- Data Visualization & Insight Communication

- Backend API Development

# Impact & Relevance

- This project aligns with:

- Responsible AI principles

- UN Sustainable Development Goals

- Ethical deployment of intelligent transportation systems

- It demonstrates how data analytics can be used beyond prediction — for fairness, safety, and trust.

# Future Enhancements

- Integration with larger real-world datasets

- Advanced bias metrics (fairness indicators)

- Role-based access and authentication

- Live deployment and real-time data streams
