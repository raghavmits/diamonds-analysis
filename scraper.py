# import os
# import pandas as pd
# import time
# import traceback
# import json
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# # Set timestamp
# timestamp = f"{pd.Timestamp('today'):%Y-%m-%d %I-%M %p}"
# # Create project directories
# os.makedirs('data', exist_ok=True)
# os.makedirs('screenshots', exist_ok=True)
# # Define CSV path
# cwd = os.getcwd()
# csv_path = ''.join((cwd, '/data/', timestamp, '.csv'))

# def create_driver():
#     """Creates a Firefox WebDriver instance."""
#     try:
#         options = Options()
#         # Set to False if you want to see the browser in action
#         options.headless = True
#         # Print geckodriver location for debugging
#         import subprocess
#         result = subprocess.run(['which', 'geckodriver'], capture_output=True, text=True)
#         print(f"Geckodriver location: {result.stdout.strip()}")
#         # Update the path to your geckodriver location
#         service = Service(executable_path='/opt/homebrew/bin/geckodriver')
#         # Add more logging
#         print("Creating Firefox driver...")
#         driver = webdriver.Firefox(service=service, options=options)
#         print("Firefox driver created successfully!")
#         # Set page load timeout
#         driver.set_page_load_timeout(30)
#         return driver
#     except Exception as e:
#         print(f"Error creating driver: {e}")
#         print(traceback.format_exc())
#         raise

# def scrape_diamonds(page_url, max_pages=10):
#     """
#     Scrapes diamond data from Brilliant Earth's diamond search page.
    
#     Args:
#         page_url (str): URL of the diamond search page
#         max_pages (int): Maximum number of pages to scrape
    
#     Returns:
#         pandas.DataFrame: DataFrame containing scraped diamond data
#     """
#     driver = None
#     all_diamonds = []
    
#     try:
#         # Create driver
#         driver = create_driver()
        
#         # Navigate to the diamond search page
#         print(f"Navigating to {page_url}")
#         driver.get(page_url)
        
#         # Wait for the page to load
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "diamonds_search_table"))
#         )
        
#         # Take a screenshot of the initial page
#         driver.save_screenshot(f"screenshots/initial_page_{timestamp}.png")
#         print("Initial page loaded successfully")
        
#         current_page = 1
        
#         while current_page <= max_pages:
#             print(f"Scraping page {current_page}")
            
#             # Wait for the diamond items to be present
#             WebDriverWait(driver, 20).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "inner.item"))
#             )
            
#             # Take a screenshot of each page
#             driver.save_screenshot(f"screenshots/page_{current_page}_{timestamp}.png")
            
#             # Find all diamond items
#             items = driver.find_elements(By.CLASS_NAME, "inner.item")
#             print(f"Found {len(items)} diamonds on page {current_page}")
            
#             for item in items:
#                 try:
#                     # Extract the JSON data from data-upc attribute
#                     data_upc = item.get_attribute('data-upc')
#                     if data_upc:
#                         diamond_data = json.loads(data_upc)
                        
#                         # Process the JSON data to extract relevant info
#                         diamond_info = {
#                             'id': diamond_data.get('id'),
#                             'upc': diamond_data.get('upc'),
#                             'title': diamond_data.get('title'),
#                             'price': diamond_data.get('price'),
#                             'shape': diamond_data.get('shape'),
#                             'carat': diamond_data.get('carat'),
#                             'color': diamond_data.get('color'),
#                             'clarity': diamond_data.get('clarity'),
#                             'cut': diamond_data.get('cut'),
#                             'report': diamond_data.get('report'),
#                             'origin': diamond_data.get('origin'),
#                             'polish': diamond_data.get('polish'),
#                             'symmetry': diamond_data.get('symmetry'),
#                             'measurements': diamond_data.get('measurements'),
#                             'depth': diamond_data.get('depth'),
#                             'table': diamond_data.get('table'),
#                             'fluorescence': diamond_data.get('fluorescence'),
#                             'certificate_number': diamond_data.get('certificate_number'),
#                             'receive_by': diamond_data.get('receive_by'),
#                             'collection': diamond_data.get('collection'),
#                             'length_width_ratio': diamond_data.get('length_width_ratio'),
#                             'real_diamond_image': diamond_data.get('real_diamond_image'),
#                             'has_v360_video': diamond_data.get('has_v360_video'),
#                             'shipping_day': diamond_data.get('shipping_day')
#                         }
                        
