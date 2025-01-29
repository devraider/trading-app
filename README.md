# Financial Web Application

## Motivation

This project was developed as a take-home assignment for the **NCH Invest** interview.

## Tech Stack

- **Backend**: Python, Django
- **Database**: PostgreSQL
- **Frontend**: TailwindCSS
- **Data Integration**: Yahoo Finance API (`yfinance`) -  **_(To be implemented)_**
- **Containerization**: Docker, Docker Compose

---

## Features

### Implemented Features

1. **Logging**
    - Basic logging set up to track application activity.
    - Error logs to capture issues with trades or API interactions.

2. **Frontend**:
    - Responsive design using TailwindCSS.

3. **Trades Processing**:
    - Import Excel-based trades files.
    - Validate trade data for accuracy and consistency.
    - Calculate daily net positions based on imported trades.
    - Store trades and calculated positions in the database.

---

## Installation Guide

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.12+ (if running outside Docker).
- PostgreSQL 12+.

### Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd trading_app
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following:
   ```env
   DEBUG=INFO
   SECRET_KEY=<your_secret_key>
   POSTGRES_DB=<your_db>
   POSTGRES_USER=<your_user>
   POSTGRES_PASSWORD=<your_password>
   POSTGRES_HOST=<localhost>
   POSTGRES_PORT=5432
   ```

3. **Build and Start Docker Containers**:
   ```bash
   docker compose up --build
   ```

4. **Access the Application**:
    - Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## Project Structure

```
trading_app/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── samples/
│   ├── pnl
│   │   ├── trades_example.xlsx (file with formulas to guide development process)
│   │   └── pnl.xlsx (sample file for testing)
│   └── trading-processor
│       └── trading-processor
│           ├── trades_250_entries.xlsx
│           ├── trades_2000_entries.xlsx
│           └── trades_4_entries.xlsx
├── src/
│   ├── static/
│   │   └── uploads/
│   │       └── (uplded .xlsx file by the user)
│   ├── templates/
│   │   ├── base.html
│   │   ├── pnl.html
│   │   ├── trade_processor.html
│   │   └── welcome.html
│   ├── trading/
│   │   ├── models.py
│   │   ├── migrations/
│   │   │   └── (all migration after running makemigration command)
│   │   ├── repository/
│   │   │   ├── base_repo.py
│   │   │   ├── positions.py
│   │   │   └── tranzactions.py
│   │   └── tests/
│   │   ├── services/
│   │   │   ├── yahoo_finance.py
│   │   │   ├── trade_processor.py
│   │   │   └── pnl_processor.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tools.py
│   │   ├── settings.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Requirements

#### Trades Processing

- Parse Excel trade files using `pandas`.
- Validate trade data (e.g., required fields, valid symbols).
- Store validated trades in the database.
- Calculate daily net positions (quantity × price × direction).

#### Data Fetching

- Use Yahoo Finance API to fetch stock OHLCV data.
- Incrementally update the database with new data.
- Handle API rate limiting and errors gracefully.

#### P&L Calculation

- Compute daily Profit & Loss for each position.
- Differentiate between realized and unrealized P&L.

#### Frontend

- Display key financial data with TailwindCSS:
    - Current positions in a table.
    - Daily P&L in an interactive chart.

---

## Testing

Tests must be implemented and adding step to run tests during deployment (`Dockerfile`)

---

## Acknowledgments

This application was developed as part of a take-home project for **NCH Invest**.
