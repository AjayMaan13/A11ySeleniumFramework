# Tests for src/agent/ticket_dedup.py. Uses a temp SQLite file per test
# (pytest's tmp_path) - never touches the real data/dedup.db.

from src.agent.ticket_dedup import DedupStore, fingerprint


def test_fingerprint_is_deterministic():
    group = {"rule_id": "image-alt", "page_url": "page-a.html"}

    assert fingerprint(group) == fingerprint(dict(group))


def test_fingerprint_differs_by_rule_or_page():
    base = {"rule_id": "image-alt", "page_url": "page-a.html"}
    different_rule = {"rule_id": "color-contrast", "page_url": "page-a.html"}
    different_page = {"rule_id": "image-alt", "page_url": "page-b.html"}

    assert fingerprint(base) != fingerprint(different_rule)
    assert fingerprint(base) != fingerprint(different_page)


def test_already_filed_false_for_unseen_fingerprint(tmp_path):
    store = DedupStore(db_path=str(tmp_path / "dedup.db"))

    assert store.already_filed("unseen-fp") is False

    store.close()


def test_record_then_already_filed_true(tmp_path):
    store = DedupStore(db_path=str(tmp_path / "dedup.db"))
    fp = fingerprint({"rule_id": "image-alt", "page_url": "page-a.html"})

    store.record(fp, issue_number=42)

    assert store.already_filed(fp) is True
    store.close()


def test_dedup_state_persists_across_store_instances(tmp_path):
    db_path = str(tmp_path / "dedup.db")
    fp = fingerprint({"rule_id": "label", "page_url": "page-a.html"})

    first_store = DedupStore(db_path=db_path)
    first_store.record(fp, issue_number=7)
    first_store.close()

    second_store = DedupStore(db_path=db_path)
    assert second_store.already_filed(fp) is True
    second_store.close()


def test_record_is_idempotent_for_the_same_fingerprint(tmp_path):
    store = DedupStore(db_path=str(tmp_path / "dedup.db"))
    fp = fingerprint({"rule_id": "image-alt", "page_url": "page-a.html"})

    store.record(fp, issue_number=1)
    store.record(fp, issue_number=1)  # must not raise (e.g. a retried run)

    assert store.already_filed(fp) is True
    store.close()


def test_creates_missing_parent_directory(tmp_path):
    nested_path = tmp_path / "nested" / "dir" / "dedup.db"

    store = DedupStore(db_path=str(nested_path))

    assert nested_path.exists()
    store.close()