#                         all_diamonds.append(diamond_info)
#                 except Exception as e:
#                     print(f"Error extracting data from diamond item: {e}")
            
#             # Check if there's a next page button and click it
#             try:
#                 next_page_btn = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination-next:not(.disabled)"))
#                 )
                
#                 if next_page_btn:
#                     print(f"Navigating to page {current_page + 1}")
#                     driver.execute_script("arguments[0].scrollIntoView();", next_page_btn)
#                     next_page_btn.click()
                    
#                     # Wait for the new page to load
#                     time.sleep(3)
                    
#                     # Wait for the page to load
#                     WebDriverWait(driver, 20).until(
#                         EC.presence_of_element_located((By.ID, "diamonds_search_table"))
#                     )
                    
#                     current_page += 1
#                 else:
#                     print("No more pages to navigate")
#                     break
#             except Exception as e:
#                 print(f"No more pages available or error navigating: {e}")
#                 break
        
#         # Create a DataFrame from the collected data
#         df = pd.DataFrame(all_diamonds)
        
#         # Save the data to CSV
#         print(f"Saving data to {csv_path}")
#         df.to_csv(csv_path, index=False)
#         print(f"Successfully saved {len(df)} diamonds to CSV")
        
#         return df
    
#     except Exception as e:
#         print(f"An error occurred during scraping: {e}")
#         print(traceback.format_exc())
        
#         # Still try to save any data collected so far
#         if all_diamonds:
#             df = pd.DataFrame(all_diamonds)
#             df.to_csv(csv_path, index=False)
#             print(f"Saved partial data with {len(df)} diamonds to CSV")
        
#         return None
    
#     finally:
#         if driver:
#             print("Closing browser")
#             driver.quit()

# def main():
#     """Main function to run the scraper."""
#     try:
#         url = "https://www.brilliantearth.com/diamond/shop-all/"
#         print(f"Starting diamond scraper for {url}")
        
#         # Scrape diamond data
#         df = scrape_diamonds(url, max_pages=10)  # Adjust max_pages as needed
        
#         if df is not None and not df.empty:
#             # Print summary statistics
#             print("\nScraping Summary:")
#             print(f"Total diamonds scraped: {len(df)}")
#             print(f"Shapes found: {df['shape'].unique()}")
#             print(f"Price range: ${df['price'].min()} - ${df['price'].max()}")
#             print(f"Carat range: {df['carat'].min()} - {df['carat'].max()}")
#             print(f"Most common clarity: {df['clarity'].value_counts().idxmax()}")
#             print(f"Most common color: {df['color'].value_counts().idxmax()}")
            
#             print(f"\nData saved to: {csv_path}")
#             return True
#         else:
#             print("No data was collected or an error occurred")
#             return False
    
#     except Exception as e:
#         print(f"Error in main function: {e}")
#         print(traceback.format_exc())
#         return False

# if __name__ == "__main__":
#     main()

import os
import pandas as pd
import time
import traceback
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Set timestamp
timestamp = f"{pd.Timestamp('today'):%Y-%m-%d %I-%M %p}"
# Create project directories
os.makedirs('data', exist_ok=True)
os.makedirs('screenshots', exist_ok=True)
# Define CSV path
cwd = os.getcwd()
csv_path = ''.join((cwd, '/data/', timestamp, '.csv'))

