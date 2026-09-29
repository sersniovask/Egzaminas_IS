from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT
RESULTS = PROJECT / 'results' / 'main'
OUT = PROJECT / 'Egzamino_ataskaita_atnaujinta_2026-09-28.pdf'
TMP = ROOT / 'report_assets'
TMP.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('DejaVu', str(FONT_DIR / 'arial.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', str(FONT_DIR / 'arialbd.ttf')))
pdfmetrics.registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVu-Bold')

NAVY = colors.HexColor('#17324f')
BLUE = colors.HexColor('#27618e')
PALE = colors.HexColor('#edf3f8')
INK = colors.HexColor('#23313e')
MUTED = colors.HexColor('#607182')

def clean(s: str) -> str:
    return str(s).replace('–', '-').replace('—', '-').replace('−', '-').replace('\u2011', '-').replace('\u00a0', ' ')

def safe(s: str) -> str:
    return escape(clean(s))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleLT', fontName='DejaVu-Bold', fontSize=25, leading=32,
                          textColor=NAVY, spaceAfter=20))
styles.add(ParagraphStyle(name='Deck', fontName='DejaVu', fontSize=13, leading=19,
                          textColor=BLUE, spaceAfter=20))
styles.add(ParagraphStyle(name='H1LT', fontName='DejaVu-Bold', fontSize=15, leading=20,
                          textColor=NAVY, spaceBefore=14, spaceAfter=9, keepWithNext=True))
styles.add(ParagraphStyle(name='H2LT', fontName='DejaVu-Bold', fontSize=11, leading=15,
                          textColor=BLUE, spaceBefore=10, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name='BodyLT', fontName='DejaVu', fontSize=9, leading=13.7,
                          textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name='SmallLT', fontName='DejaVu', fontSize=7.7, leading=11,
                          textColor=MUTED, spaceAfter=6))
styles.add(ParagraphStyle(name='BulletLT', parent=styles['BodyLT'], leftIndent=14,
                          firstLineIndent=-9, spaceAfter=4))
styles.add(ParagraphStyle(name='CaptionLT', fontName='DejaVu', fontSize=8, leading=11,
                          textColor=MUTED, alignment=TA_CENTER, spaceBefore=3, spaceAfter=9))
styles.add(ParagraphStyle(name='TableHeadLT', fontName='DejaVu-Bold', fontSize=7.5,
                          leading=10, textColor=colors.white))
styles.add(ParagraphStyle(name='TableCellLT', fontName='DejaVu', fontSize=7.4,
                          leading=10.2, textColor=INK))

story = []

def p(text: str, style='BodyLT'):
    story.append(Paragraph(safe(text), styles[style]))

def h1(text: str): p(text, 'H1LT')
def h2(text: str): p(text, 'H2LT')
def bullet(text: str): p('• ' + text, 'BulletLT')

def table(headers, rows, widths=None, font=7.4, keep=False):
    data = [[Paragraph(safe(x), styles['TableHeadLT']) for x in headers]]
    for row in rows:
        data.append([Paragraph(safe(x), styles['TableCellLT']) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, 0), 0.6, NAVY),
    ]))
    if keep:
        story.append(KeepTogether([t, Spacer(1, 8)]))
    else:
        story.append(t)
        story.append(Spacer(1, 8))

def fig(path: Path, width=490, caption=''):
    with PILImage.open(path) as im:
        w, h = im.size
    story.append(Image(str(path), width=width, height=width * h / w, hAlign='CENTER'))
    if caption:
        p(caption, 'CaptionLT')

def make_charts():
    summary = pd.read_csv(RESULTS / 'results_summary.csv').set_index('method')
    robust = pd.read_csv(RESULTS / 'robustness_summary.csv', skiprows=3,
                         names=['method','kind','level','f1','f1sd','ba','basd'])
    rp=TMP/'robustness.png'
    ip=TMP/'importance.png'
    assert rp.exists() and ip.exists(), 'Run build_charts.py first'
    return summary,robust,rp,ip

summary, robust, robustness_path, importance_path = make_charts()

