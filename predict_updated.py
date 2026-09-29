"""Predict one new 18-feature record with the exploratory updated SVM."""
import argparse
import json
from pathlib import Path

import joblib

from src.data import validate_record

LT = {"bus": "autobusas", "opel": "Opel", "saab": "Saab", "van": "furgonas"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON failas su 18 požymių pavadinimais")
    parser.add_argument("--model", default="results/wide_svm_20260928/final_wide_svm.joblib")
    args = parser.parse_args()
    artifact = joblib.load(args.model)
    record = json.loads(Path(args.input).read_text(encoding="utf-8"))
    row = validate_record(record, artifact["feature_names"])
    predicted = artifact["pipeline"].predict(row)[0]
    print(json.dumps({"label": predicted, "label_lt": LT[predicted],
                      "model": "wide_svm_20260928", "params": artifact["params"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
