# Koliokviumo plano patikslinimai

2026-09-21, užregistruota prieš pakartotinį visą eksperimentą.

Ankstesnis eksperimentas sunaudojo 22 701 modelio pritaikymą. Kad naujas paleidimas tilptų į plane nustatytą 20 000 ribą, pašalinama vidurinė MLP alpha reikšmė 0,001 ir didžiausias RBF pločio daugiklis 2. Lieka abi reguliarizacijos diapazono kraštinės, visos MLP architektūros ir visi RBF centrų skaičiai. Ši taisyklė mažina kandidatų skaičių pagal tinklelio sandarą, ne pagal atskirų išorinių skaidinių klaidas. Ankstesni rezultatai jau žinomi, todėl šio patikslinimo negalima pristatyti kaip pradinio, dar nematant duomenų užregistruoto plano.

Naujas biudžetas: 50 × (2 + 101 + 61 + 91 + 21 + 101) + 101 = 18 951. SVM, baseline, abliacijų tinkleliai, sėklos ir vertinimo protokolas nesikeičia. Papildoma požymių trūkumo diagnostika modelių nepermoko. Programa prieš mokymą tikrina biudžetą.

Prognozavimo trukmė matuojama kiekvienam išoriniam bandymo paketui. Windows proceso PeakWorkingSetSize matuojamas po mokymo ir diagnostikos; vienas procesas leidžia įtraukti visą modelių mokymo atmintį. Ataskaitos kūrimo atskiras procesas neįtrauktas. Darbo trukmė registruojama iki rezultatų tikrinimo ir tekstinės ataskaitos kūrimo. Naudojamos iki keturių native skaičiavimo gijų.

Kodo Git revizija išsaugoma, jei repozitorija turi commit. Jei jos nėra, JSON nurodo null ir priežastį; tikslų vykdytą kodą identifikuoja failų SHA256 manifestas. Modelio versija sudaroma iš kodo tapatybės ir paleidimo UTC laiko.

Plano modulių funkcijos įgyvendintos src/data.py, src/models.py, run_experiment.py, build_report.py ir predict.py. Atskirų cv.py, evaluate.py ir robustness.py nebuvimas yra struktūros supaprastinimas, ne praleistas funkcionalumas. SVC balsų lygybė sprendžiama bibliotekos numatytąja taisykle, kaip paaiškinta ai_log.md; plano teiginys apie balų sumavimą buvo netikslus.

Grupinis bandymas negalimas be patikimų grupių identifikatorių. Trijų papildomų MLP inicializacijų atsisakoma dėl biudžeto; plane jos numatytos tik jei leidžia biudžetas. Abu apribojimai lieka atskleisti.

Papildomai `resources.json` pateikiama konservatyvi visos eigos RAM viršutinė riba: mokymo proceso pikas ir didesnis iš paeiliui vykdytų patikros bei ataskaitos procesų pikų. Taip vertinama ir pagalbinių procesų atmintis.
