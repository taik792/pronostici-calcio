import numpy as np
from scipy.stats import poisson

def ai_full_auto_v17_1():
    print("="*65)
    print("   AI PREDICTOR v17.1 - FULL AUTO (FIXED)")
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

        # --- MOTORE DI CALCOLO POTENZA (LAMBDA) ---
        l_casa = -np.log(max(0.01, 1 - (1/c_o05_q)))
        l_ospite = -np.log(max(0.01, 1 - (1/o_o05_q)))
        
        # Correzione con quota Over 1.5
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        
        l_tot = l_casa + l_ospite

        # --- LOGICA DI SELEZIONE MULTIGOL ---
        ranges = [(1,2,"1-2"), (1,3,"1-3"), (1,4,"1-4"), (2,3,"2-3"), (2,4,"2-4"), (2,5,"2-5")]

        def get_best_range(lam):
            res = sorted([(sum(poisson.pmf(k, lam) for k in range(mi, ma+1)), lbl) for mi, ma, lbl in ranges], reverse=True)
            return res[0]

        p_c, b_c = get_best_range(l_casa)
        p_o, b_o = get_best_range(l_ospite)
        p_t, b_t = get_best_range(l_tot) # Ora best_t (b_t) è correttamente definito

        # --- DECISIONE AUTOMATICA FAVORITA ---
        if q1 <= q2:
            fav_name, dc, b_mg, p_base = "CASA", "1X", b_c, p_c
            mi, ma = map(int, b_c.split('-'))
            p_combo = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if c>=o and mi<=c<=ma) * 100
        else:
            fav_name, dc, b_mg, p_base = "OSPITE", "X2", b_o, p_o
            mi, ma = map(int, b_o.split('-'))
            p_combo = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if o>=c and mi<=o<=ma) * 100

        # --- OUTPUT RISULTATI ---
        print("\n" + "📊" * 5 + " ANALISI MOTORE " + "📊" * 5)
        print(f"Favorita: {fav_name} | Potenza: {max(l_casa, l_ospite):.2f}")
        print("-" * 50)
        print(f"Miglior MG {fav_name}: {b_mg} ({p_base*100:.1f}%)")
        print(f"Miglior MG MATCH: {b_t} ({p_t*100:.1f}%)")
        
        print("\n" + "🚀" * 5 + " PRONOSTICO COMBO " + "🚀" * 5)
        print(f"GIOCATA: {dc} + MULTIGOL {fav_name} {b_mg}")
        print(f"PROBABILITÀ COMBO: {p_combo:.1f}%")

        # --- VERDETTO ---
        print("\n" + "!" * 40)
        if p_combo > 60:
            print("VERDETTO: ✅ CONSIGLIATO")
        elif p_combo > 45:
            print("VERDETTO: ⚠️ MODERATO")
        else:
            print("VERDETTO: ❌ EVITARE")
        print("="*65)

    except Exception as e:
        print(f"Errore nel calcolo: {e}")

if __name__ == "__main__":
    ai_full_auto_v17_1()