story += [Spacer(1, 62)]
p('Transporto priemonių siluetų klasifikavimas', 'TitleLT')
p('Egzamino darbo ataskaita', 'Deck')
story.append(HRFlowable(width='100%', thickness=2, color=BLUE, spaceAfter=20))
p('Kirilas Šeršniovas  |  PEPfm-26  |  Intelektualiosios sistemos')
p('Atnaujinta 2026-09-29. Pradinis palyginimas iš results/main/; vėlesni tiriamieji bandymai iš atskirų results/ aplankų.', 'SmallLT')
story.append(Spacer(1, 22))
h2('Trumpa išvada')
p('Pradiniame iš anksto apibrėžtame bandyme geriausias buvo SVM su RBF branduoliu: išorinis Macro-F1 0,842, palyginti su 5-NN 0,708. Vėliau, jau matant šio testo rezultatus, platesnė SVM paieška pasiekė 0,852, o naujas TabPFN v2 kandidatas - 0,869. Pastarasis pagerino bendrą rodiklį, tačiau Opel ir Saab tarpusavio supainiojimų nesumažino, palyginti su platesniu SVM (525 ir 522). Vėlesni bandymai tiriamieji, todėl nepriklausomai patvirtinto pranašumo neteigiame.')
p('Ataskaita apima užduotį, duomenų ir vertinimo protokolą, metodų palyginimą, abliaciją, atsparumą, klaidų analizę ir atkūrimą. B priede yra naujų bandymų lentelė bei grafikai. AI_POKALBIU_ISTORIJA.md saugo užfiksuotus pokalbių tekstus ir aiškiai pažymėtas vėlesnių etapų santraukas; sprendimų patikros pateiktos ai_log.md.')
story.append(PageBreak())

h1('1. Užduotis ir sprendimo apimtis')
p('Užduoties tikslas - pagal iš transporto priemonės silueto jau apskaičiuotus geometrinius požymius nustatyti vieną iš keturių klasių: bus, opel, saab arba van. Šaltinis - OpenML Vehicle, duomenų rinkinio ID 54, 1 versija. Pradinės nuotraukos rinkinyje nepateiktos, todėl sprendimas pradeda darbą nuo 18 skaitinių požymių, o ne nuo vaizdo.')
p('Galutinis darbas turėjo pateikti dvi paprastas bazes, bent du intelektualiuosius metodus, vienodą vertinimo protokolą, abliaciją arba jautrumą, atsparumo bandymą, rezultatų lentelę ir grafiką, klaidų analizę bei atkūrimo ir AI naudojimo dokumentaciją. Visas originalios užduoties tekstas lietuvių kalba ir vertinimo balai perkelti į A priedą.')
h2('Kolokviumo plano įgyvendinimas')
table(['Plane pasirinkta', 'Įgyvendinimas / įrodymas'], [
    ['kNN ir centroidų bazės', 'Du atskaitos metodai; rezultatai bendroje lentelėje.'],
    ['SVM RBF, MLP, RBF tinklas', 'Visi trys išmokyti ir įvertinti 50 vienodų išorinių skaidinių.'],
    ['SVM hipotezė: > 0,02 virš geriausios bazės', 'Gautas porinis skirtumas +0,134; pataisytas 95 % intervalas [+0,097; +0,170].'],
    ['Abliacija ir atsparumas', 'Tiesinis SVM, SVM be mastelio keitimo, triukšmas ir trūkstami duomenys.'],
    ['Atkuriamumas ir skaičiavimo biudžetas', 'Fiksuotos sėklos, konfigūracija, 18 951 pritaikymas, išsaugoti CSV ir modelis.'],
], [190, 315])
p('Pradinis MLP ir RBF tinklo hiperparametrų tinklelis viršijo 20 000 pritaikymų planą. Prieš pakartotinį galutinį paleidimą jis sumažintas ir pakeitimas užregistruotas plano_patikslinimai.md. Kadangi ankstesni rezultatai jau buvo žinomi, pakartotinis paleidimas nėra nepriklausomas išankstinės hipotezės patvirtinimas.')

h1('2. Duomenys ir eksperimento protokolas')
p('OpenML Vehicle v1 turi 846 įrašus ir 18 skaitinių silueto požymių: bus - 218, opel - 212, saab - 217, van - 199. Duomenų MD5: fbba18157b188f309d772f9ca4e578f5. Duomenų gavimas, stulpelių skaičius, leistinos klasės ir kontrolinė suma tikrinami prieš eksperimentą.')
p('Naudota 5 pakartojimai po 10 stratifikuotų išorinių skaidinių - iš viso 50 išorinių bandymų. Kiekvienas metodas gauna tas pačias mokymo ir bandymo indeksų poras. Kiekvienos išorinės mokymo dalies viduje hiperparametrai parenkami 5 dalių kryžminiu vertinimu pagal Macro-F1; išorinis bandymo skaidinys tam nenaudojamas.')
p('Kiekviename mokyme trūkstamų reikšmių medianos ir standartizavimo parametrai apskaičiuojami tik iš mokymo duomenų. Tos pačios išmoktos transformacijos taikomos bandymo daliai. Pagrindinės metrikos: Macro-F1 - keturių klasių F1 vidurkis; balanced accuracy - keturių klasių jautrumų vidurkis. Painiavos matrica pateikiama klaidų analizei.')

