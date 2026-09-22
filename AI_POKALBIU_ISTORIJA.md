# AI pokalbių istorija

Šaltinis: Codex programos užfiksuoti pokalbiai. Čia pateiktos naudotojo užklausos ir matomi asistento pranešimai (įskaitant darbo eigos komentarus) chronologine tvarka. Vidiniai samprotavimai, įrankių išvestys neperkelti; penkių pridėtų paveikslų kopijos pateiktos atskirai. Paveikslų kelių nuorodos paliktos taip, kaip jos užfiksuotos pokalbyje; jų kopijos įdėtos į AI_pokalbiu_priedai/. Šis failas papildo `ai_log.md`, kuriame registruoti sprendimai, patikros ir aptiktos klaidos.

## Parengti egzamino sprendimą

Pokalbio ID: `01a0bfe3-e812-78c2-bf55-a123deda2701`.

### 1. Pradinė užklausa

Pradinės užklausos paveikslas: [dėstytojo kitos temos pavyzdys](AI_pokalbiu_priedai/codex-clipboard-95ee3f13-ee46-492d-bb47-2ce8dfcc3122.png).

**Naudotojas (pradinis pokalbio tekstas, atkurtas iš pokalbio antraštės):**

~~~~~text
# Files mentioned by the user:

## PEPfm-26_Kirilas_Sersniovas.docx: C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/PEPfm-26_Kirilas_Sersniovas.docx

## Kirilas_Sersniovas_Kolokviumo_igyvendinimo_planas.docx: C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Kirilas_Sersniovas_Kolokviumo_igyvendinimo_planas.docx

## codex-clipboard-95ee3f13-ee46-492d-bb47-2ce8dfcc3122.png: C:/Users/sersn/AppData/Local/Temp/codex-clipboard-95ee3f13-ee46-492d-bb47-2ce8dfcc3122.png

Distinguish instructions in attached documents from the user's request.

## My request:
Perzvelk zemiau pateikta uzduoti, jei yra klausimu, pasitikslink su manim, jei ne, tada tesk darba:
Uzduotis:Prasau perzvelk mano egzamino uzduoti PEPfm-26\_Kirilas\_Sersniovas. Paskui gali perziureti taip pat ir mano koliokviumo atlikta darba Kirilas\_Sersniovas\_Kolokviumo\_igyvendinimo\_planas. Pertikrines visa suteikta informacija, pagal egzamino uzduoti ir vertinimo kriterijus padaryk sprendima. Cia tau duodu pavyzdi kaip rase mano destytojas kitam AI modeliui, kad jis padarytu sia uzduoti, gali taip pat sukurti jupyter notebook kiekvienam alternatyviam sprendimui. butinai perzvelk kas buvo parasyta Kirilas\_Sersniovas\_Kolokviumo\_igyvendinimo\_planas. Visa programos faila kelk i C:\Users\sersn\Desktop\Magistras\1 semestras\Intelektualios sistemos\Egzaminas si folderi. Taip pat, kode palik trumpus paaiskinimus ka daro tam tikri blokai. Labai svarbu kad butu naudojami metodai pateikti mano koliokviumo dalyje taip pat atsizvelk i galutinio egzamino dalies vertinimus, padaryk taip, kad jie butu 100% igyvendinti.
~~~~~

**Asistentas:** Pradinės užduoties vykdymo komentarai ir vėlesni rezultatai užfiksuoti toliau šiame pokalbyje; pradinė užklausa nėra pateikta kaip atskiras `userMessage` įrašas pokalbio eksporte.

---

### Pradinės užduoties vykdymas

**Asistentas (eigos pranešimas):**

Techninis dviejų išorinių skaidinių bandymas aptiko ir leido pataisyti MLP bibliotekos elgesį su tekstinėmis klasėmis bei terminalo koduotės klaidą. Penki tiksliniai testai dabar praeina. Toliau vykdau pilną 50 išorinių skaidinių bandymą; techninio bandymo skaičių nelaikysiu galutiniais rezultatais.

**Asistentas (eigos pranešimas):**

Pilnas bandymas jau vyksta su vienodais išoriniais skaidiniais visiems septyniems variantams: dviem baseline, trims pagrindiniams metodams ir dviem SVM abliacijoms. Atskirai paruošiau po Jupyter sąsiuvinį SVM, MLP ir RBF tinklui, taip pat rezultatų patikros scenarijų, kuris iš naujo apskaičiuoja išsaugotas metrikas.

**Asistentas (eigos pranešimas):**

Peržiūrėjau ir kolokviumo dokumente įdėtas formulių iliustracijas: centro klasifikatoriaus atstumą, standartizavimą, minkšto tarpo SVM, RBF branduolį ir vertinimo metrikas. Kodo vietas su jomis susiejau README faile. Pilnas bandymas šiuo metu tęsiasi; išvadas rašysiu tik patikrinęs visų 50 skaidinių išvestį.

**Asistentas (eigos pranešimas):**

Parengiau vertinimo kriterijų žemėlapį, kad būtų aišku, kuris failas pagrindžia kiekvieną egzamino dalį. Jame atskirai pažymėta gyvo gynimo dalis: kodas ir instrukcija paruošti, tačiau dėstytojo dar nepateikto nematyto testo bei jūsų paaiškinimo iš anksto įvertinti negalima.

**Asistentas (eigos pranešimas):**

Patikrinęs oficialią `scikit-learn` SVC dokumentaciją radau vieną kolokviumo plano prielaidą, kurią reikėjo patikslinti: naudojant įprastą `SVC.predict`, balsų lygybė nėra automatiškai sprendžiama sumuojant porinius balus. Tai įrašiau į AI auditą; kode klasę grąžina bibliotekos `predict`, o šeši poriniai balai naudojami tik diagnostikai.

**Asistentas (eigos pranešimas):**

Patikra papildyta ir nematyto įrašo schema: programa priima tik tuos pačius 18 požymių pavadinimų, o trūkstamą reikšmę užpildo iš mokymo duomenų išmokta mediana. Visi šeši testai praeina. Ataskaitos scenarijus taip pat paruoštas įtraukti faktinę rezultatų lentelę, abliacijų skirtumus, painiavos matricą ir klaidų pavyzdžius, kai pilnas bandymas baigsis.

**Asistentas (eigos pranešimas):**

Pirmi du iš penkių pakartojimų jau apskaičiuoti, trečiasis vyksta. Tarpiniuose skaidiniuose SVM dažnai pasirodo geriau už baseline, bet galutinį skirtumą ir pataisytą intervalą skaičiuosiu tik iš visų 50 bandymų. Projekto rezultatai saugomi po kiekvieno skaidinio, tad pažangą galima patikrinti ir failuose.

**Asistentas (eigos pranešimas):**

Trečiasis pakartojimas baigtas. Tarpinė painiavos matrica rodo kolokviumo plane numatytą sunkumą: didžiausia painiava yra tarp „opel“ ir „saab“, o „bus“ bei „van“ atskiriami geriau. Galutinėje ataskaitoje pateiksiu skaičius tik užbaigus likusius du pakartojimus.

**Asistentas (eigos pranešimas):**

Ketvirtasis pakartojimas vyksta. Grafikus vizualiai patikrinau: dėžutės diagrama ir normalizuota SVM painiavos matrica yra įskaitomos, o matricoje pateikti ir procentai, ir įrašų skaičiai. Po paskutinio skaidinio atskirai perskaičiuosiu visas metrikas iš išsaugotų prognozių.

**Asistentas (eigos pranešimas):**

Liko baigti paskutinius išorinius skaidinius. Iki šiol programa kiekvienam skaidiniui išsaugojo pasirinktus parametrus, prognozes, metrikas, atsparumo bandymus ir klaidų indeksus. Baigus paleisiu nepriklausomą rezultatų patikrą, sugeneruosiu lietuvišką išvadų ataskaitą ir perkelsiu projektą į jūsų nurodytą `Egzaminas` aplanką.

**Asistentas (eigos pranešimas):**

Prasidėjo penktasis, paskutinis pakartojimas. Tarpinis SVM ir geresnio baseline Macro-F1 skirtumas yra teigiamas, tačiau galutinį hipotezės sprendimą patvirtinsiu tik gavęs visų penkių pakartojimų rezultatus ir atlikęs išvesties patikrą.

**Asistentas (eigos pranešimas):**

Bandymas pasiekė paskutinio pakartojimo vidurį. Viename skaidinyje skirtingų metodų balai svyruoja, todėl galutinėje ataskaitoje rodysiu ir vidurkį, ir sklaidą bei porinį SVM skirtumą nuo geresnio baseline. Taip pat aiškiai pažymėsiu, kad 50 skaidinių nėra 50 nepriklausomų imčių.

**Asistentas (eigos pranešimas):**

Liko penki iš 50 išorinių skaidinių. Sąsiuvinių paleidimą papildomai patikslinau, kad jie galėtų rodyti grafikus Jupyter aplinkoje, o visi trys `.ipynb` failai praėjo formato patikrą. Po pilno skaičiavimo dar patikrinsiu galutinio modelio prognozavimo komandą su pavyzdiniu įrašu.

**Asistentas (eigos pranešimas):**

Paskutiniai skaidiniai skaičiuojami be klaidų. Kai jie baigsis, patikros scenarijus sulygins kiekvieno metodo ir skaidinio išsaugotas prognozes su užregistruotomis Macro-F1 bei balanced accuracy reikšmėmis; taip bus galima aptikti ataskaitos ir CSV neatitikimus.

**Asistentas (eigos pranešimas):**

48 iš 50 skaidinių baigti. Likus dviem, rezultatų failai vis dar nuosekliai pildomi. Po paskutinio skaidinio programa dar parinks galutinio SVM parametrus naudodama visą rinkinį ir išsaugos modelį vieno įrašo prognozei.

**Asistentas (eigos pranešimas):**

Skaičiuojamas 50-asis, paskutinis skaidinys. Toliau liks galutinio modelio išsaugojimas, metrikų perskaičiavimas ir failų perkėlimas. Jei kuri nors iš šių patikrų neatitiks išsaugotų rezultatų, ją ištaisysiu prieš pateikdamas projektą.

**Asistentas (eigos pranešimas):**

Pilnas 50 skaidinių bandymas baigėsi sėkmingai. SVM pasiekė vidutinį Macro-F1 **0,842**, o geresnis baseline, 5-NN, **0,708**; porinis skirtumas **0,134**, pataisytas 95 % intervalas **[0,097; 0,170]**. Iš anksto aprašytą hipotezės kriterijų atitinka visi penki pakartojimai. Dabar tikrinu, ar CSV ir ataskaitos skaičiai tiksliai sutampa su išsaugotomis prognozėmis.

**Asistentas (eigos pranešimas):**

Visų 50 skaidinių prognozės ir metrikos sutapo su patikros scenarijaus perskaičiavimu; šeši testai praeina, o išsaugotas SVM modelis grąžino klasę ir diagnostinius balus pavyzdiniam įrašui. Ataskaitoje taip pat atskleidžiau vieną plano biudžeto nukrypimą: dėl abiejų atskirai derintų abliacijų pritaikymų skaičius buvo 22 701 vietoje planuotų 20 000, nors mokymo laikas liko mažesnis nei 60 minučių. Dabar kopijuoju patikrintą projektą į jūsų nurodytą aplanką.

**Asistentas (galutinis atsakymas):**

Parengiau transporto priemonių siluetų klasifikavimo projektą pagal jūsų egzamino užduotį ir kolokviumo planą. Visą programą, tris Jupyter sąsiuvinius, duomenis, modelį ir rezultatus įkėliau į nurodytą `Egzaminas` aplanką.

Pilname 50 skaidinių bandyme **SVM pasiekė 0,842 Macro-F1**, o geresnis baseline, 5-NN, **0,708**. Iš anksto apibrėžta SVM hipotezė pasitvirtino: porinis skirtumas 0,134, pataisytas 95 % intervalas [0,097; 0,170]. Visų skaidinių metrikos perskaičiuotos iš išsaugotų prognozių; **6 testai praėjo**.

Pradėkite nuo [paleidimo instrukcijos](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/README.md>) ir [rezultatų ataskaitos](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/results/main/report.md>). Atskiri sąsiuviniai: [SVM](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/svm_alternatyva.ipynb>), [MLP](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/mlp_alternatyva.ipynb>) ir [RBF tinklas](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/rbf_alternatyva.ipynb>).

[AI naudojimo žurnale](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/ai_log.md>) atskleistas plano biudžeto nukrypimas: atliktas 22 701 modelio pritaikymas vietoje numatytų 20 000. Gyvo gynimo balų iš anksto užtikrinti negalima; [prognozavimo programa](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/predict.py>) paruošta dėstytojo pateiktam nematytam įrašui.

---

### 2. 2026-09-20 18:47 UTC

**Naudotojas:**

~~~~~text
dsbar visa si darba pertikrink, pagal egzamino vertinimo kriterijus pats pasirasyk sau pazymi. Jei tas pazimys ( Isskyrus tas dalis kur as turesiu apsigint ir paaiskint ai naudojima) bus zemesnis nei 95% nuo maksimalaus pazymio, pataisyk sia uzduoti, kad ji butu kuo geriau padaryta
~~~~~

**Asistentas (eigos pranešimas):**

Iš naujo patikrinsiu projektą pagal kiekvieną galutinio egzamino kriterijų, perskaičiuosiu įvertinimą be gyvo gynimo ir AI naudojimo paaiškinimo dalių. Patikrinsiu ne vien failų buvimą, bet ir eksperimento korektiškumą, rezultatų atsekamumą bei ataskaitos išvadas. Jei savęs įvertinimas bus mažesnis nei 95 % galimų balų, pataisysiu nustatytas spragas ir vėl paleisiu reikalingas patikras.

**Asistentas (eigos pranešimas):**

Pirminis mano įvertinimas, atmetus 10 balų gyvą gynimą ir 5 balus AI naudojimo paaiškinimui, yra **68/75 (90,7 %)**. Modelių ir kryžminio vertinimo dalys veikia, tačiau iki 95 % ribos trūksta stipresnės nepriklausomos rezultatų patikros ir išsamesnio atsparumo bei klaidų palyginimo ataskaitoje. Šias vietas taisau; po to įvertinsiu iš naujo.

**Asistentas (eigos pranešimas):**

Nepriklausoma patikra dabar rankiniu būdu perskaičiuoja F1 ir jautrumą iš TP, FP ir FN, patikrina kiekvieno skaidinio indeksus, visas painiavos matricas, hipotezės intervalą ir galutinio modelio išvestį. Ataskaitą papildžiau visų penkių metodų atsparumo palyginimu ir parodžiau, kurie įrašai klydo nuosekliai per penkis bandymus. Liko sutvarkyti, kad viena pagrindinė komanda automatiškai atliktų ir šias baigiamąsias patikras.

**Asistentas (eigos pranešimas):**

Po pataisymų savęs įvertinimą keliu iki **72/75 (96,0 %)** pagal tas penkias dalis. Pagrindinis eksperimentas dabar viena komanda sukuria modelį, patikros įrodymą ir ataskaitą. Papildomos patikros praėjo: 350 skaidinių ir metodų įrašų, 29 610 prognozių, 25 000 atsparumo įrašų, trys sąsiuviniai ir 7 testai. Atnaujintus failus perkeliu į tą patį jūsų `Egzaminas` aplanką.

**Asistentas (galutinis atsakymas):**

Pakartotinai įvertinau darbą pagal galutinio egzamino kriterijus. Atmetęs **gyvą gynimą (10 balų)** ir **AI naudojimo paaiškinimą (5 balai)**, iš pradžių sau skyriau **68/75 (90,7 %)**. Pataisęs spragas skiriu **72/75 (96,0 %)**:

| Vertinama dalis | Mano įvertinimas |
|---|---:|
| Duomenys, baseline ir atkuriamumas | 10/10 |
| Intelektualieji metodai | 19/20 |
| Eksperimento korektiškumas | 19/20 |
| Rezultatai, abliacija, atsparumas ir klaidos | 15/15 |
| Ribos ir praktinis tinkamumas | 9/10 |

Sustiprinau [nepriklausomą rezultatų patikrą](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/results/main/verification.json>): ji perskaičiuoja metrikas iš prognozių ir tikrina skaidinius, painiavos matricas bei išsaugotą modelį. [Ataskaitoje](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/results/main/report.md>) dabar palygintas visų metodų atsparumas ir išanalizuotos per penkis bandymus pasikartojančios klaidos. **7 testai praeina.** Atnaujintas projektas yra jūsų nurodytame aplanke; [vertinimo pagrindimas](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/vertinimo_atitiktis.md>) pateiktas atskirai.

Tai mano pagrįstas įvertinimas, o ne garantuotas dėstytojo pažymys. Likusi svarbiausia riba yra nepriklausomo duomenų rinkinio su naujais transporto modeliais nebuvimas.

---

### 3. 2026-09-21 13:54 UTC

**Naudotojas:**

~~~~~text
dar karta perziurek visus reikalavimus ir atlikta koliokviumo dali ir pasakyk ar viskas sutinka darbe
~~~~~

**Asistentas (eigos pranešimas):**

Dar kartą palyginsiu egzamino reikalavimus ir koliokviumo planą su pateiktu kodu, rezultatais bei ataskaita. Patikrinsiu ir ankstesnio vertinimo išvadas, ypač galimus nukrypimus nuo plano.

**Asistentas (eigos pranešimas):**

Pagrindiniai metodai ir eksperimentų protokolas sutampa, tačiau radau daugiau neatitikimų koliokviumo planui, nei nurodžiau ankstesniame vertinime: nesaugomas prognozavimo laikas ir Git revizija, nepateiktas atminties naudojimo matavimas, o dalis suplanuotos klaidų analizės atlikta tik iš dalies. Patikrinsiu šiuos punktus galutiniame „Egzaminas“ aplanke.

**Asistentas (galutinis atsakymas):**

**Pagrindiniai egzamino reikalavimai įgyvendinti, tačiau su koliokviumo planu darbas sutampa ne visiškai.** Ankstesnis mano 96 % vertinimas buvo pernelyg optimistiškas kaip visų plano punktų atitikties patvirtinimas.

Dar kartą patikrinau abu originalius dokumentus, kodą ir rezultatus. Taip pat palyginau 66 projekto failus su tavo „Egzaminas“ aplanku — skirtumų nėra.

| Reikalavimas | Patikros išvada |
|---|---|
| Vehicle duomenys: 846 įrašai, 18 požymių, keturios klasės | Atitinka |
| Abu baseline: 5-NN ir artimiausias centroidas | Atitinka |
| Koliokviume pasirinkti SVM, MLP ir RBF tinklas | Visi įgyvendinti |
| Hiperparametrų tinkleliai | Atitinka planą |
| 5 × 10 išorinė ir 5 dalių vidinė stratifikuota CV | Atitinka; visiems metodams vienodi išoriniai skaidiniai |
| Duomenų paruošimas mokymo dalyje | Atitinka |
| Macro-F1, balanced accuracy, painiavos matricos | Pateikta |
| Abliacijos, permutacijų jautrumas, triukšmas ir trūkstami duomenys | Atlikta |
| Hipotezės patikra ir pataisytas pasikliautinasis intervalas | Atlikta |
| Paleidimo instrukcija, priklausomybės, sėklos, formulės sąsaja su kodu | Pateikta |
| AI žurnalas ir praktinių ribų aptarimas | Pateikta; gynimas lieka tavo dalis |

**Konkretūs neatitikimai ir trūkumai pagal koliokviumo planą:**

- **Skaičiavimo biudžetas viršytas:** vietoje numatytų daugiausia 20 000 modelio pritaikymų atliktas 22 701. Nukrypimas atskleistas, bet plane numatyta tinklelių mažinimo procedūra nepritaikyta.
- **Neužregistruotas prognozavimo laikas ir didžiausias RAM naudojimas.** Yra mokymo trukmės, tačiau nėra įrodymo, kad laikytasi 2 GB ribos.
- **Nesaugomas Git revizijos identifikatorius.** Prognozės išvestyje pateikiama duomenų kontrolinė suma, tačiau nėra atskiro modelio versijos identifikatoriaus.
- **Klaidų analizė iš dalies siauresnė nei suplanuota.** Yra painiavos matrica, klaidų pavyzdžiai ir pasikartojimas, tačiau trijų požymių medianų palyginimas neatstoja pilno skirstinių bei jų kraštų tyrimo. Atskirai nenustatyta, kurių požymių trūkumas žalingiausias.
- **Vidinės paieškos rezultatai neišsaugomi visa lentele:** saugomi laimėję parametrai, bet ne visų kandidatų vertinimai.
- **SVM balsų lygybės taisyklė skiriasi nuo plano teksto.** Tai pagrįstas plane buvusios prielaidos pataisymas, aprašytas AI žurnale.
- **Programos failų struktūra supaprastinta:** dalis planuotų atskirų modulių sujungti į `run_experiment.py`. Funkcionalumas yra, tačiau struktūra nėra identiška planui.

Grupinis bandymas ir trys MLP inicializacijos plane buvo **sąlyginiai**, todėl jų nebuvimo nelaikau savaiminiu privalomų reikalavimų pažeidimu.

Darbas turi pagrindą korektiškam egzamino pateikimui, o išsaugotų rezultatų patikra praėjusi. **Vis dėlto teigti, kad įvykdytas kiekvienas koliokviumo pažadas, šiuo metu negalima.** Šios peržiūros metu failų nekeičiau.

---

### 4. 2026-09-21 16:56 UTC

**Naudotojas:**

~~~~~text
atlik reikiamus pakeitimus
~~~~~

**Asistentas (eigos pranešimas):**

Papildysiu trūkstamus matavimus, modelio ir kodo versijų informaciją bei klaidų analizę. Skaičiavimo biudžetą suderinsiu su koliokviumo riba; jei reikės pakeisti eksperimentą, rezultatus perskaičiuosiu ir atnaujinsiu galutinį „Egzaminas“ aplanką.

**Asistentas (eigos pranešimas):**

Kad naujas eksperimentas tilptų į 20 000 pritaikymų ribą, prieš paleidimą sumažinsiu du tinklelius: MLP paliksiu dvi kraštines reguliarizacijos reikšmes, o RBF tinklui — du pločio daugiklius. Visi trys metodai, MLP architektūros ir SVM abliacijos liks. Naujam eksperimentui reikės 18 951 pritaikymo; ankstesnius rezultatus išsaugosiu atskirai, o šį plano pakeitimą aiškiai aprašysiu.

**Asistentas (eigos pranešimas):**

Naujas pilnas eksperimentas jau vykdomas. Dabar saugomos visų vidinės paieškos kandidatų lentelės ir prognozavimo trukmės; papildomai tikrinama, kaip SVM veikia netekęs kiekvieno iš 18 požymių. Klaidų analizę papildžiau skirstinių palyginimu ir klaidomis prie požymių reikšmių kraštų — jų ribos nustatomos tik iš mokymo duomenų.

**Asistentas (eigos pranešimas):**

Pakeisto kodo 8 testai praėjo. Nauja patikra tikrins ir visų 251 vidinės paieškos lentelių pilnumą bei bendrą pritaikymų skaičių. Pilnas modelių perskaičiavimas dar vyksta; laiko ir atminties ribas patvirtinsiu pagal jo matavimus.

**Asistentas (eigos pranešimas):**

Baigtas pirmasis iš penkių pakartojimų — 10 iš 50 skaidinių. Papildomos analizės grafikas sugeneruotas ir patikrintas. Ataskaitoje bus aiškiai pažymėta, kad tie patys įrašai vertinami penkis kartus, todėl jų prognozės nėra nepriklausomi stebėjimai.

**Asistentas (eigos pranešimas):**

Vykdomas 14-as iš 50 skaidinių. Papildomas testas patvirtino, kad trūkstamas bandymo požymis pildomas mokymo mediana, o pats bandymas jos nepakeičia. Iš viso praėjo 9 testai.

**Asistentas (eigos pranešimas):**

Ankstesnius rezultatus ir anksčiau pateikto kodo kopiją išsaugojau archyve, kad būtų galima palyginti pakeitimus. Naujas eksperimentas pasiekė 17-ą skaidinį. Git repozitorijoje dar nėra revizijos, todėl kodo tapatybei naudojamas SHA256 failų manifestas; neegzistuojančios revizijos nenurodysiu.

**Asistentas (eigos pranešimas):**

Baigti du pilni pakartojimai, vyksta trečiasis. Iki šiol nepakeistų metodų — SVM, abiejų baseline ir abliacijų — rezultatai tiksliai sutampa su ankstesniu vykdymu. Atminties patikrą papildžiau ir ataskaitos bei rezultatų tikrinimo procesų matavimais.

**Asistentas (eigos pranešimas):**

Baigta pusė eksperimento — 25 iš 50 skaidinių. Rezultatai ir papildoma diagnostika išsaugomi po kiekvieno skaidinio. Likusios patikros — pilnų rezultatų perskaičiavimas, išteklių ribos ir galutinė ataskaita.

**Asistentas (eigos pranešimas):**

Mokymo kodo ir konfigūracijos kontrolinės sumos vis dar sutampa su paleidimo pradžioje užregistruotomis sumomis. Vykstant mokymui keičiau tik ataskaitos ir patikros dalis. Dabar vykdomas 29-as skaidinys.

**Asistentas (eigos pranešimas):**

Baigti trys iš penkių pakartojimų. Kad pateikiamas kodas turėtų ir plane numatytą Git identifikatorių, sukursiu vietinę projekto reviziją. Ji bus pažymėta kaip pateikimo versija, sukurta po mokymo pradžios; pradinis mokymo manifestas liks išsaugotas.

**Asistentas (eigos pranešimas):**

Vykdomas 35-as skaidinys iš 50. Pakeistų MLP ir RBF tinklelių rezultatai taip pat saugomi kaip naujo eksperimento rezultatai. Galutinėje ataskaitoje liks aiški pastaba, kad tinkleliai sumažinti jau po ankstesnio bandymo — tai svarbu vertinant išvadų pagrįstumą.

**Asistentas (eigos pranešimas):**

Pateikiamo kodo Git revizija sukurta: `01a5437`. Eksperimentas pasiekė 38-ą skaidinį. Baigus mokymą dar liks nepriklausoma rezultatų patikra, galutinių grafikų peržiūra ir failų perkėlimas į tavo aplanką.

**Asistentas (eigos pranešimas):**

Vykdomas 40-as skaidinys — baigiamas ketvirtasis pakartojimas. Kodo versijos registravimas jau patikrintas: Git identifikatorius nuskaitomas, o kompiuteryje be Git programa galės remtis SHA256 manifestu.

**Asistentas (eigos pranešimas):**

Prasidėjo paskutinis pakartojimas, vykdomas 42-as skaidinys. Sumažintas biudžetas nepakeitė vertinimo apimties: visi metodai vis tiek tikrinami tais pačiais 50 išorinių skaidinių.

**Asistentas (eigos pranešimas):**

Vykdomas 44-as skaidinys iš 50. Mokymas tęsiamas be klaidų; po jo automatiškai prasidės rezultatų ir biudžeto patikra.

**Asistentas (eigos pranešimas):**

Baigti 45 skaidiniai, vykdomas 46-as. Liko užbaigti mokymą ir patikrinti galutinę suvestinę; papildomos diagnostikos duomenys jau sukaupti baigtiems skaidiniams.

**Asistentas (eigos pranešimas):**

Vykdomas 48-as skaidinys. Po paskutinių dviejų bandymų bus išmokytas galutinis SVM modelis ir automatiškai patikrinti visi išsaugoti rezultatai.

**Asistentas (eigos pranešimas):**

Vykdomas paskutinis, 50-as skaidinys. Toliau tikrinsiu galutinio modelio veikimą, naują ataskaitą ir užregistruotą laiko bei atminties naudojimą.

**Asistentas (eigos pranešimas):**

Pilnas eksperimentas ir nepriklausoma patikra baigti sėkmingai: **18 951 pritaikymas, apie 26,8 min., konservatyvi bendro RAM naudojimo riba — 426 MB**. Visos trys biudžeto ribos išlaikytos. SVM Macro-F1 liko 0,842; dabar perkelsiu patikrintą versiją į tavo „Egzaminas“ aplanką.

**Asistentas (galutinis atsakymas):**

Pakeitimai atlikti ir patikrinta versija įkelta į tavo **„Egzaminas“ aplanką**.

- Pakartotas visas 50 skaidinių eksperimentas; nepriklausoma patikra praėjo.
- Biudžetas: **18 951 pritaikymas, 26,8 min., RAM riba apie 426 MB**.
- Papildyti prognozavimo laikai, kandidatų lentelės, klaidų ir trūkstamų požymių analizė, modelio bei Git versijos.
- Praėjo **9 testai**. Ankstesnė versija išsaugota archyve.

[Galutinė ataskaita](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/results/main/report.md>) · [Plano pakeitimų paaiškinimas](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/plano_patikslinimai.md>)

Mano atnaujintas savęs vertinimas: **73/75 — 97,3 %**, neįtraukiant gynimo ir AI audito. Tinklelių pakeitimai bei likusios ribos aiškiai dokumentuoti.

---

### 5. 2026-09-21 19:43 UTC

**Naudotojas:**

~~~~~text
dabar trumpai paaiskink kur ka rasiu aplankale
~~~~~

**Asistentas (galutinis atsakymas):**

Aplanke **„Egzaminas“** svarbiausia:

| Failas / aplankas | Ką ten rasi |
|---|---|
| **README.md** | Paleidimo instrukcijas ir projekto paaiškinimą. |
| **results/main/report.md** | Galutinę ataskaitą: rezultatus, grafikus, palyginimus ir išvadas. |
| **results/main/** | Visus rezultatų CSV, grafikus, patikros įrodymus ir išmokytą modelį `final_svm.joblib`. |
| **run_experiment.py** | Pagrindinę programą, paleidžiančią visą eksperimentą. |
| **src/** | Duomenų paruošimo, modelių ir analizės kodą. |
| **configs/main.yaml** | Modelių parametrus, sėklas ir eksperimento nustatymus. |
| **svm_alternatyva.ipynb**, **mlp_alternatyva.ipynb**, **rbf_alternatyva.ipynb** | Atskirą Jupyter sąsiuvinį kiekvienam metodui. |
| **predict.py** | Naujo 18 požymių įrašo klasifikavimą — pravers gynime. |
| **vertinimo_atitiktis.md** | Atitiktį vertinimo kriterijams ir mano savęs įvertinimą. |
| **plano_patikslinimai.md** | Paaiškinimą, kas ir kodėl pakeista nuo koliokviumo plano. |
| **ai_log.md** | AI naudojimo ir patikrų žurnalą. |
| **tests/** | Automatinius kodo testus. |
| **data/** | Naudotą duomenų rinkinį. |
| **results/previous_20260920/** | Ankstesnės versijos archyvą. |

**Pradėk nuo `README.md`, tada skaityk `results/main/report.md`.**

---

### 6. 2026-09-21 19:46 UTC

**Naudotojas:**

~~~~~text
kaip visa tai atidaryt jupyter?
~~~~~

**Asistentas (galutinis atsakymas):**

Atidaryk **PowerShell** ir paeiliui vykdyk:

```powershell
cd "C:\Users\sersn\Desktop\Magistras\1 semestras\Intelektualios sistemos\Egzaminas"

python -m venv .venv

.\.venv\Scripts\python.exe -m pip install -r requirements.txt jupyterlab ipykernel

.\.venv\Scripts\python.exe -m jupyterlab
```

Naršyklėje atsidarys **JupyterLab** su projekto failais. Kairėje dukart paspausk norimą sąsiuvinį:

- `svm_alternatyva.ipynb` — SVM.
- `mlp_alternatyva.ipynb` — MLP.
- `rbf_alternatyva.ipynb` — RBF tinklas.

Pasirink **Python 3** branduolį, jei paprašys. Vieną langelį paleisi **Shift + Enter**, visus — **Run → Run All Cells**. Paleidus mokymą reikės palaukti.

**Visą bendrą eksperimentą** gali paleisti naujo Python sąsiuvinio langelyje:

```python
%run run_experiment.py --config configs/main.yaml
```

Tai iš naujo atliks visus bandymus ir atnaujins `results/main/` rezultatus. Vien peržiūrai jų perskaičiuoti nereikia.

Kitą kartą užteks pirmos `cd` komandos ir paskutinės `jupyterlab` paleidimo komandos.

---

### 7. 2026-09-21 19:52 UTC

**Naudotojas:**

~~~~~text
kaip paprasciau galiu visa tai paleist? Ir kaip visa tai galiu eksportuot i gitgub?
~~~~~

**Asistentas (eigos pranešimas):**

Pridėsiu vienu dvigubu paspaudimu paleidžiamą failą ir trumpai paaiškinsiu, kaip projektą įkelti į GitHub, neįtraukiant virtualios aplinkos bei laikinųjų failų.

**Asistentas (galutinis atsakymas):**

**Paleisti dabar paprasčiau:** aplanke „Egzaminas“ dukart paspausk [START.cmd](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/START.cmd>).

- **1** — atidaro JupyterLab.
- **2** — paleidžia visą eksperimentą (~27 min.) ir atnaujina rezultatus.

Trūkstamas priklausomybes failas įdiegs automatiškai. Python aplinkos patikra praėjo.

**Į GitHub paprasčiausia įkelti per GitHub Desktop:**

1. Įdiek **GitHub Desktop** ir prisijunk.
2. Pasirink **File → Add local repository** ir nurodyk „Egzaminas“ aplanką.
3. Skiltyje **Changes** įrašyk aprašymą, pvz., „Egzamino projektas“, ir spausk **Commit**.
4. Spausk **Publish repository**, įrašyk pavadinimą.
5. Palik **Keep this code private**, jei nori privačios saugyklos, ir patvirtink publikavimą. [Oficiali instrukcija](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop).

Paruošiau `.gitignore`: bus įtrauktas **kodas, sąsiuviniai ir galutiniai rezultatai**, o virtuali aplinka bei seni bandymų archyvai liks tik kompiuteryje.

---

### 8. 2026-09-21 20:01 UTC

**Naudotojas:**

~~~~~text
# Files mentioned by the user:

## codex-clipboard-c004d40f-1e0c-4c58-8333-99f48cb34db5.png: C:/Users/sersn/AppData/Local/Temp/codex-clipboard-c004d40f-1e0c-4c58-8333-99f48cb34db5.png

Distinguish instructions in attached documents from the user's request.

## My request:
okay, gaunu stai tokia klaida
~~~~~

Pridėti vaizdai: `C:\Users\sersn\AppData\Local\Temp\codex-clipboard-c004d40f-1e0c-4c58-8333-99f48cb34db5.png` ([paveikslas](AI_pokalbiu_priedai/codex-clipboard-c004d40f-1e0c-4c58-8333-99f48cb34db5.png)).

**Asistentas (eigos pranešimas):**

Patikrinsiu, ar Jupyter serveris dar veikia ir kodėl naršyklė prarado ryšį. Jei problema paleidimo faile, jį pataisysiu.

**Asistentas (eigos pranešimas):**

Radau priežastį: Jupyter serveris dabar neveikia, todėl naršyklė neturi prie ko prisijungti. Taip galėjo nutikti uždarius paleidimo langą. Pataisysiu paleidimą, kad serveris veiktų fone, ir patikrinsiu ryšį prieš atidarant Jupyter.

**Asistentas (eigos pranešimas):**

Serveris jau paleistas fone ir atsako. Dabar atidarysiu naują Jupyter puslapį su galiojančiu prisijungimu; seną skirtuką su klaida galėsi uždaryti.

**Asistentas (galutinis atsakymas):**

Klaidą sukėlė **nebeveikiantis Jupyter serveris**. Jį paleidau iš naujo ir patikrinau — ryšys veikia.

**Uždaryk seną skirtuką su klaida ir naudok naujai atidarytą Jupyter puslapį.**

Pataisiau `START.cmd`: pasirinkus **1**, serveris dabar veiks fone, todėl paleidimo langą galėsi uždaryti nenutraukdamas ryšio.

---

### 9. 2026-09-21 20:08 UTC

**Naudotojas:**

~~~~~text
kur visi grafikai, lenteles, klaidu pavyzdziai ir tt?
~~~~~

**Asistentas (galutinis atsakymas):**

Viskas yra **`Egzaminas → results → main`**.

**Pradėk nuo [report.md](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/results/main/report.md>)** — jame sujungtos rezultatų lentelės, grafikai, klaidų pavyzdžiai ir paaiškinimai.

JupyterLab kairėje atverk `results → main`, tada ant `report.md` spausk **dešinį pelės mygtuką → Open With → Markdown Preview**, kad matytum ir paveikslėlius.

| Ko ieškai | Failai |
|---|---|
| Modelių rezultatų lentelė | `results_summary.csv` |
| Modelių palyginimo grafikas | `macro_f1_boxplot.png` |
| Painiavos matrica | `confusion_svm.png` ir `confusion_svm.csv` |
| Atsparumo triukšmui ir trūkstamiems duomenims rezultatai | `robustness_comparison.csv` |
| Klaidingų prognozių pavyzdžiai su požymiais | `error_examples_with_features.csv` |
| 10 didžiausio diagnostinio balo klaidų | `high_margin_errors.csv` |
| 10 ribinių, bet teisingų prognozių | `low_margin_correct.csv` |
| Klaidų pasikartojimo grafikas | `error_frequency.png` |
| Teisingų ir klaidingų prognozių požymių skirstiniai | `error_feature_distributions.png` |
| Požymių svarba | `feature_importance_summary.csv` |
| Kurių požymių trūkumas žalingiausias | `missing_feature_summary.csv` |

**Atskiri modelių `.ipynb` sąsiuviniai neapima visos ataskaitos — bendri rezultatai pateikti šiame aplanke.**

---

### 10. 2026-09-21 20:16 UTC

**Naudotojas:**

~~~~~text
·        Įgyvendinti duomenų paruošimo grandinę, baseline ir bent du intelektualiuosius metodus. Bent vienam modeliui parodyti formulės ar taisyklės ryšį su konkrečia kodo vieta.
·        Palyginti metodus tuo pačiu duomenų skaidymu ir tomis pačiomis metrikomis. Hiperparametrų parinkimui nenaudoti galutinio testo.
·        Atlikti bent vieną abliaciją arba požymių jautrumo bandymą ir bent vieną atsparumo bandymą: triukšmui, trūkstamiems duomenims, laiko ar grupės poslinkiui.
·        Pateikti rezultatų lentelę, tinkamą grafiką, klaidų pavyzdžius ir paaiškinti, kodėl pasirinktas metodas laimėjo arba nelaimėjo. Neigiamas rezultatas priimtinas, jei eksperimentas korektiškas.
·        Pateikti paleidimo instrukciją, priklausomybių sąrašą, fiksuotas atsitiktines sėklas ir vieną komandą pagrindiniam eksperimentui pakartoti. Duomenų failų kopijų teikti nereikia, jei yra atsisiuntimo instrukcija.
·        Pateikti AI naudojimo žurnalą: svarbiausios užklausos, priimti ir atmesti pasiūlymai, bent dvi aptiktos AI klaidos arba nepatikrintos prielaidos ir jų patikros būdas.
·        Gyvo gynimo metu paaiškinti pasirinktą formulę bei kodą, paleisti dėstytojo pateiktą nematytą bandymą ir atlikti nedidelį modelio, metrikos ar duomenų apdorojimo pakeitimą.

ar tikrai viska atlikai pagal uzduoti? Gal butu budas geriau apibendrinti visus rezultatus? pavyzdziui kiekvienam is jupyten notebook nurodyt pagrindines metrikas?
~~~~~

**Asistentas (eigos pranešimas):**

Patikrinsiu šių punktų atitiktį ir papildysiu kiekvieną Jupyter sąsiuvinį jo metodo pagrindinėmis metrikomis, palyginimu su baseline, grafikais bei klaidų pavyzdžiais. Rezultatai bus matomi iš jau atlikto eksperimento, todėl jų peržiūrai nereikės iš naujo mokyti modelių.

**Asistentas (eigos pranešimas):**

Eksperimentinė dalis įgyvendinta pagal šiuos punktus, tačiau gyvo gynimo iš anksto atlikti negalima. Rezultatų pateikimą tikrai galima pagerinti: dabartiniai sąsiuviniai pirmiausia skirti mokymui. Pridėsiu bendrą santraukos sąsiuvinį ir kiekvieno metodo rezultatų apžvalgą, o jau paleistų sąsiuvinių kopijas išsaugosiu.

**Asistentas (eigos pranešimas):**

Kiekviename sąsiuvinyje jau pridėjau pagrindines metrikas, palyginimą su abiem baseline, klasių metrikas, painiavos matricą, 10 klaidų pavyzdžių ir atsparumo grafikus. Dabar juos vykdau, kad lentelės ir grafikai būtų išsaugoti pačiuose failuose ir matomi vos atidarius.

**Asistentas (eigos pranešimas):**

Visi keturi sąsiuviniai sėkmingai įvykdyti: kiekviename išsaugotos lentelės ir po 5 grafikus. Patikrinau grafikų įskaitomumą bei skaičių sutapimą su tavo galutiniais rezultatais. Bendroje santraukoje taip pat nurodyta, kur įrodyta kiekviena užduoties dalis ir kas lieka gyvam gynimui.

**Asistentas (galutinis atsakymas):**

**Pirmos šešios tavo išvardytos dalys įgyvendintos. Gyvas gynimas lieka tau:** paaiškinti kodą, atlikti dėstytojo nematytą bandymą ir nedidelį pakeitimą. Nukrypimai nuo koliokviumo plano dokumentuoti.

Rezultatus jau pateikiau aiškiau:

- **[00_REZULTATU_SANTRAUKA.ipynb](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/00_REZULTATU_SANTRAUKA.ipynb>)** — bendras palyginimas ir visų reikalavimų atitiktis.
- **Kiekviename SVM, MLP ir RBF sąsiuvinyje** — pagrindinės metrikos, palyginimas su baseline, painiavos matrica, 10 klaidų pavyzdžių, atsparumo grafikai, išvados ir formulės ryšys su kodu.

| Metodas | Macro-F1 | Balanced accuracy |
|---|---:|---:|
| SVM | 0,842 | 0,843 |
| MLP | 0,775 | 0,781 |
| RBF tinklas | 0,727 | 0,741 |
| 5-NN | 0,708 | 0,714 |
| Centroidas | 0,441 | 0,462 |

**Lentelės ir grafikai jau išsaugoti sąsiuviniuose — mokymo paleisti nereikia.** Jupyter aplinkoje uždaryk anksčiau atvertus sąsiuvinius ir atverk atnaujintus iš naujo. Pradėk nuo `00_REZULTATU_SANTRAUKA.ipynb`.

---

### 11. 2026-09-21 20:36 UTC

**Naudotojas:**

~~~~~text
# Files mentioned by the user:

## codex-clipboard-533ca629-3dea-4666-98b5-e4ca55e8b2fe.png: C:/Users/sersn/AppData/Local/Temp/codex-clipboard-533ca629-3dea-4666-98b5-e4ca55e8b2fe.png

Distinguish instructions in attached documents from the user's request.

## My request:
dabar trumpai ir aiskiai paaiskink apie ka buvo si egzamino uzduotis, taip pat paaiskink visa darbo struktura ir ka galiu rast kiekviename is siu failu. Kurie failai (pagal egzamino uzduoti) bus svarbus gynime, ka man reikia suprasti, pagrindinius konceptus ir vietas kode. nemastyk per ilgai
~~~~~

Pridėti vaizdai: `C:\Users\sersn\AppData\Local\Temp\codex-clipboard-533ca629-3dea-4666-98b5-e4ca55e8b2fe.png` ([paveikslas](AI_pokalbiu_priedai/codex-clipboard-533ca629-3dea-4666-98b5-e4ca55e8b2fe.png)).

**Asistentas (galutinis atsakymas):**

**Užduotis buvo pagal 18 skaitinių transporto priemonės silueto požymių nustatyti klasę: autobusą, furgoną, Opel arba Saab.** Programa gauna jau apskaičiuotus požymius, o ne nuotrauką. Reikėjo palyginti paprastus ir intelektualiuosius metodus, korektiškai įvertinti rezultatus ir parodyti sprendimo ribas.

Geriausias mūsų eksperimento metodas — **SVM: Macro-F1 ≈ 0,842**, palyginti su **5-NN ≈ 0,708**.

**Darbo eiga:**

Duomenys → patikra → trūkstamų reikšmių pildymas ir standartizavimas → modelių mokymas → vertinimas → atsparumo ir klaidų analizė → ataskaita.

**Ką rasi matomuose failuose**

| Failas | Paskirtis |
|---|---|
| **`00_REZULTATU_SANTRAUKA.ipynb`** | Pagrindinis pristatymo failas: visų metodų rezultatai, grafikai, išvados ir reikalavimų atitiktis. |
| **`svm_alternatyva.ipynb`** | SVM metrikos, grafikai, klaidos, formulė ir kodas. |
| **`mlp_alternatyva.ipynb`** | Tokia pati MLP neuroninio tinklo apžvalga. |
| **`rbf_alternatyva.ipynb`** | Tokia pati RBF tinklo apžvalga. |
| **`run_experiment.py`** | Pagrindinis eksperimentas: skaidymas, parametrų paieška, vertinimas ir rezultatų išsaugojimas. |
| **`predict.py`** | Išmokyto modelio pritaikymas naujam 18 požymių įrašui. |
| **`README.md`** | Paleidimo instrukcija, metodai, formulės ir ribos. |
| **`ai_log.md`** | AI naudojimas, priimti ir atmesti pasiūlymai, klaidos ir jų patikra. |
| `verify_results.py` | Nepriklausomai perskaičiuoja metrikas ir tikrina rezultatų korektiškumą. |
| `build_report.py` | Iš rezultatų sukuria tekstinę ataskaitą ir papildomą analizę. |
| `make_notebooks.py` | Paleidžia sąsiuvinių generavimą. |
| `make_result_notebooks.py` | Sudaro sąsiuvinių skyrius ir, pasirinktinai, išsaugo jų išvestis. |
| `requirements.txt` | Reikalingos Python bibliotekos ir jų versijos. |
| `START.cmd` | Paprastas paleidimo meniu. |
| `start_jupyter.py` | Paleidžia Jupyter fone. |
| `PALEIDIMAS_IR_GITHUB.md` | Trumpa paleidimo ir įkėlimo į GitHub instrukcija. |
| `plano_patikslinimai.md` | Nukrypimai nuo koliokviumo plano ir jų priežastys. |
| `vertinimo_atitiktis.md` | Vertinimo kriterijų susiejimas su darbo įrodymais ir savęs vertinimas. |
| `Untitled.ipynb` | Papildomas sąsiuvinis; pagrindiniam sprendimui nereikalingas. |

**Svarbūs aplankai, kurių šioje nuotraukoje nesimato**

| Aplankas | Turinys |
|---|---|
| **`src/`** | Modelių realizacijos, duomenų patikra ir analizės funkcijos. |
| **`configs/main.yaml`** | Sėklos, skaidinių skaičius ir hiperparametrų tinkleliai. |
| **`results/main/`** | Galutiniai CSV, grafikai, `report.md` ir išmokytas `final_svm.joblib`. |
| `data/` | Naudoti duomenys. |
| `tests/` | Automatiniai testai. |
| `results/previous_20260920/` | Ankstesnio eksperimento archyvas. |
| `results/notebook_backups/` | Ankstesnių sąsiuvinių kopijos. |

**Ką būtina suprasti gynimui**

1. **Baseline:** 5-NN sprendžia pagal penkis artimiausius objektus; centroidų metodas — pagal artimiausią klasės vidurkį.
2. **SVM:** ieško klases skiriančios ribos. RBF branduolys leidžia netiesinę ribą. `C` valdo klaidų baudą, `gamma` — požymių panašumo lokalumą.
3. **MLP ir RBF tinklas:** MLP mokosi neuronų svorius; mūsų RBF tinklas naudoja KMeans centrus, Gauso aktyvacijas ir Ridge išvestį. **RBF tinklas ir SVM su RBF branduoliu yra skirtingi metodai.**
4. **Duomenų nutekėjimas:** testo informacija negali patekti į mokymą. Todėl pildymas ir standartizavimas atliekami `Pipeline` viduje.
5. **Įdėtinė CV:** išorėje — 5 pakartojimai po 10 skaidinių rezultatams įvertinti; viduje — 5 skaidiniai parametrams parinkti.
6. **Metrikos:** Macro-F1 yra klasių F1 vidurkis; balanced accuracy — klasių jautrumų vidurkis. Painiavos matrica parodo, kas su kuo painiojama.
7. **Abliacija ir atsparumas:** tikrinome SVM be standartizavimo ir su tiesiniu branduoliu; taip pat pridėjome triukšmo ir paslėpėme požymius.
8. **Ribos:** maža imtis, dažnai painiojami Opel ir Saab, rezultatai neįrodo tinkamumo realiam eismui. SD lentelėje nėra pasikliautinasis intervalas.

**Svarbiausios konkrečios kodo vietos**

| Vieta | Ką mokėti paaiškinti |
|---|---|
| `src/data.py → load_vehicle` | Kaip tikrinami duomenys ir jų kontrolinė suma. |
| `src/models.py → build_pipeline` | `SimpleImputer → StandardScaler → modelis`. |
| `src/models.py → SVC(kernel="rbf", ...)` | Ryšys su formule **K(z,z′) = exp(−γ‖z−z′‖²)**. |
| `src/models.py → EncodedMLP.fit` | MLP sluoksniai, ReLU, Adam ir ankstyvas stabdymas. |
| `src/models.py → RBFNetwork.fit` | Centrai, radialinės aktyvacijos ir Ridge mokymas. |
| `run_experiment.py → make_outer_splits` | Vienodi išoriniai skaidiniai visiems metodams. |
| `run_experiment.py → fit_model` | Vidinė parametrų paieška be išorinio testo. |
| `run_experiment.py → metrics`, `perturbed_scores` | Metrikos ir atsparumo bandymai. |
| `predict.py → main` | Naujo įrašo patikra ir prognozė. |

**Gynime pradėk nuo `00_REZULTATU_SANTRAUKA.ipynb`, tada parodyk SVM formulę ir `src/models.py`.** Turėk pasiruošęs `predict.py` nematytam testui ir mokėk padaryti paprastą pakeitimą, pavyzdžiui, pakeisti kNN `n_neighbors=5` į `7`. Taip pat perskaityk `ai_log.md` ir `plano_patikslinimai.md` — šiuos sprendimus turėsi paaiškinti pats.

---

### 12. 2026-09-22 09:02 UTC

**Naudotojas:**

~~~~~text
kas yra abliacija?
~~~~~

**Asistentas (galutinis atsakymas):**

**Abliacija** – eksperimentas, kai iš veikiančio modelio sąmoningai pašalinama arba pakeičiama viena dalis, kad būtų galima išmatuoti jos naudą.

Šiame darbe pagrindinis modelis yra **SVM su RBF branduoliu ir standartizavimu**. Atliktos dvi abliacijos:

1. **RBF branduolys pakeistas tiesiniu branduoliu**

   - SVM su RBF: Macro-F1 **0,842**
   - Tiesinis SVM: Macro-F1 **0,794**
   - Skirtumas: apie **−0,047**

   Tai rodo, kad netiesinė sprendimo riba šiame duomenų rinkinyje buvo naudinga.

2. **Pašalintas požymių standartizavimas**

   - SVM su standartizavimu: Macro-F1 **0,842**
   - SVM be standartizavimo: Macro-F1 **0,756**
   - Skirtumas: apie **−0,086**

   Tai rodo, kad standartizavimas labai svarbus, nes 18 požymių turi skirtingus skaitinius mastelius.

Gynime gali sakyti:

> Abliacijos eksperimente pakeičiau po vieną pagrindinio SVM komponentą, palikdamas tuos pačius duomenų skaidinius ir vertinimo metrikas. Rezultatų kritimas parodė, kad ir RBF branduolys, ir standartizavimas prisidėjo prie geresnio modelio rezultato.

Abliacija parodo **sąsają su rezultato pagerėjimu**, tačiau viena pati neįrodo, kad tai vienintelė pagerėjimo priežastis.

---

### 13. 2026-09-22 13:06 UTC

**Naudotojas:**

~~~~~text
kodel programa gauna jau apskaiciuotus pozymius, o ne nuotrauka? Kurie is atliktu metodu yra paprastieji, kurie intelektualieji?
~~~~~

**Asistentas (galutinis atsakymas):**

Programa gauna jau apskaičiuotus požymius, nes toks yra pasirinktas **OpenML Vehicle Silhouettes** duomenų rinkinys. Jame nėra originalių transporto priemonių nuotraukų ar siluetų vaizdų. Kiekviena transporto priemonė aprašyta **18 skaitinių geometrinių požymių**, apskaičiuotų iš jos silueto, pavyzdžiui:

- kompaktiškumas;
- apskritimiškumas;
- spindulio ir ašių santykiai;
- pailgėjimas;
- asimetrija;
- įdubų santykis.

Todėl programa sprendžia tik **klasifikavimo etapą**:

```text
Nuotrauka → silueto išskyrimas → 18 požymių → mūsų modelis → klasė
```

Šiame darbe įgyvendinta dalis prasideda nuo **18 požymių**. Nuotraukos apdorojimas ir silueto požymių skaičiavimas nepatenka į užduoties ribas, nes rinkinyje tam nėra pradinių vaizdų.

## Paprastieji metodai – baseline

Tai atskaitos metodai, su kuriais lyginami sudėtingesni sprendimai:

- **5-NN** – suranda penkis artimiausius mokymo objektus ir pasirenka dažniausią jų klasę.
- **Artimiausio centroido metodas** – apskaičiuoja kiekvienos klasės vidutinį požymių vektorių ir parenka artimiausią klasės centrą.

Rezultatai:

- 5-NN Macro-F1: **0,708**
- centroidų metodas: **0,441**

## Intelektualieji metodai

- **SVM su RBF branduoliu** – pagrindinis metodas. Mokosi netiesinės klases skiriančios ribos.
- **MLP** – neuroninis tinklas su vienu arba dviem paslėptais sluoksniais.
- **RBF neuroninis tinklas** – naudoja KMeans centrus, Gauso radialines aktyvacijas ir Ridge išvesties sluoksnį.

Rezultatai:

- SVM: **0,842**
- MLP: **0,775**
- RBF tinklas: **0,727**

Tiesinis SVM ir SVM be standartizavimo šiame darbe naudojami kaip **abliacijos variantai**. Jie nėra pagrindiniai alternatyvūs metodai.

Gynime trumpai gali sakyti:

> Duomenų rinkinyje pateikti ne originalūs vaizdai, o 18 iš siluetų iš anksto apskaičiuotų geometrinių požymių, todėl mano sprendimas klasifikuoja požymių vektorių. Paprastieji baseline metodai yra 5-NN ir artimiausias centroidas. Intelektualieji metodai yra SVM, MLP ir RBF neuroninis tinklas. Geriausiai pasirodė SVM su RBF branduoliu.

---

### 14. 2026-09-22 13:12 UTC

**Naudotojas:**

~~~~~text
ar musu rezultatai 0.842 svm yra pakankamai geri? kaip galime patobulinti si modeli?
~~~~~

**Asistentas (galutinis atsakymas):**

**SVM Macro-F1 = 0,842 yra geras rezultatas šiai egzamino užduočiai**, nes:

- 5-NN baseline pasiekė tik **0,708**;
- pagerėjimas yra apie **0,134**;
- SVM buvo geresnis visuose 5 pakartojimuose;
- pataisytas 95 % skirtumo intervalas buvo **[0,097; 0,170]**, todėl pagerėjimas nėra vien atsitiktinio skaidymo pasekmė;
- balanced accuracy taip pat aukštas – **0,843**.

Tačiau tai nereiškia 84,2 % patikimumo realiame eisme. Rezultatas galioja šiam mažam 846 įrašų rinkiniui. Didžiausia problema – **Opel ir Saab persidengimas**: jų jautrumas apie 71–72 %, o autobusų ir furgonų – apie 97 %. Be to, nėra naujų automobilių modelių ar kitų kamerų duomenų.

Modelį būtų galima gerinti keliais būdais:

1. **Surinkti daugiau ir įvairesnių duomenų.** Tai tikriausiai duotų didžiausią naudą, ypač Opel ir Saab atskyrimui.

2. **Išplėsti `C` ir `gamma` paiešką.** Pavyzdžiui, po dabartinės grubios paieškos atlikti smulkesnę paiešką aplink geriausias reikšmes. Ji turi likti vidinėje CV.

3. **Atlikti požymių atranką vidinėje CV.** Daugiausia įtakos turėjo `HOLLOWS_RATIO`, `RADIUS_RATIO` ir `SKEWNESS_ABOUT_MAJOR`. Galima pašalinti triukšmingus požymius, tačiau atranka privalo vykti `Pipeline` viduje.

4. **Kurti papildomus požymius.** Galima išbandyti svarbių geometrinių požymių santykius ar sąveikas, jei jie turi aiškią geometrinę prasmę.

5. **Naudoti ansamblį.** Pavyzdžiui, jungti SVM ir MLP prognozes. Naudą reikėtų patikrinti nauja įdėtine CV.

6. **Kalibruoti sprendimo balus.** Tai nebūtinai pagerins Macro-F1, bet padėtų aptikti neaiškius objektus ir perduoti juos žmogaus patikrai.

7. **Vertinti pagal fizinio modelio arba fotografavimo serijos grupes.** Tam reikėtų grupių identifikatorių. Toks testas duotų realesnį, galbūt mažesnį rezultatą.

Svarbi taisyklė: **negalima keisti modelio pagal jau matytus išorinio testo rezultatus ir paskui tuos pačius rezultatus pateikti kaip nepriklausomą įrodymą**. Naujas variantas turėtų būti vertinamas nauju korektišku eksperimentu arba nepriklausomu duomenų rinkiniu.

Gynime galima sakyti:

> 0,842 laikau geru rezultatu šiame rinkinyje, nes SVM aiškiai ir stabiliai pranoko abu baseline metodus. Tačiau modelis dar netinka realiam diegimui: lengvųjų automobilių klasės persidengia, o nepriklausomų naujų transporto priemonių duomenų neturime. Didžiausias tobulinimo potencialas būtų daugiau duomenų, smulkesnė vidinė parametrų paieška ir požymių atranka be informacijos nutekėjimo.

---

### 15. 2026-09-22 13:14 UTC

**Naudotojas:**

~~~~~text
# Files mentioned by the user:

## codex-clipboard-0d385c72-b36a-49d2-a9ae-64072a79e8dd.png: C:/Users/sersn/AppData/Local/Temp/codex-clipboard-0d385c72-b36a-49d2-a9ae-64072a79e8dd.png

Distinguish instructions in attached documents from the user's request.

## My request:
kodel cia per 5 pakartojima dideja? ar as kazka ne taip suprantu?
~~~~~

Pridėti vaizdai: `C:\Users\sersn\AppData\Local\Temp\codex-clipboard-0d385c72-b36a-49d2-a9ae-64072a79e8dd.png` ([paveikslas](AI_pokalbiu_priedai/codex-clipboard-0d385c72-b36a-49d2-a9ae-64072a79e8dd.png)).

**Asistentas (galutinis atsakymas):**

Tu supranti beveik teisingai, tik **X ašis nerodo 1-o, 2-o, 3-io, 4-o ir 5-o pakartojimų**.

Ji rodo, **kiek kartų tas pats duomenų įrašas buvo klasifikuotas klaidingai per visus 5 CV pakartojimus**:

- **0** – įrašas teisingai klasifikuotas visus 5 kartus;
- **1** – suklysta vieną kartą iš penkių;
- **2** – suklysta du kartus;
- …
- **5** – tas pats įrašas suklystas visuose 5 pakartojimuose.

Y ašis rodo, kiek yra tokių skirtingų įrašų.

Todėl paskutinis stulpelis padidėja ne todėl, kad penktame pakartojime modelis staiga veikė blogiau. Jis parodo, kad yra apie **81 sistemingai sunkus objektas**, kuriuos SVM klaidingai klasifikavo visuose penkiuose pakartojimuose.

Dauguma šių nuolatinių klaidų yra tarp **Opel ir Saab**, nes jų siluetų požymiai persidengia. Tai gali reikšti:

- objektas yra labai panašus į kitą klasę;
- pateiktų 18 požymių nepakanka jam atskirti;
- galimas neįprastas arba ribinis pavyzdys;
- modelio sprendimo riba visuose mokymo skaidiniuose lieka panaši.

Grafiką galima skaityti taip:

> Maždaug 647 įrašai buvo teisingai klasifikuoti visuose penkiuose pakartojimuose, o 81 įrašas buvo klaidingai klasifikuotas kiekvieną kartą. Tai rodo, kad dalis klaidų yra sistemingos, o ne atsiradusios tik dėl vieno nepalankaus duomenų skaidymo.

Kad būtų visiškai aišku, grafiko pavadinimą būtų galima formuluoti: **„Kiek kartų tas pats įrašas klasifikuotas klaidingai per 5 CV pakartojimus“**.

---

### 16. 2026-09-22 13:17 UTC

**Naudotojas:**

~~~~~text
kas tas CV?
~~~~~

**Asistentas (galutinis atsakymas):**

**CV – Cross-Validation**, lietuviškai **kryžminis vertinimas** arba **kryžminė patikra**. Jis naudojamas patikrinti, kaip modelis veikia su mokymo metu nematytais duomenimis.

Šiame darbe naudojama **10 dalių CV**:

1. 846 įrašai padalijami į 10 dalių.
2. Modelis mokomas iš 9 dalių.
3. Likusi 1 dalis naudojama testavimui.
4. Procesas kartojamas 10 kartų, kad kiekviena dalis vieną kartą taptų testu.

```text
1 bandymas: testas | mokymas | mokymas | ... | mokymas
2 bandymas: mokymas | testas | mokymas | ... | mokymas
...
10 bandymas: mokymas | mokymas | ... | testas
```

Visa ši 10 dalių procedūra pakartota **5 kartus su skirtingomis fiksuotomis sėklomis**. Todėl gavome:

```text
5 pakartojimai × 10 skaidinių = 50 išorinių bandymų
```

Kiekviename pakartojime tas pats įrašas teste pasirodo vieną kartą. Todėl per penkis pakartojimus kiekvienas įrašas buvo patikrintas **5 kartus**.

Be to, naudota **įdėtinė CV**:

- **vidinė 5 dalių CV** parenka `C`, `gamma` ir kitus hiperparametrus tik iš mokymo duomenų;
- **išorinė 10 dalių CV** vertina jau parinktą modelį su nematytais duomenimis.

Tai svarbu, nes išorinio testo rezultatai nedalyvauja hiperparametrų parinkime ir metrikos nėra dirbtinai pagerinamos.

Gynime trumpai:

> CV yra kryžminis vertinimas. Duomenys dalijami į mokymo ir testavimo dalis kelis kartus, todėl modelis vertinamas su skirtingais nematytais objektais. Mano darbe naudoti penki pakartojimai po dešimt išorinių skaidinių, o hiperparametrai kiekvienoje mokymo dalyje parinkti atskira penkių dalių vidine CV.

---

### 17. 2026-09-22 13:18 UTC

**Naudotojas:**

~~~~~text
·        Gyvo gynimo metu paaiškinti pasirinktą formulę bei kodą, paleisti dėstytojo pateiktą nematytą bandymą ir atlikti nedidelį modelio, metrikos ar duomenų apdorojimo pakeitimą.

del sio punkto, kaip suprast paleisti destytojo pateikta nematyta bandyma? kur ir kaip tai galesiu atlikt?
~~~~~

**Asistentas (galutinis atsakymas):**

„Nematytas bandymas“ reiškia, kad dėstytojas gynimo metu pateiks **naują transporto priemonės įrašą, kurio modelis anksčiau nematė**. Tikėtina, kad gausi 18 skaitinių silueto požymių, o programa turės išvesti prognozuojamą klasę.

Tam projekte yra:

- [predict.py](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/predict.py>) – priima naują įrašą ir pateikia prognozę;
- `results/main/final_svm.joblib` – išsaugotas galutinis SVM modelis;
- `results/main/data_metadata.json` – tikslūs 18 požymių pavadinimų.

Gynimo metu JupyterLab kairėje sukurk failą, pavyzdžiui, `unseen.json`, ir įrašyk dėstytojo pateiktas reikšmes:

```json
{
  "COMPACTNESS": 95,
  "CIRCULARITY": 48,
  "DISTANCE_CIRCULARITY": 83
}
```

Reikės pateikti **visus 18 požymių tiksliais pavadinimais**. Jų sąrašą nukopijuok iš `results/main/data_metadata.json` lauko `features`.

Tada JupyterLab atidaryk **Terminal** ir vykdyk:

```powershell
.\.venv\Scripts\python.exe predict.py --input unseen.json
```

Arba naujame sąsiuvinio langelyje:

```python
%run predict.py --input unseen.json
```

Programa pateiks maždaug tokią išvestį:

```json
{
  "label": "van",
  "label_lt": "furgonas",
  "ovo_decision_values": [...],
  "model_version": "...",
  "openml_md5": "..."
}
```

Čia:

- `label` – modelio prognozuota klasė;
- `label_lt` – lietuviškas klasės pavadinimas;
- `ovo_decision_values` – šeši SVM porinių klasifikatorių balai; tai nėra tikimybės;
- `model_version` – naudoto modelio versija.

`predict.py` taip pat patikrina, ar pateikti visi 18 požymių, ar nėra papildomų laukų ir ar reikšmės skaitinės. `null` reikšmė gali būti užpildyta mokymo duomenų mediana.

Jeigu dėstytojas pateiks **originalią nuotrauką**, dabartinis modelis jos tiesiogiai nepriims, nes užduoties duomenų rinkinyje naudojami jau apskaičiuoti 18 geometrinių požymių. Tokiu atveju reikėtų gauti šių požymių vektorių. Jeigu pateiks CSV eilutę, ją reikės perkelti į tokios pačios struktūros JSON.

Gynime paaiškink:

> Įrašas nematytas reiškia, kad jis nebuvo modelio mokymo duomenyse. `predict.py` patikrina 18 požymių schemą, įkelia išsaugotą viso mokymo rinkinio SVM `Pipeline`, taiko mokymo metu išmoktas medianas ir standartizavimą bei pateikia klasę. Naujo įrašo reikšmės nėra naudojamos modeliui permokyti.

Nedideliam pakeitimui gali parodyti, pavyzdžiui, `src/models.py` pakeisti kNN kaimynų skaičių iš `5` į `7` ir paleisti trumpą patikrą:

```powershell
.\.venv\Scripts\python.exe run_experiment.py --config configs/main.yaml --out results/defense_demo --quick
```

Tai bus demonstracinis pakeitimas, o ne galutinių rezultatų perrašymas.

---

### 18. PDF ataskaitos ir pokalbių istorijos užklausa

**Naudotojas:**

~~~~~text
ar gali padaryti PDF ataskaita viso sio darbo? kodo nereikia kelti
Į PDF reiktų įkelti užduotį, jos sprendimo dokumentaciją (ją jums sugeneruos agentas, jei paprašysite), alternatyvių sprendimų palyginimo grafikus, lenteles ir pan.
Taip pat paciame repository sukurk faila su AI naudojimu, t.y. sio chato, ir "Pideti testu rezultatu grafikus" chato uzklausas ir atsakymus, gali irgi kaip pdf ar tau tinkamu formatu, tiesiog kad destytojas matytu visa istorija
~~~~~

**Asistentas (šio etapo rezultatas):**

Parengta devynių puslapių `Egzamino_ataskaita_Kirilas_Sersniovas.pdf` ataskaita. Joje yra lietuviškas užduoties tekstas, sprendimo dokumentacija, septynių modelių palyginimo lentelė, penki grafikai, atsparumo, abliacijos ir klaidų analizė, ribos bei gynimo nuorodos. `AI_POKALBIU_ISTORIJA.md` pateikia šio pokalbio ir pokalbio „Pridėti testų rezultatų grafikus“ naudotojo užklausas bei matomus asistento atsakymus. Penki užklausose pridėti paveikslai išsaugoti `AI_pokalbiu_priedai/`.

---

### 19. Papildoma PDF lentelių peržiūra

**Naudotojas:**

~~~~~text
ar cia tikrai pakanka visu lenteliu? gal turi dar ka pridet svarbaus? dar karta perziurek uzduoti
~~~~~

**Asistentas (šio etapo rezultatas):**

Dar kartą palyginus ataskaitą su egzamino kriterijais, PDF papildytas keturių klasių preciziškumo, jautrumo ir F1 lentele; poriniu SVM palyginimu tuose pačiuose 50 skaidinių; formulės ir programos vietos, hiperparametrų paieškos, atkuriamumo patikrų bei vertinimo kriterijų atitikties lentelėmis. Paaiškinta, kad 50 skaidinių nėra nepriklausomos imtys ir kad gyvo gynimo balai dar negali būti patvirtinti. Galutinė ataskaita yra 10 puslapių, grafikai ir lentelės vizualiai patikrinti.

---

## Pridėti testų rezultatų grafikus

Pokalbio ID: `01a0c951-35b9-7bd0-95fb-badddbb93366`.

### 1. 2026-09-22 13:32 UTC

**Naudotojas:**

~~~~~text
C:\Users\sersn\Desktop\Magistras\1 semestras\Intelektualios sistemos\Egzaminas



jupyter notebook rezultatu apibendrinime pridek dar reikiamus grafikus. Pvz kazkoki palyginima tarp automobiliu atpazinimo su furgonais ir busais. Jei gali, dar sugalvok kokius nors tinkamus grafikus, kurie galetu padet lengviau suprast testu rezultatus. Taip pat primenu egzamino uzduoti:

# Galutinio egzamino dalis

Galutiniam egzaminui reikia pateikti veikiantį ir atkuriamą sprendimą bei įrodymus, leidžiančius įvertinti jo ribas.

·        Įgyvendinti duomenų paruošimo grandinę, baseline ir bent du intelektualiuosius metodus. Bent vienam modeliui parodyti formulės ar taisyklės ryšį su konkrečia kodo vieta.

·        Palyginti metodus tuo pačiu duomenų skaidymu ir tomis pačiomis metrikomis. Hiperparametrų parinkimui nenaudoti galutinio testo.

·        Atlikti bent vieną abliaciją arba požymių jautrumo bandymą ir bent vieną atsparumo bandymą: triukšmui, trūkstamiems duomenims, laiko ar grupės poslinkiui.

·        Pateikti rezultatų lentelę, tinkamą grafiką, klaidų pavyzdžius ir paaiškinti, kodėl pasirinktas metodas laimėjo arba nelaimėjo. Neigiamas rezultatas priimtinas, jei eksperimentas korektiškas.

·        Pateikti paleidimo instrukciją, priklausomybių sąrašą, fiksuotas atsitiktines sėklas ir vieną komandą pagrindiniam eksperimentui pakartoti. Duomenų failų kopijų teikti nereikia, jei yra atsisiuntimo instrukcija.

·        Pateikti AI naudojimo žurnalą: svarbiausios užklausos, priimti ir atmesti pasiūlymai, bent dvi aptiktos AI klaidos arba nepatikrintos prielaidos ir jų patikros būdas.

·        Gyvo gynimo metu paaiškinti pasirinktą formulę bei kodą, paleisti dėstytojo pateiktą nematytą bandymą ir atlikti nedidelį modelio, metrikos ar duomenų apdorojimo pakeitimą.
~~~~~

**Asistentas (eigos pranešimas):**

Peržiūrėsiu notebooką ir išsaugotus testų rezultatus, tada papildysiu apibendrinimą klasių palyginimais bei grafikais, padedančiais įvertinti metodų klaidas ir atsparumą pagal egzamino reikalavimus.

**Asistentas (eigos pranešimas):**

Rezultatuose yra keturios klasės: „Opel“, „Saab“, furgonai ir autobusai. Pridėsiu ir originalių klasių palyginimą, ir atskirą vaizdą, kuriame „Opel“ bei „Saab“ sujungiami į lengvuosius automobilius. Taip bus aišku, ar modelis painioja automobilių modelius, ar skirtingas transporto priemonių rūšis. Taip pat papildysiu visų metodų atsparumo bei rezultatų skirtumų tuose pačiuose skaidiniuose grafikus.

**Asistentas (eigos pranešimas):**

Papildyta santrauka jau sėkmingai įvykdyta iš išsaugotų rezultatų, nepermokant modelių. Dabar tikrinu grafikų įskaitomumą ir skaičiavimus, ypač kad „Opel“ ir „Saab“ sujungimas nebūtų pateiktas kaip originalaus modelio tikslumo pagerėjimas.

**Asistentas (eigos pranešimas):**

Grafikai parodo aiškų skirtumą: SVM lengvųjų automobilių grupę atpažįsta 97,6 % atvejų, tačiau konkretų „Opel“ ar „Saab“ modelį – 71,4 %. Pagrindinė problema yra šių dviejų modelių painiojimas. Patikros praėjo; dabar išsaugosiu papildytą santrauką jūsų nurodytame aplanke, palikdamas ankstesnių keičiamų failų kopijas.

**Asistentas (galutinis atsakymas):**

Papildžiau [rezultatų santrauką](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/00_REZULTATU_SANTRAUKA.ipynb>):

- Visų metodų klasių F1 ir jautrumo palyginimas.
- Automobilių, furgonų ir autobusų atpažinimas bei painiavos matricos.
- SVM pranašumas tuose pačiuose skaidiniuose, įskaitant abliacijas.
- Visų metodų atsparumas ir rezultatų kritimas.

**Ryškiausia išvada:** SVM automobilių grupę atpažįsta 97,6 %, bet konkretų „Opel“ ar „Saab“ modelį – 71,4 % atvejų.

Grafikai jau išsaugoti notebooke, skaičiavimai patikrinti. Papildytas AI žurnalas ir išsaugotos ankstesnių failų kopijos.

---

### 2. 2026-09-22 13:42 UTC

**Naudotojas:**

~~~~~text
# Files mentioned by the user:

## codex-clipboard-d2f951f1-aba7-4f3f-9ea8-9c7d73ae862e.png: C:/Users/sersn/AppData/Local/Temp/codex-clipboard-d2f951f1-aba7-4f3f-9ea8-9c7d73ae862e.png

Distinguish instructions in attached documents from the user's request.

## My request:
paaiskink kas cia
~~~~~

Pridėti vaizdai: `C:\Users\sersn\AppData\Local\Temp\codex-clipboard-d2f951f1-aba7-4f3f-9ea8-9c7d73ae862e.png` ([paveikslas](AI_pokalbiu_priedai/codex-clipboard-d2f951f1-aba7-4f3f-9ea8-9c7d73ae862e.png)).

**Asistentas (galutinis atsakymas):**

Šis grafikas parodo, **ar pagrindinis SVM modelis lenkia kitus metodus skirtinguose duomenų skaidiniuose**, o ne tik pagal bendrą vidurkį.

Kiekviename skaidinyje modeliai mokomi su ta pačia mokymo dalimi ir tikrinami su ta pačia testavimo dalimi. Tada skaičiuojama:

**Skirtumas = pagrindinio SVM Macro-F1 − lyginamo metodo Macro-F1.**

Pavyzdžiui, jei SVM gauna **0,85**, o MLP **0,75**, grafike atsiranda taškas ties **+0,10**.

Kaip skaityti žymes:

- **Mėlynas taškas** – vieno iš 50 skaidinių rezultatų skirtumas.
- **Raudona punktyrinė linija ties 0** – abu metodai pasirodė vienodai. Dešinėje geresnis SVM, kairėje – kitas metodas.
- **Dėžutė** – viduriniai 50 % skirtumų. Siauresnė dėžutė reiškia mažesnę pranašumo kaitą.
- **Oranžinė linija** – mediana: pusė skirtumų mažesni, pusė didesni.
- **„Ūsai“** – įprastos sklaidos ribos; už jų gali būti išsiskiriančių taškų.

**Ką rodo tavo rezultatai?**

- Prieš **artimiausią centroidą** SVM pranašumas didžiausias.
- Prieš **5-NN ir RBF tinklą** SVM geresnis visuose parodytuose skaidiniuose.
- Prieš **MLP** SVM dažniausiai laimi, tačiau dalis taškų yra kairėje nulio – kai kuriuose skaidiniuose MLP pasirodė geriau.
- Prieš **tiesinį SVM** pagrindinis SVM dažniausiai laimi. Tai palaiko RBF branduolio naudingumą šiame rinkinyje.
- Prieš **SVM be standartizavimo** pagrindinis variantas taip pat dažniausiai laimi – požymių mastelių suvienodinimas padeda.

Dvi viršutinės eilutės yra **abliacijos**: palyginimai su pakeistu pagrindinio modelio variantu, leidžiantys įvertinti branduolio ir standartizavimo svarbą.

Gynime gali pasakyti: **„SVM pranašumas matomas daugelyje tų pačių testavimo skaidinių, tačiau prieš MLP jis nėra visuotinis. Kadangi skaidiniuose kartojasi tie patys objektai, šis grafikas pats savaime neįrodo statistinio reikšmingumo.“**

---

### 3. 2026-09-22 13:42 UTC

**Naudotojas:**

~~~~~text
kas yra skaidinys
~~~~~

**Asistentas (galutinis atsakymas):**

**Skaidinys – konkretus duomenų padalijimas į mokymo ir testavimo dalis.**

Tavo eksperimente yra **846 įrašai**. Viename skaidinyje:

- Apie **761 įrašas** naudojamas modeliui mokyti.
- Likę **85 įrašai** – patikrinti, kaip modelis atpažįsta mokymo metu nematytus pavyzdžius.

Duomenys padalijami į **10 dalių**. Kiekviena dalis paeiliui tampa testavimo dalimi, o likusios devynios – mokymo dalimi. Taip gaunami **10 skaidinių**.

Visa procedūra pakartojama **5 kartus**, kaskart kitaip padalijant duomenis: **10 × 5 = 50 skaidinių**.

Todėl tavo grafike **vienas taškas rodo dviejų metodų rezultatų skirtumą viename tokiame mokymo ir testavimo padalijime**. Visi metodai gauna tuos pačius padalijimus, kad palyginimas būtų sąžiningas.

---

### 4. 2026-09-22 13:48 UTC

**Naudotojas:**

~~~~~text
ka dar galima patobulinti? pavyzdziui ar gali kode parasyt kuo daugiau komentaru ka kiekviena funkcija daro? Arba tam tikri kodo blokai daro?
~~~~~

**Asistentas (eigos pranešimas):**

Papildysiu kodą lietuviškais komentarais: ką daro funkcijos, kokius duomenis jos gauna ir grąžina, bei ką reiškia svarbiausi skaičiavimo blokai. Daugiausia dėmesio skirsiu toms vietoms, kurias reikės paaiškinti gynime: duomenų skaidymui, modeliams, metrikoms, abliacijoms ir atsparumo bandymams.

**Asistentas (eigos pranešimas):**

Radau svarbią atkuriamumo detalę: patikra lygina mokymo kodo failų kontrolines sumas, o jas pakeičia net komentarai. Išsaugosiu originalius mokymo failus ir papildysiu patikrą taip, kad ji leistų dokumentavimo pakeitimus tik įsitikinusi, jog vykdomo kodo struktūra nepakito. Taip komentarai nesugadins rezultatų audito.

**Asistentas (eigos pranešimas):**

Jau paaiškinau 49 funkcijas ir pagrindinius skaičiavimo blokus. Pridėsiu ir trumpą kodo skaitymo gidą su gynimo klausimais, kad būtų lengviau susieti komentarus su visa eksperimento eiga. Toliau patikrinsiu, ar komentarai nepakeitė programos veikimo ir ar auditas vis dar atmeta tikrus algoritmo pakeitimus.

**Asistentas (eigos pranešimas):**

Praėjo visi 12 techninių testų ir pilna išsaugotų rezultatų patikra. Palyginimas patvirtino, kad dokumentuojant mokymo kodą jo vykdoma struktūra nepasikeitė. Dabar atnaujinu notebookų išvestis, kad modelių kodo ištraukose matytųsi ir nauji blokų paaiškinimai.

**Asistentas (galutinis atsakymas):**

Papildžiau kodą lietuviškais komentarais:

- **49 funkcijų** paskirtis, įvestys ir rezultatai.
- Svarbiausių blokų paaiškinimai: modelių mokymas, skaidiniai, parametrų parinkimas, metrikos ir grafikai.
- Formulių ryšys su kodu ir paaiškinimai, kodėl tam tikri veiksmai atliekami būtent taip.

Sukūriau [kodo ir gynimo gidą](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/KODO_GIDAS.md>) su skaitymo eiga, terminų paaiškinimais ir galimais gynimo klausimais. Atnaujinau visus keturis notebookus.

**Patikra:** 12 testų ir pilnas rezultatų auditas praėjo. Mokymo algoritmas nepakeistas; ankstesni failai išsaugoti.

Toliau naudingiausia būtų pasiruošti gynimui: ranka apskaičiuoti mažos painiavos matricos metrikas ir pasipraktikuoti paaiškinti vieno įrašo kelią nuo požymių iki prognozės.

---

### 5. 2026-09-22 14:08 UTC

**Naudotojas:**

~~~~~text
## Ar pranašumas kartojasi tuose pačiuose skaidiniuose?

Teigiamas skirtumas reiškia SVM pranašumą. Paskutinės dvi eilutės parodo branduolio ir standartizavimo abliacijas. Dėžutė apima kvartilius, linija žymi medianą; taškai – visi skaidiniai. 50 priklausomų skaidinių nėra 50 nepriklausomų eksperimentų, o pergalių skaičius nėra statistinio reikšmingumo įrodymas.

paired\_comparison(data)

|                             | **Vidutinis skirtumas** | **SVM geresnis, skaidinių** | **Lygiosios** |
| --------------------------: | ----------------------: | --------------------------: | ------------: |
|          **Palyginimas su** |                         |                             |               |
|                     **MLP** |                   0.067 |                          42 |             0 |
|             **RBF tinklas** |                   0.115 |                          50 |             0 |
|                    **5-NN** |                   0.134 |                          50 |             0 |
| **Artimiausias centroidas** |                   0.401 |                          50 |             0 |
|            **Tiesinis SVM** |                   0.047 |                          48 |             0 |
|  **SVM be standartizavimo** |                   0.086 |                          49 |             0 |

## Abliacija ir požymių jautrumas

ablations(data)

|                            | **Macro-F1 ± SD** | **Balanced accuracy ± SD** | **Mokymas su paieška, s** |
| -------------------------: | ----------------: | -------------------------: | ------------------------: |
|                **Metodas** |                   |                            |                           |
|                **SVM RBF** |     0.842 ± 0.031 |              0.843 ± 0.030 |                     3.812 |
|           **Tiesinis SVM** |     0.794 ± 0.036 |              0.797 ± 0.036 |                     2.012 |
| **SVM be standartizavimo** |     0.756 ± 0.040 |              0.765 ± 0.037 |             5.031<br><br> |

dar karta paaiskink kas cia daroma, pabandyk kuo paprasciau
~~~~~

**Asistentas (galutinis atsakymas):**

Čia pagrindinis **SVM RBF** modelis lyginamas su kitais modeliais. Tikrinama ne tik bendra galutinė metrika, bet ir tai, **kaip dažnai SVM buvo geresnis tuose pačiuose 50 duomenų padalijimų**.

### Pirmoji lentelė

Kiekviename skaidinyje SVM ir kitas modelis tikrinami su tais pačiais testavimo įrašais. Apskaičiuojamas skirtumas:

`SVM Macro-F1 − kito modelio Macro-F1`

Pavyzdžiui:

- SVM rezultatas: 0,85
- MLP rezultatas: 0,78
- Skirtumas: `0,85 − 0,78 = 0,07`

Teigiamas skirtumas reiškia, kad SVM pasirodė geriau.

| Palyginimas | Paprastas paaiškinimas |
|---|---|
| MLP | SVM vidutiniškai geresnis 0,067 ir laimėjo 42 iš 50 skaidinių |
| RBF tinklas | SVM geresnis visuose 50 skaidinių |
| 5-NN | SVM geresnis visuose 50 skaidinių |
| Artimiausias centroidas | SVM daug geresnis visuose 50 skaidinių |
| Tiesinis SVM | SVM RBF geresnis 48 iš 50 skaidinių |
| SVM be standartizavimo | Standartizuotas SVM geresnis 49 iš 50 skaidinių |

„Lygiosios – 0“ reiškia, kad nė viename skaidinyje modeliai negavo visiškai vienodo Macro-F1.

Pagrindinė išvada: **SVM RBF pranašumas kartojasi beveik visuose duomenų padalijimuose**, todėl rezultatas nėra atsiradęs tik dėl vieno palankaus padalijimo.

### Antroji lentelė: abliacija

Abliacija reiškia, kad iš pagrindinio modelio kažką pašaliname arba pakeičiame ir žiūrime, kas nutinka rezultatui.

Pagrindinis modelis:

`duomenys → standartizavimas → SVM su RBF branduoliu`

Buvo patikrinti du pakeitimai.

**1. RBF branduolys pakeistas tiesiniu branduoliu**

- SVM RBF: 0,842
- Tiesinis SVM: 0,794
- Kritimas: `0,842 − 0,794 = 0,048`

Tai rodo, kad RBF branduolys padeda. Tikėtina, kad klasių neįmanoma gerai atskirti viena paprasta tiesine riba.

**2. Pašalintas standartizavimas**

- SVM RBF su standartizavimu: 0,842
- SVM be standartizavimo: 0,756
- Kritimas: `0,842 − 0,756 = 0,086`

Tai rodo, kad standartizavimas labai svarbus. Požymiai turi skirtingus skaičių mastelius, todėl be standartizavimo dideles reikšmes turintys požymiai gali per stipriai veikti atstumus.

### Ką reiškia „± SD“?

`0,842 ± 0,031` reiškia:

- 0,842 – vidutinis rezultatas per 50 skaidinių;
- 0,031 – rezultatų svyravimas tarp skaidinių.

Mažesnis SD reiškia stabilesnius rezultatus. Tačiau tai nėra garantija, kad kiekviename skaidinyje rezultatas pateks tiksliai į šį intervalą.

Gynime galima pasakyti taip:

> Pagrindinį SVM palyginau su kitais metodais tuose pačiuose 50 duomenų skaidinių. SVM lenkė MLP 42 kartus, RBF tinklą ir abu baseline metodus – beveik arba visiškai visada. Ablacijos parodė, kad pakeitus RBF branduolį tiesiniu Macro-F1 sumažėjo nuo 0,842 iki 0,794, o pašalinus standartizavimą – iki 0,756. Todėl geram rezultatui buvo svarbūs ir netiesinis RBF branduolys, ir požymių standartizavimas.

---

### 6. 2026-09-22 14:11 UTC

**Naudotojas:**

~~~~~text
tai kuris pasirode geriau? nes cia atrodo jog geriausia rezultata pasiekes svm rbf ner geriausias
~~~~~

**Asistentas (galutinis atsakymas):**

**Geriausiai pasirodė SVM su RBF branduoliu.** Lentelė gali suklaidinti, nes pirmojoje dalyje nerodomas pats SVM RBF rezultatas – rodomas tik jo skirtumas nuo kitų metodų.

Pagrindinis rezultatas:

- **SVM RBF: Macro-F1 = 0,842** – geriausias.
- Tiesinis SVM: 0,794.
- MLP: apie 0,775.
- SVM be standartizavimo: 0,756.
- RBF tinklas: apie 0,727.
- 5-NN: apie 0,708.
- Artimiausias centroidas: apie 0,441.

Pirmojoje lentelėje, pavyzdžiui, prie MLP nurodyta `0,067`. Tai nėra MLP rezultatas. Tai yra:

`SVM RBF rezultatas − MLP rezultatas = 0,842 − 0,775 = 0,067`

Vadinasi, teigiamas skaičius rodo, **kiek SVM RBF buvo geresnis**.

Lygiai taip pat:

- prieš RBF tinklą: `0,842 − 0,727 = 0,115`;
- prieš 5-NN: `0,842 − 0,708 = 0,134`;
- prieš tiesinį SVM: `0,842 − 0,794 = 0,048`;
- prieš SVM be standartizavimo: `0,842 − 0,756 = 0,086`.

Stulpelis „SVM geresnis, skaidinių“ irgi nurodo pagrindinio **SVM RBF pergales**:

- prieš MLP laimėjo 42 iš 50 skaidinių;
- prieš RBF tinklą ir 5-NN – visuose 50;
- prieš tiesinį SVM – 48;
- prieš SVM be standartizavimo – 49.

Taigi išvada vienareikšmė: **SVM RBF pasiekė geriausią vidutinį Macro-F1 ir dažniausiai laimėjo tiesioginius palyginimus tuose pačiuose skaidiniuose.** „RBF tinklas“ lentelėje yra atskiras modelis, jis nėra tas pats kaip „SVM RBF“.

---

### 7. 2026-09-22 14:13 UTC

**Naudotojas:**

~~~~~text
kas yra pipeline?
~~~~~

**Asistentas (galutinis atsakymas):**

**Pipeline – nuosekli duomenų apdorojimo ir prognozavimo grandinė.**

Tavo projekte vienas įrašas pereina šiuos žingsnius:

```text
18 pradinių požymių
        ↓
trūkstamų reikšmių užpildymas
        ↓
požymių standartizavimas
        ↓
SVM RBF klasifikatorius
        ↓
prognozė: bus / van / opel / saab
```

Kode pipeline sukuriamas maždaug taip:

```python
Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", SVC(kernel="rbf"))
])
```

Kiekvienas žingsnis turi savo paskirtį:

- `imputer` trūkstamas reikšmes užpildo mokymo duomenų medianomis;
- `scaler` standartizuoja požymius, kad jų masteliai būtų panašūs;
- `model` pagal apdorotus požymius prognozuoja transporto priemonės klasę.

Kai iškviečiama:

```python
pipeline.fit(X_train, y_train)
```

visa grandinė mokoma tik naudojant mokymo duomenis:

1. Apskaičiuojamos mokymo požymių medianos.
2. Apskaičiuojami mokymo požymių vidurkiai ir standartiniai nuokrypiai.
3. Apdorotais mokymo duomenimis išmokomas modelis.

Kai iškviečiama:

```python
pipeline.predict(X_test)
```

testavimo duomenims pritaikomos tos pačios mokymo metu apskaičiuotos medianos, vidurkiai ir standartiniai nuokrypiai, o tada gaunama prognozė.

Pipeline ypač svarbus kryžminiame vertinime. Jis užtikrina, kad testavimo duomenų informacija nepatektų į mokymą. Jei standartizavimas būtų atliktas visam rinkiniui prieš skaidymą, modelis netiesiogiai panaudotų testo informaciją.

Gynime gali sakyti:

> Pipeline yra bendra duomenų apdorojimo ir modelio grandinė. Mano projekte ji užpildo trūkstamas reikšmes, standartizuoja požymius ir pritaiko klasifikatorių. Visi apdorojimo parametrai apskaičiuojami tik iš mokymo dalies, todėl išvengiama duomenų nutekėjimo.

---

### 8. 2026-09-22 14:14 UTC

**Naudotojas:**

~~~~~text
kaip atliekama trukstamu reiksmiu uzpildymas, pozymiu standartizavimas? kam reikia uzpildyt trukstamas reiksmes? ar musu duomenyse gali buti trukstamu reiksmiu? ar nebebutu geriau tiesiog atmest tokius duomenis?
~~~~~

**Asistentas (galutinis atsakymas):**

Pradiniame tavo duomenų rinkinyje trūkstamų reikšmių nėra. Tačiau užpildymas įtrauktas tam, kad modelis galėtų veikti, jei trūkstama reikšmė atsirastų atsparumo bandyme arba naujame dėstytojo pateiktame įraše.

Pipeline veikia tokia tvarka:

```text
Pradiniai požymiai
        ↓
Trūkstamų reikšmių užpildymas mokymo medianomis
        ↓
Standartizavimas
        ↓
Modelio prognozė
```

### Kaip užpildomos trūkstamos reikšmės?

Kode naudojama:

```python
SimpleImputer(strategy="median")
```

Kiekvienam iš 18 požymių atskirai apskaičiuojama mokymo duomenų mediana.

Pavyzdžiui, mokymo dalyje vieno požymio reikšmės yra:

```text
10, 12, 14, 17, 100
```

Mediana yra `14`. Jeigu naujame įraše šio požymio reikšmė yra `NaN`, ji pakeičiama į `14`.

Svarbu, kad mediana apskaičiuojama tik iš mokymo dalies. Testavimo duomenys medianai nustatyti nenaudojami.

Mediana pasirinkta todėl, kad ją mažiau veikia labai didelės ar labai mažos reikšmės. Pavyzdyje vidurkį stipriai padidintų reikšmė `100`, o mediana išliktų `14`.

Tikslinė klasė – `bus`, `van`, `opel` arba `saab` – neužpildoma. Užpildomi tik įvesties požymiai.

### Kaip atliekamas standartizavimas?

Po užpildymo naudojamas:

```python
StandardScaler()
```

Kiekvienam požymiui iš mokymo duomenų apskaičiuojamas:

- vidurkis;
- standartinis nuokrypis.

Tada kiekviena reikšmė pakeičiama pagal formulę:

\[
z=\frac{x-\mu}{\sigma}
\]

Čia:

- \(x\) – pradinė reikšmė;
- \(\mu\) – mokymo dalies vidurkis;
- \(\sigma\) – mokymo dalies standartinis nuokrypis;
- \(z\) – standartizuota reikšmė.

Pavyzdžiui, jeigu mokymo vidurkis yra `50`, standartinis nuokrypis `10`, o įrašo reikšmė `70`, gauname:

\[
z=\frac{70-50}{10}=2
\]

Tai reiškia, kad reikšmė yra dviem standartiniais nuokrypiais didesnė už mokymo vidurkį.

Testavimo ir naujiems duomenims naudojami tie patys mokymo metu apskaičiuoti \(\mu\) ir \(\sigma\). Jie neperskaičiuojami.

### Kam reikalingas standartizavimas?

Skirtingi požymiai gali turėti labai skirtingus mastelius. Pavyzdžiui:

- vienas požymis gali svyruoti nuo 0 iki 10;
- kitas – nuo 0 iki 1 000.

Be standartizavimo antrasis požymis daug stipriau veiktų atstumus vien todėl, kad jo skaičiai didesni. Tai ypač svarbu SVM su RBF branduoliu, nes jis remiasi atstumais tarp objektų.

Tavo rezultatai tai patvirtina:

- SVM su standartizavimu: **Macro-F1 0,842**;
- SVM be standartizavimo: **Macro-F1 0,756**.

Taigi standartizavimas šiame eksperimente pagerino rezultatą maždaug `0,086`.

### Ar tavo duomenyse yra trūkstamų reikšmių?

Originaliame OpenML duomenų faile:

- 846 įrašai;
- 18 požymių;
- **0 trūkstamų langelių**.

Tačiau trūkstamos reikšmės dirbtinai sukuriamos atsparumo bandyme. Testavimo duomenyse atsitiktinai paslepiama:

- 5 % langelių;
- 10 % langelių.

Taip tikrinama, kaip modelis veiktų, jeigu realiame naudojime dalis matavimų nebūtų gauta.

Be to, `predict.py` leidžia naujo įrašo požymiui turėti `NaN`. Tokiu atveju pipeline panaudoja mokymo medianą.

### Ar nebūtų geriau tokius įrašus atmesti?

Kartais būtų, bet tavo atveju automatinis atmetimas nėra geriausias numatytasis sprendimas.

Duomenų rinkinys turi tik 846 įrašus. Jeigu pradėtume šalinti visas eilutes, kuriose trūksta bent vieno iš 18 požymių, galėtume prarasti nemažą dalį ir taip nedidelio rinkinio.

Be to, praktinio prognozavimo metu gali būti pateiktas vienas automobilis su vienu trūkstamu matavimu. Jei tokį įrašą atmestume, modelis apskritai nepateiktų atsakymo. Medianos užpildymas leidžia pateikti prognozę, nors ji gali būti mažiau patikima.

Tinkamas pasirinkimas priklauso nuo trūkumo dydžio:

- Jei trūksta vieno ar kelių požymių, medianų užpildymas yra pagrįstas paprastas sprendimas.
- Jei viename įraše trūksta daugumos požymių, prognoze pasitikėti nereikėtų ir įrašą būtų protinga atmesti arba pažymėti papildomam patikrinimui.
- Jei tam tikro požymio beveik visada trūksta, reikėtų svarstyti jo pašalinimą arba geresnį užpildymo metodą.
- Jei trūksta tikrosios klasės mokymo duomenyse, tokio įrašo negalima naudoti prižiūrimam modelio mokymui.

Gynime gali paaiškinti taip:

> Pradiniame rinkinyje trūkstamų reikšmių nėra, tačiau medianų užpildymas įtrauktas dėl atsparumo bandymų ir būsimų nematytų įrašų. Trūkstama požymio reikšmė pakeičiama tik iš mokymo dalies apskaičiuota mediana. Po to požymiai standartizuojami pagal mokymo vidurkį ir standartinį nuokrypį. Įrašų automatiškai nešalinau, nes rinkinys mažas, o pavienį trūkstamą matavimą galima pagrįstai užpildyti. Jei trūktų daug požymių, tokį įrašą reikėtų atmesti arba prognozę pažymėti kaip nepatikimą.

---

### 9. 2026-09-22 14:16 UTC

**Naudotojas:**

~~~~~text
kaip atlikeamas atsparumo bandymas?
~~~~~

**Asistentas (galutinis atsakymas):**

Atsparumo bandymas tikrina, kaip modelių rezultatai pasikeičia, kai testavimo duomenys yra tyčia sugadinami.

Svarbiausia: modelis mokomas su švariais mokymo duomenimis. Trikdžiai pridedami tik testavimo daliai, kai modelis jau išmokytas.

Bendra eiga:

```text
Švarūs mokymo duomenys
        ↓
Išmokomas modelis
        ↓
Paimami testavimo duomenys
        ↓
Pridedamas triukšmas arba paslepiamos reikšmės
        ↓
Modelis pateikia prognozes
        ↓
Apskaičiuojamas Macro-F1
        ↓
Palyginama su švaraus testo rezultatu
```

### 1. Triukšmo bandymas

Prie kiekvienos testavimo požymio reikšmės pridedamas atsitiktinis Gauso triukšmas:

\[
x' = x + \epsilon\cdot\sigma_{\text{mokymo}}
\]

Čia:

- \(x\) – originali testavimo reikšmė;
- \(x'\) – pakeista reikšmė;
- \(\epsilon\) – atsitiktinis triukšmas;
- \(\sigma_{\text{mokymo}}\) – to požymio standartinis nuokrypis mokymo dalyje.

Tikrinami trys triukšmo lygiai:

- `0,05` – nedidelis triukšmas;
- `0,10` – vidutinis;
- `0,20` – didžiausias bandytas triukšmas.

Jeigu požymio mokymo standartinis nuokrypis yra `20`, tai naudojant triukšmo lygį `0,10`, pridedamo triukšmo standartinis nuokrypis bus:

\[
0,10 \times 20 = 2
\]

Triukšmas proporcingas konkretaus požymio masteliui. Todėl didelių reikšmių požymiai negauna tokio paties absoliutaus triukšmo kaip maži požymiai.

### 2. Trūkstamų reikšmių bandymas

Testavimo lentelėje atsitiktinai paslepiama:

- 5 % langelių;
- 10 % langelių.

Paslėptos reikšmės pakeičiamos į `NaN`.

Pavyzdžiui:

```text
Prieš:  [42, 15, 88, 31]
Po:     [42, NaN, 88, 31]
```

Kai toks įrašas perduodamas pipeline, `SimpleImputer` trūkstamą reikšmę pakeičia mokymo duomenų mediana. Po to duomenys standartizuojami ir perduodami modeliui.

### Kodėl kiekvienas bandymas kartojamas?

Atsitiktinai parinktas triukšmas arba paslėpti langeliai vieną kartą gali būti neįprastai lengvi ar sunkūs. Todėl kiekviename skaidinyje ir kiekvienam trikdžio lygiui sukuriama po **20 skirtingų realizacijų**.

Pavyzdžiui, 10 % trūkstamų reikšmių bandyme:

1. Pirmą kartą paslepiami vieni langeliai.
2. Antrą kartą – kiti.
3. Taip kartojama 20 kartų.
4. Galutiniame grafike rodomas jų rezultatų vidurkis.

### Kaip užtikrinamas sąžiningas modelių palyginimas?

Visi modeliai gauna tuos pačius pakeistus testavimo duomenis.

Jeigu vienoje realizacijoje paslepiamas tam tikro įrašo trečias požymis, jis paslepiamas lyginant ir SVM, ir MLP, ir RBF tinklą, ir abu baseline metodus.

Taip vienas modelis negauna lengvesnio trikdžio už kitą.

Bandymas atliekamas:

- visuose 50 išorinių skaidinių;
- penkiems pagrindiniams metodams;
- su 3 triukšmo lygiais;
- su 2 trūkstamų reikšmių lygiais;
- po 20 atsitiktinių realizacijų.

Vienam metodui gaunama:

\[
50 \times 5 \times 20 = 5000
\]

atsparumo rezultatų, nes iš viso yra penki trikdžių lygiai.

### Kaip vertinamas atsparumas?

Kiekvienu atveju apskaičiuojamas Macro-F1 ir balanced accuracy. Rezultatas palyginamas su to paties modelio rezultatu švariame teste.

Pavyzdžiui:

```text
Švaraus testo Macro-F1:       0,842
Su 20 % triukšmu:             0,766
Kritimas:                     0,076
```

Kuo mažesnis kritimas, tuo modelis stabilesnis konkrečiam trikdžiui.

Tačiau reikia žiūrėti ir į galutinį rezultatą. Modelis gali beveik nenukristi todėl, kad jo pradinis rezultatas jau buvo žemas.

Pavyzdžiui:

```text
Modelis A: 0,84 → 0,76, kritimas 0,08
Modelis B: 0,45 → 0,44, kritimas 0,01
```

Modelis B nukrito mažiau, bet jo galutinis rezultatas vis tiek daug blogesnis. Todėl tavo grafike rodomi abu dalykai:

- likęs Macro-F1;
- kritimas nuo švaraus testo.

Dar atliekamas atskiras požymių jautrumo bandymas: po vieną visiškai paslepiamas kiekvienas iš 18 požymių. Taip nustatoma, kurių požymių praradimas SVM rezultatui pakenkia labiausiai.

Gynime gali sakyti:

> Modelį mokiau su švaria mokymo dalimi, o trikdžius taikiau tik išoriniam testui. Tikrinau tris Gauso triukšmo lygius ir 5 bei 10 procentų trūkstamų langelių. Kiekvieną lygį kartojau 20 kartų visuose 50 skaidinių. Visi modeliai gavo tas pačias perturbacijas. Atsparumą vertinau pagal likusį Macro-F1 ir jo kritimą nuo švaraus testo.

---

### 10. 2026-09-22 15:04 UTC

**Naudotojas:**

~~~~~text
parodyk kuriuose failuose yra treniruojami tam tikri modeliai
~~~~~

**Asistentas (eigos pranešimas):**

Patikrinsiu dabartines failų eilutes, kad galėčiau pateikti tikslias nuorodas į kiekvieno modelio sukūrimą, mokymą ir hiperparametrų paiešką.

**Asistentas (galutinis atsakymas):**

Visi modeliai aprašyti viename pagrindiniame faile – [src/models.py](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:18>). Pats jų mokymas per visus skaidinius valdomas faile [run_experiment.py](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:63>).

| Modelis | Kur sukuriamas | Kur faktiškai mokomas |
|---|---|---|
| Artimiausias centroidas | [models.py:92](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:92>) | [run_experiment.py:70](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:70>) |
| 5-NN | [models.py:94](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:94>) | [run_experiment.py:70](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:70>) |
| SVM RBF | [models.py:98](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:98>) | [run_experiment.py:73](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:73>) |
| Tiesinis SVM | [models.py:100](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:100>) | [run_experiment.py:73](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:73>) |
| MLP neuroninis tinklas | [models.py:59](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:59>) | [models.py:76](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:76>) ir [run_experiment.py:77](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:77>) |
| RBF tinklas | [models.py:18](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:18>) | KMeans centrai mokomi [models.py:36](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:36>), Ridge išvestis – [models.py:46](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:46>) |

Bendra mokymo eiga yra tokia:

1. [run_experiment.py:267](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:267>) ciklas paeiliui ima visus septynis modelių variantus.
2. [run_experiment.py:269](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:269>) iškviečia `fit_model`.
3. `fit_model` sukuria modelio pipeline per [build_pipeline](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/src/models.py:90>).
4. Jei modelis turi hiperparametrų, [GridSearchCV](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:73>) išbando jų kombinacijas.
5. Tikras mokymo iškvietimas yra `search.fit(X_train, y_train)` [run_experiment.py:77](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:77>).
6. Baseline modeliams be parametrų paieškos tiesiogiai kviečiamas `pipeline.fit` [run_experiment.py:70](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:70>).

Tikrinami hiperparametrai aprašyti [configs/main.yaml](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/configs/main.yaml:10>). Pavyzdžiui, ten pateiktos SVM `C` ir `gamma`, MLP sluoksnių konfigūracijos bei RBF tinklo centrų skaičiai.

Pabaigoje dar mokomas galutinis SVM modelis naudojant visus 846 įrašus – [run_experiment.py:317](<C:/Users/sersn/Desktop/Magistras/1 semestras/Intelektualios sistemos/Egzaminas/run_experiment.py:317>). Jis skirtas naujiems įrašams prognozuoti, o metodų kokybė vertinama pagal ankstesnius 50 išorinių skaidinių.

---


