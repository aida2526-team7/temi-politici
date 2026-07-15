"""Test unitari dell'audit NMF su fixture sintetica."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pandas.testing import assert_frame_equal

from src.news_topic_audit import (
    article_distribution,
    build_audit_results,
    confidence_statistics,
    dominant_domain_share,
    exact_excerpt_duplicates,
    exact_title_excerpt_duplicates,
    load_review_csv,
    near_duplicate_proxy,
    sample_assigned_records,
    validate_required_columns,
    write_audit_outputs,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "topic_review_fixture.csv"


def fixture_config() -> dict[str, object]:
    return {
        "input_review_csv": "data/processed/topic_review_fixture.csv",
        "input_metadata_json": "data/processed/topic_metadata_fixture.json",
        "output_dir": "reports/topic_audit",
        "random_seed": 42,
        "near_duplicate_prefix_length": 29,
        "confidence_thresholds": [0.5, 0.6],
        "top_domains": 10,
        "top_records": 3,
        "sample_records": 2,
        "encoding": "utf-8-sig",
        "dominant_domain_warning_threshold": 0.5,
    }


class TopicAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.frame = load_review_csv(FIXTURE, "utf-8-sig")

    def test_required_columns(self) -> None:
        self.assertEqual(validate_required_columns(self.frame), ["topic_0_peso", "topic_1_peso"])

    def test_missing_columns_raise(self) -> None:
        with self.assertRaisesRegex(ValueError, "Colonne obbligatorie mancanti"):
            validate_required_columns(self.frame.drop(columns=["domain"]))

    def test_article_counts_and_percentages(self) -> None:
        result = article_distribution(self.frame).set_index("topic_id")
        self.assertEqual(int(result.loc[0, "articles"]), 4)
        self.assertEqual(int(result.loc[1, "articles"]), 4)
        self.assertAlmostEqual(float(result.loc[0, "percentage"]), 50.0)
        self.assertAlmostEqual(float(result.loc[1, "percentage"]), 50.0)

    def test_confidence_statistics(self) -> None:
        result = confidence_statistics(self.frame, [0.5, 0.6]).set_index("metric")
        self.assertAlmostEqual(float(result.loc["mean", "value"]), 0.74375)
        self.assertAlmostEqual(float(result.loc["median", "value"]), 0.775)
        self.assertAlmostEqual(float(result.loc["below_0.60_percentage", "value"]), 12.5)

    def test_dominant_domain(self) -> None:
        result = dominant_domain_share(self.frame).set_index("topic_id")
        self.assertEqual(result.loc[0, "domain"], "a.test")
        self.assertEqual(int(result.loc[0, "articles"]), 2)
        self.assertAlmostEqual(float(result.loc[0, "topic_percentage"]), 50.0)

    def test_exact_excerpt_duplicates(self) -> None:
        result = exact_excerpt_duplicates(self.frame)
        self.assertEqual(result["records_in_duplicate_groups"], 4)
        self.assertEqual(result["duplicate_groups"], 2)
        self.assertEqual(result["largest_group"], 2)

    def test_exact_title_excerpt_duplicates(self) -> None:
        result = exact_title_excerpt_duplicates(self.frame)
        self.assertEqual(result["records_in_duplicate_groups"], 4)
        self.assertEqual(result["duplicate_groups"], 2)

    def test_near_duplicate_proxy(self) -> None:
        result = near_duplicate_proxy(self.frame, 29)
        self.assertEqual(result["records_in_duplicate_groups"], 6)
        self.assertEqual(result["duplicate_groups"], 3)

    def test_sampling_is_reproducible(self) -> None:
        first = sample_assigned_records(self.frame, records_per_topic=2, seed=42)
        second = sample_assigned_records(self.frame, records_per_topic=2, seed=42)
        self.assertEqual(first["url"].tolist(), second["url"].tolist())

    def test_calculation_does_not_modify_input(self) -> None:
        original = self.frame.copy(deep=True)
        build_audit_results(self.frame, {"n_topics": 2, "articles": 8}, fixture_config())
        assert_frame_equal(self.frame, original)

    def test_outputs_and_manifest_are_written_without_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "data" / "processed"
            input_dir.mkdir(parents=True)
            review_path = input_dir / "topic_review_fixture.csv"
            metadata_path = input_dir / "topic_metadata_fixture.json"
            shutil.copy2(FIXTURE, review_path)
            metadata_path.write_text(json.dumps({"n_topics": 2, "articles": 8}), encoding="utf-8")
            frame = load_review_csv(review_path)
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            config = fixture_config()
            results = build_audit_results(frame, metadata, config)
            paths = write_audit_outputs(
                root,
                config,
                frame,
                results,
                [review_path, metadata_path],
                run_time_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
            )
            expected = {
                "topic_distribution",
                "confidence_summary",
                "domain_summary",
                "duplicate_summary",
                "audit_report",
                "run_manifest",
            }
            self.assertEqual(set(paths), expected)
            self.assertTrue(all(path.is_file() for path in paths.values()))
            manifest_text = paths["run_manifest"].read_text(encoding="utf-8")
            manifest = json.loads(manifest_text)
            self.assertNotIn(str(root), manifest_text)
            self.assertEqual(manifest["review_rows"], 8)
            self.assertEqual(manifest["random_seed"], 42)
            self.assertTrue(all(not Path(item["path"]).is_absolute() for item in manifest["inputs"]))
            self.assertTrue(all(not Path(item["path"]).is_absolute() for item in manifest["outputs"]))


if __name__ == "__main__":
    unittest.main()
