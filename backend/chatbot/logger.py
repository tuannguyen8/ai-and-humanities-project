import csv
import os
from datetime import datetime

def log_conversation(question, answer, path="data/conversations.csv"):
    log_exists = os.path.exists(path)
    with open(path, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["Timestamp", "User Question", "Bot Response"])
        writer.writerow([datetime.now().isoformat(), question, answer])
