# Transporto priemonių siluetų klasifikavimas

## Dabartinis paleidimas

`START.cmd` meniu dabar turi keturis pasirinkimus: **1** atidaro JupyterLab, **2** pakartoja tik istorinį `results/main/` eksperimentą, **3** iš naujo patikrina išsaugotus papildomų bandymų rezultatus jų nepermokydamas, **4** klasifikuoja vieną naują 18 požymių JSON įrašą su tiriamuoju TabPFN v2 modeliu. Pasirinkimas 4 paprašo įrašo failo kelio. Komandinėje eilutėje tas pats veiksmas:

```cmd
.\START.cmd --predict-tabpfn "C:\kelias\mano_irasas.json"
.\START.cmd --verify-further
.\START.cmd --check-tabpfn
```

Šiame kompiuteryje 4 pasirinkimas naudoja jau įdiegtą atskirą TabPFN aplinką `C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn`. Jei jos nėra, sukuriama projekto `.venv_tabpfn` ir įdiegiamos `requirements_tabpfn_v2_lock.txt` priklausomybės; pirmam modeliui įkelti gali reikėti atsisiųsti oficialius svorius. 2 pasirinkimas TabPFN eksperimento nepakartoja. Naujausi dokumentai yra `Egzamino_ataskaita_papildyti_bandymai_2026-09-28.pdf` ir `Kirilas_Sersniovas_Kolokviumo_planas_papildyti_bandymai_2026-09-28.pdf`.

Jei reikia **tęsti nutrūkusį papildomų modelių mokymą**, projekto aplanke vykdykite šias komandas. Baigti skaidiniai pagal nutylėjimą praleidžiami, todėl esami įrodymai neperrašomi. Šiame kompiuteryje TabPFN Python kelias yra `C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn\Scripts\python.exe`; jei naudojate vietinę projekto aplinką, pakeiskite jį į `.\.venv_tabpfn\Scripts\python.exe`.

```powershell
.\.venv\Scripts\python.exe experiment_next_20260928.py svm_extended --max-splits 50
.\.venv\Scripts\python.exe experiment_next_20260928.py extra_trees --max-splits 50
& 'C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn\Scripts\python.exe' experiment_next_20260928.py tabpfn_v2 --max-splits 50
.\.venv\Scripts\python.exe summarize_next_20260928.py
.\START.cmd --verify-further
```

Norint viską perskaičiuoti nuo nulio, pirmiausia reikia atskiros projekto kopijos; `--no-resume` perrašytų esamus skaidinių kontrolinius taškus. Dabartiniai pateikimo rezultatai jau patikrinti, todėl įprastam paleidimui pakanka `START.cmd` 3 arba 4 pasirinkimo.

## 2026-09-28 atnaujinimas

Po dėstytojo pastabų atlikta naujesnės literatūros peržiūra, Opel ir Saab klaidų gerinimo bandymai, parametrų bei MLP mokymo kokybės auditas. Visą eigą, įskaitant nepavykusį bandymą, skaitinį metrikų pavyzdį ir pakartojimo komandas pateikia [ATNAUJINIMAS_2026-09-28.md](ATNAUJINIMAS_2026-09-28.md). Atnaujinta pateikimo ataskaita yra `Egzamino_ataskaita_atnaujinta_2026-09-28.pdf`, kolokviumo planas – `Kirilas_Sersniovas_Kolokviumo_planas_atnaujintas_2026-09-28.docx`.

Pradinis `results/main/` išsaugotas nepakeistas. Tiriamasis platesnės paieškos SVM pasiekė 0,852 Macro-F1 prieš pradinį 0,842; Opel F1 0,736 prieš 0,716 ir Saab F1 0,747 prieš 0,721. Kadangi naujos idėjos buvo pasirinktos jau matant pradinį testą ir skirtumo intervalas apima nulį, tai preliminarus, nepriklausomai dar nepatvirtintas pagerėjimas. `predict_updated.py` leidžia išbandyti šį variantą; senasis `predict.py` toliau naudoja pradinį modelį.

Šis projektas įgyvendina Kirilo Šeršniovo PEPfm-26 egzamino užduotį ir kolokviumo planą. Įvestis yra 18 skaitinių silueto požymių, išvestis – `bus`, `opel`, `saab` arba `van`. Saulės elektrinės užklausa pateiktoje ekrano nuotraukoje yra kitos užduoties pavyzdys ir šiame projekte nenaudojama.

## Rezultatų peržiūra JupyterLab

Pradėkite nuo `00_REZULTATU_SANTRAUKA.ipynb`: čia vienoje vietoje pateiktos visų metodų metrikos, grafikai, SVM hipotezė ir septynių egzamino reikalavimų atitiktis.

Kiekvienas `svm_alternatyva.ipynb`, `mlp_alternatyva.ipynb` ir `rbf_alternatyva.ipynb` dabar turi pagrindines metrikas, palyginimą su abiem baseline, klasių metrikas, painiavos matricą, dešimt klaidų pavyzdžių, atsparumo grafikus, rezultatų interpretaciją ir formulės ryšį su tikru kodu. SVM abliacija aiškiai pažymėta kaip bendro eksperimento dalis.

Lentelės ir grafikai jau išsaugoti sąsiuvinių išvestyse. `Run → Run All Cells` tik atnaujina apžvalgą iš `results/main/`; mokymo blokas pagal nutylėjimą turi `RUN_TRAINING = False`. Mokymui iš naujo šį jungiklį reikia sąmoningai pakeisti. Sąsiuviniams sugeneruoti su išvestimis naudokite `python make_notebooks.py --execute` iš aplinkos, kurioje įdiegtas Jupyter. Generatorius išsaugo ankstesnių sąsiuvinių kopijas `results/notebook_backups/`.

## Paleidimas Windows aplinkoje

Patikrinta su Python 3.10. Pagrindiniam eksperimentui nereikia Jupyter.

```powershell
cd 'C:\Users\sersn\Desktop\Magistras\1 semestras\Intelektualios sistemos\Egzaminas'
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_experiment.py --config configs/main.yaml
```

Tai viena pagrindinė komanda: ji išmoko ir įvertina modelius, patikrina rezultatus, tada sugeneruoja ataskaitą. Oficialus OpenML ID 54, 1 versijos ARFF failas jau yra `data/vehicle.arff`, o jei jo nėra, programa mėgina atsisiųsti iš OpenML. Prieš mokymą tikrinama oficiali MD5 suma `fbba18157b188f309d772f9ca4e578f5`, 846 įrašai, 18 požymių ir keturios klasės. Duomenys: https://www.openml.org/d/54. UCI platesnio rinkinio aprašas: https://archive.ics.uci.edu/dataset/149/statlog+vehicle+silhouettes.

Trijuose papildomuose sąsiuviniuose `svm_alternatyva.ipynb`, `mlp_alternatyva.ipynb` ir `rbf_alternatyva.ipynb` kiekvienas intelektualusis metodas gali būti nagrinėjamas atskirai. Jiems reikia Jupyter aplinkos su šio projekto Python priklausomybėmis; paleidimo katalogas turi būti šis projekto aplankas. Sąsiuviniai sugeneruojami iš naujo komanda `python make_notebooks.py`.

Trumpam techniniam patikrinimui: `python run_experiment.py --config configs/main.yaml --out results/smoke --quick`. Šių dviejų skaidinių rezultatai nėra galutinis egzamino palyginimas.

## Metodai ir vertinimas

`src/models.py` turi du privalomus baseline (artimiausias centroidas ir fiksuotas 5-NN) ir tris kolokviume pasirinktus intelektualiuosius metodus: SVM su RBF branduoliu, MLP ir RBF tinklą. RBF tinklo centrai mokomi `KMeans`, aktyvacijos skaičiuojamos Gauso funkcija, o išvestis mokoma reguliuota `Ridge` regresija. Visiems metodams taikoma `SimpleImputer` ir `StandardScaler` grandinė, išskyrus aiškiai pažymėtą standartizavimo abliaciją.

