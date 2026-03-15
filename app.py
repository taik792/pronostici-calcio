import numpy as np
from scipy.stats import poisson

def ai_predictor_recovery_pro():
    print("="*60)
    print("   AI PREDICTOR v14.0 - RECOVERY & MARGIN CLEANER")
    print("="*60)
    
    try:
        # 1. INPUT CON PULIZIA AGGIO
        q1 = float(input("Quota 1: "))
        qx = float(input("Quota X: "))
        q2 = float(input("Quota 2: "))
        qgg = float(input("Quota Goal: "))
        qng = float(input("Quota No Goal: "))
        
        # Calcolo aggio (margine bookmaker)
        margin = (1/q1 + 1/qx + 1/q2) - 1
        # Quote "Pure" senza il guadagno del bookmaker
        p1_pure = (1/q1) / (1 + margin)
        px_pure = (1/qx) / (1 + margin)
        p2_pure = (1/q2) / (1 + margin)

        print("\n[ GOL SQUADRA ]")
        c_o15_q = float(input("Quota Over 1.5 Casa: "))
        o_o15_q = float(input("Quota Over 1.5 Ospite: "))

        # 2. CALCOLO LAMBDA RAFFINATO (DIFESA vs ATTACCO)
        # Usiamo il mercato Goal/No Goal per capire la chiusura delle difese
        p_gg = (1/qgg) / (1/qgg + 1/qng)
        
        # Stima media gol basata sulla forza relativa (p1, p2) e propensione al goal (p_gg)
        l_casa = (p1_pure * 2.5) + (p_gg * 0.5)
        l_ospite = (p2_pure * 2.5) + (p_gg * 0.5)

        # 3. VERIFICA COERENZA (CRUCIALE!)
        # Se la quota Over 1.5 è alta (>2.10) ma Lambda è alto, correggiamo al ribasso
        if c_o15_q > 2.0: l_casa *= 0.85
        if o_o15_q > 2.0: l_ospite *= 0.85

        # 4. CALCOLO MULTIGOL CON FILTRO PRUDENZA
        mg_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        mg_o13 = sum(poisson.pmf(k, l_ospite) for k in range(1, 4)) * 100
        
        # COMBO DI SICUREZZA
        p_1x_mg14 = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(5) for o in range(5) if c>=o and 1<=(c+o)<=4) * 100

        # --- OUTPUT PROFESSIONALE ---
        print("\n" + "!"*15 + " ANALISI POST-LOSS " + "!"*15)
        print(f"Potenza Attacco: Casa {l_casa:.2f} | Ospite {l_ospite:.2f}")
        
        # FILTRO SELEZIONE
        print("\n[ PRONOSTICI AD ALTA SELEZIONE ]")
        if mg_c13 > 65 and q1 < 2.0:
            print(f"✅ CONSIGLIATO: Multigol Casa 1-3 ({mg_c13:.1f}%)")
        else:
            print("⚠️  RISCHIO ALTO: Multigol Casa non garantito.")

        if p_1x_mg14 > 55:
            print(f"✅ CONSIGLIATO: 1X + Multigol 1-4 ({p_1x_mg14:.1f}%)")
            
        # CALCOLO "VALORE"
        quota_equa = 100 / mg_c13
        print(f"\nQuota minima consigliata per MG Casa 1-3: {quota_equa:.2f}")
        print("="*60)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_predictor_recovery_pro()