h1('3. Metodai ir formulės ryšys su realizacija')
table(['Vaidmuo', 'Metodas', 'Trumpas veikimo principas'], [
    ['Atskaitos', '5-NN', 'Klasė pagal penkis artimiausius mokymo objektus.'],
    ['Atskaitos', 'Artimiausias centroidas', 'Parenkamas arčiausias klasės požymių vidurkis.'],
    ['Pagrindinis', 'SVM RBF', 'Netiesinė skiriamoji riba su C ir gamma reguliavimu.'],
    ['Alternatyva', 'MLP', 'Daugiasluoksnis perceptronas su reguliavimu ir ankstyvu stabdymu.'],
    ['Alternatyva', 'RBF tinklas', 'KMeans centrai, Gauso aktyvacijos, Ridge išvestis.'],
], [75, 125, 305])
p('SVM naudotas standartizavimas z_j = (x_j - μ_j) / s_j ir RBF branduolys K(z,z\u2032) = exp(-γ ||z-z\u2032||²). Čia μ_j ir s_j yra tik mokymo dalies statistikos; γ valdo lokalumą, o C - maržos ir mokymo klaidų kompromisą. src/models.py funkcija build_pipeline jungia SimpleImputer, StandardScaler ir SVC(kernel="rbf"). C ir gamma kandidatų atranka atliekama run_experiment.py vidinėje CV. Keturioms klasėms SVC naudoja šešis porinius sprendimus.')
p('RBF tinklo realizacijoje src/models.py klasė RBFNetwork.fit apskaičiuoja KMeans centrus ir Ridge išvesties sluoksnį. Šis metodas yra atskiras nuo SVM RBF branduolio: vienoda radialinių funkcijų idėja nereiškia vienodo mokymo algoritmo.')
h2('Formulės ir konkrečios programos vietos')
table(['Formulė arba taisyklė','Programos vieta','Kas ten atliekama'],[
    ['z_j = (x_j - μ_j) / s_j','src/models.py: build_pipeline','StandardScaler mokomas tik atitinkamo mokymo skaidinio duomenimis.'],
    ['K(z,z\u2032) = exp(-γ ||z-z\u2032||²)','src/models.py: build_pipeline("svm")','SVC RBF branduolys; C ir gamma kandidatai vertinami vidinėje CV.'],
    ['Macro-F1 = keturių klasių F1 vidurkis','run_experiment.py: metrics','Ta pati pagrindinė metrika skaičiuojama kiekviename išoriniame teste.'],
],[150,145,210])
h2('Iš anksto apibrėžta vidinė paieška')
table(['Metodas','Derinti parametrai','Atrankos taisyklė'],[
    ['SVM RBF','C: 0,1; 1; 10; 100. Gamma: scale; 0,001; 0,01; 0,1; 1.','Geriausias vidinis Macro-F1.'],
    ['MLP','Sluoksniai: 16; 32; (32,16). Alpha: 0,0001; 0,01. Mokymosi žingsnis: 0,001; 0,01.','Geriausias vidinis Macro-F1.'],
    ['RBF tinklas','Centrai: 8; 16; 32. Plotis: 0,5; 1. Ridge alpha: 0,001; 0,01; 0,1.','Geriausias vidinis Macro-F1.'],
],[96,285,124])
p('MLP ir RBF parametrai atitinka prieš pakartotinį galutinį paleidimą dokumentuotą sumažintą tinklelį; abiejų baseline parametrai nebuvo derinami.', 'SmallLT')

h1('4. Pagrindiniai rezultatai')
labels={'svm':'SVM RBF','mlp':'MLP','rbf':'RBF tinklas','knn':'5-NN',
        'centroid':'Centroidas','svm_linear':'SVM tiesinis','svm_unscaled':'SVM be stand.'}
roles={'svm':'pagrindinis','mlp':'intelektualus','rbf':'intelektualus','knn':'bazė',
       'centroid':'bazė','svm_linear':'abliacija','svm_unscaled':'abliacija'}
rows=[]
for method,row in summary.iterrows():
    rows.append([labels[method],roles[method],
                 f"{row.macro_f1_mean:.3f} ± {row.macro_f1_sd:.3f}",
                 f"{row.balanced_accuracy_mean:.3f} ± {row.balanced_accuracy_sd:.3f}",
                 f"{row.train_seconds_mean:.3f}"])
