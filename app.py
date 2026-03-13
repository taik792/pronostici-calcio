import numpy as np
from scipy.stats import poisson

def calcolo_multigol_stabile():
    print("="*45)
    print("   AI PREDICTOR v1.0 - MULTIGOL & VALORE")
    print("="*45)
    
    try:
        # INPUT QUOTE
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal (GG): "))
        ng = float(input("Quota No Goal (NG): "))
        
        # CALCOLO PROBABILITÀ REALE (Senza margine del bookmaker)
        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))

        # STIMA MEDIA GOL (Lambda)
        media_totale = 1.7 + (p_over * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # CALCOLO PROBABILITÀ CON POISSON
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        p_t24 = sum(poisson.pmf(k, media_totale) for k in range(2, 5)) * 100

        # RISULTATI ESATTI PIÙ PROBABILI
        risultati = []
        for c in range(4):
            for o in range(4):
                prob = (poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)) * 100
                risultati.append((f"{c}-{o}", prob))
        risultati.sort(key=lambda x: x[1], reverse=True)

        # OUTPUT FINALE
        print("\n" + "*"*15 + " REPORT MATCH " + "*"*15)
        print(f"Media Gol Prevista: {media_totale:.2f}")
        print("-" * 45)
        print(f"MULTIGOL CASA 1-3:      {p_c13:.1f}%")
        print(f"MULTIGOL OSPITE 2-4:    {p_o24:.1f}%")
        print(f"MULTIGOL TOTALE 2-4:    {p_t24:.1f}%")
        print("-" * 45)
        print(f"TOP 3 RISULTATI ESATTI:")
        for i in range(3):
            print(f"  {i+1}. {risultati[i][0]} ({risultati[i][1]:.1f}%)")
        print("*"*45)
        
        # QUOTA EQUA
        q_equa = 100 / p_t24
        print(f"\nQuota Minima Consigliata (MG 2-4): {q_equa:.2f}")
        print("Scommetti solo se la quota reale è più alta!")

    except ValueError:
        print("\nERRORE: Inserisci solo numeri e usa il PUNTO per i decimali!")

if __name__ == "__main__":
    calcolo_multigol_stabile()
