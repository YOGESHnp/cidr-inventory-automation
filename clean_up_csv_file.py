import pandas as pd

# Load the CSV file into a DataFrame
file_path = './subnets.csv'  # Update with the correct file path
df = pd.read_csv(file_path)

# Remove unwanted columns
columns_to_remove = ['Profile', 'Range of Addresses', 'Hosts', 'Divide', 'Join']
df.drop(columns=columns_to_remove, inplace=True)

# Modify the 'Profile' column to remove '_all'
df['Account Name'] = df['Account Name'].str.replace('_all', '', regex=False)

# Add the 'Reserved IP\'s' column
# Assuming "Usable IPs" is at index 5, you can use a custom condition for setting Reserved IPs.

# Create a new column for Reserved IP's
df['Reserved IP\'s'] = ""

# Loop through the DataFrame rows and populate the 'Reserved IP\'s' column
# Assuming the condition is that for every 7th and 8th row in a block of 8 rows, you want to set the 'Reserved IP\'s' based on 'Usable IPs' (which is column index 5 in your case)
for idx, row in df.iterrows():
    if idx % 8 == 6 or idx % 8 == 7: # Rows 7th (6) and 8th (7) in each block of 8 rows
        df.at[idx, 'Reserved IP\'s'] = row['Usable IPs'] # Assuming 'Usable IPs' is the correct column name

# Save the cleaned DataFrame to a new CSV file
output_file = './cleaned_subnets.csv'  # Update with the desired output file path
df.to_csv(output_file, index=False)

print(f"Cleaned CSV saved as: {output_file}")