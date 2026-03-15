import numpy as np
from scipy.stats import poisson

def ai_predictor_combo_multigol():
    print("="*55)
    print("   AI PREDICTOR v11.0 - INTEGRALE & COMBO MULTIGOL")
    print("="*55)
    
    try:
        # --- 1. QUOTE ESITO FINALE ---
        print("[ MERCATO 1X2 ]")
        q1 = float(input("Quota 1: "))
        qx = float(input("Quota X: "))
        q2 = float(input("Quota 2: "))
        
        # --- 2. QUOTE GOAL/NO GOAL ---
        print("\n[ MERCATO GOAL ]")
        qgg = float(input("Quota Goal: "))
        qng = float(input("Quota No Goal: "))

        # --- 3. QUOTE SQUADRA CASA ---
        print("\n[ GOL SQUADRA CASA ]")
        c_o05_q = float(input("Quota Over 0.5 Casa: "))
        c_o15_q = float(input("Quota Over 1.5 Casa: "))
        
        # --- 4. QUOTE SQUADRA OSPITE ---
        print("\n[ GOL SQUADRA OSPITE ]")
        o_o05_q = float(input("Quota Over 0.5 Ospite: "))
        o_o15_q = float(input("Quota Over 1.5 Ospite: "))

        # --- CALCOLO PROBABILITÀ REALI E LAMBDA ---
        p_c_o05 = 1 / c_o05_q
        p_o_o05 = 1 / o_o05_q
        
        # Lambda basati su Over 0.5 (probabilità di non segnare 0 gol)
        l_casa = -np.log(1 - p_c_o05)
        l_ospite = -np.log(1 - p_o_o05)
        
        # Raffinamento medie con 1X2 e Goal
        p_1_real = (1/q1) / ((1/q1) + (1/qx) + (1/q2))
        p_x_real = (1/qx) / ((1/q1) + (1/qx) + (1/q2))
        p_2_real = (1/q2) / ((1/q1) + (1/qx) + (1/q2))
        p_gg_real = (1/qgg) / ((1/qgg) + (1/qng))

        # --- CALCOLO COMBO MULTIGOL ---
        prob_1x_mg13_casa = 0
        prob_1x_mg24_totale = 0
        prob_x2_mg13_ospite = 0
        prob_gg_mg25_totale = 0

        for c in range(7):
            for o in range(7):
                p_res = poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)
                tot_gol = c + o
                
                # Combo 1X + Multigol Casa 1-3
                if c >= o and 1 <= c <= 3:
                    prob_1x_mg13_casa += p_res
                
                # Combo 1X + Multigol Totale 2-4
                if c >= o and 2 <= tot_gol <= 4:
                    prob_1x_mg24_totale += p_res
                
                # Combo X2 + Multigol Ospite 1-3
                if o >= c and 1 <= o <= 3:
                    prob_x2_mg13_ospite += p_res
                
                # Combo Goal + Multigol Totale 2-5
                if c >= 1 and o >= 1 and 2 <= tot_gol <= 5:
                    prob_gg_mg25_totale += p_res

        # --- OUTPUT RISULTATI ---
        print("\n" + "*"*15 + " REPORT PRONOSTICI " + "*"*15)
        
        # Multigol Singoli
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        print(f"MG CASA 1-3:      {p_c13:.1f}%")
        print(f"MG OSPITE 2-4:    {p_o24:.1f}%")
        
        print("\n" + "-"*15 + " COMBO MULTIGOL " + "-"*15)
        print(f"1X + MG CASA 1-3:   {prob_1x_mg13_casa*100:.1f}%")
        print(f"1X + MG TOT 2-4:    {prob_1x_mg24_totale*100:.1f}%")
        print(f"X2 + MG OSPITE 1-3: {prob_x2_mg13_ospite*100:.1f}%")
        print(f"GOAL + MG TOT 2-5:  {prob_gg_mg25_totale*100:.1f}%")
        
        print("\n" + "-"*15 + " ESITO FINALE " + "-"*15)
        print(f"1: {p_1_real*100:.1f}% | X: {p_x_real*100:.1f}% | 2: {p_2_real*100:.1f}%")
        print("="*55)

    except Exception as e:
        print(f"Errore: Verifica l'inserimento delle quote! ({e})")

if __name__ == "__main__":
    ai_predictor_combo_multigol()
