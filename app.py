import numpy as np
from scipy.stats import poisson

def calcolo_combo_ultimate():
    print("="*45)
    print("   AI PREDICTOR v3.5 - COMBO & GOAL/OVER")
    print("="*45)
    
    try:
        u25_q = float(input("Quota Under 2.5: "))
        o25_q = float(input("Quota Over 2.5: "))
        gg_q = float(input("Quota Goal: "))
        ng_q = float(input("Quota No Goal: "))

        # Calcolo probabilità reali
        p_over25 = (1/o25_q) / ((1/o25_q) + (1/u25_q))
        p_gg_real = (1/gg_q) / ((1/gg_q) + (1/ng_q))
        
        # Stima dei gol medi
        media_totale = 1.7 + (p_over25 * 1.6)
        l_casa = media_totale * (0.55 if p_gg_real > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # Inizializziamo le probabilità Combo
        prob_gg_ov25 = 0
        prob_1x_ov15 = 0
        prob_1x_mg24 = 0
        
        # Ciclo su tutti i risultati (fino a 6 gol per squadra)
        for c in range(7):
            for o in range(7):
                p_res = poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                tot_gol = c + o
                
                # 1. COMBO: Goal + Over 2.5
                if c >= 1 and o >= 1 and tot_gol > 2.5:
                    prob_gg_ov25 += p_res
                
                # 2. COMBO: 1X + Over 1.5
                if c >= o and tot_gol > 1.5:
                    prob_1x_ov15 += p_res
                
                # 3. COMBO: 1X + Multigol 2-4
                if c >= o and 2 <= tot_gol <= 4:
                    prob_1x_mg24 += p_res

        print("\n" + "*"*15 + " ANALISI COMBO " + "*"*15)
        print(f"GOAL + OVER 2.5:      {prob_gg_ov25*100:.1f}%")
        print(f"1X + OVER 1.5:        {prob_1x_ov15*100:.1f}%")
        print(f"1X + MULTIGOL 2-4:    {prob_1x_mg24*100:.1f}%")
        print("-" * 45)
        
        # Statistiche Multigol Squadra (Il tuo punto di riferimento)
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        print(f"MG CASA 1-3: {p_c13:.1f}% | MG OSPITE 2-4: {p_o24:.1f}%")
        print("*"*45)

        # Suggerimento Strategico
        if prob_gg_ov25 > 0.40:
            print("\nSUGGERIMENTO: Partita da 'festa del gol'. Valuta il Goal+Over.")
        elif prob_1x_ov15 > 0.65:
            print("\nSUGGERIMENTO: 1X+Over 1.5 molto probabile per una multipla.")

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    calcolo_combo_ultimate()
