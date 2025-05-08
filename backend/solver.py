from gurobipy import Model, GRB

def solve_transportation(warehouses, clients, supply, demand, cost_matrix):
    model = Model("Transport Optimization")
    model.setParam('OutputFlag', 0)

    x = model.addVars(warehouses, clients, vtype=GRB.CONTINUOUS, name="x")

    total_cost = sum(cost_matrix[(w, c)] * x[w, c] for w in warehouses for c in clients)
    model.setObjective(total_cost, GRB.MINIMIZE)

    for w in warehouses:
        model.addConstr(sum(x[w, c] for c in clients) <= supply[w], f"Supply_{w}")
    for c in clients:
        model.addConstr(sum(x[w, c] for w in warehouses) == demand[c], f"Demand_{c}")

    model.optimize()

    if model.status == GRB.OPTIMAL:
        solution = {(w, c): x[w, c].x for w in warehouses for c in clients}
        return model.objVal, solution
    else:
        return None, None