`run_experiment.py` generuoja 5 pakartojimus po 10 stratifikuotų išorinių skaidinių. Kiekviename išoriniame mokymo skaidinyje SVM, MLP ir RBF tinklo hiperparametrai parenkami penkių dalių vidine CV pagal Macro-F1. Išorinis bandymo skaidinys dalyvauja tik vertinime. Pagrindinės metrikos: Macro-F1, balanced accuracy ir painiavos matrica. Hipotezei naudojamas porinių skirtumų pataisytas kartotinės CV intervalas. Penki pakartojimai nesudaro 50 nepriklausomų rinkinių.

Ablacijos: linijinis SVM ir RBF SVM be standartizavimo. Atsparumas: Gauso matavimo triukšmas, išreikštas išorinės mokymo dalies standartiniu nuokrypiu, ir atsitiktinai paslėpti bandymo požymiai. Tie patys perturbuoti bandymo įrašai duodami visiems penkiems pagrindiniams metodams. Požymių permutacijos jautrumas atliekamas tik diagnostikai, jau parinktam SVM.

## Rezultatai

Pilnas paleidimas į `results/main/` įrašo skaidinių metrikas, parinktus parametrus, prognozes, rezultatų suvestinę, painiavos matricas, klasių ataskaitą, dvi diagramas, abliaciją, atsparumo rezultatus, požymių jautrumą, klaidų pavyzdžius, hipotezės testą ir galutinį `final_svm.joblib`. Jeigu SVM nėra geriausias, tai būtina sąžiningai aptarti pagal `results_summary.csv`; galutinio diegimo pavyzdys vis tiek saugo iš anksto numatytą pagrindinį SVM.

`high_margin_errors.csv` ir `low_margin_correct.csv` nurodo **skaitinius požymių įrašų indeksus**, nes OpenML versijoje nėra pradinių vaizdų. Šeši `decision_function` balai nėra tikimybės. Klaidingų prognozių priežastis negali būti patikimai nustatyta be pradinio vaizdo ir fotografavimo sąlygų.

Pagrindinė komanda automatiškai vykdo `verify_results.py` ir `build_report.py`. Pirmasis scenarijus rankiniu TP, FP ir FN skaičiavimu patikrina visas skaidinių metrikas, tuos pačius bandymo indeksus, painiavos matricas, hipotezės intervalą ir išsaugotą modelį; patikros įrodymas yra `results/main/verification.json`. Antrasis sukuria `results/main/report.md` pagal faktinius rezultatus. Ataskaitą galima atnaujinti be naujo modelių mokymo komanda `python run_experiment.py --postprocess-only`.

## Nematytas įrašas gyvo gynimo metu

Gavus dėstytojo 18 požymių įrašą, išsaugokite JSON objektą su tiksliais `data_metadata.json` esančiais požymių pavadinimais. Tiriamuoju TabPFN modeliu prognozuokite per `START.cmd` 4 pasirinkimą arba `--predict-tabpfn` komandą aukščiau. Jei reikia pademonstruoti pirminį egzamino SVM, vykdykite:

```powershell
.\.venv\Scripts\python.exe predict.py --input unseen.json
```

Abu prognozavimo scenarijai tikrina 18 požymių schemą. Pirminio SVM grandinėje trūkstamos reikšmės pildomos išmoktomis mokymo duomenų medianomis; TabPFN eiga atskira. Mažo pakeitimo gynimo metu pavyzdys: `src/models.py` pakeisti kNN `n_neighbors=5` į `7` ir paleisti `--quick` bandymą atskirame `results/defense_demo` kataloge. Šis bandymas būtų demonstracija, o ne galutinio 50 skaidinių palyginimo pakaitalas. Gynimo vertinimas priklauso nuo studento paaiškinimo ir realiai pateikto nematyto bandymo, todėl jo iš anksto atlikti negalima.

## Ribos

Rinkinyje yra keturi konkretūs modeliniai automobiliai ir kontroliuojamos fotografavimo sąlygos. Nėra patikimų serijų `e2`–`e5` identifikatorių OpenML lentelėje, todėl grupinio poslinkio bandymas neatliekamas ir atsitiktinės CV rezultatai negali pagrįsti veikimo naujiems fiziniams modeliams ar realiame eisme. Klaidų kaštai pagal praktinį diegimą nežinomi. Nėra vaizdų, todėl sistema vertina tik jau apskaičiuotus požymius.

## Formulių sąsaja su kodu

