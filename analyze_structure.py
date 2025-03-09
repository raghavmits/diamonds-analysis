import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def analyze_website_structure():
    """Analyzes the structure of Brilliant Earth diamond listing page"""
    driver = None
    try:
        # Set up directories
        os.makedirs('debug', exist_ok=True)
        
        # Set up driver
        options = Options()
        options.headless = True
        service = Service(executable_path='/opt/homebrew/bin/geckodriver')
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(30)
        
        # Navigate to website
        url = "https://www.brilliantearth.com/diamond/shop-all/"
        print(f"Navigating to {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Save full page source
        with open('debug/full_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Saved full page source")
        
        # Take a screenshot
        driver.save_screenshot('debug/full_page.png')
        print("Saved full page screenshot")
        
        # Analyze the potential diamond containers
        containers = [
            "#diamonds_search_table",
            ".listpage-lists-v2",
            ".diamond-list",
            "[data-testid='diamond-list']",
            ".product-grid"
        ]
        
        for container_selector in containers:
            try:
                containers = driver.find_elements(By.CSS_SELECTOR, container_selector)
                print(f"Found {len(containers)} elements matching '{container_selector}'")
                
                if containers:
                    # Save the first container HTML
                    with open(f'debug/container_{container_selector.replace(".", "dot_").replace("#", "id_").replace("[", "").replace("]", "").replace("=", "_")}.html', 'w', encoding='utf-8') as f:
                        f.write(containers[0].get_attribute('outerHTML'))
                    
                    # Try to find potential diamond rows
                    row_selectors = [
                        "tr", "tr:not(.header)", ".diamond-list-item", 
                        ".product-item", ".grid-item", "[data-testid='diamond-item']"
                    ]
                    
                    for row_selector in row_selectors:
                        try:
                            rows = containers[0].find_elements(By.CSS_SELECTOR, row_selector)
                            print(f"  - Found {len(rows)} potential diamond rows with '{row_selector}'")
                            
                            if rows:
                                # Save the first row HTML
                                with open(f'debug/row_{container_selector.replace(".", "dot_").replace("#", "id_").replace("[", "").replace("]", "").replace("=", "_")}_{row_selector.replace(".", "dot_").replace("#", "id_").replace("[", "").replace("]", "").replace("=", "_")}.html', 'w', encoding='utf-8') as f:
                                    f.write(rows[0].get_attribute('outerHTML'))
                                
                                # Print sample text from first row
                                row_text = rows[0].text
                                print(f"  - Sample row text: {row_text[:100]}...")
                        except Exception as e:
                            print(f"  - Error finding rows with '{row_selector}': {e}")
            except Exception as e:
                print(f"Error analyzing container '{container_selector}': {e}")
        
        print("Analysis complete. Check debug folder for details.")
        return True
        
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("Starting website structure analysis...")
    analyze_website_structure()
    print("Analysis script completed")