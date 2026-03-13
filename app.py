import numpy as np
from scipy.stats import poisson

def analizzatore_tattico_pro():
    print("="*45)
    print("   AI STRATEGIST - MULTIGOL & LOGICA")
    print("="*45)
    
    try:
        u25 = float(input("Quota Under 2.5: "))
        o25 = float(input("Quota Over 2.5: "))
        gg = float(input("Quota Goal: "))
        ng = float(input("Quota No Goal: "))

        p_over = (1/o25) / ((1/o25) + (1/u25))
        p_gg = (1/gg) / ((1/gg) + (1/ng))
        media_totale = 1.7 + (p_over * 1.6)
        l_casa = media_totale * (0.55 if p_gg > 0.5 else 0.62)
        l_ospite = media_totale - l_casa

        # --- CALCOLO PROBABILITÀ ---
        p_c13 = sum(poisson.pmf(k, l_casa) for k in range(1, 4)) * 100
        p_o24 = sum(poisson.pmf(k, l_ospite) for k in range(2, 5)) * 100
        p_1 = sum(poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite) for c in range(8) for o in range(8) if c > o) * 100

        # --- LOGICA DI ANALISI (IL "PERCHÉ") ---
        analisi = ""
        if media_totale < 2.2:
            analisi = "PARTITA BLOCCATA: Le difese prevalgono. Il Multigol Casa 1-3 è molto solido."
        elif media_totale > 3.0:
            analisi = "PARTITA APERTA: Alto rischio Over. Il Multigol 2-4 Ospite è interessante se giocano in contropiede."
        
        if p_1 > 60:
            analisi += "\nDOMINIO CASA: La squadra di casa ha una pressione offensiva costante."
        elif p_gg < 45:
            analisi += "\nMONOLOGO: Una delle due squadre potrebbe non segnare affatto."

        # --- OUTPUT ---
        print("\n" + "*"*12 + " VERDETTO TATTICO " + "*"*12)
        print(f"Sintesi: {analisi}")
        print("-" * 45)
        print(f"MG CASA 1-3:   {p_c13:.1f}%")
        print(f"MG OSPITE 2-4: {p_o24:.1f}%")
        print(f"PROB. VITTORIA CASA (1): {p_1:.1f}%")
        
        # Risultato più probabile
        res = [(f"{c}-{o}", poisson.pmf(c, l_casa) * poisson.pmf(o, l_ospite)) for c in range(4) for o in range(4)]
        res.sort(key=lambda x: x[1], reverse=True)
        print(f"RISULTATO TOP: {res[0][0]} ({res[0][1]*100:.1f}%)")
        print("*"*45)

    except ValueError:
        print("Errore: Usa il punto per i decimali!")

if __name__ == "__main__":
    analizzatore_tattico_pro()
