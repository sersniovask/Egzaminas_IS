"""Predict one new 18-feature silhouette with the saved TabPFN v2 candidate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from tabpfn import TabPFNClassifier

from src.data import validate_record

ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = ROOT / "results" / "further_20260928" / "tabpfn_v2" / "final_tabpfn_v2.tabpfn_fit"
DEFAULT_METADATA = ROOT / "results" / "further_20260928" / "tabpfn_v2" / "final_model_metadata.json"
LT = {"bus": "autobusas", "opel": "Opel", "saab": "Saab", "van": "furgonas"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON failas su tiksliai 18 požymių")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--metadata", type=Path, default=None)
    args = parser.parse_args()
    metadata_path = args.metadata or (DEFAULT_METADATA if args.model == DEFAULT_MODEL else args.model.parent / "final_model_metadata.json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    digest = hashlib.sha256(args.model.read_bytes()).hexdigest()
    if digest != metadata["model_sha256"]:
        raise ValueError("Išsaugoto TabPFN modelio SHA-256 nesutampa su metaduomenimis")
    record = json.loads(Path(args.input).read_text(encoding="utf-8"))
    row = validate_record(record, metadata["feature_names"])
    estimator = TabPFNClassifier.load_from_fit_state(args.model, device="cpu")
    predicted = str(estimator.predict(row)[0])
    print(json.dumps({"label": predicted, "label_lt": LT[predicted],
                      "model": "tabpfn_v2_exploratory",
                      "model_sha256": digest,
                      "openml_md5": metadata["data_md5"],
                      "result_status": "tiriamasis, nepriklausomai nepatvirtintas"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
