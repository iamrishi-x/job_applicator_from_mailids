import pandas as pd

def GetRecipients():
    # Path to your Excel file
    EXCEL_PATH = r"data\Mail_id.xlsx"

    # Read the Excel file and clean column names
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces

    # Display available city options
    print("-" * 15 + " MENU " + "-" * 15)
    city_list = list(df.columns)  # Extract city names from column headers
    for i, c_name in enumerate(city_list, 1):
        print(f"{i}. {c_name} ({len(df[c_name].dropna())} recipients)")

    # Get user input for multiple city selections
    choices = input("Enter the numbers of your chosen cities (comma-separated, e.g., 1,3,5): ")

    # Convert user input into a list of selected city names
    selected_cities = []
    try:
        selected_indices = [int(choice.strip()) - 1 for choice in choices.split(",") if choice.strip().isdigit()]
        selected_cities = [city_list[i] for i in selected_indices if 0 <= i < len(city_list)]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

    # Collect email IDs from selected cities
    BCC_EMAILS = []
    for city in selected_cities:
        if city in df.columns:
            BCC_EMAILS.extend(df[city].dropna().tolist())  # Merge emails from selected cities

    # Remove duplicates (if any)
    BCC_EMAILS = list(set(BCC_EMAILS))

    # Check if there are recipients
    if not BCC_EMAILS:
        print("No email IDs found. Exiting...")
        exit()

    # Print selected cities and total recipients
    print(f"Selected Cities: {', '.join(selected_cities)}")
    print(f"Total Recipients: {len(BCC_EMAILS)}")
    print(f"Recipients are : {BCC_EMAILS[:100]}")

    return BCC_EMAILS