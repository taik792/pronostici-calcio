import numpy as np
from scipy.stats import poisson

def ai_oracle_v18_fixed():
    print("="*65)
    print("   AI ORACLE v18.0 - IL PRONOSTICO DEFINITIVO")
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
        
        # Raffinamento medie
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        
        l_tot = l_casa + l_ospite

        # --- MATRICE DI TUTTE LE COMBO ---
        ranges = [(1,2), (1,3), (1,4), (2,3), (2,4), (2,5)]
        all_options = []

        # 1. Calcolo Combo 1X + MG Casa (Se 1 è favorita o equilibrata)
        for mi, ma in ranges:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if c >= o and mi <= c <= ma) * 100
            all_options.append((p, f"1X + MULTIGOL CASA {mi}-{ma}"))

        # 2. Calcolo Combo X2 + MG Ospite (Se 2 è favorita)
        for mi, ma in ranges:
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(7) for o in range(7) if o >= c and mi <= o <= ma) * 100
            all_options.append((p, f"X2 + MULTIGOL OSPITE {mi}-{ma}"))

        # 3. Calcolo Combo GOAL + MG Match
        for mi, ma in ranges:
            # P(c>=1 AND o>=1 AND mi<=c+o<=ma)
            p = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(1, 7) for o in range(1, 7) if mi <= (c + o) <= ma) * 100
            all_options.append((p, f"GOAL + MULTIGOL MATCH {mi}-{ma}"))

        # --- SELEZIONE VINCITORE ---
        all_options.sort(key=lambda x: x[0], reverse=True)
        best_p, best_desc = all_options[0]

        # --- OUTPUT PULITO ---
        print("\n" + "🎯" * 5 + " ESITO DEL CALCOLO " + "🎯" * 5)
        print("-" * 50)
        print(f"IL MOTORE HA DECISO: {best_desc}")
        print(f"PROBABILITÀ REALE:  {best_p:.1f}%")
        print("-" * 50)

        # --- VERDETTO FINALE ---
        if best_p > 65:
            print("VERDETTO: ✅ ALTA AFFIDABILITÀ - GIOCATA CONSIGLIATA")
        elif best_p > 50:
            print("VERDETTO: ⚠️ MEDIA AFFIDABILITÀ - PROCEDI CON CAUTELA")
        else:
            print("VERDETTO: ❌ BASSA AFFIDABILITÀ - NO BET")
        
        print("\n(Il sistema ha analizzato 18 combinazioni diverse per scegliere questa)")
        print("="*65)

    except Exception as e:
        print(f"Errore tecnico: {e}")

if __name__ == "__main__":
    ai_oracle_v18_fixed()
