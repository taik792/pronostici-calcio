import numpy as np
from scipy.stats import poisson

def calcola():
    print("--- SOFTWARE PRONOSTICI MULTIGOL ---")
    try:
        # Input quote
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal (GG): "))
        ng = float(input("Quota No Goal (NG): "))

        # Calcolo probabilità (senza aggio)
        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))

        # Formula per i gol attesi
        media_gol = 1.7 + (p_over * 1.6)
        l_casa = media_gol * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_gol - l_casa

        # Calcolo Multigol con Poisson
        p_casa_13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_ospite_24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100

        print("\n" + "="*30)
        print(f"GOL ATTESI CASA: {l_casa:.2f}")
        print(f"GOL ATTESI OSPITE: {l_ospite:.2f}")
        print("-" * 30)
        print(f"PRONOSTICO MULTIGOL:")
        print(f"CASA 1-3: {p_casa_13:.1f}%")
        print(f"OSPITE 2-4: {p_ospite_24:.1f}%")
        print("="*30)
    except:
        print("ERRORE: Inserisci i numeri usando il punto (es. 1.75)")

if __name__ == "__main__":
    calcola()
