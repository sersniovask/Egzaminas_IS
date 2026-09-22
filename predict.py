"""Vieno nematyto 18 požymių JSON įrašo klasifikavimas gynimo metu."""
import argparse
import json
from pathlib import Path

import joblib

from src.data import validate_record

LT = {"bus": "autobusas", "opel": "Opel", "saab": "Saab", "van": "furgonas"}


# Perskaito vieną JSON įrašą, patikrina jo schemą ir pritaiko išsaugotą grandinę.
# Išveda klasę, modelio versiją ir diagnostinius porinius balus; modelio nemoko.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="results/main/final_svm.joblib")
    parser.add_argument("--input", required=True, help="JSON failas su 18 požymių pavadinimais")
    args = parser.parse_args()
    artifact = joblib.load(args.model)
    record = json.loads(Path(args.input).read_text(encoding="utf-8"))
    row = validate_record(record, artifact["feature_names"])
    prediction = artifact["pipeline"].predict(row)[0]
    distances = artifact["pipeline"].decision_function(row)[0]
    print(json.dumps({"model_version": artifact["model_version"], "code_sha256": artifact["code_sha256"], "label": prediction, "label_lt": LT[prediction],
                      "ovo_decision_values": distances.tolist(),
                      "openml_md5": artifact["openml_md5"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
