## V2V-BIAS Safety Lab

An interactive web-based platform for bias detection, privacy auditing, simulation, and visualization in Vehicle-to-Vehicle (V2V) safety datasets.
The system helps ensure fair, ethical, and reliable decision-making in intelligent transportation systems.

## Project Overview

The V2V-BIAS Safety Lab analyzes vehicular datasets before model training to identify:

- Data bias affecting safety decisions

- Privacy risks in shared vehicular information

- Collision risk patterns involving vulnerable road users (VRUs)

The platform uses a FastAPI backend, HTML/CSS/JavaScript frontend, and local file storage instead of a database for simplicity and transparency.

## System Modules

1.Data Ingestion

2.Preprocessing

3.Bias Detection

4.Privacy Audit

5.Simulation

6.Dashboard

## Technologies Used Backend

- Python

- FastAPI

- Pandas

- NumPy

- Frontend

- HTML

- CSS

- JavaScript

- Storage

- Local File System (CSV files)

## Project Structure

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



- How to Run the Project

- Start Backend
uvicorn main:app --reload

- Open Frontend

- Open frontend/home.html in a browser
(or use Live Server in VS Code)

## Sample Outputs
<img width="1916" height="697" alt="Screenshot 2025-12-13 223051" src="https://github.com/user-attachments/assets/6fe8a0dc-3c45-4dae-bfcb-8188c1ce4f2f" />

<img width="1919" height="924" alt="Screenshot 2025-12-13 223631" src="https://github.com/user-attachments/assets/55b37318-3121-4b2a-a453-0fac94609469" />

<img width="1919" height="988" alt="Screenshot 2025-12-13 224226" src="https://github.com/user-attachments/assets/1ec0df84-b500-4145-b7c5-08fccfa203ff" />

<img width="1919" height="1017" alt="Screenshot 2025-12-13 225504" src="https://github.com/user-attachments/assets/d317437f-f1db-4b28-881e-711177b80951" />

<img width="1919" height="732" alt="Screenshot 2025-12-13 230338" src="https://github.com/user-attachments/assets/679fa30f-4a8f-4543-8185-043dd64b635d" />

<img width="1919" height="901" alt="Screenshot 2025-12-13 230548" src="https://github.com/user-attachments/assets/431d50ec-346d-48e7-ba25-c4feb5a05f38" />

<img width="1919" height="977" alt="Screenshot 2025-12-13 230816" src="https://github.com/user-attachments/assets/43ead11e-95f6-4065-96e4-dff85182700f" />

## Key Features

- Bias-aware V2V dataset analysis

- Privacy-preserving safety auditing

- Rule-based collision risk simulation

- Interactive visualization dashboard

- Modular and scalable architecture

## Future Enhancements

- Integration of real-time V2V/V2X data

- Machine learning-based bias prediction

- Explainable AI (XAI) for safety decisions

- Cloud deployment and blockchain-based data security

- Federated learning for privacy preservation
