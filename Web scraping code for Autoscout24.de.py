from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Start WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the AutoScout24 used car page
url = "https://www.autoscout24.de/lst?sort=standard&desc=0&ustate=N%2CU&atype=C&cy=D&ocs_listing=include&source=homepage_search-mask"
driver.get(url)

# Wait for main content to load
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.XPATH, "//article")))

# Initialize lists to store data
car_names, prices, mileages, transmissions, first_registrations, fuels, performances, images = [], [], [], [], [], [], [], []

def scroll_page():
    """Scroll down the page to load more results."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Allow content to load

def scrape_cars():
    """Extracts car details from the current page."""
    cars = driver.find_elements(By.XPATH, "//article")
    print(f"Found {len(cars)} cars on this page.")

    for car in cars:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", car)
            time.sleep(0.5)  # Simulate human-like behavior

            car_name = car.find_element(By.XPATH, ".//h2").text if car.find_elements(By.XPATH, ".//h2") else "N/A"
            price = car.find_element(By.XPATH, './/p').text if car.find_elements(By.XPATH, './/p') else "N/A"
            mileage = car.find_element(By.XPATH, './/span[1]').text if car.find_elements(By.XPATH, './/span[1]') else "N/A"
            transmission_type = car.find_element(By.XPATH, './/span[2]').text if car.find_elements(By.XPATH, './/span[2]') else "N/A"
            registration = car.find_element(By.XPATH, './/span[3]').text if car.find_elements(By.XPATH, './/span[3]') else "N/A"
            fuel = car.find_element(By.XPATH, './/span[4]').text if car.find_elements(By.XPATH, './/span[4]') else "N/A"
            performance = car.find_element(By.XPATH, './/span[5]').text if car.find_elements(By.XPATH, './/span[5]') else "N/A"
            image = car.find_element(By.XPATH, './/picture/img').get_attribute("src") if car.find_elements(By.XPATH, './/picture/img') else "N/A"



        # Append data to lists
            car_names.append(car_name)
            prices.append(price)
            mileages.append(mileage)
            transmissions.append(transmission_type)
            first_registrations.append(registration)
            fuels.append(fuel)
            performances.append(performance)
            images.append(image)


        except Exception as e:
            print(f"Error extracting data for a car: {e}")

# Scrape first page
scrape_cars()

# Pagination: Loop through numbered buttons
current_page = 1
while len(car_names) < 1000:
    try:
        # Find the next page button (e.g., 2, 3, 4, ...)
        next_page_button = driver.find_element(By.XPATH, f"//button[contains(text(), '{current_page + 1}')]")
        if next_page_button.is_enabled():
            driver.execute_script("arguments[0].click();", next_page_button)
            time.sleep(5)  # Wait for the next page to load
            current_page += 1
            scrape_cars()
        else:
            print("No more pages available.")
            break
    except Exception as e:
        print(f"Pagination error: {e}")
        break

# Close the browser
driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Car Name": car_names[:1000],
    "Price": prices[:1000],
    "Miles Driven": mileages[:1000],
    "Transmission": transmissions[:1000],
    "First Registration": first_registrations[:1000],
    "Fuel Type": fuels[:1000],
    "Performance": performances[:1000],
    "Image URL": images[:1000],
})

# Save to CSV
df.to_csv("autoscout24_used_cars.csv", index=False)
print("Scraping completed! Data saved as 'autoscout24_used_cars.csv'.")
