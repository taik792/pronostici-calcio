import numpy as np
from scipy.stats import poisson

def ai_oracle_v19_totale():
    print("="*65)
    print("   AI ORACLE v19.0 - COMBO MULTIGOL TOTALE")
    print("="*65)
    
    try:
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

        l_casa = -np.log(max(0.01, 1 - (1/c_o05_q)))
        l_ospite = -np.log(max(0.01, 1 - (1/o_o05_q)))
        
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        
        l_tot = l_casa + l_ospite

        # Range Multigol Totale Match
        ranges_tot = [(1,3), (1,4), (2,3), (2,4), (2,5), (2,6)]
        all_options = []

        # 1. COMBO 1X + MULTIGOL TOTALE
        for mi, ma in ranges_tot:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if c >= o and mi <= (c+o) <= ma) * 100
            all_options.append((p, f"1X + MULTIGOL TOTALE {mi}-{ma}"))

        # 2. COMBO X2 + MULTIGOL TOTALE
        for mi, ma in ranges_tot:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if o >= c and mi <= (c+o) <= ma) * 100
            all_options.append((p, f"X2 + MULTIGOL TOTALE {mi}-{ma}"))

        # 3. COMBO GOAL + MULTIGOL TOTALE
        for mi, ma in ranges_tot:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(1, 7) for o in range(1, 7) if mi <= (c + o) <= ma) * 100
            all_options.append((p, f"GOAL + MULTIGOL TOTALE {mi}-{ma}"))

        all_options.sort(key=lambda x: x[0], reverse=True)
        best_p, best_desc = all_options[0]

        print("\n" + "🎯" * 5 + " PRONOSTICO COMBO TOTALE " + "🎯" * 5)
        print("-" * 50)
        print(f"CONSIGLIO: {best_desc}")
        print(f"PROBABILITÀ: {best_p:.1f}%")
        print("-" * 50)

        if best_p > 60:
            print("VERDETTO: ✅ ALTA AFFIDABILITÀ")
        else:
            print("VERDETTO: ⚠️ ATTENZIONE - RISCHIO MEDIO")
        print("="*65)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_oracle_v19_totale()