def create_driver():
    """Creates a Firefox WebDriver instance."""
    try:
        options = Options()
        # Set to False if you want to see the browser in action
        options.headless = True
        # Print geckodriver location for debugging
        import subprocess
        result = subprocess.run(['which', 'geckodriver'], capture_output=True, text=True)
        print(f"Geckodriver location: {result.stdout.strip()}")
        # Update the path to your geckodriver location
        service = Service(executable_path='/opt/homebrew/bin/geckodriver')
        # Add more logging
        print("Creating Firefox driver...")
        driver = webdriver.Firefox(service=service, options=options)
        print("Firefox driver created successfully!")
        # Set page load timeout
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        print(f"Error creating driver: {e}")
        print(traceback.format_exc())
        raise

def scroll_to_load_more(driver, max_scroll_attempts=200):
    """
    Scrolls down the page to trigger loading more items.
    
    Args:
        driver: Selenium WebDriver instance
        max_scroll_attempts: Maximum number of scroll attempts
        
    Returns:
        int: Number of items found after scrolling
    """
    print("Starting scroll to load more diamonds...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll_attempts = 0
    items_count = 0
    
    while current_scroll_attempts < max_scroll_attempts:
        # Get current item count
        items = driver.find_elements(By.CLASS_NAME, "inner.item")
        current_count = len(items)
        
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolling down (attempt {current_scroll_attempts + 1}/{max_scroll_attempts}): found {current_count} items")
        
        # Take a screenshot after scrolling
        driver.save_screenshot(f"screenshots/scroll_{current_scroll_attempts}_{timestamp}.png")
        
        # Wait to load more results
        time.sleep(3)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        new_items = driver.find_elements(By.CLASS_NAME, "inner.item")
        new_count = len(new_items)
        
        # If no new items loaded and height didn't change, we've reached the end
        if new_count == current_count and new_height == last_height:
            consecutive_no_change_count += 1
            if consecutive_no_change_count >= 3:  # Try a few more times before giving up
                print(f"No new items loaded after {consecutive_no_change_count} scroll attempts. Stopping scrolling.")
                break
        else:
            consecutive_no_change_count = 0
            
        # Update heights
        last_height = new_height
        items_count = new_count
        current_scroll_attempts += 1
        
        # If we've collected a very large number of items, we can stop
        if items_count > 1000:
            print(f"Reached significant number of items ({items_count}). Stopping scrolling.")
            break
    
    print(f"Finished scrolling. Total items found: {items_count}")
    return items_count

def scrape_diamonds(page_url, max_pages=10):
    """
    Scrapes diamond data from Brilliant Earth's diamond search page.
    
    Args:
        page_url (str): URL of the diamond search page
        max_pages (int): Maximum number of pages to scrape
    
    Returns:
        pandas.DataFrame: DataFrame containing scraped diamond data
    """
    driver = None
    all_diamonds = []
    
    try:
        # Create driver
        driver = create_driver()
        
        # Navigate to the diamond search page
        print(f"Navigating to {page_url}")
        driver.get(page_url)
        
        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "diamonds_search_table"))
        )
        
        # Take a screenshot of the initial page
        driver.save_screenshot(f"screenshots/initial_page_{timestamp}.png")
        print("Initial page loaded successfully")
        
        current_page = 1
        
        while current_page <= max_pages:
            print(f"Scraping page {current_page}")
            
            # Wait for the diamond items to be present
            WebDriverWait(driver, 199).until(
                EC.presence_of_element_located((By.CLASS_NAME, "inner.item"))
            )
            
            # Scroll to load all diamonds on this page
            scroll_to_load_more(driver)
            
            # Take a screenshot after loading all items on the page
            driver.save_screenshot(f"screenshots/page_{current_page}_loaded_{timestamp}.png")
            
            # Find all diamond items
            items = driver.find_elements(By.CLASS_NAME, "inner.item")
            print(f"Found {len(items)} diamonds on page {current_page}")
            
            # Process visible diamonds
            for item in items:
                try:
                    # Extract the JSON data from data-upc attribute
                    data_upc = item.get_attribute('data-upc')
                    if data_upc:
                        diamond_data = json.loads(data_upc)
                        
                        # Process the JSON data to extract relevant info
                        diamond_info = {
                            'id': diamond_data.get('id'),
                            'upc': diamond_data.get('upc'),
                            'title': diamond_data.get('title'),
                            'price': diamond_data.get('price'),
                            'shape': diamond_data.get('shape'),
                            'carat': diamond_data.get('carat'),
                            'color': diamond_data.get('color'),
                            'clarity': diamond_data.get('clarity'),
                            'cut': diamond_data.get('cut'),
                            'report': diamond_data.get('report'),
                            'origin': diamond_data.get('origin'),
                            'polish': diamond_data.get('polish'),
                            'symmetry': diamond_data.get('symmetry'),
                            'measurements': diamond_data.get('measurements'),
                            'depth': diamond_data.get('depth'),
                            'table': diamond_data.get('table'),
                            'fluorescence': diamond_data.get('fluorescence'),
                            'certificate_number': diamond_data.get('certificate_number'),
                            'receive_by': diamond_data.get('receive_by'),
                            'collection': diamond_data.get('collection'),
                            'length_width_ratio': diamond_data.get('length_width_ratio'),
                            'real_diamond_image': diamond_data.get('real_diamond_image'),
                            'has_v360_video': diamond_data.get('has_v360_video'),
                            'shipping_day': diamond_data.get('shipping_day')
                        }
                        
                        all_diamonds.append(diamond_info)
                except Exception as e:
                    print(f"Error extracting data from diamond item: {e}")
            
            # Check if there's a next page button and click it
            try:
                next_page_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination-next:not(.disabled)"))
                )
                
                if next_page_btn:
                    print(f"Navigating to page {current_page + 1}")
                    driver.execute_script("arguments[0].scrollIntoView();", next_page_btn)
                    next_page_btn.click()
                    
                    # Wait for the new page to load
                    time.sleep(3)
                    
                    # Wait for the page to load
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.ID, "diamonds_search_table"))
                    )
                    
                    current_page += 1
                else:
                    print("No more pages to navigate")
                    break
            except Exception as e:
                print(f"No more pages available or error navigating: {e}")
                break
        
        # Create a DataFrame from the collected data
        df = pd.DataFrame(all_diamonds)
        
        # Save the data to CSV
        print(f"Saving data to {csv_path}")
        df.to_csv(csv_path, index=False)
        print(f"Successfully saved {len(df)} diamonds to CSV")
        
        return df
    
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        print(traceback.format_exc())
        
        # Still try to save any data collected so far
        if all_diamonds:
            df = pd.DataFrame(all_diamonds)
            df.to_csv(csv_path, index=False)
            print(f"Saved partial data with {len(df)} diamonds to CSV")
        
        return None
    
    finally:
        if driver:
            print("Closing browser")
            driver.quit()

def main():
    """Main function to run the scraper."""
    try:
        url = "https://www.brilliantearth.com/diamond/shop-all/"
        print(f"Starting diamond scraper for {url}")
        
        # Scrape diamond data
        df = scrape_diamonds(url, max_pages=10)  # Adjust max_pages as needed
        
        if df is not None and not df.empty:
            # Print summary statistics
            print("\nScraping Summary:")
            print(f"Total diamonds scraped: {len(df)}")
            print(f"Shapes found: {df['shape'].unique()}")
            print(f"Price range: ${df['price'].min()} - ${df['price'].max()}")
            print(f"Carat range: {df['carat'].min()} - {df['carat'].max()}")
            print(f"Most common clarity: {df['clarity'].value_counts().idxmax()}")
            print(f"Most common color: {df['color'].value_counts().idxmax()}")
            
            print(f"\nData saved to: {csv_path}")
            return True
        else:
            print("No data was collected or an error occurred")
            return False
    
    except Exception as e:
        print(f"Error in main function: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    main()