# Binance Kline Collector

A lightweight and containerized Python service that fetches candlestick (kline) data from the Binance API and stores it in a local TimescaleDB instance for efficient time-series querying, analysis, and backtesting.

## 📦 Features

- Fetches historical and real-time kline (candlestick) data from Binance
- Stores data in TimescaleDB (PostgreSQL-based time-series database)
- Supports customizable trading pairs and intervals
- Optional FastAPI interface for querying and automation
- Dockerized architecture with `docker-compose` support

## 🚀 Tech Stack

- **Python** — Data fetching and logic
- **FastAPI** — Optional RESTful API for access and automation
- **TimescaleDB** — Time-series database for storing and querying klines
- **Docker & Docker Compose** — Easy deployment and environment isolation

## 📁 Project Structure
```
binance-kline-collector/
├── app/
│ ├── fetcher.py # Binance data fetching
│ ├── models.py # SQLAlchemy models (TimescaleDB schema)
│ ├── crud.py # DB operations
│ ├── scheduler.py # Data pull scheduling
│ └── main.py # FastAPI (optional)
├── db/
│ └── init.sql # TimescaleDB initialization
├── docker/
│ ├── Dockerfile # Python service
│ └── docker-compose.yml # Services orchestration
│ └── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md
```

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/binance-kline-collector.git
cd binance-kline-collector
```

### 2. Configure .env
```
DB_HOST=timescaledb
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=<yourpassword>
DB_NAME=klines
BINANCE_API_BASE=https://api.binance.com
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```
This will start the TimescaleDB instance and the Python service.

### 4. (Optional) Access the API
If the FastAPI interface is enabled, visit:
```bash
http://localhost:8000/docs
```
to view and test the endpoints via Swagger UI.

## 📜 License
This project is licensed under the GPLv3 License. See the LICENSE file for details.

##  🙌 Contributions
Feel free to open issues or submit pull requests. Feedback and collaboration are welcome!
