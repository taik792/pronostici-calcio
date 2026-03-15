import numpy as np
from scipy.stats import poisson

def ai_predictor_precision_v8():
    print("="*45)
    print("   AI PREDICTOR v8.0 - PRECISION TEAM STATS")
    print("="*45)
    
    try:
        # INPUT QUOTE
        q1 = float(input("Quota 1: "))
        q2 = float(input("Quota 2: "))
        u25_q = float(input("Quota Under 2.5: "))
        o25_q = float(input("Quota Over 2.5: "))
        gg_q = float(input("Quota Goal: "))
        ng_q = float(input("Quota No Goal: "))

        # 1. BILANCIAMENTO FORZE
        p_vinc_1 = 1/q1
        p_vinc_2 = 1/q2
        w_casa = p_vinc_1 / (p_vinc_1 + p_vinc_2)
        w_ospite = p_vinc_2 / (p_vinc_1 + p_vinc_2)

        p_over25_real = (1/o25_q) / ((1/o25_q) + (1/u25_q))
        media_totale = 1.7 + (p_over25_real * 1.6)
        
        l_casa = media_totale * w_casa
        l_ospite = media_totale * w_ospite

        # 2. CALCOLO UNDER/OVER PER SQUADRA (PRECISION)
        # Probabilità Casa
        c_o05 = (1 - poisson.pmf(0, l_casa)) * 100
        c_o15 = (1 - (poisson.pmf(0, l_casa) + poisson.pmf(1, l_casa))) * 100
        c_u35 = (sum(poisson.pmf(k, l_casa) for k in range(4))) * 100

        # Probabilità Ospite
        o_o05 = (1 - poisson.pmf(0, l_ospite)) * 100
        o_o15 = (1 - (poisson.pmf(0, l_ospite) + poisson.pmf(1, l_ospite))) * 100
        o_u35 = (sum(poisson.pmf(k, l_ospite) for k in range(4))) * 100

        # 3. CALCOLO MULTIGOL (BASATO SUI CALCOLI SOPRA)
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        
        # 4. COMBO E HANDICAP
        p_h_casa_15 = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if (c-o) >= 2) * 100

        # --- OUTPUT ---
        print("\n" + "*"*10 + " ANALISI SQUADRE (U/O) " + "*"*10)
        print(f"CASA:   O0.5: {c_o05:.1f}% | O1.5: {c_o15:.1f}% | U3.5: {c_u35:.1f}%")
        print(f"OSPITE: O0.5: {o_o05:.1f}% | O1.5: {o_o15:.1f}% | U3.5: {o_u35:.1f}%")
        
        print("\n" + "-"*15 + " PRONOSTICO MULTIGOL " + "-"*15)
        print(f"MG CASA 1-3:   {p_c13:.1f}%")
        print(f"MG OSPITE 2-4: {p_o24:.1f}%")
        
        print("\n" + "-"*15 + " ALTRI ESITI " + "-"*15)
        print(f"HANDICAP -1.5 (1): {p_h_casa_15:.1f}%")
        print(f"GOAL + OVER 2.5:   {((1-poisson.pmf(0,l_casa))*(1-poisson.pmf(0,l_ospite))*p_over25_real)*100:.1f}%")
        print("="*45)

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    ai_predictor_precision_v8()
