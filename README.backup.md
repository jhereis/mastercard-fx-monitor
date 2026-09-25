<<<<<<< HEAD
# Mastercard FX Monitor

A Python-based foreign exchange monitoring pipeline that integrates with the Mastercard Currency Conversion APIs to retrieve, validate, and store FX conversion rates for treasury and financial analytics use cases.

> **Current status:** Sandbox integration validated successfully with OAuth 1.0a authentication and Mastercard PKCS#12 signing keys.

---

## Overview

The **Mastercard FX Monitor** was designed to automate the daily collection of foreign exchange conversion rates directly from Mastercard APIs.

The project combines API integration, authentication, data engineering, validation, and historical storage into a lightweight FX monitoring pipeline.

The first validated use case retrieves the Mastercard conversion rate for:

```text
USD → BRL
```

Example sandbox response:

```text
HTTP Status: 200
1 USD = 5.5025 BRL
Historical data saved.
```

The current value above is a **Sandbox response** and must not be interpreted as a production FX rate.

---

## Business Problem

Treasury and financial operations teams often depend on manual FX checks across multiple platforms.

This creates operational issues such as:

- Manual data collection
- Lack of historical traceability
- Repetitive daily checks
- Inconsistent data sources
- Limited monitoring of FX variations
- Difficulty comparing rates across providers

The Mastercard FX Monitor creates a reusable pipeline capable of automatically retrieving and storing FX data for further analysis.

---

## Solution

The project implements the following data flow:

```text
Mastercard API
      │
      ▼
OAuth 1.0a Authentication
      │
      ▼
PKCS#12 Signing Key
      │
      ▼
Python Request
      │
      ▼
FX Conversion Response
      │
      ├── Raw JSON
      │
      └── Historical CSV
              │
              ▼
        FX Analytics Layer
```

The solution is designed to evolve into a broader Treasury FX Monitoring platform.

---

## Key Features

- Mastercard Currency Conversion API integration
- OAuth 1.0a authentication
- PKCS#12 private signing key support
- Secure environment variable management
- USD/BRL FX rate retrieval
- Raw API response storage
- Historical FX dataset generation
- API response validation
- HTTP error handling
- Modular Python structure
- Ready for scheduled daily execution
- Designed for multi-currency expansion

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Requests | HTTP API communication |
| Mastercard OAuth1 Signer | Mastercard OAuth 1.0a request signing |
| python-dotenv | Environment variable management |
| PKCS#12 | Private signing key format |
| CSV | Historical FX storage |
| JSON | Raw API response storage |
| Mastercard Developer Sandbox | API integration environment |

---

## Project Structure

```text
mastercard-fx-monitor/
│
├── src/
│   └── mastercard_fx.py
│
├── data/
│   ├── raw/
│   │   └── mastercard_USD_BRL_*.json
│   │
│   └── processed/
│       └── mastercard_fx_history.csv
│
├── secrets/
│   └── mastercard-fx-monitor-signing.p12
│
├── logs/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> The `secrets/` directory and `.env` file must never be committed to GitHub.

---

## Authentication

Mastercard APIs use **OAuth 1.0a** with a private signing key.

The project requires:

```text
Consumer Key
PKCS#12 Signing Key
Keystore Password
```

These credentials are generated through the Mastercard Developers portal.

The signing key is loaded by Python and used to cryptographically sign API requests before they are sent to Mastercard.

---

## Environment Variables

Create a `.env` file in the project root:

```env
MASTERCARD_CONSUMER_KEY=YOUR_CONSUMER_KEY
MASTERCARD_KEYSTORE_PATH=./secrets/mastercard-fx-monitor-signing.p12
MASTERCARD_KEYSTORE_PASSWORD=YOUR_KEYSTORE_PASSWORD
MASTERCARD_BASE_URL=https://sandbox.api.mastercard.com
```

Never expose real credentials in GitHub.

---

## Security

The following files must be excluded from version control:

```gitignore
.env

secrets/
*.p12
*.pem
*.key

.venv/
__pycache__/

.DS_Store

