import numpy as np
from scipy.stats import poisson

def ai_gold_master_v13():
    print("="*60)
    print("   AI GOLD MASTER v13.0 - LOGICA DI VALIDAZIONE")
    print("="*60)
    
    try:
        # --- INPUT DATI ---
        q1 = float(input("Quota 1: "))
        qx = float(input("Quota X: "))
        q2 = float(input("Quota 2: "))
        qgg = float(input("Quota Goal: "))
        qng = float(input("Quota No Goal: "))
        
        print("\n[ MERCATI CASA ]")
        c_o05_q = float(input("Quota Over 0.5 Casa: "))
        c_o15_q = float(input("Quota Over 1.5 Casa: "))
        
        print("\n[ MERCATI OSPITE ]")
        o_o05_q = float(input("Quota Over 0.5 Ospite: "))
        o_o15_q = float(input("Quota Over 1.5 Ospite: "))

        # --- MOTORE DI CALCOLO ---
        # 1. Calcolo Medie Gol (Lambda) raffinate
        l_casa = -np.log(1 - (1/c_o05_q))
        l_ospite = -np.log(1 - (1/o_o05_q))
        
        # 2. Probabilità Reali
        p_1 = (1/q1) / ((1/q1) + (1/qx) + (1/q2))
        p_gg = (1/qgg) / ((1/qgg) + (1/qng))
        
        # 3. Calcolo Esiti Granulari
        mg_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        mg_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        
        # 4. LOGICA DI VALIDAZIONE (Il "Cervello" del software)
        # Verifichiamo se la quota 1X2 concorda con i gol squadra
        score = 0
        if p_1 > 0.5 and l_casa > 1.4: score += 1 # Coerenza favorita/attacco
        if p_gg > 0.5 and l_ospite > 0.9: score += 1 # Coerenza Goal/attacco ospite
        if c_o15_q < 1.8 and l_casa > 1.2: score += 1 # Coerenza quota Over/media gol
        if (1/qng) > 0.4 and l_ospite < 1.0: score += 1 # Coerenza difesa casa
        
        stelle = "⭐" * (score + 1)

        # --- OUTPUT ---
        print("\n" + "!"*15 + " VERDETTO FINALE " + "!"*15)
        print(f"AFFIDABILITÀ: {stelle}")
        print("-" * 50)
        
        print(f"MG CASA 1-3:    {mg_c13:.1f}%")
        print(f"MG OSPITE 2-4:  {mg_o24:.1f}%")
        
        # Nuova Combo suggerita basata sulla validazione
        p_1x_mg24 = sum(poisson.pmf(c, l_casa)*poisson.pmf(o, l_ospite) for c in range(5) for o in range(5) if c>=o and 2<=(c+o)<=4) * 100
        
        print(f"\n[ COMBO VALIDATA ]")
        print(f"1X + MULTIGOL 2-4: {p_1x_mg24:.1f}%")
        
        if score >= 3:
            print("\n🔥 NOTA: I dati sono molto coerenti. Alta probabilità statistica.")
        else:
            print("\n⚠️  NOTA: Dati discordanti. Possibile trappola del bookmaker.")
        print("="*60)

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    ai_gold_master_v13()
