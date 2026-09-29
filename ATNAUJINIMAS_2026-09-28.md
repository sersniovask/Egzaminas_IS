# Egzamino darbo atnaujinimas po dėstytojo pastabų

2026-09-28. Šis dokumentas papildo pradinį `results/main/` eksperimentą. Pradiniai 846 OpenML Vehicle v1 įrašai ir 50 išorinių skaidinių nekeičiami. Vėlesni bandymai aiškiai žymimi tiriamaisiais, nes pradiniai rezultatai jau buvo žinomi.

## Praktinė problema ir terminai

Pagal 18 iš dvejetainių siluetų jau apskaičiuotų geometrinių požymių reikia atpažinti keturis konkrečius modelinius transporto priemonių tipus: autobusą, furgoną, Opel ir Saab. Programa nepriima vaizdo pikselių ir neįrodo tinkamumo naujoms markėms ar kameroms. Opel ir Saab atskyrimas yra kritinė šio keturių klasių uždavinio vieta. Pradiniame SVM 563 iš 671 klaidų buvo šios poros supainiojimai (penkių CV kartojimų suma).

Toliau vartojami terminai: **atskaitos metodas** (baseline), **duomenų paruošimo grandinė** (pipeline), **vidinė kryžminė patikra** (parametrams rinkti), **išorinis testavimo skaidinys** (galutiniam to skaidinio vertinimui), **preciziškumas** (precision), **jautrumas** (recall), **subalansuotas tikslumas** (balanced accuracy). Išorinio testo rezultatas nėra mokymo ar vidinės patikros rezultatas.

## Du nauji tyrimai

