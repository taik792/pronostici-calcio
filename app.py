import numpy as np
from scipy.stats import poisson

def calcolo_multigol():
    print("="*40)
    print("   AI PREDICTOR: MULTIGOL CASA & OSPITE")
    print("="*40)
    
    try:
        # Input delle quote
        u25 = float(input("Inserisci Quota Under 2.5: "))
        o25 = float(input("Inserisci Quota Over 2.5: "))
        gg = float(input("Inserisci Quota Goal: "))
        ng = float(input("Inserisci Quota No Goal: "))

        # Calcolo probabilità reale (senza il margine del bookmaker)
        prob_over = (1/o25) / ((1/o25) + (1/u25))
        prob_gg = (1/gg) / ((1/gg) + (1/ng))

        # Stima della forza d'attacco (Lambda) basata sulle quote
        media_gol_totale = 1.6 + (prob_over * 1.8)
        
        # Distribuzione gol tra Casa e Ospite
        if prob_gg > 0.52: 
            l_casa = media_gol_totale * 0.54
            l_ospite = media_gol_totale * 0.46
        else:
            l_casa = media_gol_totale * 0.62
            l_ospite = media_gol_totale * 0.38

        # Calcolo Multigol richiesti con la formula di Poisson
        # Casa 1-3 gol
        prob_c_13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        # Ospite 2-4 gol
        prob_o_24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100

        print("\n" + "*"*15 + " RISULTATI " + "*"*15)
        print(f"Stima Gol Casa: {l_casa:.2f}")
        print(f"Stima Gol Ospite: {l_ospite:.2f}")
        print("-" * 41)
        print(f"PROBABILITÀ MULTIGOL CASA 1-3:  {prob_c_13:.1f}%")
        print(f"PROBABILITÀ MULTIGOL OSPITE 2-4: {prob_o_24:.1f}%")
        print("*"*41)
        
    except ValueError:
        print("Errore: Usa il punto per i decimali (es. 1.85) e inserisci solo numeri.")

if __name__ == "__main__":
    calcolo_multigol()
