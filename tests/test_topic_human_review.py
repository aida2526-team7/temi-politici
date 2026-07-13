"""Test del campione riproducibile per lo human check su fixture sintetica."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from pandas.testing import assert_frame_equal

from src.topic_human_review import (
    HUMAN_COLUMNS,
    build_review_sample,
    deterministic_sample,
    exclude_title_excerpt_duplicates,
    load_inputs,
    select_top_weight,
    validate_inputs,
    write_outputs,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "topic_human_review_fixture.csv"


def fixture_config() -> dict[str, object]:
    return {
        "input_review_csv": "data/processed/topic_human_review_fixture.csv",
        "input_topic_terms_csv": "data/processed/topic_terms_fixture.csv",
        "output_directory": "reports/topic_human_review",
        "random_seed": 42,
        "topic_utili": [1],
        "topic_artefatto": [0, 2],
        "top_weight_per_topic": 2,
        "random_per_topic": 2,
        "artifact_checks_per_topic": 1,
        "max_same_domain_per_topic": 2,
        "excerpt_max_chars": 500,
        "encoding": "utf-8-sig",
        "categorie_di_revisione": [
            "tema politico coerente", "tema politico misto",
            "boilerplate o formato editoriale", "contenuto non politico", "dubbio",
        ],
    }


class TopicHumanReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        import pandas as pd

        cls.review = pd.read_csv(FIXTURE, encoding="utf-8-sig")
        cls.review.insert(0, "source_row_index", cls.review.index.astype(int))
        cls.terms = pd.DataFrame({
            "topic_id": [0, 1, 2],
            "termini_caratteristici": ["termini zero", "termini uno", "termini due"],
        })
        validate_inputs(cls.review, cls.terms, fixture_config())

    def test_reproducible_seed_42(self) -> None:
        frame = exclude_title_excerpt_duplicates(self.review)
        first, _, _ = deterministic_sample(frame, 1, 3, 42, set(), {}, 2)
        second, _, _ = deterministic_sample(frame, 1, 3, 42, set(), {}, 2)
        self.assertEqual(first["source_row_index"].tolist(), second["source_row_index"].tolist())

    def test_correct_row_count_and_topic_coverage(self) -> None:
        result = build_review_sample(self.review, fixture_config())
        self.assertEqual(len(result.sample), 6)
        self.assertEqual(set(result.sample["topic_id"]), {0, 1, 2})
        self.assertEqual(int((result.sample["topic_id"] == 1).sum()), 4)

    def test_top_weight_respects_weight_and_domain_diversity(self) -> None:
        frame = exclude_title_excerpt_duplicates(self.review)
        selected, _, exception = select_top_weight(frame, 1, 2, set(), {}, 2)
        self.assertEqual(selected["source_row_index"].tolist(), [2, 4])
        self.assertFalse(exception)

    def test_no_exact_title_excerpt_duplicates(self) -> None:
        sample = build_review_sample(self.review, fixture_config()).sample
        self.assertFalse(sample.duplicated(["title", "estratto"]).any())

    def test_domain_limit_when_applicable(self) -> None:
        sample = build_review_sample(self.review, fixture_config()).sample
        useful = sample[sample["topic_id"] == 1]
        self.assertLessEqual(int(useful["domain"].value_counts().max()), 2)

    def test_domain_exception_is_documented(self) -> None:
        import pandas as pd

        constrained = self.review[self.review["topic_id"] != 1].copy()
        useful = self.review[self.review["topic_id"] == 1].iloc[:4].copy()
        useful["domain"] = "only.test"
        frame = pd.concat([constrained, useful], ignore_index=True)
        frame["source_row_index"] = range(len(frame))
        result = build_review_sample(frame, fixture_config())
        self.assertEqual(len(result.exceptions), 1)
        self.assertEqual(result.exceptions[0]["topic_id"], 1)

    def test_human_columns_are_empty(self) -> None:
        sample = build_review_sample(self.review, fixture_config()).sample
        for column in HUMAN_COLUMNS:
            self.assertTrue(sample[column].eq("").all())

    def test_source_frame_is_not_modified(self) -> None:
        original = self.review.copy(deep=True)
        build_review_sample(self.review, fixture_config())
        assert_frame_equal(self.review, original)

    def test_missing_column_has_clear_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "Colonne obbligatorie mancanti"):
            validate_inputs(self.review.drop(columns=["url"]), self.terms, fixture_config())

    def test_review_ids_are_unique(self) -> None:
        sample = build_review_sample(self.review, fixture_config()).sample
        self.assertFalse(sample["review_id"].duplicated().any())

    def test_outputs_and_manifest_have_relative_paths(self) -> None:
        import pandas as pd

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "data" / "processed"
            input_dir.mkdir(parents=True)
            review_path = input_dir / "topic_human_review_fixture.csv"
            terms_path = input_dir / "topic_terms_fixture.csv"
            shutil.copy2(FIXTURE, review_path)
            self.terms.to_csv(terms_path, index=False, encoding="utf-8-sig")
            config = fixture_config()
            review, _ = load_inputs(review_path, terms_path, config)
            result = build_review_sample(review, config)
            paths = write_outputs(
                root, config, review_path, terms_path, result,
                run_time_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
            )
            manifest_text = paths["selection_manifest"].read_text(encoding="utf-8")
            manifest = json.loads(manifest_text)
            self.assertNotIn(str(root), manifest_text)
            self.assertEqual(manifest["random_seed"], 42)
            self.assertFalse(manifest["personal_absolute_paths_present"])
            self.assertEqual(set(paths), {
                "review_sample", "selection_summary", "review_guide", "selection_manifest"
            })
            self.assertTrue(all(not Path(item["path"]).is_absolute() for item in manifest["outputs"]))


if __name__ == "__main__":
    unittest.main()
