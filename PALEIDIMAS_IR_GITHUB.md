# Paprastas paleidimas ir GitHub

Dukart paspauskite START.cmd. Pasirinkimas 1 atidaro JupyterLab, pasirinkimas 2 pakartoja visą eksperimentą ir atnaujina results/main. Pirmą kartą trūkstamos priklausomybės įdiegiamos automatiškai; reikia Python ir interneto. Jupyter serveris veikia fone, todėl START.cmd langą galima uždaryti. Serverį sustabdysite Jupyter meniu File → Shut Down. Pakartotinai pasirinkus 1, atidaromas jau veikiantis šio projekto serveris. Paleidimo klaidos saugomos vietiniame .jupyter-run/server.log; šis aplankas nekeliamas į GitHub.

GitHub Desktop programoje prisijunkite prie savo paskyros, pasirinkite File → Add local repository ir nurodykite šį Egzaminas aplanką. Changes skiltyje patikrinkite failus, įrašykite pakeitimų pavadinimą ir spauskite Commit. Tuomet pasirinkite Publish repository, įrašykite pavadinimą ir pasirinkite, ar saugykla privati (Keep this code private), ar vieša. Patvirtinkite Publish repository.

.gitignore paruoštas įtraukti programą, sąsiuvinius ir galutinius results/main rezultatus. Virtuali aplinka, laikini failai, ankstesnių bandymų archyvas ir atsisiunčiama data kopija neįtraukiami. Tai nekeičia vietinių failų. Eksperimento duomenų failą programa gali atsisiųsti pagal oficialią nuorodą ir patikrina jo kontrolinę sumą.

Tolimesniems pakeitimams: Commit, tada Push origin.

Oficiali instrukcija: https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop
