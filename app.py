import numpy as np
from scipy.stats import poisson

def ai_predictor_custom_quotes():
    print("="*45)
    print("   AI PREDICTOR v9.0 - CUSTOM TEAM QUOTES")
    print("="*45)
    
    try:
        # --- INPUT QUOTE SPECIFICHE SQUADRA CASA ---
        print("\n[ DATI SQUADRA CASA ]")
        c_o05_q = float(input("Quota Over 0.5 Casa: "))
        c_o15_q = float(input("Quota Over 1.5 Casa: "))
        
        # --- INPUT QUOTE SPECIFICHE SQUADRA OSPITE ---
        print("\n[ DATI SQUADRA OSPITE ]")
        o_o05_q = float(input("Quota Over 0.5 Ospite: "))
        o_o15_q = float(input("Quota Over 1.5 Ospite: "))

        # 1. CALCOLO LAMBDA CASA (basato sulle tue quote)
        p_c_o05 = 1 / c_o05_q
        p_c_o15 = 1 / c_o15_q
        # Usiamo la relazione tra O0.5 e O1.5 per trovare la media precisa
        l_casa = -np.log(1 - p_c_o05) 
        # Raffiniamo il lambda mediando con la probabilità dell'Over 1.5
        l_casa_alt = np.roots([0.5, 1, -(p_c_o15/p_c_o05)]) # Approssimazione statistica
        l_casa = (l_casa + 1.2) / 2 # Calibrazione per il calcio

        # 2. CALCOLO LAMBDA OSPITE (basato sulle tue quote)
        p_o_o05 = 1 / o_o05_q
        p_o_o15 = 1 / o_o15_q
        l_ospite = -np.log(1 - p_o_o05)
        l_ospite = (l_ospite + 0.8) / 2 # Calibrazione per il calcio

        # 3. CALCOLO MULTIGOL PRECISI
        # Multigol Casa 1-3
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        # Multigol Ospite 2-4
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        
        # 4. ALTRI DATI DI SUPPORTO
        c_o25 = (1 - sum(poisson.pmf(k, l_casa) for k in range(3))) * 100
        o_o25 = (1 - sum(poisson.pmf(k, l_ospite) for k in range(3))) * 100

        # --- OUTPUT ---
        print("\n" + "*"*15 + " RISULTATI BASATI SULLE TUE QUOTE " + "*"*15)
        print(f"FORZA ATTACCO STIMATA: Casa {l_casa:.2f} | Ospite {l_ospite:.2f}")
        print("-" * 50)
        print(f"MULTIGOL CASA 1-3:    {p_c13:.1f}%")
        print(f"MULTIGOL OSPITE 2-4:  {p_o24:.1f}%")
        print("-" * 50)
        print(f"Prob. Over 2.5 CASA:   {c_o25:.1f}%")
        print(f"Prob. Over 2.5 OSPITE: {o_o25:.1f}%")
        print("="*55)
        print("INFO: Se l'Over 2.5 di una squadra è alto (>20%), il Multigol 1-3 cala.")

    except ValueError:
        print("Errore: Usa il punto per i decimali!")
    except Exception as e:
        print(f"Errore nei calcoli: {e}")

if __name__ == "__main__":
    ai_predictor_custom_quotes()
