import os
import json
import pandas as pd
import argparse
import pickle
import sqlite3
import colorama
from multiprocessing import Pool, Lock

# Set up command-line argument parser
parser = argparse.ArgumentParser(description='Silly-man\'s multiprocessing: Run multiple instances of this script or make it better.')
parser.add_argument('--db_path', type=str)
parser.add_argument('--pickle_path')

args = parser.parse_args()

# Load data
file = args.pickle_path
df = pd.DataFrame()

with open(file, 'rb') as f:
    data = pickle.load(f)
df = data

# Remove first 3 characters in all rows of the "parent_id" column
df['parent_id'] = df['parent_id'].str[3:]

print("df head:")
print(df.head())
print("df length:", len(df))

# Define the function to build conversation chain by ID
def build_convo_chain_by_id(df, id):
    HAS_PARENT = True
    convo_chain = []
    while HAS_PARENT:
        try:
            row = df[df['id'] == id]
            convo_chain.append(row[['author', 'body', 'score']].values[0].tolist())
            if row['parent_id'].isna().values[0]:
                HAS_PARENT = False
            else:
                id = row['parent_id'].values[0]
        except IndexError:
            break
    convo_chain = convo_chain[::-1]
    return convo_chain

ids = df['id'].unique()

import random

# Shuffle ids
random.shuffle(ids)

MIN_LEN = 2
MIN_SCORE = 3

BOT_NAME = "dogbot"

hm_samples = 1000000
sample_count = 0
current_ill = 0
total_samples = len(ids)
num_ids = len(ids)

lock = Lock()  # Create a lock object

def process_id(idx):
    global sample_count, current_ill, num_ids
    current_ill += 1
    chain = build_convo_chain_by_id(df, idx)
    reply_score = int(chain[-1][-1])
    if len(chain) >= MIN_LEN and reply_score >= MIN_SCORE:
        final_reply_author = chain[-1][0]
        author_ids = {final_reply_author: BOT_NAME}
        start_id = 0
        in_str = "### BEGIN CONVERSATION ###\n\n"
        for i in chain[:-1]:
            author = i[0]
            if author not in author_ids:
                author_ids[author] = "Speaker_" + str(start_id)
                start_id += 1
            in_str += "## "+author_ids[author] + ": ##\n" + i[1] + "\n\n"
        in_str += "## " + author_ids[final_reply_author] + ": ##\n"
        out_str = chain[-1][1] + "\n\n### END CONVERSATION ###"
        train_string = in_str + out_str
        # Create a new SQLite connection for each process
        conn = sqlite3.connect(args.db_path)
        c = conn.cursor()
        # Create the table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS dogbot
                     (id TEXT PRIMARY KEY, train_text TEXT, score INT, length INT)''')
        conn.commit()
        # Add to SQLite database if not already present
        with lock:  # Acquire the lock before accessing the database
            c.execute("SELECT * FROM dogbot WHERE id=?", (idx,))
            if c.fetchone() is None:
                c.execute("INSERT INTO dogbot (id, train_text, score, length) VALUES (?, ?, ?, ?)", (idx, train_string, reply_score, len(chain)))
                conn.commit()
                sample_count += 1
                print(colorama.Fore.GREEN + f"Percentage: {(current_ill/num_ids*.17) * 5000}" + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.RED + "Already in database" + colorama.Style.RESET_ALL)
        conn.close()
    if sample_count >= hm_samples:
        return

if __name__ == '__main__':
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_id, ids)
