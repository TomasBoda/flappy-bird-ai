# Dokumentácia
Tomáš Boďa

## Obsah
* [ Stručné zadanie. ](#strucne-zadanie)
* [ Zvolený algoritmus ](#zvoleny-algoritmus)
  * [ Vstup algoritmu ](#vstup-algoritmu)
  * [ Výstup algoritmu ](#vystup-algoritmu)
* [ Program ](#program)
  * [ Neurálna sieť ](#neuralna-siet)
  * [ Feed Forward algoritmus a Sigmoid funkcia ](#feed-forward-sigmoid)
* [ Priebeh práce ](#priebeh-prace)
* [ Čo nebolo dokončené ](#co-nebolo-dokoncene)
* [ Záverečný povzdych ](#zaverecny-povzdych)

<a name="strucne-zadanie"></a>
## Zadanie
Cieľom programu bolo vytvoriť jednoduchú umelú inteligenciu skladajúcu sa z **Feed Forward Neural Network** a **Genetic Learning Algorithm**, ktorá sa dokáže naučiť hrať hru Flappy Bird.

## Použité technológie
Program je napísaný v programovacom jazyku **Python**. Na Game Loop a renderovanie hernej časti programu som využil knižnicu **PyGame** a vytvoril som si pomocnú triedu **Rectangle** s funkciu `intersects`, ktorá uľahčuje detekciu kolízí objektov v hre. Okrem toho program využíva iba štandardné Python balíčky.

<a name="zvoleny-algoritmus"></a>
## Hlavná funkcionalita
Hlavným zámerom bolo vytvoriť umelú inteligenciu, za pomoci ktorej sa vták učí skákať a zdolávať prekážky tak, aby po istom čase dokázal hrať hru takmer bezchybne. Na túto úlohu som sa rozhodol použiť neurálnu sieť. Na učenie neurálnych sietí je v mnohých prípadoch častou voľbou **Back Propagation Algorithm**, ktorý podľa odchýlky od požadovaného výsledku cestuje v neurálnej sieti smerom naspäť a upravuje neurálne spojenia, aby sa čoraz viac približovali k správnemu riešeniu. Flappy Bird si však vyžaduje trochu odlišný, až priam tématický prístup. Pre tento program som si preto zvolil heuristický **Genetic Algorithm** inšpirovaný Darwinovou teóriou evolúcie. Funguje na báze prirodzeného výberu, kde slabší jedinci zahynú a tí silnejší sú vybraní na vyprodukovanie novej, lepšej generácie.

**Genetic Algorithm** zoberie najzdatnejších jedincov (resp. ich neurálne siete) z predošlej generácie ako svoje vstupné dáta a pomocou **crossover** funkcie vyprodukuje nových jedincov, ktorí zdedia charakteristiky po svojich rodičoch. Na to je potrebná funkcia, ktorá si na vstupe vypýta dvoch rodičov a na základe ich neurálnych sietí vyprodukuje nového jedinca. Táto funckia sa vola **Crossover** a implementoval som ju následovne.

```python
def crossover(brain_1, brain_2) -> Bird:
    new_weights = copy.deepcopy(brain_1.weights)

    for i in range(len(brain_1.weights)):
        for j in range(len(brain_1.weights[i])):
            for k in range(len(brain_1.weights[i][j])):
                chosen_weights = random.choice([ brain_1.weights, brain_2.weights ])

                new_weights[i][j][k] = copy.deepcopy(chosen_weights[i][j][k])

    return Bird(0, "Crossover", NeuralNetwork([ 2, 6, 1 ], new_weights))
```

**Genetic Algorithm** sa dá navrhnúť rôznymi spôsobmi a má mnoho obmien, ja som si však zvolil jeho jednoduchšiu variantu, ktorá vyzerá a funguje následovne.

<a name="vstup-algoritmu"></a>
### Vstup algoritmu
10 vtákov zoradených od najzdatnejšieho po najslabšieho

<a name="vystup-algoritmu"></a>
### Výstup algoritmu
10 vtákov novej generácie, z toho
- 4 vtáky sú priame kópie 4 najzdatnejších vtákov
- 1 vták je potomok 2 najzdatnejších vtákov
- 3 vtáky sú potomkovia náhodných 2 zo 4 najzdatnejších vtákov
- 2 vtáky sú vygenerované úplne náhodne (aby sa vývoj nezacyklil)

Algoritmus som implementoval následovne.

```python
def spawn_new_generation(dead) -> list:
    brains = [ bird.brain for bird in dead ]
    next_gen = []

    # 4 nové vtáky -> kópie 4 víťazov
    for i in range(4):
        next_gen.append(Bird(0, "Copy of winner",  brains[-i]))

    # 1 nový vták -> potomok prvých dvoch víťazov
    next_gen.append(crossover(brains[-1], brains[-2]))

    # 3 nové vtáky -> potomkovia náhodných dvoch víťazov
    for i in range(3):
        winners = [ brains[-1], brains[-2], brains[-3], brains[-4] ]
        winner_1 = random.choice(winners)
        winner_2 = random.choice(winners)

        next_gen.append(crossover(winner_1, winner_2))

    # 2 nové vtáky -> náhodné, úplne nové
    next_gen.append(Bird(0, "Random"))
    next_gen.append(Bird(0, "Random"))

    # nastavenie obrázkov a y pozící pri štarte novej hry
    for i in range(10):
        next_gen[i].y = 25 + (50 * i)
        next_gen[i].set_image(bird_colors[i])

    return next_gen
```

<a name="program"></a>
## Program
Program sa neskladá zo žiadnych komplexných alebo náročnejších datových štruktúr. Všetky situácie sa dali vyriešiť pomocou **tried** alebo bežných **zoznamov**. Zložitosť programu naopak spočíva v navrhnutí a implementácií neurálnej siete a jej aplikovaní do behu hry.

<a name="neuralna-siet"></a>
### Neurálna sieť
Cieľom pri implementácí neurálnej sieťe bolo vytvoriť ju čo najviac škálovateľnú a flexibilnú, aby sa dala jej topológia jednoducho meniť v prípade potreby. Preto si inicializácia neurálnej sieťe vyžaduje parameter `layers: list`, ktorý reprezentuje počet vrstiev neurálnej siete a počet neurónov na každej vrstve. Podľa tohoto parametru zinicializuje neurálna sieť **neuróny** s počiatočnými hodnotami 0, **weights** s náhodnými počiatočnými hodnotami z intervalu [0, 1] a **biases**, ktoré v neurálnej sieti nehrajú zatiaľ žiadnu rolu, preto s počiatočnými hodnotami 0.

Čo sa týka topológie neurálnej siete, skúšal som mnoho variant, no veľa z nich nefungovalo. Najlepšie fungovala neurálna sieť s 2 input neurónmi, 6 hidden-layer neurónmi a 1 output neurónom (`layers: list = [ 2, 6, 1 ]`). Vstupom neurálnej siete je vertikálna a horizontálna vzdialenosť vtáka od diery najbližšieho potrubia a výstupom je jedno číslo z intervalu [0, 1], ktoré determinuje, či má vták skočiť alebo nie.

```python
class NeuralNetwork:
    def __init__(self, layers, weights = None):
        self.layers = layers

        self.nodes = self.init_nodes()
        self.weights = self.init_weights() if weights is None else weights
        self.biases = self.init_biases()
```

<a name="feed-forward-sigmoid"></a>
### Feed Forward algoritmus a Sigmoid funkcia
Feed Forward algoritmus je zodpovedný za postupné posúvanie vstupných dát cez neurálnu sieť až do poslednej vrstvy. Hodnota každého neurónu na nejakej vrstve sa rovná sume cez neuróny predošlej vrstvy, každý vynásobený neurónovým spojením (weight) a ku nemu pripočítaná hodnota bias. Výsledná hodnota tejto sumy sa ešte pošle do **Sigmoid** funkcie, ktorá túto hodnotu znormalizuje na číslo z intervalu [0, 1]. Takýmto spôsobom putujú dáta v neurálnej sieti z input vrstvy až do output vrstvy.

V priebehu hry v každom prekreslení (niekoľko desiatok krát za sekundu) vypočítam horizontálnu a vertikálnu vzdialenosť vtáka od diery najbližšieho potrubia, pošlem tieto dáta do neurálnej siete, spustím **Feed Forward** algoritmus, získam výsledok a podľa neho sa rozhodnem, či vták skočí, alebo nie.

```python
def sigmoid(self, value):
    if value > 700:
        value = 700

    return 1 / (1 + math.exp(value))

def feed_forward(self, input_data):
    for i in range(len(self.nodes[0])):
        self.nodes[0][i] = input_data[i]

    for i in range(len(self.weights)):
        previous_nodes = self.nodes[i]
        layer_values = []

        for j in range(len(self.weights[i])):
            value = 0

            for k in range(len(self.weights[i][j])):
                # neurón = minulý neurón * weight + bias
                value += self.weights[i][j][k] * previous_nodes[k] + self.biases[i][j]
  
            # výsledná hodnota ešte musí prejsť cez sigmoid funkciu,
            # ktorá ju znormalizuje do intervalu [0, 1]
            layer_values.append(self.sigmoid(value))

        self.nodes[i + 1] = layer_values
```

<a name="priebeh-prace"></a>
## Priebeh práce
Začiatky písania kódu boli vcelku jednoduché. Začal som programovaním samotnej hry (vtákov, potrubí, pozadia, fyziky, kolízí), aby som mohol neskôr svoju neurálnu sieť testovať priamo v hre. Problém nastal, keď som sa pustil do programovania neurálnej siete. Nikdy som nič podobné nerobil, takže som vôbec nevedel, kde začať, akým spôsobom si sieť navrhnúť a pomocou akých dátových štruktúr ju reprezentovať. Začal som čítať rôzne zdroje literatúry a pozerať mnoho videí, kde sa neurálne siete vysvetlovali, no stále sa mi moc nedarilo. Zlom nastal, keď som bol vo vlaku na ceste domov do Bratislavy a prestala fungovať Wi-Fi. Času som mal ešte veľa a jediné, čo som pri sebe mal bol počítač a knižka lineárnej algebry, tak som sa rozhodol, že sa do toho idem pustiť a že vytvorím svoju neurálnu sieť dokým prídeme do Bratislavy. A tak sa aj stalo. Dve hodiny som čítal a študoval lineárnu algebru a počas toho ma napadlo, akým spôsobom si sieť navrhnem a ako by asi mala fungovať. Z vlaku som odchádzal s náhodne vygenerovanou neurálnou sieťou, ktorá riadila skoky vtáka.

Začiatky písania kódu neurálnej siete boli ťažké. Vôbec som nevedel, kde začať, akým spôsobom si sieť navrhnúť, pomocou akých datových štruktúr ju reprezentovať. Pozeral som mnoho videí a blogových príspevkov rozoberajúcich neurálne siete, no spraviť jednu sám bolo ťažšie, ako sa zdalo. Zlom nastal vo vlaku na ceste z Prahy do Bratislavy, keď z ničoho nič prestal fungovať internet a jediné, čo mi zostalo bol Python na počítači a učebnica lineárnej algebry. Cesta bola ešte dlhá, tak som sa rozhodol, že idem skúšať. Z vlaku som nakoniec víťazne odchádzal s fungujúcou neurálnou sieťou a prvým vtákom, ktorý vedel nešikovne skákať a prekonávať prekážky.

Od tohoto malého úspechu to už išlo ľahko. Vtáky a neurálnu sieť som prepísal, hlavne zovšeobecnil, doladil som detaily a začal som písať **Genetic Algorithm**. Ten ku podivu nebol veľmi zložitý, zvládol som ho napísať sám na základe článku popisujúci základy tohoto algoritmu. V tomto bode som si myslel, že mi hra fungovala bezchybne. Avšak, narazil som na problém.

Problém nastával, keď sa prvá generácia vtákov s náhodne vygenerovanými neurálnymi sieťami nevedela prebojovať ani cez prvé (alebo druhé) potrubie. Znamenalo to, že ani jeden vták nebol dostatočne schopný na to, aby sa podľa neho mohla vytvoriť **lepšia** nová generácia. Preto sa program zacyklil a každá ďalšia generácia bola iba horšia a horšia. Dlho som rozmýšlal, ako tento problém vyriešiť nejako šikovne, no nakoniec som ho vyriešil trikom. Tento trik spočíva v tom, že v každej generáci vygenerujem okrem 8 nových potomkov a ktomu 2 úplne náhodné vtáky, ktoré v prípade, že týchto 8 potomkov bude neschopných, majú šancu prebojovať sa. Týmto spôsobom sa hra teoreticky nikdy nezacyklí.

<a name="co-nebolo-dokoncene"></a>
## Čo nebolo dokončené
S výsledkom som veľmi spokojný, všetky moje ciele boli splnené. Jediná vec, nad ktorou by som ešte strávil čas by bolo vyriešiť problém cyklenia, ktorý spomínam vyššie. Riešenie by si vyžadovalo si naštudovať **Genetic Algorithm** podrobnejšie a vyskúšať rôzne techniky, aby sa tomuto problému vyhlo. Okrem toho však všetko funguje tak, ako má.

<a name="zaverecny-povzdych"></a>
## Záverečný povzdych
Ako som spomínal vyššie, práca na tomto projekte bola veľmi obohacujúcim zážitkom. Zistil som pri nej, že ma umelá inteligencia veľmi baví a začal som rozmýšlať, že si ju zvolím ako špecializáciu v ďalších ročníkoch. Taktiež to bol veľmi príjemne strávený čas pri programovaní **reálneho** problému popri tých všetkých algoritmoch a datových štruktúrach, ktoré sa učíme a implementujeme celý rok. Prácu a všeobecne projekt teda hodnotím veľmi pozitívne.
