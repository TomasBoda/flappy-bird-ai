# Dokumentácia
Tomáš Boďa

## Stručné zadanie
Cieľom programu bolo vytvoriť jednoduchú umelú inteligenciu skladajúcu sa z **Feed Forward Neural Network** a **Genetic Learning Algorithm**, ktorá sa dokáže naučiť hrať hru Flappy Bird.

## Zvolený algoritmus
Každá neurálna sieť potrebuje nejaký algoritmus, za pomoci ktorého sa zlepšuje, uči, vyvíja. Častou voľbou je BackPropagation algoritmus, ktorý podľa odchýlky svojich výsledkov od požadovaného výsledku cestuje smerom naspäť v neurálnej sieti a upravuje neurónové spojenia.

Flappy Bird si však vyžaduje trochu odlišný, až priam tématický prístup. Pre tento program som si zvolil heuristický **Genetic Learning Algorithm** inšpirovaný Darwinovou teóriou evolúcie. Funguje na báze prirodzeného výberu, kde slabší jedinci zahynú a tí silnejší sú vybraní na vyprodukovanie novej, lepšej generácie.

**Genetic Learning Algorithm** zoberie najzdatnejśích jedincov ako svoje vstupné dáta a pomocou **crossover** funkcie vyprodukuje nových jedincov, ktorí zdedia charakteristiky po svojich rodičoch. Tento algoritmus sa však dá navrhnúť rôznymi spôsobmi a má mnoho obmien, ja som si zvolil jeho jednoduchšiu variantu, ktorá funguje následovne.

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
Cieľom pri implementácí neurálnej sieťe bolo vytvoriť ju čo najviac škálovateľnú a flexibilnú, aby sa dala jej topológia jednoducho meniť v prípade potreby. Preto si inicializácia neurálnej sieťe vyžaduje parameter `layers: list`, ktorý reprezentuje poćet vrstiev neurálnej siete a počet neurónov na každej vrstve. Podľa tohoto parametru zinicializuje neurálna sieť **neuróny** s počiatočnými hodnotami 0, **weights** s náhodnými počiatočnými hodnotami z intervalu [0, 1] a **biases**, ktoré v neurálnej sieti nehrajú zatiaľ žiadnu rolu, preto s počiatočnými hodnotami 0.

**Feed Forward algoritmus a Sigmoid funkcia**
Feed Forward algoritmus je zodpovedný za postupné posúvanie vstupných dát cez neurálnu sieť až do poslednej vrstvy. Hodnota každého neurónu na nejakej vrstve je suma cez neuróny predošlej vrstvy, každý vynásobený neurónovým spojením (weight) a ku nemu pripočítaná hodnota bias. Výsledná hodnota tejto sumy sa ešte pošle do **Sigmoid** funkcie, ktorá túto hodnotu znormalizuje na číslo z intervalu [0, 1].
