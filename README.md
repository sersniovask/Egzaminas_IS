# Transporto priemonių siluetų klasifikavimas

Šis projektas pagal 18 skaitinių silueto požymių klasifikuoja keturias klases: `bus`, `opel`, `saab` ir `van`. Pradinių nuotraukų rinkinyje nėra. Pagrindiniame aplanke paliktas dabar naudojamas kodas, naujausi pateikimo dokumentai ir jų rezultatų įrodymai; senos versijos sudėtos į `old/`.

## Nuo ko pradėti

1. **Pateikimui:** atverkite `Egzamino_ataskaita_papildyti_bandymai_2026-09-28.pdf` ir `Kirilas_Sersniovas_Kolokviumo_planas_papildyti_bandymai_2026-09-28.pdf`. To paties kolokviumo plano redaguojamas šaltinis yra `.docx` failas tuo pačiu baziniu pavadinimu. Šie trys failai yra naujausios versijos.
2. **Rezultatų patikrai be mokymo:** projekto aplanke paleiskite `.\START.cmd --verify-further`. Komanda patikrina tris naujausius modelius, kiekvieno 50 išorinių skaidinių ir 4230 prognozių.
3. **Naujam įrašui:** paruoškite JSON failą su tiksliais 18 požymių pavadinimais iš `results/main/data_metadata.json` ir paleiskite `.\START.cmd --predict-tabpfn "C:\kelias\irasas.json"`. Tai pritaiko išsaugotą tiriamąjį TabPFN v2 modelį. Pavyzdinio mokymo įrašo prognozė nėra nepriklausomas kokybės testas.
4. **Kodo supratimui:** skaitykite `KODO_GIDAS.md`, tada `src/data.py`, `src/models.py` ir `experiment_next_20260928.py`. Pradinis septynių variantų eksperimentas aprašytas `run_experiment.py`.

Dukart paspaudus `START.cmd`, pasirinkimas **1** atidaro JupyterLab, **2** iš naujo paleidžia tik pradinį eksperimentą ir perrašo `results/main/`, **3** patikrina jau išsaugotus naujų bandymų rezultatus, **4** prognozuoja vieną naują įrašą su TabPFN v2. Prieš renkantis 2 verta pasidaryti rezultatų kopiją. Pirmą kartą paleidžiant gali būti įdiegtos priklausomybės; TabPFN reikalinga atskira aplinka ir oficialūs modelio svoriai. Daugiau apie paleidimą yra `PALEIDIMAS_IR_GITHUB.md`.

## Dabartinio projekto žemėlapis

| Kur | Kam naudojama dabar |
|---|---|
| `START.cmd`, `start_jupyter.py`, `requirements.txt`, `requirements_tabpfn_v2_lock.txt` | Paleidimas ir dviejų Python aplinkų priklausomybės. Vietinė `.venv/` skirta pagrindiniam kodui; TabPFN naudojama `.venv_tabpfn/` arba šiame kompiuteryje jau esanti bendra TabPFN aplinka. |
| `data/vehicle.arff`, `src/data.py`, `configs/main.yaml`, `src/models.py` | Duomenų šaltinis, 18 požymių schema, pradiniai modeliai ir jų parametrai. `src/` taip pat turi rezultatų, klaidų bei grafikų funkcijas. |
| `run_experiment.py`, `verify_results.py`, `build_report.py` | Pradinis vienodų 50 išorinių skaidinių eksperimentas, jo techninė patikra ir tekstinė suvestinė. Pasirinkimas 2 naudoja šią eigą. |
| `tune_svm.py`, `improve_cars.py`, `verify_improvement.py`, `audit_training.py`, `diagnose_persistent_cars.py` | Ataskaitoje aptartų SVM derinimo, Opel–Saab specialisto, mokymo parametrų ir klaidų diagnostikos bandymų atkūrimas. Tai nėra automatiškai vykdoma `START.cmd` 2 pasirinkimu. |
| `experiment_next_20260928.py`, `summarize_next_20260928.py`, `verify_next_20260928.py` | Papildomi dar platesnio SVM, ExtraTrees ir TabPFN v2 bandymai; kiekvieno skaidinio rezultatai išsaugomi atskirai, vėliau suvedami ir patikrinami. |
| `fit_final_tabpfn.py`, `predict_tabpfn.py` | Visais 846 įrašais pritaikytas TabPFN kandidatas ir vieno naujo įrašo prognozė. `predict.py` taiko pradinį SVM, `predict_updated.py` – ankstesnį platesnį SVM, jei gynime reikia palyginimo. |
| `00_REZULTATU_SANTRAUKA.ipynb`, `svm_alternatyva.ipynb`, `mlp_alternatyva.ipynb`, `rbf_alternatyva.ipynb` | Pradinio eksperimento sąsiuviniai. Naujausi TabPFN ir ExtraTrees rezultatai pateikti galutiniame PDF, o ne šiuose sąsiuviniuose. `make_notebooks.py` kviečia `make_result_notebooks.py` jų išvestims atnaujinti. |
| `build_exam_pdf.py`, `build_further_charts.py`, `build_further_exam_pdf.py` | Naujausios egzamino ataskaitos atkūrimas iš išsaugotų rezultatų. `build_updated_plan.py` ir `build_further_plan.py` sudaro naujausią kolokviumo DOCX. `report_assets/` turi naudojamus šaltinius ir grafikų paveikslus. |
| `results/main/` | Pradinio eksperimento prognozės, metrikos, painiavos matricos, modelis ir patikros failai. |
| `results/improvement_20260928/`, `results/wide_svm_20260928/`, `results/training_audit_20260928/`, `results/further_20260928/` | Ataskaitos tobulinimo bandymų įrodymai. `results/further_20260928/tabpfn_v2/` yra ir galutinis tiriamasis modelis. |
| `tests/`, `audit/training_sources/` | Techniniai testai ir originalių mokymo failų kontrolinis archyvas, reikalingas kodo kilmės patikrai. |

