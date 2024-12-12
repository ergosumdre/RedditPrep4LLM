#!/bin/bash

# Check if a parameter is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file_path>"
    exit 1
fi

# Access the parameter
file_path="$1"

# Extract filename without extension
filename_without_extension=$(basename -- "$file_path")
filename_without_extension="${filename_without_extension%.*}"

# Execute the Python script with the provided file path
echo "Creating JSON file..."
unzstd "$file_path" -o "data/json_file/$filename_without_extension.json"

echo "JSON to Pickle File..."
python3 scripts/json_to_pkl_1.py "data/json_file/$filename_without_extension.json" 
echo "Pickle to Database.."
python3 scripts/pkl_to_db_2.py --pickle_path "data/pickle_file/$filename_without_extension.pkl" --db_path "data/database/$filename_without_extension.db" 
python3 scripts/filter_db_to_json_3.py --db_path "data/database/$filename_without_extension.db" --output_file "data/complete_json/$filename_without_extension.json"
