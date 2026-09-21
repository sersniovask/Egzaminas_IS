# Egzamino ir koliokviumo plano atitiktis

Pakartotinė patikra 2026-09-21. Šis dokumentas nurodo įrodymus ir atskleidžia plano patikslinimus. Savęs vertinimas nėra dėstytojo pažymio garantija.

| Egzamino kriterijus | Maksimumas | Įrodymai |
|---|---:|---|
| Baseline, duomenų grandinė ir atkuriamumas | 10 | Duomenų kontrolinė suma, du baseline, Pipeline, fiksuotos versijos ir sėklos, vienos komandos vykdymas, kodo manifestai ir vietinė Git saugykla |
| Bent du intelektualieji metodai | 20 | SVM, MLP ir RBF tinklas; formulės ir kodo sąsaja README; trys atskiri sąsiuviniai |
| Korektiškas eksperimentas | 20 | Tie patys 50 išorinių skaidinių, atskira vidinė CV, 251 kandidatų lentelė, nepriklausomas metrikų perskaičiavimas |
| Rezultatai, abliacija, atsparumas, klaidos | 15 | Lentelės ir grafikai, dvi abliacijos, triukšmas ir trūkstami duomenys, permutacija, klasių porų klaidos, skirstiniai, pakartojimai ir skirstinių kraštai |
| Ribos, rizikos ir praktinis tinkamumas | 10 | Klaidų kaina, maža imtis, klasių persidengimas, nėra grupių ir pradinių vaizdų, pamatuotas laikas bei atmintis, nematyto įrašo CLI |
| AI auditas | 5 | ai_log.md su klaidomis, nepatikrintomis prielaidomis, patikros būdais ir šio audito pataisymais |
| Gyvas gynimas | 10 | predict.py ir pakeitimo demonstravimo instrukcija; pats gynimas lieka studentui |

## Ankstesnio audito trūkumų uždarymas

| Trūkumas | Pataisymas arba aiškus apribojimas |
|---|---|
| Viršyti 20 000 pritaikymų | Prieš naują pilną paleidimą dokumentuoti mažesni tinkleliai; naujas skaičius 18 951, tikrinamas pagal visų vidinių paieškų lenteles |
| Nėra prognozavimo trukmių | fold_metrics.csv turi predict_seconds ir test_rows kiekvienam modeliui ir skaidiniui |
| Nėra RAM matavimo | resources.json turi Windows proceso atminties piką ir konservatyvią mokymo bei pagalbinių procesų bendros atminties ribą |
| Nėra kodo ir modelio versijų | Modelis turi model_version ir code_sha256; mokymo ir ataskaitos manifestai bei vietinė Git revizija |
| Neišsaugoti visi kandidatų rezultatai | results/main/inner_search/ turi 250 išorinių paieškų ir vieną galutinio SVM paiešką |
| Nepakankama klaidų analizė | Visų požymių kvantiliai, svarbiausių skirstinių grafikas, klaidos prie mokymo procentilių kraštų ir kiekviename pakartojime, klasių porų skaičiai ir dalys |
| Neaišku, kurių požymių trūkumas žalingiausias | missing_feature_summary.csv su kiekvieno iš 18 požymių paslėpimo diagnostika |
| Plano struktūra ir SVM balsų lygybė | Funkcijos sujungtos į mažiau modulių; bibliotekos taisyklė ir plano netikslumas aiškiai paaiškinti plano_patikslinimai.md |

Pradinis mokymo manifestas turi Git null, nes tuo metu repozitorija dar neturėjo commit. Tai neperrašyta atgaline data. Galutinė pateikimo revizija yra report_provenance.json, o mokymo algoritmų failai patikrinti pagal pradines SHA256 sumas. Kituose paleidimuose pradinė revizija jau bus fiksuojama.

Koliokviumo plano sąlyginiai punktai: papildomas grupinis bandymas negalimas be e2–e5 identifikatorių; trijų MLP inicializacijų atsisakyta dėl biudžeto. Realių kamerų ar naujų automobilių duomenų nėra. Šios ribos negali būti pašalintos vien kodo pataisymu ir nėra slepiamos.

## Savęs vertinimas

Neįtraukiant gyvo gynimo 10 balų ir AI audito 5 balų, lieka 75 balai. Po šio audito ir pilno pakartotinio bandymo mano vertinimas yra **73/75 (97,3 %)**: atkuriamumas 9/10, metodai 20/20, eksperimento korektiškumas 19/20, rezultatai ir analizė 15/15, ribos ir praktinis tinkamumas 10/10. Rezervą palieku dėl pateikimo Git revizijos sukūrimo po mokymo pradžios ir retrospektyvaus tinklelių patikslinimo. Tai argumentuotas savęs vertinimas, o ne matematiškai įrodomas procentas.

Ankstesnis 96 % įvertinimas nepakankamai atsižvelgė į konkrečius koliokviumo plano pažadus. Dabar atitiktis grindžiama išvardytais artefaktais, o tikslios originalaus plano ir įgyvendinimo skirtybės aprašytos atskirai.