## Kur skaityti paaiškinimus

`KODO_GIDAS.md` paaiškina mokymo grandinę, metrikas ir kodo vietas. `ATNAUJINIMAS_2026-09-28.md` aprašo literatūrą, pirmuosius tobulinimo bandymus ir skaitinį metrikų pavyzdį. `plano_patikslinimai.md` saugo prieš pakartotinį pradinio eksperimento vykdymą užregistruotą strategijos pakeitimą. `TESTINIO_EKSPERIMENTO_TESIMAS_2026-09-28.md` pateikia papildomų eksperimentų tęstinumo komandas. `vertinimo_atitiktis.md` sieja egzamino kriterijus su įrodymais. `ai_log.md` registruoja priimtus ir atmestus DI pasiūlymus; `AI_POKALBIU_ISTORIJA.md` saugo pokalbių tekstą ir aiškiai pažymėtas vėlesnių etapų santraukas. `PALEIDIMAS_IR_GITHUB.md` skirtas greitam paleidimui ir GitHub Desktop veiksmams.

## Kaip skaityti rezultatus

Pradinis SVM pasiekė **0,842** Macro-F1, ankstesnis platesnis SVM **0,852**, dar platesnis SVM **0,849**, ExtraTrees **0,755**, TabPFN v2 **0,869**. Šie skaičiai gauti iš išorinių testavimo skaidinių, ne iš mokymo prognozių. TabPFN bendrą rezultatą pagerino, bet Opel ir Saab tarpusavio supainiojimų buvo **525**, palyginti su **522** platesnio SVM. Vėlesni bandymai yra tiriamieji: jų idėjos parinktos jau mačius ankstesnių tų pačių testų rezultatus, todėl nepriklausomo naujo rinkinio patvirtinimo nėra.

`results/main/` ir keturi aukščiau išvardyti tobulinimo rezultatų aplankai yra dabar naudojami ataskaitos įrodymai. Jų nekeiskite rankomis. Jei bandymas nutrūksta, naudokite `TESTINIO_EKSPERIMENTO_TESIMAS_2026-09-28.md`; skaidinių kontroliniai taškai leidžia tęsti darbą neperrašant baigtų rezultatų. Techninius testus galima paleisti `.\.venv\Scripts\python.exe -m pytest tests -q`.

## Aplankas `old/`

Čia sudėtos ankstesnės dokumentų versijos, pasenusių eksperimentų rezultatai, ankstesnės sąsiuvinių kopijos ir juodraščiai. Kasdieniam paleidimui jų nereikia. **`old/document_sources/` turi dvi tarpines versijas, kurias skaito galutinių PDF ir DOCX atkūrimo scenarijai**, todėl šio poaplankio netrinkite, jei ketinate dokumentus generuoti iš naujo. Nauji sąsiuvinių generatoriaus atsarginiai egzemplioriai taip pat keliauja į `old/notebook_backups/`. Moodle pateikimui rinkitės tik šio README pradžioje nurodytus naujausius PDF.