table(['Metodas','Vaidmuo','Macro-F1 ± SD','Balanced acc. ± SD','Mokymas, s'],rows,[126,87,111,117,64])
p('Lentelėje pateiktas 50 išorinių skaidinių vidurkis ir standartinis nuokrypis. Šie skaidiniai priklausomi, nes tie patys įrašai vertinami per penkis pakartojimus; todėl SD nėra nepriklausomų 50 imčių paklaida. Laikas yra vidutinis vieno išorinio modelio mokymo laikas su vidine paieška.')
p('SVM RBF pranoko abi privalomas bazes ir kitas intelektualiąsias alternatyvas pagal iš anksto pasirinktą Macro-F1. SVM ir geresnio baseline, 5-NN, porinis skirtumas +0,134; pataisytas 95 % intervalas [+0,097; +0,170]. SVM buvo geresnis visuose penkiuose pakartojimuose. Tai dera su hipoteze, kad netiesinė riba naudinga persidengiančioms klasėms, nors vien šis bandymas neįrodo tikslaus laimėjimo mechanizmo.')
h2('Porinis SVM palyginimas tuose pačiuose skaidiniuose')
folds=pd.read_csv(RESULTS/'fold_metrics.csv').pivot(index='split',columns='method',values='macro_f1')
assert folds.shape==(50,7) and folds.notna().all().all()
paired=[]
for method in ['knn','centroid','mlp','rbf','svm_linear','svm_unscaled']:
    diff=folds['svm']-folds[method]
    paired.append([labels[method],f'{diff.mean():+.3f}',f'{(diff>0).sum()}/50'])
table(['Palyginimas su','Vidutinis SVM Macro-F1 skirtumas','SVM geresnis skaidiniuose'],paired,[161,187,157])
p('Šis pergalių skaičius yra aprašomasis: tie patys objektai kartojasi, todėl 50 skaidinių nėra 50 nepriklausomų bandymų. Pataisytas intervalas pateiktas tik iš anksto numatytam SVM ir geriausio baseline, 5-NN, hipotezės palyginimui.', 'SmallLT')
fig(RESULTS/'macro_f1_boxplot.png',480,'1 pav. Macro-F1 pasiskirstymas tų pačių išorinių skaidinių vertinime.')

h1('5. Abliacija ir požymių jautrumas')
p('Pakeitus RBF branduolį tiesiniu, Macro-F1 sumažėjo nuo 0,842 iki 0,794 (-0,047). Pašalinus standartizavimą jis sumažėjo iki 0,756 (-0,086). Abu variantai buvo vertinti tais pačiais išoriniais skaidiniais; jų hiperparametrai derinti tik vidinėje mokymo dalyje.')
fig(importance_path,475,'2 pav. Didžiausi vidutiniai Macro-F1 kritimai permutavus po vieną požymį tik išorinėje bandymo dalyje.')
p('Svarbiausi pagal šį diagnostinį bandymą: HOLLOWS_RATIO (0,234), RADIUS_RATIO (0,216), SKEWNESS_ABOUT_MAJOR (0,171). Permutacijos kritimas rodo šio išmokyto modelio jautrumą, o ne priežastinę požymio įtaką. Rezultatai nebuvo naudoti modeliui perrinkti.')

h1('6. Atsparumo bandymai')
p('Visiems penkiems pagrindiniams metodams tie patys išoriniai bandymo objektai buvo perturbuoti vienodai. Gauso triukšmo lygiai: 0,05, 0,10 ir 0,20 nuo atitinkamos mokymo dalies požymio standartinio nuokrypio. Atskirai paslėpta 5 % ir 10 % bandymo langelių, kuriuos užpildo tik mokymo dalyje išmoktas medianų imputatorius. Kiekvienam lygiui panaudota 20 fiksuotų realizacijų.')
fig(robustness_path,495,'3 pav. Metodų Macro-F1, didinant triukšmą ir trūkstamų požymių dalį. Nulinis taškas - švarus išorinis testas.')
robrows=[]
for method in ['centroid','knn','svm','mlp','rbf']:
    cleanv=float(summary.loc[method,'macro_f1_mean'])
    noise=float(robust[(robust.method==method)&(robust.kind=='noise')&(robust.level==0.2)].f1.iloc[0])
    miss=float(robust[(robust.method==method)&(robust.kind=='missing')&(robust.level==0.1)].f1.iloc[0])
    robrows.append([labels[method],f'{cleanv:.3f}',f'{noise:.3f}',f'{noise-cleanv:+.3f}',f'{miss:.3f}',f'{miss-cleanv:+.3f}'])
table(['Metodas','Švarus','Triukšmas 0,20','Pokytis','Trūksta 10 %','Pokytis'],robrows,[100,66,94,70,100,75])
p('SVM išlieka pirmas esant abiem stipriausiems bandytiems trikdžiams, tačiau jo kritimas didžiausias: -0,077 su triukšmu 0,20 ir -0,118, kai trūksta 10 % langelių. Trikdžio realizacijos ir CV skaidiniai nėra nepriklausomos naujos duomenų imtys. Šie testai neapima naujų kamerų, naujų automobilių modelių ar laiko poslinkio.')

