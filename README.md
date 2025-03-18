# Stock Data Dashboard

A Streamlit dashboard for displaying and visualizing stock data from Alpha Vantage API.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a `.env` file in the root directory with your Alpha Vantage API key:
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

## Features

- Daily stock data visualization
- Intraday data with customizable intervals
- Price and volume charts
- Daily data refresh
- Manual refresh option

## Project Structure

```
├── main.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not tracked by git)
├── .gitignore               # Git ignore file
└── src/
    ├── __init__.py          # Makes src a Python package
    ├── alpha_vantage_api.py # Alpha Vantage API integration
    └── backend.py           # Data processing functions
```
