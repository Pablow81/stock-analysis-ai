# Import required libraries
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List
from sklearn.linear_model import LinearRegression
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Python snippet to read a list of ISINs or WKNs from a text file
# Assuming the file "isin_wkn_list.txt" contains:
# ISIN1234
# WKN5678
# ISIN9101
# WKN1121
# ...
def read_isin_wkn_from_file(filename):
    isin_wkn_list = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                isin_wkn_list.append(line.strip())
        return isin_wkn_list
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None

# Function to fetch and analyze news
def fetch_and_analyze_news(ticker: str) -> None:
    stock = yf.Ticker(ticker)
    news = stock.get_news()

    if not news:
        print("No news found.")
        return

    for index, article in enumerate(news[-10:]):
        print(f"News {index + 1}: {article['title']}")
        sentiment = sia.polarity_scores(article.get('summary', ''))
        if sentiment['compound'] > 0.05:
            print("Sentiment: Good")
        elif sentiment['compound'] < -0.05:
            print("Sentiment: Bad")
        else:
            print("Sentiment: Neutral")

# Function to plot stock prices
def plot_stock_price(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch historical data for the last 5 years and last 3 months
    data_5y = stock.history(period="5y")
    data_3d = stock.history(period="3d")
    
    # Plot stock prices for the last 5 years
    plt.figure(figsize=(12, 6))
    plt.title(f"{ticker} Stock Price - Last 5 Years")
    plt.plot(data_5y['Close'], label="Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.legend()
    plt.show()

    # Plot stock prices for the last 3 days
    plt.figure(figsize=(12, 6))
    plt.title(f"{ticker} Stock Price - Last 3 Days")
    plt.plot(data_3d['Close'], label="Close Price")
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.legend()
    plt.show()  

# Function to plot stock prices along with dividends
def plot_stock_price_with_dividends(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch historical data for the last 5 years
    data_5y = stock.history(period="5y")
    dividends = stock.dividends
    
    # Plot stock prices for the last 5 years
    plt.figure(figsize=(12, 6))
    plt.title(f"{ticker} Stock Price and Dividends - Last 5 Years")
    plt.plot(data_5y['Close'], label="Close Price")
    

    # Match dividends with actual close prices on those days
    dividend_prices = data_5y.loc[dividends.index, 'Close']

    # Plot the scatter chart using matched prices
    plt.scatter(dividends.index, dividend_prices, color='red', label="Dividends")

    
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.legend()
    plt.show()

# Function to analyze trend for a specific metric (e.g., Close Price)
def analyze_trend(ticker, metric='Close'):
    stock = yf.Ticker(ticker)
    
    # Fetch historical data for the last 5 years
    data_5y = stock.history(period="5y")
    
    # Extract the metric of interest
    y = data_5y[metric].values.reshape(-1, 1)
    
    # Create an array of index values representing time
    x = np.array(range(len(y))).reshape(-1, 1)
    
    # Perform linear regression
    model = LinearRegression()
    model.fit(x, y)
    
    # Plot the actual data and the regression line
    plt.scatter(x, y, color='blue')
    plt.plot(x, model.predict(x), color='red')
    plt.title(f"{ticker} {metric} Trend Analysis - Last 5 Years")
    plt.xlabel("Time")
    plt.ylabel(metric)
    plt.show()
    
    # Determine the trend
    slope = model.coef_[0][0]
    if slope > 0:
        print(f"The trend for {metric} is upward.")
    elif slope < 0:
        print(f"The trend for {metric} is downward.")
    else:
        print(f"The trend for {metric} is flat.")

def fetch_and_display_all_kpis(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch key statistics
    key_stats = stock.info
    
    print("Key Statistics:")
    for key, value in key_stats.items():
        print(f"{key}: {value}")

# Function to fetch and display key financial metrics
def fetch_and_display_kpis(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch key statistics like Market Cap, Forward P/E, etc.
    key_stats = stock.info
    
    # Fetch historical financials like income statements, balance sheet, etc.
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow
    
    print("Key Statistics:")
    print(f"Market Cap: {key_stats.get('Market Cap', 'N/A')}")
    print("...and many more")
    
    print("\nFinancials:")
    print("Income Statement:")
    print(financials)
    print("Balance Sheet:")
    print(balance_sheet)
    print("Cash Flow:")
    print(cashflow)

# Function to display dividends and dividend yield
def display_dividends_and_yield(ticker):
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    
    # Calculate the average stock price over the period for which we have dividend data
    data_5y = stock.history(period="5y")
    avg_stock_price = data_5y['Close'].mean()
    
    # Calculate total dividends and dividend yield
    total_dividends = dividends.sum()
    dividend_yield = (total_dividends / avg_stock_price) * 100
    
    print("Dividends:")
    print(dividends)
    
    print(f"Total Dividends: {total_dividends}")
    print(f"Average Stock Price: {avg_stock_price}")
    print(f"Dividend Yield: {dividend_yield}%")

# Function to find alternative companies or competitors in the same sector
def find_alternative_companies(ticker):
    stock = yf.Ticker(ticker)
    tickers_list = [f'{ticker}']  # Replace with a comprehensive list

    # Your sector
    sector = stock.info.get('Sector', 'N/A')

    # Find alternative companies
    alternative_companies = []
    for ticker in tickers_list:
        other_stock = yf.Ticker(ticker)
        other_sector = other_stock.info.get('Sector', 'N/A')
        if other_sector == sector:
            alternative_companies.append(ticker)
    print(f"Alternative companies or competitors in the same sector ({sector}):")
    print(alternative_companies)

def main():
    
    isin_wkn_list = read_isin_wkn_from_file("isin_wkn_list.txt")
    for isin_wkn in isin_wkn_list:
        print(isin_wkn)
        fetch_and_analyze_news(f'{isin_wkn}')
        plot_stock_price(f'{isin_wkn}')
        plot_stock_price_with_dividends(f'{isin_wkn}')
        display_dividends_and_yield(f'{isin_wkn}')
        fetch_and_display_all_kpis(f'{isin_wkn}')
        analyze_trend(f'{isin_wkn}', 'Close')
        find_alternative_companies(f'{isin_wkn}')

#TODO: Add AI that finds alternative companies based on fundamentals and does also sentiment analysis of news

if __name__ == "__main__":
    main()
