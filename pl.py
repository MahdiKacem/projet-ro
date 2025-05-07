from gurobipy import Model, GRB

# Données du problème
warehouses = input("Entrez les entrepôts Wi (séparés par des virgules): ").split(",")
clients = input("Entrez les clients Ci (séparés par des virgules): ").split(",")

# Capacités des entrepôts
supply = {}
for i in range(len(warehouses)):
    supply[warehouses[i]] = int(input(f"Entrez la capacité de l'entrepôt {warehouses[i]}: "))
# Demandes des clients
demand = {}
for i in range(len(clients)):
    demand[clients[i]] = int(input(f"Entrez la capacité du client {clients[i]}: "))


# Coûts de transport (W -> C)
cost = {}
for w in warehouses:
    for c in clients:
        cost[(w.strip(), c.strip())] = int(input(f"Entrez le coût de transport de {w.strip()} à {c.strip()}: "))

# Création du modèle
model = Model("Transport Optimization")

# Variables de décision
x = model.addVars(warehouses, clients, vtype=GRB.CONTINUOUS, name="x")

# Fonction objectif : Minimiser le coût total
total_cost = sum(cost[w, c] * x[w, c] for w in warehouses for c in clients)
model.setObjective(total_cost, GRB.MINIMIZE)

# Contraintes de capacité des entrepôts
for w in warehouses:
    model.addConstr(sum(x[w, c] for c in clients) <= supply[w], f"Supply_{w}")

# Contraintes de satisfaction de la demande
for c in clients:
    model.addConstr(sum(x[w, c] for w in warehouses) >= demand[c], f"Demand_{c}")

# Résolution du modèle
model.optimize()

# Affichage des résultats
if model.status == GRB.OPTIMAL:
    print("Coût total minimal:", model.objVal)
    for w in warehouses:
        for c in clients:
            print(f"Transport de {w} à {c}: {x[w, c].x}")
else:
    print("Solution non optimale trouvée.")
