# Prevents re-filing the same accessibility issue every triage run. Backed
# by a small SQLite file - no need for a real database server for this.

import hashlib
import os
import sqlite3


def fingerprint(group: dict) -> str:
    """Stable id for a group, so the same (rule, page) is only ever filed once."""
    raw = f"{group['rule_id']}:{group['page_url']}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class DedupStore:
    def __init__(self, db_path="data/dedup.db"):
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS filed_tickets
            (fingerprint TEXT PRIMARY KEY, issue_number INTEGER, first_seen TEXT)"""
        )
        self.conn.commit()

    def already_filed(self, fp: str) -> bool:
        return (
            self.conn.execute(
                "SELECT 1 FROM filed_tickets WHERE fingerprint = ?", (fp,)
            ).fetchone()
            is not None
        )

    def record(self, fp: str, issue_number: int):
        # OR IGNORE: a duplicate record() call (e.g. a retried run) shouldn't
        # crash or clobber the original first_seen timestamp.
        self.conn.execute(
            "INSERT OR IGNORE INTO filed_tickets VALUES (?, ?, datetime('now'))",
            (fp, issue_number),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
