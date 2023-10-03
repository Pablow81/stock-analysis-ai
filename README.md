# Stock Analysis AI
This Python script provides various functions for analyzing and visualizing stock data. It utilizes packages like yfinance, matplotlib, and sklearn to fetch data, analyze news sentiment, plot prices and perform trend analysis. AI is planned to be introduced.

## Features
Fetch stock price data from Yahoo Finance API
Analyze sentiment of recent news articles using NLTK Vader
Plot historical stock prices and dividends over time
Perform linear regression to analyze price trends

## Usage
The main capabilities are provided via functions like:

read_isin_wkn_from_file - Read ISIN/WKN codes from a file
fetch_and_analyze_news - Get news for a ticker and analyze sentiment
plot_stock_price - Plot historical prices over 5 years and 3 days
plot_stock_price_with_dividends - Plot prices and dividends over time
analyze_trend - Run regression to analyze trends for a metric like price

### Sample usage:

```
# Read list of stocks  
stocks = read_isin_wkn_from_file('isin_wkn_list.txt')

# Get news and sentiment for first stock
fetch_and_analyze_news(stocks[0]) 

# Plot prices and dividends 
plot_stock_price_with_dividends(stocks[0])

# Analyze price trend
analyze_trend(stocks[0], 'Close')
```

## TODOs
Some ideas for future improvements:

- Add AI that finds alternative companies based on fundamentals and does also sentiment analysis of news etc.
- Add a nice UI / interface where all the data is shown and updated frequently
- Containerize script into a Docker image for easy deployment
- Automate analysis over list of stocks
- Add more trend analysis methods like moving averages
- Build web interface or Jupyter notebook for interactive use
- Add more visualizations like candlestick charts
- Compare sentiment with price movements
- etc.

## License
This project is open source and available under the MIT License.
