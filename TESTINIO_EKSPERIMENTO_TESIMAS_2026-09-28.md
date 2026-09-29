# Tęstinio eksperimento būsena ir atkūrimas

Šis failas skirtas tam atvejui, jei darbas nutrūktų prieš baigiant visus bandymus. Projekto darbo kopija yra `C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\Egzaminas_20260928`. Ankstesni `results/main`, `results/wide_svm_20260928` ir dokumentai neperrašyti.

## Dabartinė eiga

- `experiment_next_20260928.py svm_extended`: 50/50 skaidinių baigta; vidutinis išorinis Macro-F1 0,848758, ankstesnio platesnio SVM 0,851664.
- `experiment_next_20260928.py extra_trees`: 50/50 skaidinių baigta; Macro-F1 0,754911.
- `experiment_next_20260928.py tabpfn_v2`: 50/50 skaidinių baigta; Macro-F1 0,868662.
- Kaimynų diagnostika baigta: `results/further_20260928/diagnosis/summary.json` ir `car_neighborhoods.csv`.
- Suvestinės generuojamos komanda `summarize_next_20260928.py`; jos tikrina senųjų testų indeksų ir žymų sutapimą. Daliniai rezultatai nėra galutiniai.
- `verify_next_20260928.py` patvirtino visus 50 kiekvieno modelio skaidinių ir po 4230 prognozių. Dokumentai sugeneruoti ir peržiūrėti: `build_further_plan.py` bei `build_further_exam_pdf.py`. Išsaugotas galutinis tiriamasis TabPFN kandidatas `results/further_20260928/tabpfn_v2/final_tabpfn_v2.tabpfn_fit` ir patikrinta jo prognozė.

## Tęsimo komandos

Projekto kataloge (PowerShell):

```powershell
& 'C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv\Scripts\python.exe' experiment_next_20260928.py extra_trees --max-splits 50
& 'C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn\Scripts\python.exe' experiment_next_20260928.py tabpfn_v2 --max-splits 50
& 'C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv\Scripts\python.exe' summarize_next_20260928.py
& 'C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv\Scripts\python.exe' verify_next_20260928.py
```

`experiment_next_20260928.py` pagal nutylėjimą praleidžia baigtus ir patikrintus skaidinius, todėl galima tiesiog pakartoti komandą. Nenaudoti `--no-resume`, jei norima išsaugoti atliktą darbą.

„TabPFN v2“ įdiegta atskiroje `.venv_tabpfn` aplinkoje, kurios paketai užfiksuoti `requirements_tabpfn_v2_lock.txt`. Oficialių svorių failas šioje Windows paskyroje yra `%APPDATA%\tabpfn\tabpfn-v2-classifier-finetuned-zk73skhh.ckpt`; SHA-256 `CF8C519C01EAF1613EE91239006D57B1C806FF5F23AC1AEB1315BA1015210E49`. Prireikus jis atsisiunčiamas iš oficialaus „Prior Labs“ šaltinio automatiškai. Svorių failas nekopijuojamas į projektą.

## Baigiamieji veiksmai

Visi skaičiavimai ir dokumentų kūrimas baigti. Į naudotojo `Desktop\Magistras\1 semestras\Intelektualios sistemos\Egzaminas` katalogą nukopijuota 15 aukščiausio lygmens failų ir 177 `results/further_20260928/` failai; jų SHA-256 sutapimas patikrintas. Nauji rezultatai yra tiriamieji, nes ankstesnė išorinių testų informacija jau buvo matyta. Nepriklausomas naujų ženklintų siluetų testas dar neįmanomas, nes tokių duomenų negauta.

2026-09-29 papildomai sutvarkyta paleidimo eiga: `START.cmd` 3 pasirinkimas tikrina išsaugotus naujus rezultatus, 4 pasirinkimas taiko TabPFN naujam JSON įrašui. Komandinės alternatyvos: `.\START.cmd --verify-further` ir `.\START.cmd --predict-tabpfn "C:\kelias\irasas.json"`. Antras meniu pasirinkimas sąmoningai paliktas tik pradiniam eksperimentui; daugiau informacijos `PALEIDIMAS_IR_GITHUB.md` ir README.
