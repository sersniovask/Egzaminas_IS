"""Append a reproducible follow-up study to the existing exam PDF."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from PIL import Image as PILImage


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "Egzamino_ataskaita_atnaujinta_2026-09-28.pdf"
OUT = ROOT / "Egzamino_ataskaita_papildyti_bandymai_2026-09-28.pdf"
APPENDIX = ROOT / "tmp" / "further_experiments_appendix.pdf"
RESULTS = ROOT / "results" / "further_20260928"

FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("ArialLT", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialLT-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFontFamily("ArialLT", normal="ArialLT", bold="ArialLT-Bold")
NAVY = colors.HexColor("#17324f")
BLUE = colors.HexColor("#27618e")
INK = colors.HexColor("#23313e")
PALE = colors.HexColor("#edf3f8")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BTitle", fontName="ArialLT-Bold", fontSize=17,
                          leading=22, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="BH1", fontName="ArialLT-Bold", fontSize=11,
                          leading=15, textColor=BLUE, spaceBefore=11,
                          spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name="BBody", fontName="ArialLT", fontSize=9,
                          leading=13, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="BSmall", fontName="ArialLT", fontSize=7.5,
                          leading=10.5, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="BHead", fontName="ArialLT-Bold", fontSize=7.5,
                          leading=10, textColor=colors.white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="BCell", fontName="ArialLT", fontSize=7.5,
                          leading=10, textColor=INK, alignment=TA_CENTER))


def load(name):
    return json.loads((RESULTS / name / "summary.json").read_text(encoding="utf-8"))


def f(x):
    return f"{x:.3f}".replace(".", ",")


def clean(value):
    return escape(str(value).replace("–", "-").replace("—", "-").replace("−", "-"))


story = []


def p(value, style="BBody"):
    story.append(Paragraph(clean(value), styles[style]))


def h(value):
    p(value, "BH1")


def table(headers, rows, widths):
    values = [[Paragraph(clean(c), styles["BHead"]) for c in headers]]
    values += [[Paragraph(clean(c), styles["BCell"]) for c in row] for row in rows]
    t = Table(values, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9d9d9")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 7))


def figure(name, caption):
    path = ROOT / "report_assets" / name
    with PILImage.open(path) as source:
        width, height = source.size
    target_width = 505
    story.append(Image(str(path), width=target_width,
                       height=target_width * height / width, hAlign="CENTER"))
    p(caption, "BSmall")


def main():
    for chart in ("further_paired_differences.png", "further_confusion_comparison.png"):
        if not (ROOT / "report_assets" / chart).exists():
            raise FileNotFoundError(f"Pirmiausia paleiskite build_further_charts.py: {chart}")
    results = {name: load(name) for name in ["svm_extended", "extra_trees", "tabpfn_v2"]}
    if any(value["completed_splits"] != 50 for value in results.values()):
        raise RuntimeError("Visi 50 kiekvieno metodo skaidinių turi būti baigti")
    diag = json.loads((RESULTS / "diagnosis" / "summary.json").read_text(encoding="utf-8"))
    specialist = json.loads((ROOT / "results" / "improvement_20260928" / "summary.json").read_text(encoding="utf-8"))["improved"]
    with (ROOT / "results" / "improvement_20260928" / "confusion_improved.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        specialist_confusion = list(csv.reader(handle))
    specialist_cross = int(specialist_confusion[2][3]) + int(specialist_confusion[3][2])
    baseline = results["svm_extended"]
    variants = [
        ("Pradinis SVM", baseline["original"]),
        ("Ankstesnis platesnis SVM", baseline["wide_svm"]),
        ("Dar platesnis SVM", results["svm_extended"]["svm_extended"]),
        ("ExtraTrees", results["extra_trees"]["extra_trees"]),
        ("TabPFN v2", results["tabpfn_v2"]["tabpfn_v2"]),
    ]
    best_name, best = max(variants, key=lambda row: row[1]["mean_outer_fold_macro_f1"])
    p("B priedas. Papildomi automobilių klasių atskyrimo bandymai", "BTitle")
    p("2026 m. rugsėjo 28-29 d. tiriamasis tęsinys. Pagrindinės ataskaitos 1-11 skyrių ir A priedo "
      "rezultatai palikti nepakeisti. Čia pateikiami trys nauji bandymai, atlikti jau žinant "
      "ankstesnių bandymų išorinių testų rezultatus. Todėl skaičiai aprašo šį rinkinį, bet "
      "nėra nepriklausomas naujo metodo pranašumo patvirtinimas.")
    h("Uždavinio ir duomenų ribos")
    p("OpenML Vehicle v1 turi 846 įrašus, keturias klases ir 18 iš modelinių transporto "
      "priemonių siluetų apskaičiuotų formos požymių. Įvestyje nėra pradinių pikselių ar "
      "patikimų rakurso žymų; jų iš 18 skaičių neatkursime. UCI aprašas patvirtina, kad "
      "naudoti modeliniai autobusas, furgonas, Opel Manta 400 ir Saab 9000. Darbo išvadų "
      "negalima perkelti į realaus kelių eismo vaizdų atpažinimą.")
    h("Metodai ir apsauga nuo duomenų nutekėjimo")
    p("Visiems trims naujiems metodams atkurti tie patys 5 kartus kartoti 10 dalių "
      "stratifikuoti išoriniai skaidiniai. SVM derina C iš {100; 1000; 10000} ir gamma "
      "iš {0,003; 0,01; 0,03; scale}; ExtraTrees - 150 medžių, max_features iš {sqrt; visi} "
      "ir min_samples_leaf iš {1; 2; 4}. Abiem parametrus parenka penkių dalių vidinė "
      "kryžminė patikra pagal Macro-F1. Medianų pildymas ir SVM standartizavimas yra "
      "mokymo grandinėje. TabPFN v2 su 4 ansamblio įvertinimais tiesiogiai pritaikomas "
      "kiekvienos išorinės mokymo dalies 18 požymių. Šis modelis iš anksto išmokytas "
      "kitais sintetiniais duomenimis; jo svoriai yra papildomas metodinis išteklius.")
    p("Kiekvieno naujo modelio 50 JSON kontrolinių taškų saugo išorinio testo indeksus, "
      "tiesos žymas, prognozes, sėklą, parinktus parametrus ir trukmę. "
      "summarize_next_20260928.py patikrina indeksų ir žymų sutapimą su ankstesniu SVM, "
      "perskaičiuoja F1 iš prognozių ir sudaro painiavos matricas. Testo objektai "
      "nepatenka į to skaidinio modelio mokymą.")
    h("Palyginimas ant 50 išorinių testų")
    rows = [["Opel-Saab specialistas", f(specialist["macro_f1_fold_mean"]),
             f(specialist["per_class"]["opel"]["f1"]),
             f(specialist["per_class"]["saab"]["f1"]), str(specialist_cross)]]
    for name, data in variants:
        rows.append([name, f(data["mean_outer_fold_macro_f1"]),
                     f(data["per_class_pooled"]["opel"]["f1"]),
                     f(data["per_class_pooled"]["saab"]["f1"]),
                     str(data["opel_saab_cross_errors"])])
    rows.insert(0, rows.pop(1))  # Pradinis SVM pirmas, tada nepavykęs specialistas.
    table(["Metodas", "Macro-F1", "Opel F1", "Saab F1", "Opel-Saab klaidos"],
          rows, [190, 75, 75, 75, 90])
    p("Macro-F1 - skaidinių vidurkis. Klasių F1 ir poros klaidos - iš sujungtų penkių "
      "kartojimų prognozių; kiekvienas 846 įrašų ten pasirodo po penkis kartus. "
      "Paskutinis stulpelis nėra skirtingų objektų skaičius.", "BSmall")
    p(f"Didžiausias stebėtas Macro-F1 šiame rinkinyje: {best_name} ({f(best['mean_outer_fold_macro_f1'])}). "
      "Modelių reitingas pasirinktas jau matant šių pačių testų balus, todėl negalima "
      "jo pateikti kaip patvirtinto naujo bendrinimo rezultato.")
    tab = results["tabpfn_v2"]
    p("TabPFN ypač sumažino autobusų ir furgonų klaidas, tačiau specifinė "
      f"Opel-Saab painiava liko: {tab['tabpfn_v2']['opel_saab_cross_errors']} "
      f"tarpusavio klaidos prieš {tab['wide_svm']['opel_saab_cross_errors']} "
      "ankstesnio platesnio SVM. Todėl didesnis bendras Macro-F1 nereiškia, "
      "kad dviejų automobilių atskyrimo uždavinys išspręstas.")

    h("Kaip buvo tobulintas sprendimas")
    p("Pradinio SVM Opel ir Saab tarpusavio klaidos sudarė 563 iš 671 visų klaidų. "
      "Pirmiausia mokymo dalyje derintas atskiras porinis Opel-Saab klasifikatorius, "
      "kuris tikslino SVM automobilių prognozes. Jis padidino šios poros klaidų "
      f"skaičių iki {specialist_cross} ir sumažino Macro-F1 iki "
      f"{f(specialist['macro_f1_fold_mean'])}, todėl variantas atmestas.")
    p("Tada tikrinta 12 arba 18 požymių atranka ir didesnės SVM C reikšmės; atranka "
      "visuose 50 išorinių mokymų pasirinko visus 18 požymių, o platesnė C paieška "
      "pakėlė Macro-F1 nuo 0,842 iki 0,852. Tai tiriamasis skaitinis pagerėjimas, "
      "kurio pataisytas skirtumo intervalas apima nulį. Dar padidinus C ribą iki "
      "10000 rodiklis sumažėjo iki 0,849. Šis neigiamas bandymas parodė, kad "
      "paprastas paieškos intervalo plėtimas nebūtinai padeda.")
    p("Toliau išbandytas 150 atsitiktinai skaidomų medžių ExtraTrees ansamblis su "
      "vidiniu lapo dydžio ir požymių skaičiaus derinimu. Macro-F1 0,755 ir "
      "839 Opel-Saab tarpusavio klaidos reiškia aiškų pablogėjimą; ansamblis "
      "nepasirinktas. TabPFN v2, naudodamas oficialius iš anksto išmokytus svorius, "
      "pasiekė 0,869 ir pagerino bendrą klasifikavimą. Vis dėlto prieš platesnį "
      "SVM Opel-Saab klaidų buvo trimis daugiau, tad šis bandymas nepagrindžia "
      "teiginio, kad svarbiausia automobilių atskyrimo problema išspręsta.")

    h("Naujų bandymų grafikai")
    figure("further_paired_differences.png",
           "6 pav. Kiekvienas taškas - vieno iš 50 tų pačių išorinių testų Macro-F1 "
           "skirtumas nuo ankstesnio platesnio SVM; rombas - vidurkis. Tie patys 846 "
           "įrašai kartojasi penkis kartus, todėl taškai nėra nepriklausomi bandymai.")
    p("TabPFN vidutiniškai laimi, bet ne kiekviename skaidinyje: 31 geresnis ir 19 "
      "blogesnių. Papildomas SVM C plėtimas dažniausiai nekeitė arba blogino "
      "rezultatą, o ExtraTrees beveik visuose skaidiniuose atsiliko. Grafikas "
      "papildo vidurkių lentelę, nes rodo rezultatų sklaidą, ne vieną skaičių.")
    figure("further_confusion_comparison.png",
           "7 pav. Ankstesnio platesnio SVM ir TabPFN v2 painiavos matricos iš "
           "tų pačių 4230 išorinių prognozių. Langelyje - prognozių skaičius "
           "ir eilutės procentas; raudonai apibrėžta Opel-Saab pora.")
    p("TabPFN autobusų teisingų prognozių skaičių padidino nuo 1063 iki 1084, "
      "furgonų - nuo 953 iki 988. Tačiau Opel-Saab kryžminių klaidų suma "
      "pasikeitė nuo 522 iki 525. Šitaip grafikas paaiškina, kodėl geresnis "
      "bendras Macro-F1 nereiškia tikslinio automobilių poros atskyrimo.")

    h("Kiek keitėsi rezultatas ir kokie parametrai laimėjo")
    for name, label in [("svm_extended", "Didesnis SVM tinklelis"),
                        ("extra_trees", "ExtraTrees"),
                        ("tabpfn_v2", "TabPFN v2")]:
        s = results[name]
        delta = s["versus_wide_svm"]["mean_paired_difference"]
        ci = s["versus_wide_svm"]["corrected_95pct_interval_descriptive"]
        car_delta = s["versus_wide_svm"]["mean_paired_car_f1_difference"]
        car_ci = s["versus_wide_svm"]["corrected_95pct_car_interval_descriptive"]
        p(f"{label}: porinis Macro-F1 pokytis prieš ankstesnį platesnį SVM "
          f"{delta:+.3f}; geresnis {s['versus_wide_svm']['better_splits']}, "
          f"lygus {s['versus_wide_svm']['equal_splits']}, blogesnis "
          f"{s['versus_wide_svm']['worse_splits']} iš 50 skaidinių. "
          f"Apytikslis pataisytas 95 % intervalas [{ci[0]:+.3f}; {ci[1]:+.3f}] "
          f"Automobilių klasių F1 vidurkio pokytis {car_delta:+.3f}, intervalas "
          f"[{car_ci[0]:+.3f}; {car_ci[1]:+.3f}]. Intervalai tik aprašomieji, "
          "nes metodai parinkti jau matant ankstesnius testus.")
    c_counts = Counter()
    for encoded, count in results["svm_extended"]["parameter_counts"].items():
        c_counts[json.loads(encoded)["model__C"]] += count
    p(f"Naujame SVM tinklelyje C=100 laimėjo {c_counts[100]}, C=1000 - "
      f"{c_counts[1000]}, C=10000 - {c_counts[10000]} kartų. Net jei didesnė C "
      "riba kartais parenkama, ji nepagerino bendro išorinio Macro-F1 prieš ankstesnį "
      "platesnį SVM. Todėl vien tolesnis C didinimas nėra pakankamai pagrįstas.")
    tree_counts = Counter()
    for encoded, count in results["extra_trees"]["parameter_counts"].items():
        tree_counts[json.loads(encoded)["model__min_samples_leaf"]] += count
    p("ExtraTrees min_samples_leaf laimėtojai: " + ", ".join(
        f"{k} - {tree_counts[k]}/50" for k in [1, 2, 4]) +
      ". Šie dažniai aprašo vidinės paieškos pasirinkimus, o ne išorinės naudos įrodymą.")

    h("Klaidų struktūra ir tolesnis duomenų poreikis")
    p(f"Pradiniame SVM {diag['persistent_errors_all_classes']} įrašas buvo klaidingas "
      f"visuose penkiuose pakartojimuose, iš jų {diag['persistent_car_errors']} - "
      "Opel arba Saab. Atliekant tik aprašomąją viso rinkinio kaimynų analizę, "
      f"{diag['persistent']['opposite_closer_fraction']*100:.1f} % šių automobilių "
      "arčiausias kitos klasės kaimynas buvo arčiau negu savos klasės; tarp "
      f"nė karto neklydusių automobilių - {diag['never_wrong']['opposite_closer_fraction']*100:.1f} %. "
      "Identiškų požymių eilučių nėra. Analizė naudoja visas žymas tik diagnostikai; "
      "ji nenaudota modelio mokymui ir neįrodo, kad kurios nors žymos klaidingos.")
    p("Naujų ženklintų siluetų negavome, todėl jų neišgalvojome ir nedauginome senų "
      "įrašų kaip tariamai nepriklausomų pavyzdžių. Vertingiausias tolesnis bandymas "
      "būtų surinkti naujus Opel ir Saab modelių siluetus su rakurso žymomis arba gauti "
      "pradinius vaizdus. Iš anksto fiksuotas, pagal objektą ir rakursą grupuotas "
      "nepriklausomas testas leistų patikrinti tikrą naudą.")
    h("Atkūrimas ir šaltiniai")
    p("Komandos: python diagnose_persistent_cars.py; python experiment_next_20260928.py "
      "svm_extended; analogiškai extra_trees ir tabpfn_v2; python "
      "summarize_next_20260928.py. TabPFN paleisti .venv_tabpfn aplinkoje. "
      "Kontroliniai taškai ir suvestinės: results/further_20260928/. "
      "TabPFN v2 tyrimas: Hollmann ir kt., Nature (2025), DOI "
      "10.1038/s41586-024-08328-6. Duomenų aprašas: UCI Statlog Vehicle "
      "Silhouettes, DOI 10.24432/C5HG6N. Ankstesni du 2024 m. tyrimai ir "
      "jų taikymo ribos pateikti pagrindinės ataskaitos 10 skyriuje.", "BSmall")

    APPENDIX.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(APPENDIX), pagesize=A4, leftMargin=44,
                            rightMargin=44, topMargin=48, bottomMargin=42,
                            title="Papildomi automobilių atpažinimo bandymai")

    def page(canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setFont("ArialLT", 7.5)
        canvas.setFillColor(colors.HexColor("#607182"))
        canvas.drawString(44, height - 28, "Kirilas Šeršniovas | Papildomi automobilių klasių bandymai")
        canvas.drawRightString(width - 44, 26, f"B priedas - {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=page, onLaterPages=page)
    writer = PdfWriter()
    writer.append(PdfReader(str(BASE)))
    writer.append(PdfReader(str(APPENDIX)))
    with OUT.open("wb") as handle:
        writer.write(handle)
    print(OUT)


if __name__ == "__main__":
    main()
