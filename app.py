import numpy as np
from scipy.stats import poisson

def ai_full_auto_v17():
    print("="*65)
    print("   AI PREDICTOR v17.0 - FULL AUTO & SMART COMBO")
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
        
        # Correzione con quota Over 1.5 per evitare stime eccessive
        if (1/c_o15_q) < 0.45: l_casa *= 0.85
        if (1/o_o15_q) < 0.45: l_ospite *= 0.85
        
        l_tot = l_casa + l_ospite

        # --- LOGICA DI SELEZIONE MULTIGOL ---
        ranges = [(1,2,"1-2"), (1,3,"1-3"), (1,4,"1-4"), (2,3,"2-3"), (2,4,"2-4"), (2,5,"2-5")]

        def get_best_range(lam):
            # Trova il range con la probabilità più alta
            res = sorted([(sum(poisson.pmf(k, lam) for k in range(mi, ma+1)), lbl) for mi, ma, lbl in ranges], reverse=True)
            return res[0] # (probabilità, etichetta)

        p_c, b_c = get_best_range(l_casa)
        p_o, b_o = get_best_range(l_ospite)
        p_t, b_t = get_best_range(l_tot)

        # --- DECISIONE AUTOMATICA FAVORITA ---
        if q1 <= q2:
            favorita = "CASA"
            doppia_chance = "1X"
            best_mg_team = b_c
            prob_base = p_c
            # Calcolo Combo 1X + MG Casa scelto dal motore
            mi, ma = map(int, b_c.split('-'))
            p_combo = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(6) for o in range(6) if c>=o and mi<=c<=ma) * 100
        else:
            favorita = "OSPITE"
            doppia_chance = "X2"
            best_mg_team = b_o
            prob_base = p_o
            # Calcolo Combo X2 + MG Ospite scelto dal motore
            mi, ma = map(int, b_o.split('-'))
            p_combo = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(6) for o in range(6) if o>=c and mi<=o<=ma) * 100

        # --- OUTPUT RISULTATI ---
        print("\n" + "📊" * 5 + " ANALISI MOTORE " + "📊" * 5)
        print(f"Favorita rilevata:  {favorita} (Quota: {min(q1, q2)})")
        print(f"Potenza Attacco:    {favorita} {max(l_casa, l_ospite):.2f}")
        print("-" * 50)
        
        print(f"Miglior MG {favorita}: {best_mg_team} (Affidabilità: {prob_base*100:.1f}%)")
        print(f"Miglior MG MATCH:  {best_t} (Affidabilità: {p_t*100:.1f}%)")
        
        print("\n" + "🚀" * 5 + " PRONOSTICO COMBO DEFINITIVO " + "🚀" * 5)
        print(f"GIOCATA: {doppia_chance} + MULTIGOL {favorita} {best_mg_team}")
        print(f"PROBABILITÀ CALCOLATA: {p_combo:.1f}%")

        # --- FILTRO SICUREZZA ---
        print("\n" + "!" * 40)
        if p_combo > 60:
            print("VERDETTO: ✅ CONSIGLIATO (Alta Coerenza)")
        elif p_combo > 45:
            print("VERDETTO: ⚠️ MODERATO (Usa prudenza)")
        else:
            print("VERDETTO: ❌ EVITARE (Rischio troppo elevato)")
        print("="*65)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_full_auto_v17()
