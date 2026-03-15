import numpy as np
from scipy.stats import poisson

def ai_predictor_full_custom():
    print("="*50)
    print("   AI PREDICTOR v10.0 - INTEGRALE TOTALE")
    print("="*50)
    
    try:
        # --- 1. QUOTE ESITO FINALE (Per la Favorita) ---
        print("[ MERCATO 1X2 ]")
        q1 = float(input("Quota 1: "))
        q2 = float(input("Quota 2: "))
        
        # --- 2. QUOTE GOAL/NO GOAL (Per l'Incastro) ---
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

        # --- LOGICA DI CALCOLO ---
        
        # Probabilità Reali dai Mercati Squadra
        p_c_o05 = 1 / c_o05_q
        p_c_o15 = 1 / c_o15_q
        p_o_o05 = 1 / o_o05_q
        p_o_o15 = 1 / o_o15_q
        
        # Calcolo Lambda basato sui logaritmi (Probabilità 0 gol)
        l_casa = -np.log(1 - p_c_o05)
        l_ospite = -np.log(1 - p_o_o05)
        
        # Raffinamento con l'incrocio 1X2 e Goal/No Goal
        p_gg_real = (1/qgg) / ((1/qgg) + (1/qng))
        p_1_real = (1/q1) / ((1/q1) + (1/q2))
        
        # Il software bilancia le forze
        l_casa = (l_casa + (p_1_real * 2)) / 2
        l_ospite = (l_ospite + ((1-p_1_real) * 1.5)) / 2

        # --- OUTPUT RISULTATI ---
        print("\n" + "*"*15 + " REPORT COMPLETO " + "*"*15)
        
        # Multigol Casa 1-3
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        # Multigol Ospite 2-4
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        # Combo Goal + Over 2.5 (usando il dato Goal/No Goal che hai inserito)
        p_ov25_match = (1 - sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(3) for o in range(3) if c+o < 2.5))
        p_gg_ov25 = (p_gg_real * p_ov25_match) * 100

        print(f"Dati Attacco: Casa {l_casa:.2f} | Ospite {l_ospite:.2f}")
        print("-" * 45)
        print(f"MULTIGOL CASA 1-3:    {p_c13:.1f}%")
        print(f"MULTIGOL OSPITE 2-4:  {p_o24:.1f}%")
        print("-" * 45)
        print(f"GOAL + OVER 2.5:      {p_gg_ov25:.1f}%")
        
        # Risultato esatto più probabile
        res = []
        for c in range(4):
            for o in range(4):
                res.append((f"{c}-{o}", poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite)))
        res.sort(key=lambda x: x[1], reverse=True)
        print(f"RISULTATO TOP:        {res[0][0]} ({res[0][1]*100:.1f}%)")
        print("="*50)

    except Exception as e:
        print(f"Errore: Assicurati di inserire i numeri correttamente! ({e})")

if __name__ == "__main__":
    ai_predictor_full_custom()
