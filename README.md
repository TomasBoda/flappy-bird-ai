# Dokumentácia
Tomáš Boďa

## Stručné zadanie
Cieľom programu bolo vytvoriť jednoduchú umelú inteligenciu skladajúcu sa z **Feed Forward Neural Network** a **Genetic Learning Algorithm**, ktorá sa dokáže naučiť hrať hru Flappy Bird.

## Zvolený algoritmus
Na učenie neurálnych sietí je v mnohých prípadoch častou voľbou **Back Propagation Algorithm**, ktorý podľa odchýlky od požadovaného výsledku cestuje v neurálnej sieti smerom naspäť a upravuje neurálne spojenia, aby sa čoraz viac približovali k správnemu riešeniu. Flappy Bird si však vyžaduje trochu odlišný, až priam tématický prístup. Pre tento program som si zvolil heuristický **Genetic Learning Algorithm** inšpirovaný Darwinovou teóriou evolúcie. Funguje na báze prirodzeného výberu, kde slabší jedinci zahynú a tí silnejší sú vybraní na vyprodukovanie novej, lepšej generácie.

**Genetic Learning Algorithm** zoberie najzdatnejśích jedincov (resp. ich neurálne siete) ako svoje vstupné dáta a pomocou **crossover** funkcie vyprodukuje nových jedincov, ktorí zdedia charakteristiky po svojich rodičoch. Tento algoritmus sa dá navrhnúť rôznymi spôsobmi a má mnoho obmien, ja som si zvolil jeho jednoduchšiu variantu, ktorá funguje následovne.

### Vstup algoritmu
10 vtákov zoradených od najzdatnejšieho po najslabšieho

### Výstup algoritmu
10 vtákov novej generácie, z toho
- 4 vtáky sú priame kópie 4 najzdatnejších vtákov
- 1 vták je potomok 2 najzdatnejších vtákov
- 3 vtáky sú potomkovia náhodných 2 zo 4 najzdatnejších vtákov
- 2 vtáky sú vygenerované úplne náhodne (aby sa vývoj nezacyklil)

## Program
Program sa neskladá zo žiadnych komplexných alebo náročnejších datových štruktúr. Všetky situácie sa dali vyriešiť pomocou **tried** alebo bežných **zoznamov**. Zložitosť programu naopak spočíva v navrhnutí a implementácií neurálnej siete a jej aplikovaní do behu hry.

### Neurálna sieť
Cieľom pri implementácí neurálnej sieťe bolo vytvoriť ju čo najviac škálovateľnú a flexibilnú, aby sa dala jej topológia jednoducho meniť v prípade potreby. Preto si inicializácia neurálnej sieťe vyžaduje parameter `layers: list`, ktorý reprezentuje počet vrstiev neurálnej siete a počet neurónov na každej vrstve. Podľa tohoto parametru zinicializuje neurálna sieť **neuróny** s počiatočnými hodnotami 0, **weights** s náhodnými počiatočnými hodnotami z intervalu [0, 1] a **biases**, ktoré v neurálnej sieti nehrajú zatiaľ žiadnu rolu, preto s počiatočnými hodnotami 0.

Čo sa týka topológie neurálnej siete, skúšal som mnoho variant, no veľa z nich nefungovalo. Najlepšie fungovala neurálna sieť s 2 input neurónmi, 6 hidden-layer neurónmi a 1 output neurónom. Vstupom neurálnej siete je vertikálna a horizontálna vzdialenosť vtáka od diery najbližšieho potrubia a výstupom je jedno číslo z intervalu [0, 1], ktoré determinuje, či má vták skočiť alebo nie.

## Feed Forward algoritmus a Sigmoid funkcia
Feed Forward algoritmus je zodpovedný za postupné posúvanie vstupných dát cez neurálnu sieť až do poslednej vrstvy. Hodnota každého neurónu na nejakej vrstve je suma cez neuróny predošlej vrstvy, každý vynásobený neurónovým spojením (weight) a ku nemu pripočítaná hodnota bias. Výsledná hodnota tejto sumy sa ešte pošle do **Sigmoid** funkcie, ktorá túto hodnotu znormalizuje na číslo z intervalu [0, 1]. Takýmto spôsobom putujú dáta v neurálnej sieti z input vrstvy až do output vrstvy.

