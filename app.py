import numpy as np
from scipy.stats import poisson

def calcolo_combo_pro():
    print("="*45)
    print("   AI PREDICTOR v3.0 - COMBO EDITION")
    print("="*45)
    
    try:
        u25_q = float(input("Quota Under 2.5: "))
        o25_q = float(input("Quota Over 2.5: "))
        gg_q = float(input("Quota Goal: "))
        ng_q = float(input("Quota No Goal: "))

        # Calcolo probabilità reali
        p_over25 = (1/o25_q) / ((1/o25_q) + (1/u25_q))
        p_gg = (1/gg_q) / ((1/gg_q) + (1/ng_q))
        media_totale = 1.7 + (p_over25 * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # Inizializziamo i contenitori per le Combo
        prob_1_ov25 = 0
        prob_1x_mg24 = 0
        prob_x2_mg13casa = 0
        
        # Ciclo su tutti i risultati possibili (fino a 6 gol per squadra)
        for c in range(7):
            for o in range(7):
                p_risultato = poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                tot_gol = c + o
                
                # 1. COMBO: 1 + Over 2.5
                if c > o and tot_gol > 2.5:
                    prob_1_ov25 += p_risultato
                
                # 2. COMBO: 1X + Multigol 2-4 Totale
                if c >= o and 2 <= tot_gol <= 4:
                    prob_1x_mg24 += p_risultato

                # 3. COMBO: X2 + Multigol 1-3 Casa (Molto usata per coprirsi)
                if o >= c and 1 <= c <= 3:
                    prob_x2_mg13casa += p_risultato

        print("\n" + "*"*15 + " COMBO SUGGERITE " + "*"*15)
        print(f"1 + OVER 2.5:         {prob_1_ov25*100:.1f}%")
        print(f"1X + MULTIGOL 2-4:    {prob_1x_mg24*100:.1f}%")
        print(f"X2 + MG CASA 1-3:     {prob_x2_mg13casa*100:.1f}%")
        print("-" * 45)
        
        # Il tuo Multigol Casa 1-3 classico (per confronto)
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        print(f"PROBABILITÀ MG CASA 1-3: {p_c13:.1f}%")
        print("*"*45)

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    calcolo_combo_pro()
