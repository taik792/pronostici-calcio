import numpy as np
from scipy.stats import poisson

def calcolo_avanzato():
    print("="*45)
    print("   PREDICTOR PRO: MULTIGOL CASA/OSPITE/TOTAL")
    print("="*45)
    
    try:
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal: "))
        ng = float(input("Quota No Goal: "))

        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))

        # Stima media gol
        media_totale = 1.7 + (p_over * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # CALCOLO PROBABILITÀ (Poisson)
        # 1. I tuoi Multigol Squadra
        p_c_13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o_24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        
        # 2. Nuovi Multigol Totali (Somma dei gol)
        # Calcoliamo la probabilità sulla media totale
        p_multi_24 = sum(poisson.pmf(k, media_totale) for k in range(2, 5)) * 100
        p_multi_25 = sum(poisson.pmf(k, media_totale) for k in range(2, 6)) * 100

        print("\n" + "*"*15 + " RISULTATI " + "*"*15)
        print(f"Stima Gol Casa: {l_casa:.2f} | Ospite: {l_ospite:.2f}")
        print(f"Media Gol Totale Match: {media_totale:.2f}")
        print("-" * 41)
        print(f"MULTIGOL CASA 1-3:      {p_c_13:.1f}%")
        print(f"MULTIGOL OSPITE 2-4:    {p_o_24:.1f}%")
        print("-" * 41)
        print(f"MULTIGOL TOTALE 2-4:    {p_multi_24:.1f}%")
        print(f"MULTIGOL TOTALE 2-5:    {p_multi_25:.1f}%")
        print("*"*41)
        
    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    calcolo_avanzato()
