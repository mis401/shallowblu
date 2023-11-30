## Stanje
### Opšte stanje
- immutable matrica\[n]\[n] tipa Polja
### Polje
- stack(tipa Mica) do 8 elemenata
boja tipa enum boje
### Skor
- po jedan brojač tipa stack 
### Potez
- igrač na potezu
### Mica
- boja

Broj mica:
\(n-2)\*(n/2) ukupno, pola po timu 

## Flowchart aplikacije

interfejs bira dimenzije N i pocetnog igraca -> formiranje pocetnog stanja po parametru N -> iscrtavanje stanja -> 
start: pocetak poteza -> 
	-> AI igra potez -> generise potez
	-> korisnik selektuje startnu Micu -> provera ispravnosti selekcije i valjanosti svih mogucih poteza te Mice 
		-> korisnik selektuje dest polje 
		->  provera ispravnosti dest polja i valjanosti poteza (moze i na osnovu liste vracenih mogucih poteza ili ponovo kalkulacija)->generise se validan potez
-> dobija se potez -> modifikuje se stanje -> iscrtava se stanje -> menja se igrac na potezu -> start