h1('7. Klaidų analizė')
p('Sujungtoje SVM painiavos matricoje kiekvienas iš 846 įrašų pasirodo penkis kartus. Daugiausia painiavos tarp Opel ir Saab: Opel priskirtas Saab 290 kartų, Saab priskirtas Opel 273 kartus. Autobusai ir furgonai atpažinti geriau. Ši matrica nėra 4 230 skirtingų transporto priemonių.')
class_report=json.loads((RESULTS/'class_report_svm.json').read_text(encoding='utf-8'))
class_rows=[]
for name in ['bus','opel','saab','van']:
    metrics=class_report[name]
    class_rows.append([name,f"{metrics['precision']:.3f}",f"{metrics['recall']:.3f}",f"{metrics['f1-score']:.3f}",str(int(metrics['support']))])
table(['Tikroji klasė','Preciziškumas','Jautrumas','F1','Prognozių sk.'],class_rows,[119,114,101,67,104])
p('Lentelės klasės metrikos apskaičiuotos sujungus visų penkių pakartojimų išorines prognozes. Todėl čia pateiktas bendras keturių klasių F1 vidurkis gali nežymiai skirtis nuo pagrindinio 50 skaidinių Macro-F1 vidurkio 0,842. Support reiškia pakartotas išorines prognozes, ne skirtingus įrašus.', 'SmallLT')
p('Opel-Saab kryptinių klaidų suma yra 563 iš 671 visų SVM klaidų (83,9 %). Tai pagrindinė keturių klasių uždavinio silpnoji vieta; dviejų modelių painiojimas nepakeičia reikalavimo teisingai klasifikuoti keturias atskiras klases.')
h2('Kaip skaityti metrikas: skaitinis Opel pavyzdys')
p('Penkis kartus kartoto išorinio testo painiavos matricoje yra 1 060 tikrųjų Opel vertinimų. Iš jų 753 teisingai priskirti Opel (TP), 307 priskirti kitoms klasėms (FN). Dar 289 kitų klasių objektai klaidingai pavadinti Opel (FP). Preciziškumas P = TP/(TP+FP) = 753/(753+289) = 0,723: maždaug 72 iš 100 Opel prognozių yra teisingos. Jautrumas R = TP/(TP+FN) = 753/1 060 = 0,710: aptinkama apie 71 iš 100 tikrųjų Opel. F1 = 2TP/(2TP+FP+FN) = 1 506/2 102 = 0,716. Macro-F1 yra keturių klasių F1 vidurkis; subalansuotas tikslumas - jų jautrumų vidurkis. Tikslumas nėra tas pats, kas preciziškumas. Šie 1 060 vertinimų atitinka 212 skirtingų Opel įrašų penkis kartus.')
fig(RESULTS/'confusion_svm.png',460,'4 pav. SVM RBF painiavos matrica, sudaryta tik iš išorinių prognozių.')
errors=pd.read_csv(RESULTS/'high_margin_errors.csv').head(5)
table(['Įrašo indeksas','Tikroji klasė','Prognozė','Diagnostinis tarpas'],
      [[str(int(r.row_index)),str(r.true),str(r.predicted),f'{r.margin:.3f}'] for r in errors.itertuples()],
      [102,107,107,189],keep=True)
p('Pavyzdžiai rodo klaidingas prognozes su didžiausiu diagnostiniu porinio sprendimo tarpu. Šis tarpas nėra kalibruota tikimybė ir neleidžia teigti, kad konkretus įrašas buvo pažymėtas klaidingai. Originalių silueto vaizdų rinkinyje nėra.')
fig(RESULTS/'error_frequency.png',450,'5 pav. Kiek kartų tas pats įrašas buvo klaidingai klasifikuotas per penkis CV pakartojimus.')
p('647 skirtingi įrašai teisingai klasifikuoti visus penkis kartus, o 81 - neteisingai visus penkis. Paskutinis grafiko stulpelis reiškia penkias to paties įrašo klaidas, o ne prastesnį penktą pakartojimą.')

