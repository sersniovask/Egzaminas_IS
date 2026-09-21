# AI naudojimo žurnalas

Data: 2026-09-20. Įrankis: Codex. Užduotis: pagal pateiktą egzamino dokumentą ir kolokviumo planą sukurti veikiantį, atkuriamą sprendimą.

| Užklausa arba pasiūlymas | Sprendimas | Patikra |
|---|---|---|
| Perskaityti `PEPfm-26_Kirilas_Sersniovas.docx` ir kolokviumo planą, įgyvendinti vertinimo kriterijus. | Priimta: du baseline, SVM, MLP, RBF tinklas, įdėtinė CV, abliacija ir atsparumas. | Palyginta su abiejų dokumentų skyriais ir kodu. |
| Ekrano nuotraukoje pateiktas saulės elektrinės prognozavimo pavyzdys. | Atmesta kaip šios užduoties tema. | Tikroji individuali užduotis aiškiai nurodo transporto priemonių siluetus. |
| Nepatikrinta prielaida: „UCI puslapyje 946, vadinasi OpenML faile taip pat 946“. | Atmesta. | OpenML ID 54, 1 versijos metaduomenyse nurodyta 846; oficialus UCI aprašas paaiškina, kad 100 atidėti validacijai; ARFF tikrinamas kode. |
| Nepatikrinta prielaida: SVM `decision_function` reikšmės yra kalibruotos tikimybės. | Atmesta. | `SVC` OVO funkcija grąžina šešis porinius balus. Kode jie pažymėti diagnostiniais balais ir nėra vadinami tikimybėmis. |
| Kolokviumo teksto prielaida: balsų lygybė visada sprendžiama sumuojant porinius balus. | Pataisyta įgyvendinime. | Oficiali `scikit-learn` SVC dokumentacija nurodo, kad su `break_ties=False` grąžinama pirmoji iš lygiųjų klasių; kodas remiasi tik bibliotekos `predict`, o balus naudoja diagnostikai. |
| Nepatikrinta prielaida: standartizavimą galima atlikti prieš kryžminį vertinimą. | Atmesta. | `Pipeline` įdėta į `GridSearchCV` ir kiekvieną išorinį mokymą; techninis patikrinimas pateikiamas `tests/test_experiment.py`. |
| Sugeneruoti modelių rezultatus tekste neįvykdžius visos CV. | Atmesta. | Rezultatai generuojami tik paleidžiant `run_experiment.py` ir išsaugomi CSV; techninis `--quick` bandymas pažymėtas negalutiniu. |
| Literatūros nuorodos iš kolokviumo plano. | Priimtos tik patikrinus bibliografinius duomenis. | SVM straipsnis patikrintas Springer, MLP – Nature, RBF tinklas – MIT Press, duomenų aprašas – OpenML ir UCI; Nadeau–Bengio DOI patikrintas straipsnio įraše. |
| Nepatikrinta prielaida: visi planuoti vidiniai derinimai kartu su abliacijomis tilps į 20 000 pritaikymų biudžetą. | Aptikta po pritaikymų skaičiaus audito. | Pilnas 50 skaidinių eksperimentas su abiem atskirai derinamomis abliacijomis sudaro 22 600 išorinių pritaikymų su vidinėmis paieškomis ir 101 galutinio SVM parinkimo pritaikymą – iš viso 22 701. Planuotą pritaikymų ribą viršijo 2 701, nors užregistruota modelių mokymo trukmė buvo 30,1 min. Šis nukrypimas turi būti atskleistas gynime. |
| Pilno bandymo rezultatai ir kodo patikra. | Priimta po vykdymo. | 50 skaidinių × 7 variantai baigti; SVM Macro-F1 0,842, 5-NN 0,708; pataisytas porinio skirtumo 95 % intervalas [0,097; 0,170]. `verify_results.py` sutikrino visus indeksus ir perskaičiavo metrikas; 6 testai praėjo; `predict.py` sėkmingai priėmė pavyzdinį 18 požymių įrašą. |
| Pakartotinis darbo savęs vertinimas pagal egzamino kriterijus. | Pirminis vertinimas 68/75; po pataisymų 72/75, žr. `vertinimo_atitiktis.md`. | Pirminė patikra naudojo tą pačią metrikų funkciją kaip eksperimentas, todėl galėjo pakartoti jos klaidą. Ji pakeista rankiniu TP, FP ir FN skaičiavimu, papildomai tikrinamos matricos, intervalas ir galutinis modelis. Ataskaita papildyta visų metodų atsparumo ir įrašų klaidų pasikartojimo palyginimu. 7 testai praeina, įskaitant vienodų perturbacijų visiems modeliams patikrą. |

