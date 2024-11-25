import pandas as pd

# Load the CSV file into a DataFrame
file_path = './subnets.csv'  # Update with the correct file path
df = pd.read_csv(file_path)

# Remove unwanted columns
columns_to_remove = ['Profile', 'Range of Addresses', 'Hosts', 'Divide', 'Join']
df.drop(columns=columns_to_remove, inplace=True)

# Modify the 'Profile' column to remove '_all'
df['Account Name'] = df['Account Name'].str.replace('_all', '', regex=False)

# Save the cleaned DataFrame to a new CSV file
output_file = './cleaned_subnets.csv'  # Update with the desired output file path
df.to_csv(output_file, index=False)

print(f"Cleaned CSV saved as: {output_file}")