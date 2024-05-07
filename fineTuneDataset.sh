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
unzstd "$file_path" -o "/Users/dre/Downloads/llm_data_process/data/json_file/$filename_without_extension.json"

echo "JSON to Pickle File..."
python3 /Users/dre/Downloads/llm_data_process/scripts/json_to_pkl_1.py "/Users/dre/Downloads/llm_data_process/data/json_file/$filename_without_extension.json" 
echo "Pickle to Database.."
python3 /Users/dre/Downloads/llm_data_process/scripts/pkl_to_db_2.py --pickle_path "/Users/dre/Downloads/llm_data_process/data/pickle_file/$filename_without_extension.pkl" --db_path "/Users/dre/Downloads/llm_data_process/data/database/$filename_without_extension.db" 
python3 /Users/dre/Downloads/llm_data_process/scripts/filter_db_to_json_3.py --db_path "/Users/dre/Downloads/llm_data_process/data/database/$filename_without_extension.db" --output_file "/Users/dre/Downloads/llm_data_process/data/complete_json/$filename_without_extension.json"