h1('8. Atkuriamumas, ribos ir gynimas')
p('Pagrindinis eksperimentas kartojamas iš projekto aplanko komanda: python run_experiment.py --config configs/main.yaml. Priklausomybės nurodytos requirements.txt, sėklos - 2026, 2027, 2028, 2029, 2030. Atsisiuntimo instrukcija ir duomenų kontrolinė suma pateiktos README.md. Pilni skaidinių rezultatai, prognozės, patikros JSON ir galutinis SVM modelis saugomi results/main/.')
p('Pakartotiniam paleidimui užregistruota 18 951 modelio pritaikymas ir apie 26,8 min. iki pirmos ataskaitos. Patikros scenarijus perskaičiuoja metrikas iš išsaugotų prognozių, tikrina tuos pačius skaidinius, painiavos matricas ir išsaugoto modelio vientisumą. Tai rodo techninį atkuriamumą nurodytoje aplinkoje; kitose bibliotekų versijose skaičiai gali nežymiai skirtis.')
resources=json.loads((RESULTS/'resources.json').read_text(encoding='utf-8'))
verification=json.loads((RESULTS/'verification.json').read_text(encoding='utf-8'))
table(['Patikra','Užregistruota reikšmė','Įrodymo failas'],[
    ['Išoriniai skaidiniai / variantai',f"{verification['outer_splits']} / {verification['model_variants']}",'verification.json'],
    ['Modelio pritaikymai',f"{resources['model_fits']:,}".replace(',',' '),'resources.json'],
    ['Laikas iki pirmos ataskaitos',f"{resources['seconds_from_manifest_to_first_report']/60:.1f} min",'resources.json'],
    ['Konservatyvi RAM viršutinė riba',f"{resources['workflow_peak_rss_upper_bound_bytes']/1_000_000:.1f} MB",'resources.json'],
    ['Vidinės paieškos lentelės',str(verification['inner_search_tables']),'verification.json'],
    ['Nepriklausomas metrikų perskaičiavimas','Atliktas','verification.json'],
],[197,138,170])
h2('Svarbiausios ribos')
bullet('Duomenys apima keturias konkrečias klases ir kontroliuojamą fotografavimą; realaus eismo tinkamumas neįrodytas.')
bullet('OpenML lentelėje nėra pradinių vaizdų ir patikimų fotografavimo serijų identifikatorių grupiniam testui.')
bullet('Atsitiktinė stratifikacija gali pervertinti veikimą naujam fiziniam automobiliui ar kamerai.')
bullet('Praktinė klaidų kaina konkrečiam diegimo scenarijui nenustatyta; Opel-Saab painiojimas gali būti mažiau svarbus nei rūšių supainiojimas.')
h2('Gyvo gynimo veiksmai')
p('Studentas turi paaiškinti standartizavimo ir SVM RBF formulės ryšį su src/models.py, paleisti dėstytojo pateiktą naują 18 požymių įrašą per predict.py (pradinis SVM) arba START.cmd 4 pasirinkimą (tiriamasis TabPFN v2) ir gyvai atlikti nedidelį modelio, metrikos arba apdorojimo pakeitimą. Šie veiksmai ataskaitos rengimo metu dar nebuvo atlikti ir priklausys nuo dėstytojo pateikto bandymo.')
h2('AI naudojimo auditas')
p('Repository failas ai_log.md registruoja priimtus ir atmestus pasiūlymus, nepatikrintas prielaidas bei jų patikrą. AI_POKALBIU_ISTORIJA.md saugo ankstyvųjų pokalbių tekstus ir pažymėtas vėlesnių etapų santraukas; pastarosios nėra pažodinis eksportas. Tarp užfiksuotų pataisų: 846, o ne 946 OpenML įrašai; SVM sprendimo balai nėra tikimybės; duomenų standartizavimas negali būti apskaičiuotas prieš CV; ankstesnė balsų lygybės prielaida neatitiko bibliotekos nustatymų.')
h1('9. Egzamino kriterijų atitiktis')
table(['Kriterijus','Balai','Kur parodyti įrodymai'],[
    ['Duomenų grandinė, baseline, atkuriamumas','10','2, 3 ir 8 skyriai; README.md; verification.json'],
    ['Bent du intelektualieji metodai','20','3 ir 4 skyriai; trys alternatyvių metodų sąsiuviniai'],
    ['Korektiškas eksperimentas ir vienodas palyginimas','20','2 ir 4 skyriai; tie patys indeksai; vidinė CV'],
    ['Rezultatai, abliacija, atsparumas, klaidos','15','4-7 skyriai; lentelės, grafikai ir konkretūs pavyzdžiai'],
    ['Ribos, rizikos, praktinis tinkamumas','10','7 ir 8 skyriai; duomenų apribojimai ir trikdžių analizė'],
    ['AI naudojimo auditas','5','ai_log.md ir AI_POKALBIU_ISTORIJA.md'],
    ['Gyvas gynimas, nematytas testas, mažas pakeitimas','10','Instrukcija 8 skyriuje; veiksmai atliekami tik gynimo metu'],
],[226,42,237])
p('Balai paimti iš originalios užduoties, o trečioje skiltyje pateiktos įrodymų vietos. Lentelė nėra pažymio garantija: gyvo gynimo dalį vertins dėstytojas po realaus bandymo.', 'SmallLT')
h1('10. Naujesnė literatūra ir metodų svarstymas')
p('Pradinis klasikinis SVM, MLP ir RBF pasirinkimas buvo pagrįstas bendrais algoritmų šaltiniais. Peržiūrėti du 2024 m. tyrimai, kuriuose taip pat naudotas Vehicle Silhouettes rinkinys. Jų rezultatai nelyginami skaičius prieš skaičių su šiuo darbu: skiriasi skaidymai, duomenų pateikimas ir vertinimo sąlygos.')
table(['2024 m. tyrimas', 'Kodėl svarbus šiam uždaviniui', 'Sprendimas šiame darbe'], [
    ['Yang ir kt.; DOI 10.32604/cmes.2024.048049',
     'Nagrinėja daugiatikslę požymių atranką; tarp bandymų yra Vehicle Silhouettes. Klaidingų Opel ir Saab prognozių gausa motyvuoja patikrinti, ar mažesnis informatyvių požymių rinkinys padėtų.',
     'Įgyvendinta paprastesnė k požymių atranka mokymo grandinėje ir derinta vidinėje patikroje. Tai straipsnio idėjos adaptacija, o ne jo banginių optimizatoriaus reprodukcija.'],
    ['Przybyła-Kasperek ir Marfo; DOI 10.1371/journal.pone.0311041',
     'Modifikuotas MLP su vietiniais modeliais taip pat bandytas su Vehicle Silhouettes. Vertinga alternatyva, kai požymiai paskirstyti tarp skirtingų šaltinių.',
     'Tiesiogiai netaikyta, nes čia turime vieną pilną 18 požymių lentelę. Dirbtinis jos skaidymas nepadidintų turimų fizinių objektų įvairovės.'],
], [113, 190, 202])
p('Tiksli praktinė problema: klasifikuoti keturis konkrečius iš modelinių transporto priemonių siluetų išvestų požymių rinkinius. Tai gali patikrinti požymių klasifikavimo grandinę, bet neįrodo veikimo naujų markių automobiliams ar iš kamerų gautiems vaizdams. Opel ir Saab supainiojimas svarbus todėl, kad užduotis reikalauja keturių atskirų klasių.')

