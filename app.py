import numpy as np
from scipy.stats import poisson

def ai_super_selector_v15():
    print("="*60)
    print("   AI PREDICTOR v15.0 - MULTIGOL SMART SELECTOR")
    print("="*60)
    
    try:
        # INPUT QUOTE
        q1 = float(input("Quota 1: "))
        qx = float(input("Quota X: "))
        q2 = float(input("Quota 2: "))
        qgg = float(input("Quota Goal: "))
        qng = float(input("Quota No Goal: "))
        
        print("\n[ GOL SQUADRA ]")
        c_o05_q = float(input("Quota Over 0.5 Casa: "))
        c_o15_q = float(input("Quota Over 1.5 Casa: "))
        o_o05_q = float(input("Quota Over 0.5 Ospite: "))
        o_o15_q = float(input("Quota Over 1.5 Ospite: "))

        # CALCOLO LAMBDA (PULITO)
        l_casa = -np.log(max(0.01, 1 - (1/c_o05_q)))
        l_ospite = -np.log(max(0.01, 1 - (1/o_o05_q)))
        
        # Correzione con quota Over 1.5
        if (1/c_o15_q) < 0.4: l_casa *= 0.8
        if (1/o_o15_q) < 0.4: l_ospite *= 0.8

        def check_multigol(lam, min_g, max_g):
            return sum(poisson.pmf(k, lam) for k in range(min_g, max_g + 1)) * 100

        # LISTA MULTIGOL DA TESTARE
        ranges = [
            (1, 2, "1-2"), (1, 3, "1-3"), (1, 4, "1-4"),
            (2, 3, "2-3"), (2, 4, "2-4"), (2, 5, "2-5"), (3, 5, "3-5")
        ]

        def get_best_mg(lam, team_name):
            best_p = 0
            best_r = ""
            for mi, ma, label in ranges:
                prob = check_multigol(lam, mi, ma)
                if prob > best_p:
                    best_p = prob
                    best_r = label
            return best_r, best_p

        # CALCOLO MIGLIORI OPZIONI
        best_casa_label, best_casa_p = get_best_mg(l_casa, "CASA")
        best_ospite_label, best_ospite_p = get_best_mg(l_ospite, "OSPITE")
        
        # MULTIGOL TOTALE MATCH
        l_tot = l_casa + l_ospite
        best_tot_label, best_tot_p = get_best_mg(l_tot, "MATCH")

        # --- OUTPUT ---
        print("\n" + "!"*15 + " SELEZIONE INTELLIGENTE " + "!"*15)
        print(f"Potenza Attacco: Casa {l_casa:.2f} | Ospite {l_ospite:.2f}")
        
        print(f"\n🥇 MIGLIOR MG CASA:    {best_casa_label} ({best_casa_p:.1f}%)")
        print(f"🥇 MIGLIOR MG OSPITE:  {best_ospite_label} ({best_ospite_p:.1f}%)")
        print(f"🔥 MIGLIOR MG MATCH:   {best_tot_label} ({best_tot_p:.1f}%)")

        print("\n" + "-"*15 + " ANALISI DI SICUREZZA " + "-"*15)
        if best_casa_p > 70:
            print(f"CONSIGLIO: Il Multigol {best_casa_label} Casa è statisticamente blindato.")
        elif l_tot < 1.5:
            print("CONSIGLIO: Match da 'Under'. Evita Multigol alti, meglio MG 1-2 Totale.")
        else:
            print("CONSIGLIO: Match incerto. Preferire le Doppie Chance + MG 1-4.")
        print("="*60)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_super_selector_v15()