- `src/models.py::build_pipeline`: standartizavimas `z_j=(x_j-μ_j)/s_j`, kur `μ_j` ir `s_j` gaunami tik iš `fit` mokymo dalies.
- `src/models.py::build_pipeline("svm")`: `SVC(kernel="rbf")` realizuoja minkšto tarpo SVM su `C`; RBF branduolys `exp(-γ||z-z'||²)`, `γ` parenkama vidinėje CV.
- `src/models.py::RBFNetwork.fit`: RBF aktyvacijos ir reguliuotas išvesties sluoksnis.
- `run_experiment.py::metrics`: Macro-F1 ir balanced accuracy; `save_outputs` sudaro painiavos matricą.

Pirminiai šaltiniai: [Cover ir Hart, 1967](https://doi.org/10.1109/TIT.1967.1053964) (kNN), [Tibshirani ir kt., 2002](https://doi.org/10.1073/pnas.082099299) (centroidų metodų kontekstas; čia naudojamas paprastas centroidas be mažinimo), [Cortes ir Vapnik, 1995](https://doi.org/10.1007/BF00994018) (SVM), [Rumelhart, Hinton ir Williams, 1986](https://doi.org/10.1038/323533a0) (MLP mokymas), [Moody ir Darken, 1989](https://doi.org/10.1162/neco.1989.1.2.281) (RBF tinklas), [Nadeau ir Bengio, 2003](https://doi.org/10.1023/A:1024068626366) (kartotinės CV intervalo pataisa). Visas literatūros sąrašas ir hipotezė yra kolokviumo plane.

## Patikslintas eksperimentas ir papildomi įrodymai

2026-09-21 pakartotiniam eksperimentui prieš paleidimą užregistruotas `plano_patikslinimai.md`. Dėl 20 000 pritaikymų ribos MLP alpha yra [0.0001, 0.01], RBF plotis [0.5, 1]; kiti tinkleliai nepakitę. Naujo eksperimento biudžetas yra 18 951. Ankstesnis pilnas eksperimentas saugomas `results/previous_20260920/`, dabartinis vertinimas yra tik `results/main/`. Ankstesnio bandymo žinojimas atskleistas ir nelaikomas nepriklausoma validacija.

`resources.json` registruoja pagrindinio proceso didžiausią RAM, visą mokymo ir diagnostikos laiką iki ataskaitos bei pritaikymų skaičių. Naudojamas `--jobs 1` ir keturių native gijų limitas. Ataskaitos atskiro proceso atmintis neįtraukta. `fold_metrics.csv` turi kiekvieno modelio prognozavimo trukmę visam testavimo paketui, o `inner_search/` saugo 251 visų kandidatų vidinės paieškos lentelę.

`provenance.json` yra mokymo pradžios kodo manifestas; `report_provenance.json` – ataskaitos generavimo kodo manifestas. Ataskaitos scenarijai gali būti papildyti po mokymo pradžios, todėl jų kontrolinės sumos gali skirtis; mokymo failai turi atitikti mokymo manifestą. Git revizija registruojama, jei pasiekiama; nesant jos pateikiama priežastis ir tikslūs SHA256. `predict.py` grąžina modelio versiją ir kodo SHA256.

Papildomi klaidų analizės failai: `class_pair_errors.csv`, `error_feature_distributions.csv`, `error_feature_distributions.png`, `error_by_repeat.csv`, `error_edges.csv`, `error_edge_summary.csv`. Požymių kraštai nustatomi tik iš atitinkamos mokymo dalies. `missing_feature_summary.csv` parodo atskiro požymio visiško trūkumo žalą. Ši diagnostika nenaudojama mokymui ar hiperparametrams keisti.

Testai vykdomi projekto aplanke: `python -m pytest tests -q`. Sąsiuviniams papildomai įdiekite JupyterLab (`python -m pip install jupyterlab`) ir paleiskite `python -m jupyterlab`; tai neprivaloma pagrindinei vienos komandos eigai.

Papildomai `resources.json` pateikiama konservatyvi visos eigos RAM viršutinė riba: mokymo proceso pikas ir didesnis iš paeiliui vykdytų patikros bei ataskaitos procesų pikų. Taip vertinama ir pagalbinių procesų atmintis.

Pateikimo versijai sukurta vietinė projekto Git saugykla. Jos revizija įrašyta `results/main/report_provenance.json` po galutinio ataskaitos atnaujinimo. Šio pakartotinio mokymo pradžioje revizijos dar nebuvo, todėl pradinis `provenance.json` sąžiningai palieka null; modelio mokymo failus patvirtina jų pradinės kontrolinės sumos. Kitų paleidimų pradžioje Git revizija jau bus registruojama automatiškai.

## 2026-09-29 papildomi tiriamieji bandymai

Po ankstesnio platesnio SVM išbandyti trys nauji variantai ant tų pačių 50 išorinių skaidinių. Išorinis Macro-F1: ankstesnis platesnis SVM **0,852**, dar platesnis SVM (`C` iki 10000) **0,849**, ExtraTrees **0,755**, TabPFN v2 **0,869**. TabPFN Opel ir Saab F1 atitinkamai **0,745** ir **0,752**, tačiau jų tarpusavio supainiojimų **525**, palyginti su **522** ankstesnio SVM. Taigi bendras pagerėjimas neišsprendė dviejų automobilių atskyrimo problemos. TabPFN porinis Macro-F1 pokytis +0,017; apytikslis pataisytas 95 % intervalas [−0,011; +0,045] apima nulį. Visi palyginimai tiriamieji, nes ankstesnių tų pačių testų rezultatai jau buvo matyti.

2026-09-29 peržiūrint pateikimą aptikta, kad pokalbių istorija baigėsi 2026-09-22, o trys nauji bandymai PDF buvo aprašyti tik lentele. `AI_POKALBIU_ISTORIJA.md` papildyta aiškiai pažymėta vėlesnių užklausų santrauka. Naujausios egzamino ataskaitos B priede dabar yra visų bandymų, įskaitant atmestą Opel-Saab specialistą, lentelė ir du grafikai: poriniai 50 išorinių testų Macro-F1 skirtumai bei platesnio SVM ir TabPFN painiavos matricos. Grafikai kuriami iš išsaugotų testavimo rezultatų komanda `python build_further_charts.py` pagrindinėje `.venv` aplinkoje, tada `python build_exam_pdf.py` ir `python build_further_exam_pdf.py` PDF aplinkoje su `reportlab` ir `pypdf`. Modelių permokyti nereikia. Galutinis PDF: `Egzamino_ataskaita_papildyti_bandymai_2026-09-28.pdf`.

Kiekvienas baigtas skaidinys išsaugotas `results/further_20260928/<modelis>/splits/NN.json`; ten yra testų indeksai, žymos, prognozės, parametrai ir trukmė. `summarize_next_20260928.py` sudaro suvestines, o `verify_next_20260928.py` patvirtina visus 50 kiekvieno metodo išorinių testų ir po 4230 prognozių. Papildoma kaimynų diagnostika `results/further_20260928/diagnosis/` yra tik aprašomoji ir mokymui nenaudota. Nauji PDF: `Egzamino_ataskaita_papildyti_bandymai_2026-09-28.pdf` ir `Kirilas_Sersniovas_Kolokviumo_planas_papildyti_bandymai_2026-09-28.pdf`.

Pagrindinei aplinkai pakanka `requirements.txt`. TabPFN v2 vykdomas atskiroje aplinkoje, kurios paketai užfiksuoti `requirements_tabpfn_v2_lock.txt`. Jis naudoja iš anksto išmokytus oficialius svorius, saugomus `%APPDATA%\tabpfn\`. Po kryžminės patikros visais 846 įrašais pritaikytas kandidatas išsaugotas `results/further_20260928/tabpfn_v2/final_tabpfn_v2.tabpfn_fit`; jo veikimą su tiksliai 18 požymių JSON įrašu galima patikrinti komanda `python predict_tabpfn.py --input unseen.json` iš TabPFN aplinkos. Jo mokymo įrašų prognozės nėra testavimo rodiklis. Įdiegimo ir tęstinumo komandos pateiktos `TESTINIO_EKSPERIMENTO_TESIMAS_2026-09-28.md`.
