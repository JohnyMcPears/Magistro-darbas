# Magistro-darbas
J.Launikonio Magistrinio darbo programos. Kodas parašytas Python kalba, 3.9 versija. Programoms sukurti buvo naudojamas Python kurimo aplinka Pycharm.
Magistrinio darbo tema: Daugiakalbių garso įrašų segmentacija pagal kalbos tipą.

Visos programos kreipiasi į tekstinius arba kitokio tipo failus, dėl to svarbu nurodyti kiekvienoje programoje šių failų kelią.

##  Programos:
### Segmentavimo Algoritmas:
1. Feature_extraction - tai dvi programos, kurios apskaičiuoja garso įrašo požymius, dvejais skirtingais būdais. Spectogram - apskaičiuoja ir išveda spektrogramos arba mel-spektrogramos tenzorius. Wav2vec apskaičiuoja ir išveda matrica su įrašo požymiais. Abi programos išveda .npy tipo failus. Šiom programoms reikia nurodyti garso įrašo kelią.
2. VAD - tai balso veiklos detektorius. šiai programai reikia nurodyti garso įrašo kelią. Porgrama išveda tektisnius failus su balso veiklos segmentais.
3. Clustering - tai programa, kuri suklasifikuoja rastus balso veiklos segmentus pasitelkus išvestais įrašo požymiais ir k-vidurkių metodu. Programai reikia pateikti garso įrašo surastus balso veiklos segmentus ir apskaičiuotus požymius. Išveda tekstinius failus su balso veiklos segmentais, kurie suklasifikuoti pagal kalbos tipą. Tai galutinis segmentavimo rezultatas.
### Orakulo tyrimas:
Oracle_clustering - tai programa skirta suklasifikuoti balso veiklos segmentus pagal atskaitos duomenis. Programai reikia pateikti tekstinį failą su balso veiklos segmentais, bei atskaitos duomenis. Išveda  tekstinius failus su balso veiklos segmentais, kurie suklasifikuoti pagalatskaitos duomenis. Programa buvo naudojama ištirti balso veiklos detektoriaus efektyvumą.
### Suskaidymo algoritmas:
WAV-creator - tai programa, kuri suskaido originalų įrašą pagal išvestus segmentavimo rezultatus ir išveda naujus garso takelius, kuriuose vartojama tik po viena kalbą. Jei įraše kalbama lietuviškai ir angliškai, tai programa išves du naujus įrašus: viename išsaugoti lietuviškos dalys, kitame angliškos originalaus įrašo dalys.
### Segmentavimo tikslumo įvertinimas:
DER - tai programa, kuri įvertina atliktų segmentavimo algoritmo tikslumą, pasitelkus diarizacijos klaidų dažnį. Programai pateikiami atskaitos duomenis ir segmentavimo algoritmo rezultatai. Išveda tekstinį failą su įvertinimais.

Atskaitos duomenis buvo sukurti su praat programa, dėl to šie duomenys buvo textgrid (trumpuoju) formatu. Taigi siūloma atsaitos duomenis turėti textgrid trumpuoju formatu. 
