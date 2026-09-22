# Kodo skaitymo ir gynimo gidas

## Nuo ko pradėti

1. `src/data.py`: `load_vehicle` atskiria 18 požymių X ir tikrąją klasę y. Tai jau iš siluetų išvesti skaičiai, ne nuotraukų atpažinimas nuo nulio.
2. `src/models.py`: `build_pipeline` sujungia medianų pildymą, standartizavimą ir klasifikatorių. `fit` išmoksta parametrus; `predict` tik taiko išmoktą taisyklę.
3. `run_experiment.py`: `make_outer_splits` sukuria vienodus bandymus, `fit_model` viduje parenka parametrus, `metrics` įvertina išorines prognozes.
4. `perturbed_scores` ir SVM diagnostikos blokas parodo atsparumą bei požymių jautrumą.
5. `src/notebook_report.py` ir `src/summary_plots.py` iš jau išsaugotų rezultatų sukuria lenteles ir grafikus.
6. `verify_results.py` nepriklausomai perskaičiuoja metrikas ir tikrina įrodymų vientisumą.
7. `predict.py` pritaiko išsaugotą galutinį modelį vienam naujam JSON įrašui.

## Terminai, kuriuos verta mokėti paaiškinti

- **Įrašas:** viena transporto priemonės silueto požymių eilutė.
- **Skaidinys:** konkretūs mokymo ir testavimo indeksai. Išorinė 10 dalių CV kartojama 5 kartus, taigi vertinama 50 skaidinių. Kiekvienas objektas teste pasirodo 5 kartus.
- **Vidinė CV:** tik išorinės mokymo dalies skaidymas hiperparametrams rinkti. Išorinis testas šiam pasirinkimui nenaudojamas.
- **Hiperparametras:** prieš mokymą parenkamas nustatymas, pvz., SVM C ir gamma. Išmokti svoriai yra modelio parametrai.
- **Standartizavimas:** z=(x−mokymo vidurkis)/mokymo SD. Testui vidurkis ir SD nepervertinami.
- **Macro-F1:** kiekvienos klasės F1 vidurkis, suteikiant klasėms vienodą svorį. F1=2TP/(2TP+FP+FN).
- **Jautrumas (recall):** TP/(TP+FN), t. y. kokia tikrosios klasės dalis aptikta. Balanced accuracy yra klasių jautrumų vidurkis.
- **Abliacija:** pasirinkto komponento pakeitimas ar pašalinimas, pvz., tiesinis branduolys vietoje RBF arba standartizavimo išjungimas.
- **SD:** rezultatų sklaida, ne vidurkio pasikliautinasis intervalas.

## Formulė ir kodas

SVM RBF branduolys: K(z,z′)=exp(−gamma × ||z−z′||²).
`build_pipeline` sukuria `SVC(kernel="rbf")`, o `grid_for` pateikia C ir gamma kandidatus. Gamma valdo panašumo mažėjimą didėjant atstumui; C valdo klaidų baudos ir reguliarizavimo kompromisą. Branduolio skaičiavimą vykdo biblioteka.

RBF tinklas taip pat naudoja Gauso funkcijas, bet yra kitas modelis: `RBFNetwork.fit` išmoksta KMeans centrus, skaičiuoja aktyvacijas ir Ridge išvestį. SVM su RBF branduoliu ir RBF tinklo nereikia sutapatinti.

## Savikontrolės klausimai gynimui

- Kodėl negalima standartizuoti viso rinkinio prieš CV? Taip testo statistika patektų į mokymą.
- Kodėl Opel ir Saab sujungimas pagerina grupės metriką? Jų tarpusavio supainiojimai tampa teisingais automobilių grupės atsakymais; originalus keturių klasių modelis nepasikeičia.
- Kodėl mažas kritimas dėl triukšmo dar nereiškia geriausio modelio? Pradinis rezultatas gali būti žemas; reikia matyti ir galutinį lygį.
- Kodėl 50 taškų nėra 50 nepriklausomų eksperimentų? Mokymo imtys persidengia, tie patys objektai vėl patenka į testą.
- Ar OVO balai yra tikimybės? Ne. Jie naudojami tik diagnostikai.
- Kam galutinis SVM mokomas visais duomenimis? Vėlesnėms naujų įrašų prognozėms. Jo kokybę aprašo ankstesnės išorinės CV rezultatai, o ne mokymo tikslumas.

## Komandos projekto aplanke

- Visi eksperimentai: `python run_experiment.py --config configs/main.yaml`
- Rezultatų auditas: `python verify_results.py`
- Techniniai testai: `python -m pytest tests -q`
- Tik santraukos grafikai: `python make_result_notebooks.py --overview-only --execute`
- Naujas įrašas: `python predict.py --input mano_irasas.json`

## Komentarai ir atkuriamumas

2026-09-22 pridėti komentarai nekeičia mokymo algoritmo. Originalūs trys dokumentuoti mokymo failai išsaugoti `audit/training_sources/`. Pirminis mokymo manifestas ir modelio versija nepakeisti.

`src/source_audit.py` pirmiausia tikrina originalią SHA256 sumą. Jei dabartinis failas skiriasi, tikrina archyvo atitiktį pirminiam manifestui, tada lygina Python sintaksės medį ir vykdomus tokenus. Leidžiami komentarai bei tarpų pakeitimai; tikras algoritmo pakeitimas auditą sustabdo. Po tikro mokymo logikos pakeitimo reikia naujo eksperimento ir naujų rezultatų, o ne taisyti seną manifestą.

Tolimesnis prasmingas pasirengimas: ranka perskaičiuoti mažos painiavos matricos metrikas, paaiškinti vieno įrašo kelią per Pipeline ir atskiroje rezultatų direktorijoje išbandyti nedidelį modelio pakeitimą. Tai patikrintų supratimą, kurio komentarai vieni neįrodo.