AI paruoštas kodas ir paaiškinimai turi būti peržiūrėti studento. Galutinės išvados turi būti sutikrintos su `results/main/` failais; bent vieno skaidinio painiavos matricą ir metrikas studentas turi perskaičiuoti ranka ar atskiru scenarijumi. Gyvo gynimo užduotys negali būti iš anksto patvirtintos.

## 2026-09-21 pakartotinė peržiūra ir pataisymai

Užklausa: dar kartą sutikrinti egzaminą su koliokviumo planu ir atlikti reikiamus pakeitimus. Ankstesnis 96 % savęs įvertinimas buvo per stiprus visų plano pažadų atitikties patvirtinimas: nebuvo prognozavimo trukmės, RAM matavimo, visų vidinės paieškos kandidatų lentelių ir išsamios kraštinių požymių analizės.

Priimta: pridėti šiuos matavimus, kodo SHA256 manifestą ir modelio versiją, papildyti 18 požymių skirstinių, klasių porų, pakartojimų ir atskirų trūkstamų požymių analizę. Praplėsta automatinė patikra tikrina naujų įrašų pilnumą ir jų ryšį su pagrindinėmis prognozėmis. Naujas testas tikrina mokymo medianos išsaugojimą apdorojant nematytą duomenį; kitas – vidinės paieškos kandidatų išsaugojimą.

Prieš naują pilną paleidimą užregistruotas `plano_patikslinimai.md`: tinkleliai sumažinti iki 18 951 pritaikymo. Tai retrospektyvus ankstesnio plano patikslinimas; ankstesnių rezultatų žinojimas atskleidžiamas. Atmesta galimybė tiesiog sumažinti ataskaitoje parašytą pritaikymų skaičių ar priskirti seno vykdymo RAM ir prognozavimo laikus jų neišmatavus. Vietoje to atliekamas naujas pilnas eksperimentas, o ankstesni įrodymai išsaugoti `results/previous_20260920/`.

Git patikra: repozitorijos HEAD nurodo dar nesukurtą šakos reviziją; tiesioginis `git --git-dir=... rev-parse --verify HEAD` neranda revizijos. Išsaugota `git_revision=null`, o vykdytą kodą identifikuoja SHA256 manifestas. Ataskaitos kūrimo manifestas saugomas atskirai, nes ataskaitos ir patikros scenarijai papildyti vykstant modelių mokymui. Mokymo algoritmo failai nuo paleidimo nekeisti ir tikrinami pagal pradinį manifestą.

Pateikimo atkuriamumui sukurta vietinė projekto Git saugykla ir galutinio kodo revizija. Ji nevaizduojama kaip egzistavusi mokymo pradžioje: pirminis manifestas išlieka nepakeistas, o pateikimo revizija registruojama ataskaitos manifeste. Git aptikimo funkcija papildyta aiškiu git-dir; tai versijos registravimo pataisymas, ne modelio ar vertinimo algoritmo pakeitimas.

Galutinis pakartotinio vykdymo rezultatas: visi 50 skaidinių ir 7 variantai baigti, nepriklausoma patikra praėjo. Patikrintos 251 paieškos lentelės ir 18 951 pritaikymas; vykdymas iki pirmos ataskaitos truko 26,8 min., konservatyvi visos eigos RAM riba 425,9 MB. Praėjo 9 vienetiniai testai. Galutinio modelio CLI patikrintas su funkciniu pavyzdžiu; tai nelaikoma dėstytojo nematytu gynimo testu. Nauji SVM, MLP ir RBF Macro-F1 vidurkiai: 0,841682; 0,775126; 0,726541. SVM, baseline ir abliacijų rezultatai sutampa su ankstesniu vykdymu. Naujas skirstinių grafikas vizualiai patikrintas.
