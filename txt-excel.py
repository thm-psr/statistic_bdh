import os
import pandas as pd

# Input text file path
input_file = r'C:\Users\acer\Downloads\Testdata\testdaten\ergebnis_aus_count.txt'  # Update to the actual path of your input file
output_folder = r'C:\Users\acer\Downloads\Testdata\testdaten'  # Specify the desired output folder

# Specify the output Excel file name
output_file_name = "ergebnis.xlsx"
output_excel_file = os.path.join(output_folder, output_file_name)

# Process the text file and save as an Excel file
try:
    # Read the text file line by line
    data = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Split each line into the name and the count
            if ':' in line:
                name, count = line.rsplit(':', 1)
                data.append([name.strip().strip("'"), int(count.strip())])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Unterlagensname', 'Anzahl der Anfragen'])

    # Write the DataFrame to an Excel file
    df.to_excel(output_excel_file, index=False, engine='openpyxl')
    print(f"Excel file created successfully: {output_excel_file}")

except Exception as e:
    print(f"Error occurred: {e}")
