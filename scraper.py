import requests
from bs4 import BeautifulSoup
import json
import os

# Load the list of universities
with open('universities.json', 'r') as f:
    URLS = json.load(f)

DB_FILE = "seen.txt"

def load_seen():
    if not os.path.exists(DB_FILE): return set()
    with open(DB_FILE, "r") as f: return set(line.strip() for line in f)

def check_conferences():
    seen = load_seen()
    new_found = []
    
    for uni, url in URLS.items():
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Look for any bold or heading text with "Conference"
            for tag in soup.find_all(['h2', 'h3', 'strong', 'a']):
                text = tag.get_text().strip()
                if "Conference" in text and len(text) > 15:
                    entry = f"{uni}: {text}"
                    if entry not in seen:
                        new_found.append(entry)
        except Exception as e:
            print(f"Error at {uni}: {e}")
    return new_found

new_events = check_conferences()
if new_events:
    print(f"NEW_FOUND={len(new_events)}")
    with open(DB_FILE, "a") as f:
        for e in new_events:
            print(f"Found: {e}")
            f.write(e + "\n")
