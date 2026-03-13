import numpy as np
from scipy.stats import poisson

def ai_betting_total_system():
    print("="*45)
    print("   AI PREDICTOR v4.0 - SISTEMA COMPLETO")
    print("="*45)
    
    try:
        u25_q = float(input("Quota Under 2.5: "))
        o25_q = float(input("Quota Over 2.5: "))
        gg_q = float(input("Quota Goal: "))
        ng_q = float(input("Quota No Goal: "))

        # 1. CALCOLO PROBABILITÀ REALI E MEDIE GOL
        p_over25 = (1/o25_q) / ((1/o25_q) + (1/u25_q))
        p_gg_real = (1/gg_q) / ((1/gg_q) + (1/ng_q))
        media_totale = 1.7 + (p_over25 * 1.6)
        l_casa = media_totale * (0.55 if p_gg_real > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # 2. INIZIALIZZAZIONE VARIABILI
        p_1, p_x, p_2 = 0, 0, 0
        p_h_casa_15 = 0
        prob_gg_ov25 = 0
        prob_1x_mg24 = 0
        
        # 3. CICLO POISSON PER RISULTATI ESATTI E COMBO
        risultati = []
        for c in range(7):
            for o in range(7):
                p_res = poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                tot_gol = c + o
                
                # 1X2 e Handicap
                if c > o: p_1 += p_res
                elif c == o: p_x += p_res
                else: p_2 += p_res
                if (c - o) >= 2: p_h_casa_15 += p_res
                
                # Combo
                if c >= 1 and o >= 1 and tot_gol > 2.5: prob_gg_ov25 += p_res
                if c >= o and 2 <= tot_gol <= 4: prob_1x_mg24 += p_res
                
                if c < 4 and o < 4:
                    risultati.append((f"{c}-{o}", p_res))

        risultati.sort(key=lambda x: x[1], reverse=True)

        # 4. SPIEGAZIONE TATTICA
        analisi = "PARTITA BILANCIATA"
        if media_totale > 2.8: analisi = "ALTO SPETTACOLO: Attacchi dominanti, probabili molti gol."
        elif media_totale < 2.1: analisi = "DIFESE CHIUSE: Partita tattica, pochi spazi."
        if p_1 > 60: analisi += " Dominio netto della squadra di casa."

        # --- OUTPUT FINALE COMPLETO ---
        print("\n" + "*"*12 + " ANALISI TATTICA " + "*"*12)
        print(f"Sintesi: {analisi}")
        print(f"Gol Previsti: Casa {l_casa:.2f} | Ospite {l_ospite:.2f}")
        
        print("\n" + "-"*15 + " MULTIGOL " + "-"*15)
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
    ai_betting_total_system()
