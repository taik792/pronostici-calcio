import numpy as np
from scipy.stats import poisson

def ai_oracle_v20_integrale():
    print("="*65)
    print("   AI ORACLE v20.0 - MULTIGOL INTEGRALE & C+O")
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
        
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        
        l_tot = l_casa + l_ospite

        # --- SEZIONE 1: IL PRONOSTICO DEFINITIVO (LOGICA V19) ---
        ranges_tot = [(1,3), (1,4), (2,3), (2,4), (2,5), (2,6)]
        all_options = []

        # Combo 1X + Totale
        for mi, ma in ranges_tot:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if c >= o and mi <= (c+o) <= ma) * 100
            all_options.append((p, f"1X + MULTIGOL TOTALE {mi}-{ma}"))

        # Combo X2 + Totale
        for mi, ma in ranges_tot:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if o >= c and mi <= (c+o) <= ma) * 100
            all_options.append((p, f"X2 + MULTIGOL TOTALE {mi}-{ma}"))

        all_options.sort(key=lambda x: x[0], reverse=True)
        best_p, best_desc = all_options[0]

        # --- SEZIONE 2: NUOVA AGGIUNTA - MULTIGOL CASA + OSPITE ---
        # Definiamo i range classici per le singole squadre
        m_ranges = [(1,2), (1,3), (2,3)]
        combo_co = []

        for mi_c, ma_c in m_ranges:
            for mi_o, ma_o in m_ranges:
                # P(mi_c <= c <= ma_c AND mi_o <= o <= ma_o)
                p_c = sum(poisson.pmf(k, l_casa) for k in range(mi_c, ma_c + 1))
                p_o = sum(poisson.pmf(k, l_ospite) for k in range(mi_o, ma_o + 1))
                prob_final = (p_c * p_o) * 100
                combo_co.append((prob_final, f"CASA {mi_c}-{ma_c} + OSPITE {mi_o}-{ma_o}"))

        combo_co.sort(key=lambda x: x[0], reverse=True)
        best_co_p, best_co_desc = combo_co[0]

        # --- OUTPUT RISULTATI ---
        print("\n" + "🎯" * 5 + " 1. PRONOSTICO COMBO 1X2 " + "🎯" * 5)
        print(f"CONSIGLIO: {best_desc}")
        print(f"PROBABILITÀ: {best_p:.1f}%")
        
        print("\n" + "🎰" * 5 + " 2. COMBO MULTIGOL CASA+OSPITE " + "🎰" * 5)
        print(f"MIGLIOR OPZIONE: {best_co_desc}")
        print(f"PROBABILITÀ: {best_co_p:.1f}%")

        print("\n" + "-" * 50)
        if best_p > 60 or best_co_p > 40: # Le combo C+O hanno probabilità più basse perché più difficili
            print("VERDETTO FINALE: ✅ I dati mostrano una via chiara.")
        else:
            print("VERDETTO FINALE: ⚠️ Match molto incerto, prudenza.")
        print("="*65)

    except Exception as e:
        print(f"Errore tecnico: {e}")

if __name__ == "__main__":
    ai_oracle_v20_integrale()
