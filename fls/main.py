import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Definisanje ulaznih promenljivih
temperatura = np.arange(0, 41, 1)
vlaznost = np.arange(0, 101, 1)
nivo_co2 = np.arange(0, 2001, 1)

# Definisanje izlazne promenljive
brzina_ventilatora = np.arange(0, 101, 1)

# Definisanje funkcija pripadnosti za temperaturu
temperatura_nisko = fuzz.trapmf(temperatura, [0, 0, 10, 20])
temperatura_srednje = fuzz.trapmf(temperatura, [15, 20, 25, 30])
temperatura_visoko = fuzz.trapmf(temperatura, [25, 30, 40, 40])

# Definisanje funkcija pripadnosti za vlažnost
vlaznost_nisko = fuzz.trapmf(vlaznost, [0, 0, 25, 50])
vlaznost_srednje = fuzz.trapmf(vlaznost, [30, 40, 60, 70])
vlaznost_visoko = fuzz.trapmf(vlaznost, [60, 75, 100, 100])

# Definisanje funkcija pripadnosti za nivo CO2
nivo_co2_nisko = fuzz.trapmf(nivo_co2, [0, 0, 500, 1000])
nivo_co2_srednje = fuzz.trapmf(nivo_co2, [800, 900, 1100, 1200])
nivo_co2_visoko = fuzz.trapmf(nivo_co2, [1000, 1500, 2000, 2000])

# Definisanje funkcija pripadnosti za brzinu ventilatora
brzina_ventilatora_nisko = fuzz.trapmf(brzina_ventilatora, [0, 0, 25, 50])
brzina_ventilatora_srednje = fuzz.trapmf(brzina_ventilatora, [30, 40, 60, 70])
brzina_ventilatora_visoko = fuzz.trapmf(brzina_ventilatora, [60, 75, 100, 100])

# Funkcija za predikciju brzine ventilatora koristeći min i max operacije
def predvidi_brzinu_ventilatora(temp, vlaz, co2):
    # Fazifikacija
    temp_nisko = fuzz.interp_membership(temperatura, temperatura_nisko, temp)
    temp_srednje = fuzz.interp_membership(temperatura, temperatura_srednje, temp)
    temp_visoko = fuzz.interp_membership(temperatura, temperatura_visoko, temp)

    vlaz_nisko = fuzz.interp_membership(vlaznost, vlaznost_nisko, vlaz)
    vlaz_srednje = fuzz.interp_membership(vlaznost, vlaznost_srednje, vlaz)
    vlaz_visoko = fuzz.interp_membership(vlaznost, vlaznost_visoko, vlaz)

    co2_nisko = fuzz.interp_membership(nivo_co2, nivo_co2_nisko, co2)
    co2_srednje = fuzz.interp_membership(nivo_co2, nivo_co2_srednje, co2)
    co2_visoko = fuzz.interp_membership(nivo_co2, nivo_co2_visoko, co2)

    # Pravila
    rule1 = np.fmax(np.fmax(temp_visoko, vlaz_visoko), co2_visoko)
    rule2 = np.fmin(np.fmin(temp_srednje, vlaz_srednje), co2_srednje)
    rule3 = np.fmin(np.fmin(temp_nisko, vlaz_nisko), co2_nisko)
    rule4 = np.fmin(np.fmin(temp_srednje, np.fmax(vlaz_nisko, vlaz_srednje)), np.fmax(co2_nisko, co2_srednje))
    rule5 = np.fmin(np.fmin(temp_nisko, vlaz_srednje), co2_nisko)
    rule6 = np.fmin(temp_visoko, vlaz_nisko)
    rule7 = np.fmin(np.fmin(temp_srednje, vlaz_visoko), co2_nisko)
    rule8 = np.fmin(np.fmin(temp_nisko, vlaz_visoko), co2_srednje)
    rule9 = np.fmin(np.fmin(temp_visoko, vlaz_srednje), co2_nisko)
    rule10 = np.fmin(np.fmin(temp_visoko, vlaz_nisko), co2_srednje)
    rule11 = np.fmin(np.fmin(temp_nisko, vlaz_visoko), co2_visoko)
    rule12 = np.fmin(np.fmin(temp_nisko, vlaz_srednje), co2_visoko)
    rule13 = np.fmin(np.fmin(temp_srednje, vlaz_nisko), co2_visoko)
    rule14 = np.fmin(np.fmin(temp_visoko, vlaz_srednje), co2_visoko)
    rule15 = np.fmin(np.fmin(temp_nisko, vlaz_nisko), co2_visoko)
    rule16 = np.fmin(np.fmin(temp_srednje, vlaz_nisko), co2_nisko)

    # Agregacija izlaza pravila
    aktivacija_nisko = np.fmax(rule3, np.fmax(rule5, rule16))
    aktivacija_srednje = np.fmax(rule2, np.fmax(rule4, np.fmax(rule6, np.fmax(rule7, np.fmax(rule8, np.fmax(rule9, np.fmax(rule10, rule12)))))))
    aktivacija_visoko = np.fmax(rule1, np.fmax(rule11, np.fmax(rule13, rule14)))

    # Kombinovanje svih aktivacija
    agregacija = np.fmax(aktivacija_nisko, np.fmax(aktivacija_srednje, aktivacija_visoko))

    # Defuzzifikacija metodom težišta (centroid)
    rezultat = fuzz.defuzz(brzina_ventilatora, agregacija, 'centroid')
    return rezultat

# Validacija ulaznih podataka
def unos_podataka():
    while True:
        try:
            temperatura_input = float(input("Unesite temperaturu (0-40): "))
            if temperatura_input < 0 or temperatura_input > 40:
                raise ValueError
            vlaznost_input = float(input("Unesite vlažnost (0-100): "))
            if vlaznost_input < 0 or vlaznost_input > 100:
                raise ValueError
            co2_input = float(input("Unesite nivo CO2 (0-2000): "))
            if co2_input < 0 or co2_input > 2000:
                raise ValueError
            return temperatura_input, vlaznost_input, co2_input
        except ValueError:
            print("Uneli ste neispravnu vrednost. Pokušajte ponovo.")

# Unos vrednosti od strane korisnika
temperatura_input, vlaznost_input, co2_input = unos_podataka()

# Predikcija brzine ventilatora
brzina_ventilatora_output = predvidi_brzinu_ventilatora(temperatura_input, vlaznost_input, co2_input)
print(f"Predviđena brzina ventilatora: {brzina_ventilatora_output:.2f}%")

# Zapisivanje rezultata u datoteku
with open('rezultati_simulacije.txt', 'w', encoding='utf-8') as f:
    f.write(f"Temperatura: {temperatura_input} °C\n")
    f.write(f"Vlažnost: {vlaznost_input} %\n")
    f.write(f"Nivo CO2: {co2_input} ppm\n")
    f.write(f"Predviđena brzina ventilatora: {brzina_ventilatora_output:.2f} %\n")

# Prikaz rezultata simulacije
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.plot(temperatura, temperatura_nisko, label='Nisko')
plt.plot(temperatura, temperatura_srednje, label='Srednje')
plt.plot(temperatura, temperatura_visoko, label='Visoko')
plt.title('Funkcija pripadnosti za Temperaturu')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Pripadnost')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(vlaznost, vlaznost_nisko, label='Nisko')
plt.plot(vlaznost, vl
