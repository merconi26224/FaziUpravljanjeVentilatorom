# Fazi upravljanje ventilatorom

Python projekat iz druge godine studija koji prikazuje primenu fazi logike za određivanje brzine ventilatora na osnovu temperature, vlažnosti vazduha i nivoa CO₂.

## Kako je zamišljen rad programa

Korisnik unosi temperaturu (0–40 °C), vlažnost (0–100%) i nivo CO₂ (0–2000 ppm). Program koristi funkcije pripadnosti i fazi pravila, a zatim računa predloženu brzinu ventilatora u procentima. Rezultat upisuje u `rezultati_simulacije.txt`.

## Tehnologije

- Python
- NumPy
- scikit-fuzzy
- Matplotlib

## Pokretanje

Instalirati potrebne biblioteke:

```bash
pip install numpy scikit-fuzzy matplotlib
```

Zatim u folderu projekta pokrenuti:

```bash
python main.py
```

Folder `.venv` nije deo repozitorijuma jer sadrži lokalno instalirane biblioteke.
