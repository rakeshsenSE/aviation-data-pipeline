# ✈️ Real-Time Flight Tracking, Weather Analysis & News Alert Pipeline

<p align="center">
  <b>Live Flight Tracking, Weather Analysis, and Delay Monitoring Dashboard.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" />
</p>
---

---

## 🚀 About The Project
This project is an end-to-end automated data engineering and analytics pipeline designed to fetch, process, and store live flight telemetry data alongside real-time meteorological metrics and aviation news alerts. The ingested data powers an interactive Streamlit dashboard for monitoring flight statuses, weather conditions, and breaking news alerts in real-time.

The live flight telemetry data collected by our automated pipeline is also hosted publicly on Kaggle [Link Here] for open-source analysis and visualization.

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python
* **Database & ORM:** MySQL, SQLAlchemy, `mysql-connector-python`
* **Data Processing:** Pandas, NumPy
* **APIs & Data Ingestion:** OpenSky Network API, OpenWeatherMap API, Google News RSS (`feedparser`)
* **Dashboard & UI:** Streamlit

---

<details>
<summary>📸 <b>Click here to view Dashboard Screenshots</b></summary>
<br>

![1. Overview Dashboard](<img width="1917" height="908" alt="Screenshot 2026-11-08 013507" src="https://github.com/user-attachments/assets/4336dda6-0bf7-46ae-afcf-16295e96dfd6" />
)
*Figure 1: Dashboard Overview & Key Metrics*

![2. AI Analyst Query](<img width="1917" height="902" alt="Screenshot 2026-11-08 014008" src="https://github.com/user-attachments/assets/95ddceb9-3fc4-4d76-9e43-40d72e7188d7" />
)
*Figure 2: Text-to-SQL AI Assistant*

![3. Live Map](<img width="1917" height="912" alt="Screenshot 2026-11-08 013623" src="https://github.com/user-attachments/assets/60792190-b953-4d31-ac11-1893cdfa60fb" />
)
*Figure 3: Geographical Distribution Map*

![4. Time Series Trend](<img width="1917" height="883" alt="Screenshot 2026-11-08 014715" src="https://github.com/user-attachments/assets/3ebe8132-4ec7-434e-b4dd-daddd5236b68" />
)
*Figure 4: Time-based Flight Activity Trend*

![5. News & Alerts](<img width="1871" height="905" alt="Screenshot 2026-11-08 014425" src="https://github.com/user-attachments/assets/0284fcf4-a32c-40c0-a59d-d05ba6b76b5b" />
)
*Figure 5: Real-time Aviation News Feed*

</details>

---

## ⚙️ Key Features
1. **Automated Data Ingestion:** Background loops to periodically fetch and sync live flight paths, weather conditions, and news alerts into a structured MySQL database.
2. **Data Cleaning & Transformation:** Handles missing coordinates, null values, and data type formatting before storing into relational tables (`flights`, `weather`, `news_alerts`).
3. **Interactive Dashboard:** Built with Streamlit to visualize movements, atmospheric metrics, and automated alerts.
4. **Public Datasets:** Telemetry data logs are regularly exported and published openly on Kaggle.

---
## 🏗️ System Architecture

```text
 ┌────────────────┐     ┌──────────────────┐     ┌───────────────────┐
 │ OpenSky API    │     │ OpenWeather API  │     │ Google News RSS   │
 └───────┬────────┘     └────────┬─────────┘     └─────────┬─────────┘
         │                       │                         │
         └───────────────┬───────┴─────────────────────────┘
                         ▼
             ┌───────────────────────┐
             │ Automated Pipeline    │ (Data Cleaning & Transformation)
             └───────────┬───────────┘
                         ▼
             ┌───────────────────────┐
             │ MY SQL Database Engine │ (Relational Schema Storage)
             └───────────┬───────────┘
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌──────────────┐                 ┌─────────────────┐
│ Streamlit UI │                 │  AI Assistant   │ (Google Gemini SDK)
└──────────────┘                 └─────────────────┘
```
## 👨‍💻 Author & License

**Rakesh Sen

** GitHub: @rakeshsenSE

** Public Dataset: [Kaggle Dataset Profile](https://www.kaggle.com/datasets/rakeshsen00/real-time-live-flight-and-aviation-tracking-dataset)

** Distributed under the MIT License / CC0: Public Domain.

## 📂 Project Structure
```text
📦 Flight Pulse
 ┣ 📜 main_pipeline.py       # Automated data fetcher & MySQL sync script
 ┣ 📜 app.py                 # Streamlit interactive dashboard application
 ┣ 📂 data                   # Exported CSV data logs (e.g., Live_Flight_data.csv)
 ┣ 📜 requirements.txt       # Project dependencies
 ┗ 📜 README.md              # Project documentation
