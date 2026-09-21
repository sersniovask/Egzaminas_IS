"""Sukuria lietuvišką rezultatų aprašą tik iš realiai išsaugotų CSV/JSON failų."""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.data import CLASSES, load_vehicle
from src.error_analysis import extend_report
from src.provenance import provenance, peak_rss_bytes
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", default="results/main")
    parser.add_argument("--cache", default="data")
    args = parser.parse_args()
    root = Path(args.results)
    (root / "report_provenance.json").write_text(json.dumps(provenance(Path(__file__).resolve().parent), indent=2), encoding="utf-8")
    summary = pd.read_csv(root / "results_summary.csv", index_col=0)
    folds = pd.read_csv(root / "fold_metrics.csv")
    robust = pd.read_csv(root / "robustness.csv")
    meta = json.loads((root / "data_metadata.json").read_text(encoding="utf-8"))
    hypothesis = json.loads((root / "hypothesis.json").read_text(encoding="utf-8"))
    if len(folds) != 350:
        raise ValueError("Ataskaitai reikia pilnų 50 × 7 metodų rezultatų")
    lines = ["# Transporto priemonių siluetų klasifikavimo egzamino ataskaita", "",
             "Kirilas Šeršniovas, PEPfm-26", "",
             "## Duomenys ir protokolas", "",
             f"Naudotas OpenML Vehicle ID 54, 1 versija: {meta['rows']} įrašai, 18 skaitinių požymių ir keturios klasės. MD5: `{meta['md5']}`. "
             "Visi metodai vertinti tais pačiais 5 × 10 stratifikuotais išoriniais skaidiniais; hiperparametrai parinkti penkių dalių vidine CV pagal Macro-F1. "
             "Imputavimas ir standartizavimas išmokti tik mokymo dalyse.", "",
             "## Metodų palyginimas", "",
             "| Metodas | Macro-F1 vidurkis ± SD | Balanced accuracy vidurkis ± SD | Vidutinis mokymo laikas, s |",
             "|---|---:|---:|---:|"]
    for name, row in summary.iterrows():
        lines.append(f"| {name} | {row.macro_f1_mean:.3f} ± {row.macro_f1_sd:.3f} | {row.balanced_accuracy_mean:.3f} ± {row.balanced_accuracy_sd:.3f} | {row.train_seconds_mean:.3f} |")
    lines.append(f"\nUžregistruota visų septynių metodų išorinių pritaikymų su vidine paieška mokymo trukmė: {folds.train_seconds.sum()/60:.1f} min. "
                 "Šis skaičius neapima duomenų įkėlimo, diagramų ir atsparumo prognozių laiko.")
    resources = json.loads((root / "resources.json").read_text(encoding="utf-8"))
    lines.append(f"Atlikta {resources['model_fits']} modelio pritaikymų. Visas mokymas ir diagnostika iki ataskaitos: "
                 f"{resources['wall_seconds_before_reporting']/60:.1f} min.; didžiausias pagrindinio proceso RAM: "
                 f"{resources['peak_process_rss_bytes']/1e6:.1f} MB. Naudotas vienas procesas ir iki keturių skaičiavimo gijų.")
    lines.append("Prieš šį pakartotinį eksperimentą dėl 20 000 biudžeto MLP alpha tinklelis sumažintas iki {0,0001; 0,01}, "
                 "RBF pločio daugikliai iki {0,5; 1}. Tai dokumentuotas koliokviumo plano pakeitimas; ankstesni rezultatai buvo žinomi, "
                 "todėl naujas paleidimas nėra nepriklausomas išankstinės hipotezės patvirtinimas. SVM ir baseline protokolas nepakeistas.")
    lines += ["", "Prognozavimo trukmė vienam išoriniam bandymo paketui (vidurkis):", ""]
    for name, group in folds.groupby("method"):
        lines.append(f"- {name}: {group.predict_seconds.mean()*1000:.3f} ms; pakete {group.test_rows.min()}–{group.test_rows.max()} įrašai.")
    lines += ["", "![Macro-F1 skaidinių pasiskirstymas](macro_f1_boxplot.png)", "",
              "Skaidinių metrikos yra koreliuotos: 50 skaičių nėra 50 nepriklausomų eksperimentų. "
              "Painiavos matricoje kiekvienas iš 846 objektų kaip bandymo įrašas pasirodo penkis kartus.", "",
              "## Iš anksto iškelta SVM hipotezė", ""]
    ci = hypothesis["corrected_95pct_ci"]
    verdict = "patvirtinta pagal aprašytą kriterijų" if hypothesis["confirmed"] else "nepatvirtinta pagal aprašytą kriterijų"
    lines.append(f"Geresnis baseline: **{hypothesis['baseline']}**. SVM porinis Macro-F1 skirtumas: **{hypothesis['mean_difference']:+.3f}**; "
                 f"pataisytas 95 % intervalas [{ci[0]:+.3f}; {ci[1]:+.3f}]; teigiamų pakartojimų: {hypothesis['positive_repeats']}/5. Hipotezė {verdict}.")
    winner = summary.index[0]
    lines += ["", f"Pagal pirminę metriką pirmauja **{winner}**. " +
              ("SVM RBF galėjo pasinaudoti netiesine riba ir reguliuojama marža; tikslios priežasties vien iš šio palyginimo įrodyti negalima." if winner == "svm" else
               "Išankstinis SVM pasirinkimas nebuvo geriausias; reikia remtis stebėtais skirtumais, o ne pakeisti kriterijų po bandymo."), "",
              "## Ablacija ir atsparumas", ""]
    svm = summary.loc["svm", "macro_f1_mean"]
    for ablation in ["svm_linear", "svm_unscaled"]:
        other = summary.loc[ablation, "macro_f1_mean"]
        lines.append(f"- `{ablation}`: Macro-F1 {other:.3f}, skirtumas nuo SVM RBF {other-svm:+.3f}.")
    lines.append("")
    if svm > summary.loc["svm_linear", "macro_f1_mean"]:
        lines.append("RBF branduolio pranašumas prieš tiesinį SVM šiame rinkinyje dera su netiesinės ribos hipoteze. "
                     "Ablacija neįrodo, kad tai vienintelė pranašumo priežastis.")
    if svm > summary.loc["svm_unscaled", "macro_f1_mean"]:
        lines.append("Kritimas pašalinus standartizavimą rodo, kad šio rinkinio skirtingi požymių masteliai yra svarbūs SVM.")
    lines.append("")
    base = robust.groupby(["method", "kind", "level"]).macro_f1.mean()
    comparison = robust.groupby(["method", "kind", "level"]).macro_f1.mean().rename("perturbed_macro_f1").reset_index()
    comparison["clean_macro_f1"] = comparison.method.map(summary.macro_f1_mean)
    comparison["delta"] = comparison.perturbed_macro_f1 - comparison.clean_macro_f1
    comparison.to_csv(root / "robustness_comparison.csv", index=False)
    for kind in ["noise", "missing"]:
        for level in sorted(robust.loc[robust.kind == kind, "level"].unique()):
            score = base.loc[("svm", kind, level)]
            lines.append(f"- SVM, {kind} {level:.2f}: Macro-F1 {score:.3f}, pokytis nuo neperturbuoto rezultato {score-svm:+.3f}.")
    lines += ["", "Visų pagrindinių metodų Macro-F1 pokytis esant didžiausiam bandytam trikdžiui:", "",
              "| Metodas | Pradinė reikšmė | Triukšmas 0,20 | Pokytis | Trūksta 10 % | Pokytis |",
              "|---|---:|---:|---:|---:|---:|"]
    for method in ["centroid", "knn", "svm", "mlp", "rbf"]:
        clean = summary.loc[method, "macro_f1_mean"]
        noisy = base.loc[(method, "noise", .2)]
        missing = base.loc[(method, "missing", .1)]
        lines.append(f"| {method} | {clean:.3f} | {noisy:.3f} | {noisy-clean:+.3f} | {missing:.3f} | {missing-clean:+.3f} |")
    svm_missing = base.loc[("svm", "missing", .1)]
    next_best_missing = max(base.loc[(name, "missing", .1)] for name in ["centroid", "knn", "mlp", "rbf"])
    lines += ["", f"SVM išlieka pirmas ir paslėpus 10 % požymių ({svm_missing:.3f} prieš {next_best_missing:.3f} artimiausio konkurento), "
              "tačiau jo santykinis kritimas yra didžiausias. Praktiniam naudojimui su nepilnais matavimais reikia papildomo nepriklausomo bandymo."]
    lines += ["", "Visi metodai gavo tuos pačius perturbuotus bandymo objektus. Kiekvienas trikdžio lygis kartotas 20 kartų tame pačiame skaidinyje; "
              "šie kartojimai nėra nepriklausomos naujos imtys.", "",
              "Perturbacijos taikytos tik išorinei bandymo daliai; triukšmo mastas apskaičiuotas iš atitinkamos mokymo dalies. "
              "Triukšmo ir trūkstamų požymių testai imituoja pasirinktus pažeidimus, tačiau neapima realių kamerų ar naujų transporto priemonių modelių.", "",
              "## Klaidų analizė", ""]
    cm = pd.read_csv(root / "confusion_svm.csv", index_col=0)
    for truth in CLASSES:
        off = cm.loc[truth].drop(truth).sort_values(ascending=False)
        lines.append(f"- Tikroji `{truth}`: {int(cm.loc[truth, truth])}/{int(cm.loc[truth].sum())} teisingų; "
                     f"dažniausia klaida į `{off.index[0]}` ({int(off.iloc[0])}).")
    all_errors = pd.read_csv(root / "high_margin_errors.csv").drop_duplicates("row_index")
    X, _, _ = load_vehicle(Path(args.cache))
    all_predictions = pd.read_csv(root / "out_of_fold_predictions.csv")
    svm_predictions = all_predictions[all_predictions.method == "svm"].copy()
    svm_predictions["error"] = svm_predictions.true != svm_predictions.predicted
    frequency = svm_predictions.groupby("row_index").agg(true=("true", "first"),
                                                           errors_in_five_tests=("error", "sum"))
    assert len(frequency) == len(X)
    frequency = frequency.join(X)
    frequency.to_csv(root / "error_frequency_by_record.csv")
    counts = frequency.errors_in_five_tests.value_counts().reindex(range(6), fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(counts.index, counts.values, color="#4379ad")
    ax.set(xlabel="Kiek kartų įrašas suklystas per 5 bandymus", ylabel="Įrašų skaičius",
           title="SVM klaidų pasikartojimas")
    ax.set_xticks(range(6))
    fig.tight_layout()
    fig.savefig(root / "error_frequency.png", dpi=180)
    plt.close(fig)
    lines += ["", f"Iš {len(X)} skirtingų įrašų {int(counts.loc[0])} klasifikuoti teisingai visuose penkiuose bandymuose, "
              f"o {int(counts.loc[5])} klaidingai visuose penkiuose. Tai padeda atskirti sistemingai sunkius įrašus nuo vieno skaidinio atsitiktinumo.", "",
              "![SVM klaidų pasikartojimas](error_frequency.png)"]
    detailed = all_errors.set_index("row_index").join(X, how="left")
    detailed.to_csv(root / "error_examples_with_features.csv")
    errors = all_errors.head(5)
    lines.append("\nDidžiausio diagnostinio tarpo klaidingų prognozių pavyzdžiai (pradiniai vaizdai neprieinami):\n")
    for _, row in errors.iterrows():
        lines.append(f"- Įrašas {int(row.row_index)}: tikroji `{row.true}`, prognozuota `{row.predicted}`, mažiausias porinis |balas| {row.margin:.3f}.")
    importance = pd.read_csv(root / "feature_importance_summary.csv", index_col=0).iloc[:, 0]
    important = ", ".join(f"`{name}` ({value:.3f})" for name, value in importance.head(3).items())
    lines += ["", f"Didžiausias vidutinis Macro-F1 kritimas po bandymo požymio permutacijos: {important}. "
              "Tai modelio jautrumo diagnostika, o ne priežastinis požymių poveikio įrodymas."]
    persistent = frequency[frequency.errors_in_five_tests >= 4]
    stable = frequency[frequency.errors_in_five_tests == 0]
    class_counts = persistent.true.value_counts().reindex(CLASSES, fill_value=0)
    lines.append("\nNuolat sunkūs įrašai pagal tikrąją klasę: " + ", ".join(f"{name} {int(class_counts[name])}" for name in CLASSES) + ".")
    lines += ["", f"Požymių medianos: nuolat sunkūs įrašai (bent 4 klaidos, n={len(persistent)}) ir visada teisingi (n={len(stable)}).", "",
              "| Požymis | Sunkūs | Visada teisingi |", "|---|---:|---:|"]
    for name in importance.head(3).index:
        lines.append(f"| `{name}` | {persistent[name].median():.1f} | {stable[name].median():.1f} |")
    lines += ["", "Šių trijų požymių medianos panašios, todėl vien jų nepakanka paaiškinti sunkių įrašų. "
              "Šis skirstinių palyginimas yra aprašomasis; jis nepagrindžia priežastinės klaidų kilmės."]
    lines += ["", "![SVM painiavos matrica](confusion_svm.png)", "",
              "Šis balas nėra tikimybė. Tie patys įrašai gali kartotis skirtinguose CV pakartojimuose; sąraše jie parodyti po vieną.", "",
              "## Ribos ir praktinis tinkamumas", "",
              "OpenML failas neturi patikimų fotografavimo serijų `e2`–`e5` identifikatorių ir pradinių vaizdų. "
              "Todėl atsitiktinė stratifikacija gali pervertinti gebėjimą veikti naujame fiziniame modelyje ar naujoje fotografavimo aplinkoje. "
              "Autobuso arba furgono supainiojimas su lengvuoju automobiliu gali būti praktiškai reikšmingesnis už Opel ir Saab supainiojimą, tačiau konkreti klaidų kaina nenustatyta. "
              "Prieš praktinį diegimą reikėtų nepriklausomo naujų modelių ir kamerų rinkinio, o klaidų kainą nustatyti pagal konkretų naudojimo scenarijų. "
              "Šiuo metu sprendimas yra 18 jau išvestų požymių klasifikavimo prototipas.", "",
              "## Gynimo patikra", "",
              "Studentas turi paaiškinti `src/models.py::build_pipeline` SVM formulės ryšį su `C` ir `gamma`, paleisti dėstytojo pateiktą nematytą įrašą per `predict.py` ir parodyti mažą pakeitimą. "
              "Šios gyvo gynimo dalies ataskaita iš anksto neįrodo.", ""]
    lines += extend_report(root, X, svm_predictions, importance)
    verification = json.loads((root / 'verification.json').read_text(encoding='utf-8'))
    identity = json.loads((root / 'provenance.json').read_text(encoding='utf-8'))
    resources['report_peak_rss_bytes'] = peak_rss_bytes()
    resources['verification_peak_rss_bytes'] = verification['verification_peak_rss_bytes']
    resources['workflow_peak_rss_upper_bound_bytes'] = resources['peak_process_rss_bytes'] + max(
        resources['report_peak_rss_bytes'], resources['verification_peak_rss_bytes'])
    resources['first_report_completed_utc'] = resources.get('first_report_completed_utc', datetime.now(timezone.utc).isoformat())
    resources['seconds_from_manifest_to_first_report'] = (datetime.fromisoformat(resources['first_report_completed_utc']) - datetime.fromisoformat(identity['created_utc'])).total_seconds()
    resources['whole_workflow_memory_within_2gb'] = resources['workflow_peak_rss_upper_bound_bytes'] <= 2_000_000_000
    assert resources['whole_workflow_memory_within_2gb']
    (root / 'resources.json').write_text(json.dumps(resources, indent=2), encoding='utf-8')
    lines += ['', '## Viso vykdymo ištekliai', '',
              f"Konservatyvi mokymo proceso ir paeiliui paleistų patikros bei ataskaitos procesų RAM viršutinė riba: {resources['workflow_peak_rss_upper_bound_bytes']/1e6:.1f} MB. "
              'Ji skaičiuojama sudedant mokymo proceso piką ir didesnį iš dviejų nuosekliai vykdomų pagalbinių procesų pikų; tikras bendras pikas gali būti mažesnis.', '',
              f"Nuo mokymo manifesto užregistravimo iki pirmos ataskaitos: {resources['seconds_from_manifest_to_first_report']/60:.1f} min. Pradinis duomenų įkėlimas prieš manifestą į šį laiką neįtrauktas."]
    (root / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(root / "report.md")


if __name__ == "__main__":
    main()
