# -*- coding: utf-8 -*-

# On definit nos taches, on les nomme, on donne leur temps d'execution (C) et leur periode (T)
TACHES = [
    {"id": "T1", "C": 1.0, "T": 10},
    {"id": "T2", "C": 3.0, "T": 10},
    {"id": "T3", "C": 2.0, "T": 20},
    {"id": "T4", "C": 2.0, "T": 20},
    {"id": "T5", "C": 2.0, "T": 40},
    {"id": "T6", "C": 2.0, "T": 40},
    {"id": "T7", "C": 3.0, "T": 80}
]

def generer_taches():
    """
    Cette fonction cree toutes les instances de taches que l'on va devoir executer
    sur une periode de 80 ms.
    """
    taches = []
    for t in TACHES:
        for i in range(80 // t["T"]):
            taches.append({
                "id": t["id"],
                "C": t["C"],
                "reveil": i * t["T"],
                "echeance": (i + 1) * t["T"]
            })
    return taches


def simuler(sacrifice_t5=False):
    """
    La fonction qui va se charger d'ordonnancer chaque tache.
    Par defaut, elle utilise la regle EDF (Echeance la plus proche en premier).
    Si sacrifice_t5 est True, la tache T5 passera toujours en dernier.
    """
    taches = generer_taches() # On prend une nouvelle liste propre
    t = 0.0
    attente_totale = 0.0
    echeances_ratees = 0

    while taches: # Tant qu'il reste des taches dans la liste
        # On prend celles dont l'heure de reveil est passee
        pretes = [j for j in taches if j["reveil"] <= t]
        
        if not pretes:
            t = min(j["reveil"] for j in taches) # On avance l'horloge au prochain reveil
            continue
            
        # Tri : on met T5 a la fin si demande, puis tri par echeance et temps d'execution
        if sacrifice_t5:
            pretes.sort(key=lambda x: (x["id"] == "T5", x["echeance"], x["C"]))
        else:
            pretes.sort(key=lambda x: (x["echeance"], x["C"]))
            
        # On traite la premiere tache et on l'enleve definitivement de la liste
        tache_choisie = pretes[0]
        taches.remove(tache_choisie)
        
        # Calculs du temps
        attente_totale += (t - tache_choisie["reveil"])
        t += tache_choisie["C"]
        
        # Verification si on a depasse la date limite
        if t > tache_choisie["echeance"]:
            echeances_ratees += 1
            
    return echeances_ratees, attente_totale


ratees_1, attente_1 = simuler(sacrifice_t5=False)
print("Simulation n1")
print(f"Echeances ratees : {ratees_1}")
print(f"Temps d'attente total : {attente_1:.3f} ms\n")

ratees_2, attente_2 = simuler(sacrifice_t5=True)
print("Simulation n2 avec tau_5 sacrifiable")
print(f"Echeances ratees : {ratees_2}")
print(f"Nouveau temps d'attente total : {attente_2:.3f} ms")
print(f"Gain global : {attente_1 - attente_2:.3f} ms")