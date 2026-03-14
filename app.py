import numpy as np
from scipy.stats import poisson

def ai_predictor_v6_power():
    print("="*45)
    print("   AI PREDICTOR v6.0 - 1X2 WEIGHTED")
    print("="*45)
    
    try:
        # INPUT QUOTE COMPLETE
        q1 = float(input("Quota Segno 1: "))
        q2 = float(input("Quota Segno 2: "))
        u25_q = float(input("Quota Under 2.5: "))
        o25_q = float(input("Quota Over 2.5: "))
        gg_q = float(input("Quota Goal: "))
        ng_q = float(input("Quota No Goal: "))

        # 1. CALCOLO PROBABILITÀ REALI
        # Togliamo l'aggio dal mercato 1-2 per capire chi è davvero favorito
        p_vinc_1 = 1/q1
        p_vinc_2 = 1/q2
        # Rapporto di forza tra le due squadre
        weight_casa = p_vinc_1 / (p_vinc_1 + p_vinc_2)
        weight_ospite = p_vinc_2 / (p_vinc_1 + p_vinc_2)

        # Probabilità Over e Goal
        p_over25 = (1/o25_q) / ((1/o25_q) + (1/u25_q))
        
        # 2. STIMA DEI GOL ATTESI (Basata sulla forza 1X2)
        # La media gol totale del match rimane legata all'Under/Over
        media_totale = 1.7 + (p_over25 * 1.6)
        
        # Assegniamo i gol in base a chi è più forte secondo le quote 1-2
        l_casa = media_totale * weight_casa
        l_ospite = media_totale * weight_ospite

        # 3. CALCOLO ESITI
        p_h_casa_15 = 0
        prob_gg_ov25 = 0
        prob_1x_mg24 = 0
        risultati = []

        for c in range(7):
            for o in range(7):
                p_res = poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                tot_gol = c + o
                if (c - o) >= 2: p_h_casa_15 += p_res
                if c >= 1 and o >= 1 and tot_gol > 2.5: prob_gg_ov25 += p_res
                if c >= o and 2 <= tot_gol <= 4: prob_1x_mg24 += p_res
                if c < 4 and o < 4: risultati.append((f"{c}-{o}", p_res))

        risultati.sort(key=lambda x: x[1], reverse=True)

        # --- OUTPUT ---
        print("\n" + "*"*12 + " ANALISI DI FORZA " + "*"*12)
        print(f"Forza Attacco Casa: {l_casa:.2f} gol previsti")
        print(f"Forza Attacco Ospite: {l_ospite:.2f} gol previsti")
        
        print("\n" + "-"*15 + " MULTIGOL SPECIFICI " + "-"*15)
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        print(f"MG CASA 1-3:   {p_c13:.1f}%")
        print(f"MG OSPITE 2-4: {p_o24:.1f}%")
        
        print("\n" + "-"*15 + " COMBO & HANDICAP " + "-"*15)
        print(f"GOAL + OVER 2.5:   {prob_gg_ov25*100:.1f}%")
        print(f"1X + MULTIGOL 2-4: {prob_1x_mg24*100:.1f}%")
        print(f"HANDICAP -1.5 (1): {p_h_casa_15*100:.1f}%")
        
        print("\n" + "-"*15 + " RISULTATI TOP " + "-"*15)
        for i in range(3):
            print(f"  {i+1}. {risultati[i][0]} ({risultati[i][1]*100:.1f}%)")
        print("="*45)

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    ai_predictor_v6_power()
