from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import solve_transportation

app = Flask(__name__)
CORS(app)


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()

    try:
        warehouses = data['warehouses']
        clients = data['clients']
        supply = {w: float(data['supply'][w]) for w in warehouses}
        demand = {c: float(data['demand'][c]) for c in clients}
        cost_matrix = {(w, c): float(data['costMatrix'][f"{w}_{c}"])
                       for w in warehouses for c in clients}

        obj_val, solution = solve_transportation(warehouses, clients, supply, demand, cost_matrix)

        if obj_val is not None:
            formatted_solution = {f"{w}_{c}": solution[(w, c)]
                                  for w in warehouses for c in clients}
            return jsonify({
                'objVal': obj_val,
                'solution': formatted_solution
            })
        else:
            return jsonify({'error': 'No solution found'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)