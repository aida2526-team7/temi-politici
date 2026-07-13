"""Test del protocollo auditabile di doppia annotazione umana."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.topic_annotation import (
    create_reviewer_files,
    read_csv_exact,
    sha256_file,
    validate_annotation_frame,
    validate_source_sample,
    verify_source_hash,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "topic_annotation_fixture.csv"


def fixture_config() -> dict[str, object]:
    return {
        "input_sample": "data/sample.csv",
        "input_manifest": "data/manifest.json",
        "output_directory": "annotations/topic_human_review",
        "protocol_version": "1.0",
        "reviewer_ids": ["R1", "R2"],
        "calibration_rows": 5,
        "categorie_classificazione": [
            "tema politico coerente", "tema politico misto",
            "boilerplate o formato editoriale", "contenuto non politico", "dubbio",
        ],
        "valori_booleani_ammessi": ["sì", "no", "incerto"],
        "decisioni_inclusione_ammesse": ["mantenere", "escludere", "riesaminare"],
        "encoding": "utf-8-sig",
        "colonne_sorgente_immutabili": [
            "review_id", "source_row_index", "topic_id", "tipo_selezione",
            "selection_rank", "domain", "seendate", "title", "url", "estratto",
            "peso_topic_dominante", "confidenza_topic", "termini_caratteristici",
            "valutazione_preliminare",
        ],
        "colonne_compilabili": [
            "classificazione_umana", "etichetta_tema_proposta", "boilerplate_si_no",
            "duplicato_sospetto_si_no", "decisione_inclusione", "note_revisore",
        ],
    }


class TopicAnnotationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = fixture_config()
        cls.sample = read_csv_exact(FIXTURE, "utf-8-sig")
        validate_source_sample(cls.sample, cls.config)

    def test_source_hash_correct_and_incorrect(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = Path(temporary) / "manifest.json"
            digest = sha256_file(FIXTURE)
            manifest_path.write_text(json.dumps({
                "outputs": [{"path": "data/sample.csv", "sha256": digest}]
            }), encoding="utf-8")
            self.assertEqual(verify_source_hash(FIXTURE, manifest_path, "data/sample.csv"), digest)
            manifest_path.write_text(json.dumps({
                "outputs": [{"path": "data/sample.csv", "sha256": "0" * 64}]
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Hash campione non coincidente"):
                verify_source_hash(FIXTURE, manifest_path, "data/sample.csv")

    def test_two_files_have_27_rows_same_order_and_ids(self) -> None:
        frames = create_reviewer_files(self.sample, self.config)
        self.assertEqual(set(frames), {"R1", "R2"})
        self.assertEqual(len(frames["R1"]), 27)
        self.assertEqual(len(frames["R2"]), 27)
        self.assertEqual(frames["R1"]["review_id"].tolist(), self.sample["review_id"].tolist())
        self.assertEqual(frames["R1"]["review_id"].tolist(), frames["R2"]["review_id"].tolist())

    def test_reviewer_ids_are_distinct_and_constant(self) -> None:
        frames = create_reviewer_files(self.sample, self.config)
        self.assertTrue(frames["R1"]["reviewer_id"].eq("R1").all())
        self.assertTrue(frames["R2"]["reviewer_id"].eq("R2").all())

    def test_first_five_are_calibration_and_rest_independent(self) -> None:
        frame = create_reviewer_files(self.sample, self.config)["R1"]
        self.assertTrue(frame.iloc[:5]["fase_revisione"].eq("calibrazione").all())
        self.assertTrue(frame.iloc[5:]["fase_revisione"].eq("indipendente").all())
        self.assertEqual(int(frame["fase_revisione"].eq("calibrazione").sum()), 5)
        self.assertEqual(int(frame["fase_revisione"].eq("indipendente").sum()), 22)

    def test_human_columns_start_empty(self) -> None:
        frame = create_reviewer_files(self.sample, self.config)["R1"]
        for column in self.config["colonne_compilabili"]:
            self.assertTrue(frame[column].eq("").all())

    def test_source_columns_are_unchanged(self) -> None:
        frame = create_reviewer_files(self.sample, self.config)["R1"]
        for column in self.config["colonne_sorgente_immutabili"]:
            self.assertEqual(frame[column].tolist(), self.sample[column].tolist())

    def test_invalid_category_is_rejected(self) -> None:
        frame = create_reviewer_files(self.sample, self.config)["R1"]
        frame.loc[0, "classificazione_umana"] = "categoria inventata"
        with self.assertRaisesRegex(ValueError, "Valori non ammessi"):
            validate_annotation_frame(frame, self.sample, "R1", self.config, require_complete=False)

    def test_modified_url_title_or_topic_is_detected(self) -> None:
        for column in ("url", "title", "topic_id"):
            with self.subTest(column=column):
                frame = create_reviewer_files(self.sample, self.config)["R1"]
                frame.loc[0, column] = "MODIFICATO"
                with self.assertRaisesRegex(ValueError, f"Colonna sorgente modificata: {column}"):
                    validate_annotation_frame(frame, self.sample, "R1", self.config, require_complete=False)

    def test_incomplete_annotations_are_recognized(self) -> None:
        frame = create_reviewer_files(self.sample, self.config)["R1"]
        with self.assertRaisesRegex(ValueError, "Annotazioni incomplete"):
            validate_annotation_frame(frame, self.sample, "R1", self.config, require_complete=True)

    def test_protocol_version_is_present_and_checked(self) -> None:
        frame = create_reviewer_files(self.sample, self.config)["R1"]
        self.assertTrue(frame["protocol_version"].eq("1.0").all())
        frame.loc[0, "protocol_version"] = ""
        with self.assertRaisesRegex(ValueError, "protocol_version"):
            validate_annotation_frame(frame, self.sample, "R1", self.config, require_complete=False)

    def test_configuration_has_no_personal_paths(self) -> None:
        serialized = json.dumps(self.config, ensure_ascii=False)
        self.assertNotIn("/Users/", serialized)


if __name__ == "__main__":
    unittest.main()
