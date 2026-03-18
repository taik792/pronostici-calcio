import numpy as np
from scipy.stats import poisson

def ai_oracle_v21_1():
    print("="*75)
    print("   AI ORACLE v21.1 - PRONOSTICO IMMEDIATO + VALUE CHECK")
    print("="*75)
    
    try:
        # --- 1. INPUT DATI INIZIALI ---
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

        # --- 2. MOTORE DI CALCOLO ---
        l_casa = -np.log(max(0.01, 1 - (1/c_o05_q)))
        l_ospite = -np.log(max(0.01, 1 - (1/o_o05_q)))
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85

        # --- 3. CALCOLO COMBO 1X2 + TOTALE ---
        ranges_tot = [(1,3), (1,4), (2,3), (2,4), (2,5), (2,6)]
        all_options = []
        for mi, ma in ranges_tot:
            p_1x = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(8) for o in range(8) if c>=o and mi<=(c+o)<=ma) * 100
            all_options.append((p_1x, f"1X + MULTIGOL TOTALE {mi}-{ma}"))
            p_x2 = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(8) for o in range(8) if o>=c and mi<=(c+o)<=ma) * 100
            all_options.append((p_x2, f"X2 + MULTIGOL TOTALE {mi}-{ma}"))

        all_options.sort(key=lambda x: x[0], reverse=True)
        best_p, best_desc = all_options[0]
        quota_reale = 100 / best_p

        # --- 4. MOSTRA IL PRONOSTICO PRIMA DELLA QUOTA ---
        print("\n" + "🎯" * 5 + " ANALISI COMPLETATA " + "🎯" * 5)
        print(f"IL MIGLIOR PRONOSTICO È: {best_desc}")
        print(f"PROBABILITÀ CALCOLATA:   {best_p:.1f}%")
        print(f"QUOTA MINIMA CONSIGLIATA: {quota_reale:.2f}")
        print("-" * 50)

        # --- 5. ORA CHIEDE LA QUOTA DEL BOOKMAKER ---
        q_book = float(input(f"Che quota ti offre il bookmaker per [{best_desc}]? "))

        # --- 6. VERDETTO FINALE ---
        print("\n" + "📢" * 5 + " VERDETTO VALUE HUNTER " + "📢" * 5)
        if q_book >= (quota_reale - 0.03):
            print(f"✅ VALUE DETECTED! La quota {q_book:.2f} è accettabile.")
            if best_p > 70: print("🔥 STATUS: INVESTIMENTO ALTO (STAKE 8/10)")
            else: print("👍 STATUS: INVESTIMENTO MEDIO (STAKE 5/10)")
        else:
            print(f"❌ NO VALUE! Quota troppo bassa ({q_book:.2f}). Dovrebbe essere almeno {quota_reale:.2f}")
            print("⚠️ CONSIGLIO: NON GIOCARE, IL RISCHIO SUPERA IL GUADAGNO.")

        print("="*75)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_oracle_v21_1()
