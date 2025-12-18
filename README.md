# tradingbot

A modular and scalable **cryptocurrency data pipeline** built in Python to collect, clean, and preprocess real-time and historical trading data from multiple exchanges (currently Nobitex). This project is designed as the foundational layer for building **algorithmic trading bots** using machine learning and deep learning.

---

## Features

- **Data Collection**
  - Fetches real-time price data for multiple cryptocurrencies (BTC, ETH, USDT) from Nobitex.
  - Can be extended to include other exchanges.

- **Data Cleaning**
  - Converts timestamps, removes duplicates, and handles missing or invalid values.
  - Ensures price and volume columns are numeric and positive.

- **Feature Engineering (Preliminary)**
  - Placeholder for technical indicators, rolling statistics, and lag features.
  - Prepares data for labeling and downstream ML tasks.

- **Labeling**
  - Generates labels for supervised learning, supporting both threshold-based classification and future price prediction.

- **Storage**
  - Saves processed data to CSV files.
  - Compatible with MongoDB for raw and historical data storage.

- **Modular Design**
  - Separate Python modules for loading, cleaning, feature engineering, and labeling.
  - Easy to extend for additional cryptocurrencies, indicators, or exchanges.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/maryamkhosravii/tradingbot.git

Create a virtual environment and install dependencies:
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install --upgrade pip
pip install pymongo pandas numpy requests
Make sure MongoDB is running locally or provide a remote URI.

Usage
from dataset_builder import DatasetBuilder

# Initialize dataset builder
builder = DatasetBuilder(output_folder="datasets")

# Build dataset for multiple cryptocurrencies
df_all = builder.build_dataset(
    symbols=["btc-irt", "eth-irt", "usdt-irt"],
    horizon=1,
    threshold=0.002,
    separate_files=False,
    output_name="crypto_dataset.csv"
)

print(df_all.head())
The processed dataset will be saved in the datasets/ folder.
Supports building separate files for each symbol if desired.

Project Structure
trader_bot/
│
├─ data_sources/
│   └─ nobitex_source.py
│
├─ utils/
│   └─ mongo_handler.py
│
├─ load_data.py
├─ cleaning_data.py
├─ features.py
├─ labels.py
├─ dataset_builder.py
└─ main.py

Future Improvements
Implement Machine Learning / Deep Learning models for price prediction and trading signals.
Add backtesting module to evaluate strategies on historical data.
Integrate FastAPI or Streamlit dashboard for real-time monitoring.
Extend data collection to multiple international exchanges (Binance, Coinbase, etc.).
Implement risk management and trade execution logic.