h1('11. Tobulinimo bandymai ir mokymo kokybė')
focused=json.loads((PROJECT/'results/improvement_20260928/summary.json').read_text(encoding='utf-8'))
wide=json.loads((PROJECT/'results/wide_svm_20260928/summary.json').read_text(encoding='utf-8'))
params=json.loads((PROJECT/'results/training_audit_20260928/parameter_summary.json').read_text(encoding='utf-8'))
mlp=json.loads((PROJECT/'results/training_audit_20260928/mlp_summary.json').read_text(encoding='utf-8'))
p('Pirmiausia tikrintas iš mokymo dalies Opel ir Saab įrašų mokomas porinis specialistas. Jo požymių skaičius, C ir gamma parinkti penkių dalių vidinėje patikroje. Kai pradinis SVM prognozavo vieną iš automobilių, specialistas patikslindavo klasę. Šio varianto išorinis Macro-F1 sumažėjo nuo '
  f"{focused['original']['macro_f1_fold_mean']:.3f} iki {focused['improved']['macro_f1_fold_mean']:.3f}; "
  f"Opel ir Saab jungtinių prognozių F1 vidurkis sumažėjo nuo {focused['original']['opel_saab_f1_mean']:.3f} iki {focused['improved']['opel_saab_f1_mean']:.3f}. Šis variantas atmestas.")
