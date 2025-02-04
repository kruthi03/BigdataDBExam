import pandas as pd

# Load dataset
file_path = r"E:\Car_Test\cars.com_used_cars.csv"
df = pd.read_csv(file_path)

# Remove leading/trailing spaces in column names
df.columns = df.columns.str.strip()

# Check if 'Price' column exists
if "Price" in df.columns:
    # Show unique values before cleaning
    print("Unique Price values before cleaning:", df["Price"].unique())

    # Convert 'Price' to string, remove $ and commas, and handle non-numeric values
    df["Price"] = (
        df["Price"]
        .astype(str)  # Ensure all values are strings
        .str.replace(r"[^\d.]", "", regex=True)  # Remove non-numeric characters except '.'
    )

    # Convert to float, replacing empty strings with NaN
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # Drop rows where 'Price' is NaN (empty values)
    df.dropna(subset=["Price"], inplace=True)

    # Show dataset after cleaning
    print("Dataset shape after cleaning:", df.shape)
    print("Remaining missing values:\n", df.isna().sum())

    # Save cleaned data
    cleaned_file_path = r"E:\Car_Test\cleaned_cars.com.csv"
    df.to_csv(cleaned_file_path, index=False)

    print("Data cleaning completed. Cleaned file saved at:", cleaned_file_path)
else:
    print("Error: 'Price' column not found in the dataset.")





