# Binance Kline Collector

A Python service to fetch historical candlestick (kline) data from the Binance API and store it in a PostgreSQL/TimescaleDB database. Supports multi-threaded fetching and insertion for high performance.

## Features
- Fetches historical kline (candlestick) data from Binance for multiple symbols and intervals
- Multi-threaded: fetch and insert operations run in parallel for each symbol-interval pair
- Stores data in PostgreSQL/TimescaleDB for efficient time-series analysis
- Configurable trading pairs and intervals via JSON files
- Dockerized for easy deployment

## Tech Stack
- Python 3
- SQLAlchemy (ORM)
- Requests (HTTP client)
- PostgreSQL/TimescaleDB
- Docker & Docker Compose

## Project Structure
```
binance-kline-collector/
├── app/
│   ├── crud.py         # Database operations
│   ├── fetcher.py      # Binance API fetching logic
│   ├── intervals.json  # List of intervals to fetch
│   ├── main.py         # Main entry point (multi-threaded)
│   ├── models.py       # SQLAlchemy models
│   ├── requirements.txt# Python dependencies
│   ├── symbols.json    # List of symbols to fetch
├── db/
│   └── init.sql        # DB initialization
├── docker/
│   ├── .env            # DB configs
│   ├── Dockerfile      # Python service Dockerfile
│   └── docker-compose.yml # Orchestration
├── README.md
└── LICENSE
```

## Setup & Usage

### 1. Clone the Repository
```zsh
git clone https://github.com/oguzhan-bolukbas/binance-kline-collector.git
cd binance-kline-collector
```

### 2. Configure Environment
Edit or create a `.env` file (see `docker/.env`):
```
DB_HOST=timescaledb
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=<yourpassword>
DB_NAME=klines
BINANCE_API_BASE=https://api.binance.com
```

### 3. Configure Symbols and Intervals
Edit `app/symbols.json` and `app/intervals.json` to specify which trading pairs and intervals to fetch.

### 4. Install Python Dependencies (for local run)
```zsh
cd app
pip install -r requirements.txt
```

### 5. Run with Docker Compose
```zsh
docker-compose -f docker/docker-compose.yml up --build
```
This will start the TimescaleDB instance and the Python service.

### 6. Run Manually (for development)
Ensure PostgreSQL/TimescaleDB is running and accessible, then:
```zsh
cd app
python main.py
```

## Multi-Threading & Performance
- The application uses Python's `ThreadPoolExecutor` to fetch and insert data in parallel for each symbol-interval pair.
- The number of threads (`max_workers`) is configurable in `main.py` (default: 32). Decrease this value if you encounter rate limit or database errors.
- Each thread uses its own database session for safe concurrent inserts.
- Binance API v3 kline endpoint allows up to 1200 requests per minute per IP. Adjust thread count and sleep interval as needed to avoid 429 errors.

## License
GPLv3. See LICENSE for details.

## Contributions
Pull requests and issues are welcome!
