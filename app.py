import numpy as np
from scipy.stats import poisson

def calcolo_professionale():
    print("="*45)
    print("   BET ANALYZER PRO: MULTIGOL & VALUE BET")
    print("="*45)
    
    try:
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal: "))
        ng = float(input("Quota No Goal: "))

        # Calcolo probabilità reale (ripulita dall'aggio)
        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))

        # Stima media gol (Lambda)
        media_totale = 1.7 + (p_over * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # --- CALCOLO PROBABILITÀ ---
        # Multigol Casa 1-3
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        # Multigol Ospite 2-4
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        # Multigol Totale 2-4
        p_t24 = sum(poisson.pmf(k, media_totale) for k in range(2, 5)) * 100

        # --- CALCOLO QUOTA EQUA (Fair Quota) ---
        q_equa_c13 = 100 / p_c13 if p_c13 > 0 else 0
        q_equa_t24 = 100 / p_t24 if p_t24 > 0 else 0

        print("\n" + "*"*13 + " REPORT STATISTICO " + "*"*13)
        print(f"Media Gol Match: {media_totale:.2f} (Casa: {l_casa:.2f} | Osp: {l_ospite:.2f})")
        print("-" * 45)
        
        print(f"MULTIGOL CASA 1-3")
        print(f"  > Probabilità: {p_c13:.1f}%")
        print(f"  > Quota Minima per valore: {q_equa_c13:.22f}"[:32]) # Tagliamo per pulizia
        
        print(f"\nMULTIGOL OSPITE 2-4")
        print(f"  > Probabilità: {p_o24:.1f}%")
        
        print(f"\nMULTIGOL TOTALE 2-4")
        print(f"  > Probabilità: {p_t24:.1f}%")
        print(f"  > Quota Minima per valore: {q_equa_t24:.22f}"[:32])
        print("*"*45)
        
        print("\nCONSIGLIO: Scommetti solo se la quota del bookmaker")
        print("è SUPERIORE alla Quota Minima indicata.")
        
    except ValueError:
        print("Errore: Inserisci le quote usando il punto (es: 1.85)")

if __name__ == "__main__":
    calcolo_professionale()
