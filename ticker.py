import requests
import pandas as pd
from datetime import datetime
import time

def get_all_stocks():
    """
    Fetches stock data from NSE and saves to CSV
    """
    try:
        # Create empty lists to store data
        symbols = []
        names = []
        exchanges = []

        # Get data from stockanalysis.com
        url = "https://stockanalysis.com/list/nse-india/"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the table using pandas
            tables = pd.read_html(response.text)
            
            # The main stock table should be the first table
            if len(tables) > 0:
                df = tables[0]
                
                # Extract symbol and company name
                for _, row in df.iterrows():
                    symbol = row['Symbol'].strip()
                    name = row['Company Name'].strip()
                    
                    symbols.append(symbol)
                    names.append(name)
                    exchanges.append('NSE')  # All are NSE stocks from this source
                    
                # Create DataFrame
                stock_df = pd.DataFrame({
                    'Symbol': symbols,
                    'Company Name': names, 
                    'Exchange': exchanges
                })
                
                # Save to CSV
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'indian_stocks_{timestamp}.csv'
                stock_df.to_csv(filename, index=False)
                print(f"Successfully saved {len(stock_df)} stocks to {filename}")
                
                return stock_df
                
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    print("Fetching all Indian stocks...")
    get_all_stocks()
