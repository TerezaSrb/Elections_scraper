## Projekt Election Scraper

### Popis projektu
Třetí projekt na Python akademii od Engeta. Cílem projektu bylo vytvořit 
skript, který z dané webové stránky vyscrapuje výsledky voleb pro daný územní 
celek a uloží je do .csv souboru.

### Instalace knihoven
Knihovny, které jsou použity k extrahování výsledků, jsou uloženy v souboru 
`requirements.txt`. Pro instalaci je doporučeno použít nové virtuální 
prostředí a s nainstalovaným manažerem spustit následovně:

    $pip3 --version
    $pip3 install -r requirements.txt

### Spuštění projektu
Projekt je určený ke spuštění v příkazovém řádku a potřebuje dva povinné 
argumenty:
1. Odkaz na webovou stránku uzemního celku, pro který chceme výsledky získat
2. Název souboru, do kterého se uloží získaná data

Příklad spuštění projektu:

    python main.py <odkaz-uzemniho-celku> <vystupni-soubor>

### Ukázka projektu

Výsledky hlasování pro okres Prostějov:
1. argument: ```https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103```
2. argument `vysledky_prostejov.csv`

Spuštění:

    python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_prostejov.csv

Průběh stahování:

    Vyčítání dat pro obec Alojzov.
    Vyčítání dat pro obec Bedihošť.
    Vyčítání dat pro obec Bílovice-Lutotín.
    Vyčítání dat pro obec Biskupice.
    Vyčítání dat pro obec Bohuslavice.
    Vyčítání dat pro obec Bousín.
    Vyčítání dat pro obec Brodek u Konice.
    ...

Výstupní .csv soubor obsahuje získaná data: jeden řádek pro jednu obec/okrsek. 
Každý řádek obsahuje kód obce, název obce, počet voličů, počet vydaných 
obálek, počet platných hlasů a počet hlasů pro jednotlivé politcké strany.
