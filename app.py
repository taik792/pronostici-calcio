import numpy as np
from scipy.stats import poisson

def calcolo_completo_v2():
    print("="*45)
    print("   BET ANALYZER PRO: MULTIGOL & HANDICAP")
    print("="*45)
    
    try:
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal: "))
        ng = float(input("Quota No Goal: "))

        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))
        media_totale = 1.7 + (p_over * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # --- CALCOLO ESITI 1X2 ---
        p_1, p_x, p_2 = 0, 0, 0
        p_h_casa_15 = 0 # Handicap -1.5 Casa (Vince con 2+ gol)
        
        for c in range(8):
            for o in range(8):
                prob = poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                if c > o: p_1 += prob
                elif c == o: p_x += prob
                else: p_2 += prob
                
                # Calcolo Handicap -1.5 Casa
                if (c - o) >= 2:
                    p_h_casa_15 += prob

        # --- OUTPUT RISULTATI ---
        print("\n" + "*"*15 + " PRONOSTICI " + "*"*15)
        print(f"Probabilità 1X2:  1: {p_1*100:.1f}% | X: {p_x*100:.1f}% | 2: {p_2*100:.1f}%")
        print("-" * 45)
        
        # Multigol (I tuoi preferiti)
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        print(f"MG CASA 1-3: {p_c13:.1f}%  |  MG OSPITE 2-4: {p_o24:.1f}%")
        
        print("-" * 45)
        # Handicap
        print(f"HANDICAP -1.5 CASA: {p_h_casa_15*100:.1f}%")
        print(f"  (La Casa vince con almeno 2 gol di scarto)")
        print(f"HANDICAP +1.5 OSPITE: {(1 - p_h_casa_15)*100:.1f}%")
        print(f"  (L'ospite non perde con più di 1 gol di scarto)")
        print("*"*45)

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    calcolo_completo_v2()