p('Senų 50 vidinių paieškų auditas parodė, kad SVM C=100 - ankstesnio tinklelio viršutinė riba - laimėjo 48 kartus; gamma=0,01 laimėjo 37 kartus, scale - 13 kartų. RBF tinklui 32 centrai ir plotis 1 laimėjo 50 kartų, vadinasi jo paieškos ribos taip pat ribojo išvadas. MLP mokymosi žingsnis 0,01 laimėjo 50 kartų. Šie dažniai aprašo modelio parinkimą, ne nepriklausomą statistinį įrodymą.')
p('Todėl antru tiriamuoju bandymu platesniame SVM tinklelyje parenkami C iš {10; 100; 1000}, gamma iš {0,003; 0,01; 0,03; scale} ir 12 arba 18 požymių. Požymių atranka, medianos ir standartizavimas išmokstami iš kiekvienos vidinės mokymo dalies. Visi 50 išorinių testų sutampa su pradiniu bandymu.')
new_winners=pd.read_json(PROJECT/'results/wide_svm_20260928/inner_winners.json')
assert (new_winners['select__k']==18).all()
p('Požymių atranka visais 50 kartų pasirinko 18 iš 18 požymių: mažesnis rinkinys nepadėjo. Platesniame tinklelyje C=1000 laimėjo 33 kartus, C=100 - 17 kartų. Taigi pagerėjimas siejamas su platesne SVM parametrų paieška, o ne su požymių mažinimu. C vėl dažnai pasirinko viršutinę ribą; tai lieka derinimo ribojimas.')
table(['Variantas', 'Išorinis Macro-F1', 'Opel F1', 'Saab F1'], [
    ['Pradinis SVM', f"{wide['original']['macro_f1_fold_mean']:.3f}", f"{wide['original']['class_metrics']['opel']['f1']:.3f}", f"{wide['original']['class_metrics']['saab']['f1']:.3f}"],
    ['Platesnis SVM su atranka', f"{wide['wide_svm']['macro_f1_fold_mean']:.3f}", f"{wide['wide_svm']['class_metrics']['opel']['f1']:.3f}", f"{wide['wide_svm']['class_metrics']['saab']['f1']:.3f}"],
], [206, 105, 95, 99])
p(f"Porinis Macro-F1 pokytis: {wide['paired_difference']:+.3f}; didesnis rezultatas {wide['better_folds']} iš 50 skaidinių, mažesnis {wide['worse_folds']}. Apytikslis pataisytas 95 % skirtumo intervalas [{wide['corrected_95pct_interval'][0]:+.3f}; {wide['corrected_95pct_interval'][1]:+.3f}] apima nulį. Šis bandymas pasirinktas žinant ankstesnio testo rezultatus, todėl intervalas čia tik aprašomasis, ne nepriklausomas naujas patvirtinimas.")
p(f"Pirminio MLP parametrų audite alpha=0,01 laimėjo 34/50, (32,16) paslėptų vienetų konfigūracija 30/50, mokymosi žingsnis 0,01 - 50/50. Pakartotinai išmokius 50 pasirinktų MLP konfigūracijų, medianinis epochų skaičius buvo {mlp['iterations_median']:.1f} (intervalas {mlp['iterations_min']}-{mlp['iterations_max']}); pradinė ir galutinė mokymo nuostolių reikšmės krito {mlp['loss_decreased_count']}/50 atvejų, konvergencijos perspėjimų {mlp['convergence_warning_count']}. Tai neįrodo, kad mokymas optimalus; ankstyvas stabdymas ir ribotas tinklelis lieka galimi kokybės ribojimai.")
p('Išorinės metrikos apskaičiuotos iš išsaugotų prognozių, o visi trys tiriamieji variantai turi atskirus rezultatų failus. Pradinis results/main/ neperrašytas. Naujiems duomenims galiojantį veikimą reikia tikrinti su nepriklausomai surinktais ir paženklintais siluetais; sintetinių ženklintų pavyzdžių iš tų pačių 846 įrašų šiame darbe nepridėta.')
h2('Šaltiniai')
p('Užduotis: PEPfm-26_Kirilas_Sersniovas.docx. Atnaujintas planas: Kirilas_Sersniovas_Kolokviumo_planas_atnaujintas_2026-09-28.docx. Duomenys: OpenML Vehicle ID 54, https://www.openml.org/d/54. Pirminiai tyrimai: https://doi.org/10.32604/cmes.2024.048049 ir https://doi.org/10.1371/journal.pone.0311041. Klasikiniai modeliai: Cortes ir Vapnik (1995), DOI 10.1007/BF00994018; Rumelhart ir kt. (1986), DOI 10.1038/323533a0; Moody ir Darken (1989), DOI 10.1162/neco.1989.1.2.281.')
story.append(PageBreak())

h1('A priedas. Originali individuali egzamino užduotis')
p('Žemiau perkeltas visas lietuviškas užduoties tekstas iš pateikto PEPfm-26_Kirilas_Sersniovas.docx. Angliškas to paties dokumento vertimas nekartojamas. Pašalintos tik dokumento formatavimo žymos.', 'SmallLT')
source=(ROOT/'report_assets'/'PEPfm-26_Kirilas_Sersniovas.docx.txt').read_text(encoding='utf-8').splitlines()
for line in source[1:]:
    if line.startswith('[Normal] Intelligent Systems'):
        break
    if line in ('[TABLE]','[/TABLE]'):
        continue
    if line.startswith('[Heading 1] '):
        h1(line.split('] ',1)[1])
    elif line.startswith('[Heading 2] '):
        h2(line.split('] ',1)[1])
    elif line.startswith('[List Bullet] '):
        bullet(line.split('] ',1)[1])
    elif line.startswith('[Normal] '):
        p(line.split('] ',1)[1])
    elif ' | ' in line:
        a,b=line.split(' | ',1)
        p(f'{a}: {b}', 'SmallLT')

def on_page(canvas, doc):
    canvas.saveState()
    w,h=A4
    canvas.setStrokeColor(colors.HexColor('#d1dce6'))
    canvas.line(44,h-35,w-44,h-35)
    canvas.setFont('DejaVu',7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(44,h-27,'Kirilas Šeršniovas | Transporto priemonių siluetų klasifikavimas')
    canvas.drawRightString(w-44,26,f'{doc.page}')
    canvas.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=44,leftMargin=44,
                      topMargin=48,bottomMargin=45,title='Transporto priemonių siluetų klasifikavimas - egzamino ataskaita',
                      author='Kirilas Šeršniovas')
doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
print(OUT)