1. D. Yang ir kt. (2024), *Multi-Strategy Assisted Multi-Objective Whale Optimization Algorithm for Feature Selection*, [DOI 10.32604/cmes.2024.048049](https://doi.org/10.32604/cmes.2024.048049). Autoriai nagrinėja klasifikavimo klaidos ir požymių skaičiaus kompromisą; tarp jų bandymų yra „Vehicle Silhouettes“. Ši idėja tinka patikrinti, ar Opel ir Saab painiojimą didina nenaudingi arba pasikartojantys požymiai. Mes išbandėme skaidresnę `SelectKBest` atranką su 12 arba 18 požymių vidinėje kryžminėje patikroje. **Tai nėra jų banginių optimizavimo algoritmo reprodukcija.**
2. M. Przybyła-Kasperek ir K. F. Marfo (2024), *A multi-layer perceptron neural network for varied conditional attributes in tabular dispersed data*, [DOI 10.1371/journal.pone.0311041](https://doi.org/10.1371/journal.pone.0311041). Modifikuotas MLP su vietinių modelių agregavimu taip pat tirtas su šiuo rinkiniu. Jis aktualus, jei požymiai gaunami iš kelių šaltinių ar skirtingų jutiklių. Mūsų 18 požymių vienoje lentelėje tokio scenarijaus nėra, todėl vien dirbtinis lentelės skaidymas nebūtų praktiškai pagrįstas. Šis metodas paliktas svarstytina alternatyva būsimiems paskirstytiems duomenims.

Šių tyrimų skelbiami skaičiai nėra tiesiogiai lyginami su mūsų rezultatu dėl skirtingų duomenų skaidymų ir vertinimo protokolų. Literatūra pagrindžia bandymo kryptį, bet ne garantuotą pagerėjimą.

## Bandymų seka ir sprendimai

| Bandymas | 50 išorinių testų Macro-F1 | Opel F1 | Saab F1 | Sprendimas |
|---|---:|---:|---:|---|
| Pradinis SVM | 0,842 | 0,716 | 0,721 | Atskaitos taškas |
| Porinis Opel–Saab specialistas su požymių atranka | 0,831 | 0,690 | 0,705 | Atmestas: pablogino abi klases |
| Platesnės paieškos SVM su 12 arba 18 požymių atranka | 0,852 | 0,736 | 0,747 | Tiriamasis geresnis variantas |

Specialistas (`improve_cars.py`) mokytas tik iš išorinės mokymo dalies Opel ir Saab įrašų. Jo `k`, `C` ir `gamma` rinkti penkių dalių vidinėje patikroje. Jis keitė pradinio SVM sprendimą tik tada, kai tas sprendimas buvo Opel arba Saab. Skirtumas nuo pradinio SVM buvo −0,011 Macro-F1; šis variantas atmetamas, o ne nutylimas.

Platesnė paieška (`tune_svm.py`) išbandė `C ∈ {10,100,1000}`, `gamma ∈ {0,003;0,01;0,03;scale}` ir `k ∈ {12,18}`. Trūkstamų reikšmių pildymas, standartizavimas ir požymių atranka buvo vienoje grandinėje, todėl kiekviena vidinė patikra juos išmoko tik iš savo mokymo dalies. **Visuose 50 skaidinių pasirinkta `k=18`**; mažesnis požymių rinkinys nepadėjo. `C=1000` pasirinktas 33 kartus, `C=100` – 17 kartų. Taigi stebimas pagerėjimas siejamas su platesniu SVM derinimu. `C=1000` vėl yra paieškos kraštas, todėl optimumo riba dar nenustatyta.

Platesnio SVM porinis vidutinis pokytis +0,010 Macro-F1; jis buvo geresnis 29 ir blogesnis 12 iš 50 skaidinių (9 lygūs). Apytikslis pataisytas 95 % intervalas **[−0,008; +0,028] apima nulį**. Jis pateiktas tik kaip priklausomų skaidinių skirtumo aprašas: metodas sukurtas žinant ankstesnius išorinio testo rezultatus. Didesnis skaičius nėra nepriklausomas pagerėjimo įrodymas. Naujas modelis skirtas tolesniam tikrinimui, o ne teiginiui, kad Opel–Saab painiojimas išspręstas galutinai.

## Parametrų ir mokymo kokybės auditas

Pradiniuose 50 vidinės paieškos laimėtojų SVM `C=100` parinktas **48** kartus, `gamma=0,01` – **37**, `scale` – **13**. Tai parodė ankstesnės `C` ribos problemą. MLP mokymosi žingsnis `0,01` laimėjo **50** kartų, `alpha=0,01` – **34**, sluoksniai `(32,16)` – **30**. RBF tinkle 32 centrai ir plotis 1 laimėjo **50** kartų; 32 buvo didžiausias bandytas centrų skaičius.

Kiekvienam metodui palygintas geriausias vidinis Macro-F1 ir išorinis Macro-F1: SVM atitinkamai **0,841 ir 0,842**, MLP **0,778 ir 0,775**, RBF tinklui **0,727 ir 0,727**. Vien panašūs vidurkiai neįrodo, kad nėra persimokymo atskiruose skaidiniuose; visi šie skaidiniai priklausomi.

Pasirinktas MLP konfigūracijas papildomai iš naujo apmokėme 50 kartų tik su atitinkamomis išorinėmis mokymo dalimis. Medianinis sustojimas **35,5 epochos** (17–64), mokymo nuostolis sumažėjo visais 50 atvejų, `ConvergenceWarning` nebuvo. Vidutinė geriausia vidinės validacijos tikslumo reikšmė buvo **0,826**. MLP taikytas ankstyvas stabdymas, todėl mažas epochų skaičius nėra savaime klaida; jis taip pat nėra įrodymas, kad modelis optimaliai suderintas. Dabartinio `run_experiment.py` globalus konvergencijos perspėjimų slopinimas riboja pirminio paleidimo diagnostiką; atskiras pakartotinis auditas šiuos perspėjimus registravo.

## Skaitinis metrikų pavyzdys

Sujungtoje penkių išorinių kartojimų pradinio SVM painiavos matricoje tikrųjų Opel vertinimų buvo **1060**. Teisingai atpažinti **753** (`TP`), praleisti **307** (`FN`), o **289** kitų klasių vertinimai klaidingai pavadinti Opel (`FP`).

- Preciziškumas `753 / (753 + 289) = 0,723`: iš 100 Opel prognozių maždaug 72 yra teisingos.
- Jautrumas `753 / (753 + 307) = 0,710`: iš 100 tikrųjų Opel aptinkama maždaug 71.
- F1 `2×753 / (2×753 + 289 + 307) = 0,716`: subalansuoja šiuos du rodiklius.
- Macro-F1: keturių klasių F1 aritmetinis vidurkis. Subalansuotas tikslumas: keturių klasių jautrumų aritmetinis vidurkis.

Tie 1060 Opel vertinimų nėra 1060 skirtingų transporto priemonių: tai 212 įrašų po penkis kartus. Todėl pagrindinio rezultato vienetas yra išorinio skaidinio metrika, o šis pavyzdys skirtas lentelės prasmei paaiškinti.

## Patikra ir atkūrimas

Paleisti projekto aplanke su `requirements.txt` priklausomybėmis:

```powershell
python audit_training.py
python improve_cars.py
python tune_svm.py
python verify_improvement.py
python predict_updated.py --input unseen.json
```

`verify_improvement.py` sutikrina visus 50 tų pačių išorinių testų indeksus, 4230 kiekvieno varianto prognozių, tikrąsias žymas, pradinio SVM prognozes ir nepriklausomai perskaičiuoja skaidinių F1. Patikrintas ir galutinio naujo modelio įkėlimas bei prognozė. Naujas galutinis modelis apmokytas visais 846 duomenimis **tik po vertinimo**; jo mokymo rinkinio tikslumas nėra ataskaitos palyginimo rodiklis.

Pradinė išorinė kryžminė patikra išlieka vienoda, bet jos kartotinis naudojimas kuriant naujas idėjas didina tyrėjo pasirinkimų šališkumą. Nepriklausomam teiginiui apie naujo varianto naudą reikėtų papildomų tikrų ir ženklintų siluetų, geriausia iš naujų transporto priemonių bei kameros sąlygų. Tokie duomenys nebuvo gauti, todėl nepridėjome sintetinių „naujų“ ženklintų objektų.