V priebehu hry v každom prekreslení (niekoľko desiatokkrát za sekundu) vypočítam horizontálnu a vertikálnu vzdialenosť vtáka od diery najbližšieho potrubia, pošlem tieto dáta do neurálnej siete, spustím **Feed Forward** algoritmus, získam výsledok a podľa neho sa rozhodnem, či vták skočí, alebo nie.

## Priebeh práce
Práca na tomto projekte bola úprimne veľmi obohacujúca a zaujímavá. Koniec koncov som si vybral tento projekt práve preto, aby som získal aspoň nejaký rozhľad a základy umelej inteligencie, keďže som ju nikdy predtým nerobil. Začiatky písania kódu neurálnej siete boli ťažké. Vôbec som nevedel, kde začať, akým spôsobom si sieť navrhnúť, pomocou akých datových štruktúr ju reprezentovať. Pozeral som mnoho videí a blogových príspevkov rozoberajúcich neurálne siete, no spraviť jednu sám bolo ťažšie, ako sa zdalo. Zlom nastal vo vlaku na ceste z Prahy do Bratislavy, keď z ničoho nič prestal fungovať internet a jediné, čo mi zostalo bol Python na počítači a učebnica lineárnej algebry. Cesta bola ešte dlhá, tak som sa rozhodol, že idem skúšať. Z vlaku som nakoniec víťazne odchádzal s fungujúcou neurálnou sieťou a prvým vtákom, ktorý vedel nešikovne skákať a prekonávať prekážky.

Od tohoto malého úspechu to už išlo ľahko. Vtáky a neurálnu sieť som prepísal, hlavne zovšeobecnil, doladil som detaily a začal som písať **Genetic Algorithm**. Ten ku podivu nebol veľmi zložitý, zvládol som ho napísať sám na základe článku popisujúci základy tohoto algoritmu. V tomto bode som si myslel, že mi hra fungovala bezchybne. Avšak, narazil som na problém.

Problém nastával, keď sa prvá generácia vtákov s náhodne vygenerovanými neurálnymi sieťami nevedela prebojovať ani cez prvé (alebo druhé) potrubie. Znamenalo to, že ani jeden vták nebol dostatočne schopný na to, aby sa podľa neho mohla vytvoriť **lepšia** nová generácia. Preto sa program zacyklil a každá ďalšia generácia bola iba horšia a horšia. Dlho som rozmýšlal, ako tento problém vyriešiť nejako šikovne, no nakoniec som ho vyriešil trikom. Tento trik spočíva v tom, že v každej generáci vygenerujem okrem 8 nových potomkov a ktomu 2 úplne náhodné vtáky, ktoré v prípade, že týchto 8 potomkov bude neschopných, majú šancu prebojovať sa. Týmto spôsobom sa hra teoreticky nikdy nezacyklí.

## Čo nebolo dokončené
S výsledkom som veľmi spokojný, všetky moje ciele boli splnené. Jediná vec, nad ktorou by som ešte strávil čas by bolo vyriešiť problém cyklenia, ktorý spomínam vyššie. Riešenie by si vyžadovalo si naštudovať **Genetic Algorithm** podrobnejšie a vyskúšať rôzne techniky, aby sa tomuto problému vyhlo. Okrem toho však všetko funguje tak, ako má.

## Záverečný povzdych
Ako som spomínal vyššie, práca na tomto projekte bola veľmi obohacujúcim zážitkom. Zistil som pri nej, že ma umelá inteligencia veľmi baví a začal som rozmýšlať, že si ju zvolím ako špecializáciu v ďalších ročníkoch. Taktiež to bol veľmi príjemne strávený čas pri programovaní **reálneho** problému popri tých všetkých algoritmoch a datových štruktúrach, ktoré sa učíme a implementujeme celý rok. Prácu a všeobecne projekt teda hodnotím veľmi pozitívne.
