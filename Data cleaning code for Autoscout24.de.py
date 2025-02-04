import pandas as pd
import re

def clean_price(price):
    """Convert price from formats like '€ 3.999,-' to numeric."""
    if isinstance(price, str):
        numeric_price = re.sub(r'[^0-9]', '', price)  # Remove non-numeric characters
        return int(numeric_price) if numeric_price else None  # Return None if empty
    return None

def clean_miles(miles):
    """Convert miles driven from strings like '12,345 km' to numeric."""
    if isinstance(miles, str):
        miles = re.sub(r'[^0-9]', '', miles)  # Remove non-numeric characters
        return int(miles) if miles else 0  # Convert empty values to 0
    return None

def clean_performance(performance):
    """Extract kW and PS values from '72 kW (98 PS)' format."""
    if isinstance(performance, str):
        kw_match = re.search(r'(\d+) kW', performance)
        ps_match = re.search(r'\((\d+) PS\)', performance)
        return int(kw_match.group(1)) if kw_match else None, int(ps_match.group(1)) if ps_match else None
    return None, None

def clean_registration(date):
    """Convert 'MM/YYYY' format to 'YYYY-MM-01' for SQL compatibility."""
    if isinstance(date, str) and re.match(r'\d{2}/\d{4}', date):
        return f"{date[3:7]}-{date[0:2]}-01"
    return None

def clean_fuel_type(fuel):
    """Standardize fuel type names."""
    fuel_mapping = {
        'Elektro/Benzin': 'Hybrid',
        'Benzin': 'Petrol',
        'Diesel': 'Diesel',
        'Elektro': 'Electric',
        'Erdgas (CNG)': 'CNG',
        'Autogas (LPG)': 'LPG'
    }
    return fuel_mapping.get(fuel, fuel)

# Load dataset
file_path = "autoscout24_used_cars.csv"
df = pd.read_csv(file_path)

# Rename columns for SQL compatibility
df.columns = df.columns.str.replace(' ', '_').str.lower()

# Clean data
df['price'] = df['price'].apply(clean_price)
df['miles_driven'] = df['miles_driven'].apply(clean_miles)
df[['performance_kw', 'performance_ps']] = df['performance'].apply(lambda x: pd.Series(clean_performance(x)))
df['first_registration'] = df['first_registration'].apply(clean_registration)
df['fuel_type'] = df['fuel_type'].apply(clean_fuel_type)

# ---- Handle Missing Values in Price Column ----
df = df.dropna(subset=['price'])  # Drop rows where price is missing
# If you prefer to replace missing prices with 0 instead of dropping, use:
# df['price'].fillna(0, inplace=True)

# Drop unnecessary columns
df.drop(columns=['performance', 'transmission'], inplace=True, errors='ignore')

# ---- Drop Columns with Too Many Missing Values ----
missing_threshold = 0.4  # Adjust threshold if needed (40% missing)
missing_percentage = df.isnull().mean()
columns_to_drop = missing_percentage[missing_percentage > missing_threshold].index.tolist()
df.drop(columns=columns_to_drop, inplace=True)

# Save cleaned data
cleaned_file_path = "autoscout24_used_car_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"Data cleaning complete. Cleaned file saved as '{cleaned_file_path}'.")
