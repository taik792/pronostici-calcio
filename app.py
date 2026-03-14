import numpy as np
from scipy.stats import poisson

def ai_predictor_v7_equalizer():
    print("="*45)
    print("   AI PREDICTOR v7.0 - THE EQUALIZER")
    print("="*45)
    
    try:
        q1 = float(input("Quota Segno 1: "))
        q2 = float(input("Quota Segno 2: "))
        u25_q = float(input("Quota Under 2.5: "))
        o25_q = float(input("Quota Over 2.5: "))
        gg_q = float(input("Quota Goal: "))
        ng_q = float(input("Quota No Goal: "))

        # 1. PROBABILITÀ REALI
        p_over25 = (1/o25_q) / ((1/o25_q) + (1/u25_q))
        p_gg = (1/gg_q) / ((1/gg_q) + (1/ng_q))
        
        # 2. CALCOLO MEDIA GOL TOTALE
        media_totale = 1.6 + (p_over25 * 1.7) # Leggermente più reattivo all'Over

        # 3. DISTRIBUZIONE GOL BILANCIATA (Equalizer)
        # Integriamo la forza 1x2 con la probabilità del Goal (GG)
        forza_1x2_casa = (1/q1) / ((1/q1) + (1/q2))
        
        # Se il GG è probabile, la distribuzione gol tende al 50/50
        # Se il GG è improbabile, la distribuzione segue l'1x2
        bilanciamento = 0.5 + (forza_1x2_casa - 0.5) * (1 - p_gg)
        
        l_casa = media_totale * bilanciamento
        l_ospite = media_totale - l_casa

        # 4. CALCOLO ESITI
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

        print("\n" + "*"*12 + " FORZA CORRETTA " + "*"*12)
        print(f"Gol attesi Casa: {l_casa:.2f} | Ospite: {l_ospite:.2f}")
        
        print("\n" + "-"*15 + " MULTIGOL " + "-"*15)
        print(f"MG CASA 1-3:   {sum(poisson.pmf(k, l_casa) for k in range(1, 4))*100:.1f}%")
        print(f"MG OSPITE 2-4: {sum(poisson.pmf(k, l_ospite) for k in range(2, 5))*100:.1f}%")
        
        print("\n" + "-"*15 + " COMBO & HANDICAP " + "-"*15)
        print(f"GOAL + OVER 2.5:   {prob_gg_ov25*100:.1f}%")
        print(f"1X + MULTIGOL 2-4: {prob_1x_mg24*100:.1f}%")
        print(f"HANDICAP -1.5 (1): {p_h_casa_15*100:.1f}%")
        
        print("\n" + "-"*15 + " TOP RISULTATI " + "-"*15)
        for i in range(3):
            print(f"  {i+1}. {risultati[i][0]} ({risultati[i][1]*100:.1f}%)")

    except ValueError:
        print("Errore nei dati!")

if __name__ == "__main__":
    ai_predictor_v7_equalizer()
