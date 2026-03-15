import numpy as np
from scipy.stats import poisson

def ai_ultimate_engine_v16():
    print("="*65)
    print("   AI PREDICTOR v16.0 - SMART SELECTOR + COMBO GOLD")
    print("="*65)
    
    try:
        # --- INPUT DATI ---
        q1 = float(input("Quota 1: "))
        qx = float(input("Quota X: "))
        q2 = float(input("Quota 2: "))
        qgg = float(input("Quota Goal: "))
        qng = float(input("Quota No Goal: "))
        
        print("\n[ GOL SQUADRA CASA ]")
        c_o05_q = float(input("Quota Over 0.5 Casa: "))
        c_o15_q = float(input("Quota Over 1.5 Casa: "))
        
        print("\n[ GOL SQUADRA OSPITE ]")
        o_o05_q = float(input("Quota Over 0.5 Ospite: "))
        o_o15_q = float(input("Quota Over 1.5 Ospite: "))

        # --- CALCOLO MEDIE GOL (LAMBDA) ---
        l_casa = -np.log(max(0.01, 1 - (1/c_o05_q)))
        l_ospite = -np.log(max(0.01, 1 - (1/o_o05_q)))
        
        # Correzione pesata sulla quota Over 1.5
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        
        l_tot = l_casa + l_ospite

        # --- FUNZIONI DI SELEZIONE ---
        ranges = [(1,2,"1-2"), (1,3,"1-3"), (1,4,"1-4"), (2,3,"2-3"), (2,4,"2-4"), (2,5,"2-5")]

        def get_best_range(lam):
            res = sorted([(sum(poisson.pmf(k, lam) for k in range(mi, ma+1)), lbl) for mi, ma, lbl in ranges], reverse=True)
            return res[0] # Ritorna (probabilità, label)

        prob_c, best_c = get_best_range(l_casa)
        prob_o, best_o = get_best_range(l_ospite)
        prob_t, best_t = get_best_range(l_tot)

        # --- CALCOLO COMBO DINAMICHE ---
        # 1X + Miglior MG Casa
        mi_c, ma_c = map(int, best_c.split('-'))
        p_1x_mg_c = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(6) for o in range(6) if c>=o and mi_c<=c<=ma
