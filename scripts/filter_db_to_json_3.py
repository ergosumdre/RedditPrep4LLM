import sqlite3
import json
import argparse

# Set up command-line argument parser
parser = argparse.ArgumentParser(description='Process data from SQLite database to JSON file')
parser.add_argument('--db_path', type=str, default='dogbot.db', help='Path to the SQLite database')
parser.add_argument('--output_file', type=str, default='output.json', help='Path to the output JSON file')
parser.add_argument('--min_score', type=int, default=2, help='Minimum score')
parser.add_argument('--min_length', type=int, default=2, help='Minimum length')
parser.add_argument('--max_chars', type=int, default=7500, help='Maximum characters')

args = parser.parse_args()

# Connect to SQLite database
conn = sqlite3.connect(args.db_path)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS dogbot
             (id TEXT PRIMARY KEY, train_text TEXT, score INT, length INT)''')
conn.commit()

# Retrieve rows from database based on minimum score and length criteria
c.execute("SELECT train_text FROM dogbot WHERE score >= ? AND length >= ?", (args.min_score, args.min_length))
rows = c.fetchall()
print('Number of samples with these settings:', len(rows))

# Define bad content to filter out
bad_contents = ["[deleted]", "[removed]", "I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.", ".jpg", ".png", ".jpeg", ".gif"]

# Write selected rows to JSON file
with open(args.output_file, 'w') as f:
    for row in rows:
        if len(row[0]) < args.max_chars and not any(bad in row[0] for bad in bad_contents):
            f.write(json.dumps({"sample": row[0]}) + "\n")
        else:
            print('bad content found')

# Close database connection
conn.close()
