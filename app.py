import numpy as np
from scipy.stats import poisson

def ai_oracle_v21_complete():
    print("="*75)
    print("   AI ORACLE v21.0 - THE DEFINITIVE VALUE HUNTER & COMBO ENGINE")
    print("="*75)
    
    try:
        # --- 1. INPUT DATI ---
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
        
        print("\n" + "-"*30)
        # Questa è la quota che vedi sul tuo sito di scommesse per la combo che ti interessa
        q_book = float(input("Che quota ti offre il bookmaker per la combo (es. 1.80)? "))

        # --- 2. MOTORE DI CALCOLO (POISSON) ---
        l_casa = -np.log(max(0.01, 1 - (1/c_o05_q)))
        l_ospite = -np.log(max(0.01, 1 - (1/o_o05_q)))
        
        # Correzione professionale delle medie
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        l_tot = l_casa + l_ospite

        # --- 3. SELEZIONE MIGLIOR COMBO 1X2 + TOTALE ---
        ranges_tot = [(1,3), (1,4), (2,3), (2,4), (2,5)]
        all_options = []
        for mi, ma in ranges_tot:
            # Calcolo 1X + Totale
            p_1x = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(8) for o in range(8) if c>=o and mi<=(c+o)<=ma) * 100
            all_options.append((p_1x, f"1X + MULTIGOL TOTALE {mi}-{ma}"))
            # Calcolo X2 + Totale
            p_x2 = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(8) for o in range(8) if o>=c and mi<=(c+o)<=ma) * 100
            all_options.append((p_x2, f"X2 + MULTIGOL TOTALE {mi}-{ma}"))

        all_options.sort(key=lambda x: x[0], reverse=True)
        best_p, best_desc = all_options[0]

        # --- 4. SELEZIONE COMBO CASA+OSPITE ---
        m_ranges = [(1,2), (1,3), (2,3)]
        combo_co = []
        for mi_c, ma_c in m_ranges:
            for mi_o, ma_o in m_ranges:
                p_c = sum(poisson.pmf(k, l_casa) for k in range(mi_c, ma_c + 1))
                p_o = sum(poisson.pmf(k, l_ospite) for k in range(mi_o, ma_o + 1))
                combo_co.append(((p_c * p_o) * 100, f"CASA {mi_c}-{ma_c} + OSPITE {mi_o}-{ma_o}"))
        combo_co.sort(key=lambda x: x[0], reverse=True)
        best_co_p, best_co_desc = combo_co[0]

        # --- 5. CALCOLO VALORE (VALUE CHECK) ---
        quota_reale = 100 / best_p
        is_value = q_book >= (quota_reale - 0.05) # Tolleranza minima di sicurezza

        # --- 6. OUTPUT FINALE ---
        print("\n" + "🎯" * 5 + " 1. IL PRONOSTICO MIGLIORE " + "🎯" * 5)
        print(f"GIOCATA:      {best_desc}")
        print(f"PROBABILITÀ:  {best_p:.1f}%")
        print(f"QUOTA MINIMA: {quota_reale:.2f} (Sotto questa non conviene)")

        print("\n" + "🎰" * 5 + " 2. COMBO CASA+OSPITE " + "🎰" * 5)
        print(f"GIOCATA:      {best_co_desc} ({best_co_p:.1f}%)")

        print("\n" + "📢" * 5 + " VERDETTO VALUE HUNTER " + "📢" * 5)
        if is_value:
            print(f"✅ VALUE DETECTED! La quota {q_book:.2f} è corretta o vantaggiosa.")
            if best_p > 70: 
                print("🔥 STATUS: INVESTIMENTO ALTO (STAKE 8/10)")
            else: 
                print("👍 STATUS: INVESTIMENTO MEDIO (STAKE 5/10)")
        else:
            print(f"❌ NO VALUE! La quota {q_book:.2f} è troppo bassa per il rischio.")
            print("⚠️ STATUS: EVITARE. La matematica dice che dovresti essere pagato almeno " + f"{quota_reale:.2f}")

        print("="*75)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_oracle_v21_complete()
