# Paprastas paleidimas ir GitHub

Dukart paspauskite START.cmd. Pasirinkimas 1 atidaro JupyterLab, 2 pakartoja tik pradinį eksperimentą ir atnaujina `results/main/`, 3 patikrina jau išsaugotus trijų papildomų modelių rezultatus be naujo mokymo, 4 paprašo naujo 18 požymių JSON failo ir pritaiko tiriamąjį TabPFN v2 modelį. Komandinei eilutei: `.\START.cmd --verify-further`, `.\START.cmd --predict-tabpfn "C:\kelias\irasas.json"`, `.\START.cmd --check-tabpfn`. Pirminio SVM prognozė atskirai vykdoma `predict.py`, ankstesnio platesnio SVM - `predict_updated.py`. Pasirinkimas 2 **neperleidžia** papildomų SVM, ExtraTrees ar TabPFN bandymų.

Pagrindinėms komandoms trūkstamos `.venv` priklausomybės įdiegiamos automatiškai. TabPFN turi atskirą aplinką: šiame kompiuteryje naudojama jau įdiegta `C:\Users\sersn\Documents\ChatGPT\IS Egzaminas\.venv_tabpfn`; jei jos nėra, START.cmd sukurs projekto `.venv_tabpfn` ir įdiegs paketus pagal `requirements_tabpfn_v2_lock.txt`. Pirmajam įdiegimui ir oficialių svorių atsisiuntimui reikia interneto. Jupyter serveris veikia fone, todėl START.cmd langą galima uždaryti; jį sustabdysite Jupyter meniu File → Shut Down. Paleidimo klaidos saugomos vietiniame `.jupyter-run/server.log`.

Jei reikia tęsti nutrūkusį naujų modelių mokymą, tikslios penkios komandos yra README skyriuje „Dabartinis paleidimas“. `experiment_next_20260928.py` išsaugo kiekvieną baigtą skaidinį ir pakartotinai jo nemoko; visos eigos perleidimas su `--no-resume` perrašytų tuos failus, todėl tokį bandymą darykite atskiroje projekto kopijoje.

GitHub Desktop programoje prisijunkite prie savo paskyros, pasirinkite File → Add local repository ir nurodykite šį Egzaminas aplanką. Changes skiltyje patikrinkite failus, įrašykite pakeitimų pavadinimą ir spauskite Commit. Tuomet pasirinkite Publish repository, įrašykite pavadinimą ir pasirinkite, ar saugykla privati (Keep this code private), ar vieša. Patvirtinkite Publish repository.

.gitignore paruoštas įtraukti programą, sąsiuvinius, pagrindinius `results/main/` ir papildomų bandymų `results/further_20260928/`, `results/wide_svm_20260928/`, `results/improvement_20260928/`, `results/training_audit_20260928/` rezultatus. Virtualios aplinkos, laikini failai, ankstesnių bandymų archyvas ir atsisiunčiama duomenų kopija neįtraukiami. Tai nekeičia vietinių failų. Eksperimento duomenų failą programa gali atsisiųsti pagal oficialią nuorodą ir patikrina jo kontrolinę sumą.

Tolimesniems pakeitimams: Commit, tada Push origin.

Oficiali instrukcija: https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop
