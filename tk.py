import tkinter as tk
from gurobipy import Model, GRB

# Fonction pour résoudre le problème de transport
def solve_transport():
    try:
        # Récupération des données
        warehouses = entry_warehouses.get().split(",")
        clients = entry_clients.get().split(",")

        # Capacités des entrepôts
        supply = {}
        for w in warehouses:
            supply[w.strip()] = int(entry_supply[w.strip()].get())

        # Demandes des clients
        demand = {}
        for c in clients:
            demand[c.strip()] = int(entry_demand[c.strip()].get())

        # Coûts de transport
        cost = {}
        for w in warehouses:
            for c in clients:
                key = f"{w.strip()}_{c.strip()}"
                cost[(w.strip(), c.strip())] = int(entry_cost[key].get())

        # Modèle Gurobi
        model = Model("Transport Optimization")
        x = model.addVars(warehouses, clients, vtype=GRB.CONTINUOUS, name="x")
        total_cost = sum(cost[w, c] * x[w, c] for w in warehouses for c in clients)
        model.setObjective(total_cost, GRB.MINIMIZE)

        # Contraintes
        for w in warehouses:
            model.addConstr(sum(x[w, c] for c in clients) <= supply[w.strip()], f"Supply_{w.strip()}")
        for c in clients:
            model.addConstr(sum(x[w, c] for w in warehouses) >= demand[c.strip()], f"Demand_{c.strip()}")

        # Optimisation
        model.optimize()

        # Affichage des résultats
        result_text.delete("1.0", tk.END)
        if model.status == GRB.OPTIMAL:
            result_text.insert(tk.END, f"Coût total minimal: {model.objVal}\n")
            for w in warehouses:
                for c in clients:
                    result_text.insert(tk.END, f"Transport de {w} à {c}: {x[w, c].x}\n")
        else:
            result_text.insert(tk.END, "Solution non optimale trouvée.")
    except Exception as e:
        result_text.insert(tk.END, f"Erreur: {str(e)}\n")

# Interface graphique
root = tk.Tk()
root.title("Problème de Transport avec Gurobi")

# Entrée des entrepôts et des clients
entry_warehouses = tk.Entry(root, width=40)
entry_warehouses.insert(0, "W1,W2")
entry_clients = tk.Entry(root, width=40)
entry_clients.insert(0, "C1,C2,C3")

# Bouton pour résoudre le problème
btn_solve = tk.Button(root, text="Résoudre", command=solve_transport)
result_text = tk.Text(root, width=60, height=20)

# Disposition des éléments
tk.Label(root, text="Entrepôts (Wi):").pack()
entry_warehouses.pack()
tk.Label(root, text="Clients (Ci):").pack()
entry_clients.pack()

entry_supply = {}
entry_demand = {}
entry_cost = {}

for w in ["W1", "W2"]:
    entry_supply[w] = tk.Entry(root, width=10)
    entry_supply[w].insert(0, "20")
    tk.Label(root, text=f"Capacité {w}:").pack()
    entry_supply[w].pack()
for c in ["C1", "C2", "C3"]:
    entry_demand[c] = tk.Entry(root, width=10)
    entry_demand[c].insert(0, "10")
    tk.Label(root, text=f"Demande {c}:").pack()
    entry_demand[c].pack()
for w in ["W1", "W2"]:
    for c in ["C1", "C2", "C3"]:
        key = f"{w}_{c}"
        entry_cost[key] = tk.Entry(root, width=10)
        entry_cost[key].insert(0, "5")
        tk.Label(root, text=f"Coût {w} -> {c}:").pack()
        entry_cost[key].pack()

btn_solve.pack()
result_text.pack()
root.mainloop()