logs/*.log
```

This prevents private authentication material from being published accidentally.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/mastercard-fx-monitor.git
cd mastercard-fx-monitor
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
requests
python-dotenv
mastercard-oauth1-signer
```

---

## Running the Project

Activate the environment:

```bash
source .venv/bin/activate
```

Run the FX monitor:

```bash
python3 src/mastercard_fx.py
```

Expected output:

```text
============================================================
MASTERCARD FX MONITOR
============================================================
Environment : https://sandbox.api.mastercard.com
Currency    : USD/BRL
FX date     : YYYY-MM-DD
Amount      : 1
------------------------------------------------------------
HTTP status : 200

RESULT
------------------------------------------------------------
1 USD = X.XXXX BRL
1 USD = X.XXXX BRL

Historical data saved.
```

---

## Historical Dataset

Successful requests are appended to:

```text
data/processed/mastercard_fx_history.csv
```

The dataset can contain fields such as:

```text
collected_at_utc
fx_date
transaction_currency
billing_currency
conversion_rate
transaction_amount
billing_amount
bank_fee
```

This creates an auditable historical FX dataset for analytics and monitoring.

---

## Raw API Responses

The original API response is also stored as JSON:

```text
data/raw/mastercard_USD_BRL_YYYYMMDD_HHMMSS.json
```

Keeping the raw response provides:

- Traceability
- Debugging support
- API response auditing
- Reprocessing capability
- Data lineage

---

## Current Pipeline

```text
Mastercard Sandbox
        │
        ▼
OAuth Authentication
        │
        ▼
FX API Request
        │
        ▼
Response Validation
        │
        ├──────────────► Raw JSON
        │
        ▼
Historical Dataset
        │
        ▼
CSV Storage
```

---

## Roadmap

The next versions of the project are planned to include:

### Multi-Currency Monitoring

```text
USD → BRL
EUR → BRL
GBP → BRL
CHF → BRL
JPY → BRL
```

### Database Layer

Migrate the historical dataset from CSV-only storage to SQLite or PostgreSQL.

Planned table:

```text
fx_rates
├── collected_at
├── fx_date
├── currency_from
├── currency_to
├── mastercard_rate
├── previous_rate
├── daily_change
├── daily_change_pct
└── api_status
```

### Daily Automation

Automated execution using:

- cron
- GitHub Actions
- Cloud Functions
- AWS Lambda
- scheduled container jobs

### Treasury Analytics

Future analytics may include:

- D-1 rate comparison
- Daily variation
- Percentage variation
- Basis-point changes
- Historical volatility
- Spread analysis
- Threshold alerts

### External FX Benchmarking

The architecture can be extended to compare Mastercard rates against:

```text
Mastercard
     │
     ├── BACEN PTAX
     ├── FX Spot
     ├── Internal Treasury Rate
     └── Previous Mastercard Rate
```

This would enable an FX comparison and monitoring layer for treasury operations.

---

## Future Architecture

```text
                ┌─────────────────┐
                │ Mastercard API  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ FX Collector    │
                │     Python      │
                └────────┬────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      ┌─────────────┐         ┌─────────────┐
      │ Raw Storage │         │ Validation  │
      │    JSON     │         │    Layer    │
      └─────────────┘         └──────┬──────┘
                                     │
                                     ▼
                             ┌───────────────┐
                             │ FX Database   │
                             │ SQLite / SQL  │
                             └───────┬───────┘
                                     │
                                     ▼
                             ┌───────────────┐
                             │ FX Analytics  │
                             └───────┬───────┘
                                     │
                                     ▼
                             ┌───────────────┐
                             │ Dashboard /   │
                             │ Alerts        │
                             └───────────────┘
```

---

## Engineering Concepts Demonstrated

This project demonstrates practical experience with:

- REST API integration
- OAuth authentication
- Cryptographic request signing
- Environment configuration
- Secure credential handling
- Data ingestion
- Data validation
- Raw data persistence
- Historical dataset construction
- Error handling
- Modular Python development
- Financial data engineering
- Treasury automation

---

## Portfolio Context

The Mastercard FX Monitor is part of a broader portfolio focused on:

- Financial Technology
- Data Engineering
- Artificial Intelligence
- Treasury Automation
- Financial Markets
- Generative AI
- Operational Efficiency

The objective is to explore how modern software and data engineering techniques can improve financial operations and decision-support workflows.

---

## Disclaimer

This project is an independent technical portfolio project and is not affiliated with, endorsed by, or sponsored by Mastercard.

Mastercard names, APIs, and trademarks belong to their respective owners.

The current integration uses the Mastercard **Sandbox environment**. Sandbox values are intended for development and testing purposes and should not be interpreted as production market data or operational FX rates.

---

## Author

**Jheniffer Reis**

Data, Technology & Financial Solutions

Focus areas:

```text
Data Engineering
Artificial Intelligence
Financial Technology
Treasury
Automation
Financial Markets
```
=======
# fx_monitor
Cards FX Monitor
>>>>>>> 31505470c68aa6a8ecce3a858474588497a45130
