import os
import json
import pandas as pd
import argparse
import pickle

# Set up command-line argument parser
parser = argparse.ArgumentParser(description='Process JSON data to pickle file')
parser.add_argument('json_path', type=str, help='Path to the JSON file')
parser.add_argument('--output_path', type=str)#, default="/home/dre/Downloads/reddit/data/processed_data/dogs.pkl", help='Path to the output pickle file')

args = parser.parse_args()


filename_without_extension = os.path.basename(args.json_path).split('.')[0]
formatted_filename = filename_without_extension.replace("_", "-")

df = pd.DataFrame(columns=["author", "subreddit", "created_utc", "parent_id", "id", "body", "score"])

tmpdf = pd.read_json(args.json_path, lines=True)
df = pd.concat([df, tmpdf[["author", "subreddit", "created_utc", "parent_id", "id", "body", "score"]]])
#print(df.head())
print('length:', len(df))
df = df.sort_values(by="created_utc")
#print(df.head())

# Save the dataframe to a pickle file
output_path = args.output_path
# with open(f"/home/dre/Downloads/reddit/data/processed_data/{formatted_filename}.pkl", "wb") as f:
#     pickle.dump(df, f)
with open(f"/Users/dre/Downloads/llm_data_process/pickle_file/{filename_without_extension}.pkl", "wb") as f:
    pickle.dump(df, f)