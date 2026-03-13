import numpy as np
from scipy.stats import poisson

def calcolo_avanzato_pro():
    print("="*45)
    print("   AI BETTING TERMINAL - VERSION 3.0")
    print("="*45)
    
    try:
        # 1. INPUT DATI
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal: "))
        ng = float(input("Quota No Goal: "))
        budget = float(input("Tuo Budget Totale (€): "))

        # 2. CALCOLO PROBABILITÀ REALI
        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))

        media_totale = 1.7 + (p_over * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # 3. RISULTATI ESATTI (Top 3)
        risultati = []
        for c in range(4): # gol casa 0-3
            for o in range(4): # gol ospite 0-3
                prob = (poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)) * 100
                risultati.append((f"{c}-{o}", prob))
        
        risultati.sort(key=lambda x: x[1], reverse=True)

        # 4. MULTIGOL E STAKE (Kelly)
        p_t24 = sum(poisson.pmf(k, media_totale) for k in range(2, 5)) * 100
        q_equa_t24 = 100 / p_t24
        
        print("\n" + "*"*10 + " ANALISI MATCH " + "*"*10)
        print(f"FORZA ATTACCO: Casa {l_casa:.2f} | Ospite {l_ospite:.2f}")
        print(f"TOP 3 RISULTATI ESATTI:")
        for i in range(3):
            print(f"  {i+1}. {risultati[i][0]} (Probabilità: {risultati[i][1]:.1f}%)")
        
        print("-" * 35)
        print(f"MULTIGOL TOTALE 2-4")
        print(f"  > Probabilità: {p_t24:.1f}%")
        print(f"  > Quota Minima Consigliata: {q_equa_t24:.2f}")
        
        # Suggerimento Puntata (Stake 2% prudenziale)
        stake = budget * 0.02
        print(f"  > STAKE CONSIGLIATO: {stake:.2f}€")
        print("*"*35)

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    calcolo_avanzato_pro()
