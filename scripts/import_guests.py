"""
Import iFly.vc Consumer Summit 2026 guests into Neo4j.
Maps CSV fields → User node properties to match the app's schema.
"""

import csv
import time
import sys
from neo4j import GraphDatabase

NEO4J_URI      = "neo4j+s://fb691b6b.databases.neo4j.io"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "UfdsQn6_jKzgFzp0c9iFgtJ0PP6-zYkJJO-cR6TUpws"
NEO4J_DATABASE = "neo4j"

CSV_PATH = "/Users/awwu/Downloads/iFly.vc Consumer Summit 2026 - Guests - 2026-05-05-05-04-00.csv"

def load_guests(path):
    guests = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            guests.append({
                "name":      name,
                "role":      (row.get("What company do you work for?") or "").strip(),
                "location":  "",
                "website":   (row.get("What is your LinkedIn profile?") or "").strip(),
                "email":     (row.get("email") or "").strip(),
                "phone":     (row.get("phone_number") or "").strip(),
                "guestId":   (row.get("guest_id") or "").strip(),
                "createdAt": int(time.time() * 1000),
            })
    return guests

MERGE_QUERY = """
UNWIND $guests AS g
MERGE (u:User {name: g.name})
ON CREATE SET
    u.role      = g.role,
    u.location  = g.location,
    u.website   = g.website,
    u.email     = g.email,
    u.phone     = g.phone,
    u.guestId   = g.guestId,
    u.createdAt = g.createdAt
ON MATCH SET
    u.role      = CASE WHEN u.role IS NULL OR u.role = '' THEN g.role ELSE u.role END,
    u.website   = CASE WHEN u.website IS NULL OR u.website = '' THEN g.website ELSE u.website END,
    u.email     = CASE WHEN u.email IS NULL OR u.email = '' THEN g.email ELSE u.email END,
    u.phone     = CASE WHEN u.phone IS NULL OR u.phone = '' THEN g.phone ELSE u.phone END,
    u.guestId   = CASE WHEN u.guestId IS NULL OR u.guestId = '' THEN g.guestId ELSE u.guestId END
RETURN count(u) AS total
"""

def main():
    guests = load_guests(CSV_PATH)
    print(f"Loaded {len(guests)} guests from CSV.")

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(MERGE_QUERY, guests=guests)
            record = result.single()
            print(f"Done. {record['total']} nodes merged into Neo4j.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        driver.close()

if __name__ == "__main__":
    main()
