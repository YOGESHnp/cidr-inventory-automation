import pandas as pd

# Load the CSV file into a DataFrame
csv_file = 'cleaned_subnets.csv'  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Convert the DataFrame to an HTML string
html_output = df.to_html(index=False, escape=False, border=1)

# Add bold styling for headers
html_output = html_output.replace('<th>', '<th style="font-weight:bold; text-align:center;">')

# Save the updated HTML to a file
html_file = 'subnets.html'
with open(html_file, 'w') as file:
    file.write(html_output)

print(f"HTML file has been created: {html_file}")