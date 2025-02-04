from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Base URL with pagination placeholder
base_url = "https://www.cars.com/shopping/results/?dealer_id=&include_shippable=false&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance=all&mileage_max=&monthly_payment=&page=1&page_size=100&sort=best_match_desc&stock_type=all&year_max=&year_min=&zip="

wait = WebDriverWait(driver, 10)  # Explicit wait

# Initialize lists to store data
car_names, prices, rates, saler_names, locations, images = [], [], [], [], [], []

# Function to scrape car details from the current page
def scrape_cars():
    car_cards = driver.find_elements(By.CSS_SELECTOR, '.vehicle-card')  # Correct selector for car cards
    print(f"Found {len(car_cards)} cars on this page.")

    for car in car_cards:
        try:
            car_name = car.find_element(By.CSS_SELECTOR, 'h2.title').text.strip()
        except:
            car_name = "N/A"

        try:
            price = car.find_element(By.CSS_SELECTOR, '.primary-price').text.strip()
        except:
            price = "N/A"

        try:
            rating_element = car.find_element(By.CSS_SELECTOR, 'spark-rating')
            rate = rating_element.get_attribute("rating")  # Extract rating from the shadow DOM
        except:
            rate = "N/A"

        try:
            saler_name = car.find_element(By.CSS_SELECTOR, '.dealer-name').text.strip()
        except:
            saler_name = "N/A"

        try:
            location = car.find_element(By.CSS_SELECTOR, '.miles-from').text.strip()
        except:
            location = "N/A"

        try:
            image_element = car.find_element(By.CSS_SELECTOR, 'img.vehicle-image')
            image = image_element.get_attribute("src")
        except:
            image = "N/A"

        # Append data to lists
        car_names.append(car_name)
        prices.append(price)
        rates.append(rate)
        saler_names.append(saler_name)
        locations.append(location)
        images.append(image)

# Start from page 1 and keep scraping until we have 1000 listings
page_number = 1
while len(car_names) < 1000:
    print(f"Scraping Page {page_number}...")
    
    # Load the current page
    driver.get(base_url.format(page_number))
    
    # Wait for the page to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.vehicle-card')))
    
    # Scrape the current page
    scrape_cars()

    # Move to the next page
    page_number += 1

    # If no new cars are found, break loop (indicating no more pages)
    if len(car_names) >= 1000 or len(driver.find_elements(By.CSS_SELECTOR, '.vehicle-card')) == 0:
        print("No more cars found. Stopping...")
        break

# Close the browser
driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Car Name": car_names[:1000],  # Limit to 1000 rows
    "Price": prices[:1000],
    "Rate": rates[:1000],
    "Location": locations[:1000],
    "Saler_name": saler_names[:1000],
    "Image URL": images[:1000]
})

# Display first few rows
print(df.head())

# Save to CSV
df.to_csv("cars_com_used_cars.csv", index=False)

print("Scraping completed! Data saved as 'cars_com_used_cars.csv'.")
