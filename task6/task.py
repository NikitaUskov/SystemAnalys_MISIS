import argparse
import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def main(temp_mf_json, heat_mf_json, rules_json, current_temp):
    temp_mfs = json.loads(temp_mf_json)
    heat_mfs = json.loads(heat_mf_json)
    rules = json.loads(rules_json)

    min_temp, max_temp = float('inf'), float('-inf')
    min_heat, max_heat = float('inf'), float('-inf')

    for state in temp_mfs["температура"]:
        for point in state["points"]:
            min_temp = min(min_temp, point[0])
            max_temp = max(max_temp, point[0])

    for state in heat_mfs["уровень нагрева"]:
        for point in state["points"]:
            min_heat = min(min_heat, point[0])
            max_heat = max(max_heat, point[0])

    temperature = ctrl.Antecedent(np.arange(min_temp, max_temp, 1), 'temperature')
    heating = ctrl.Consequent(np.arange(min_heat, max_heat, 0.1), 'heating')

    for mf in temp_mfs['температура']:
        points = np.array(mf['points'])
        temperature[mf['id']] = fuzz.trapmf(temperature.universe,
                                            [points[0][0], points[1][0], points[2][0], points[3][0]])

    for mf in heat_mfs['уровень нагрева']:
        points = np.array(mf['points'])
        heating[mf['id']] = fuzz.trapmf(heating.universe, [points[0][0], points[1][0], points[2][0], points[3][0]])

    activated_rules = []
    for rule in rules:
        if rule[0] in temperature.terms and rule[1] in heating.terms:
            temp_level = fuzz.interp_membership(temperature.universe, temperature[rule[0]].mf, current_temp)
            if temp_level > 0:
                activated_rules.append((temp_level, rule[1]))

    output_mf = np.zeros_like(heating.universe)
    for activation_level, heat_term in activated_rules:
        heat_mf = heating[heat_term].mf
        output_mf = np.maximum(output_mf, np.minimum(activation_level, heat_mf))

    if np.any(output_mf):
        return fuzz.defuzz(heating.universe, output_mf, 'centroid')
    else:
        raise ValueError("Empty output region")


def load_json(source, default):
    try:
        if source.endswith('.json'):
            with open(source, 'r', encoding='utf-8') as f:
                return json.load(f)
        return json.loads(source)
    except Exception as e:
        print(f"Ошибка при загрузке JSON из {source}: {e}")
        raise

parser = argparse.ArgumentParser(description="Calculate optimal heating level based on fuzzy logic.")
parser.add_argument('--temp_file', type=str, help="Path to temperature membership functions JSON file.")
parser.add_argument('--heat_file', type=str, help="Path to heating membership functions JSON file.")
parser.add_argument('--rules_file', type=str, help="Path to rules JSON file.")
parser.add_argument('--current_temp', type=int, required=True, help="Current temperature (integer).")
args = parser.parse_args()

default_temp_mf = {
    "температура": [
        {"id": "холодно", "points": [[0, 0], [5, 1], [10, 1], [12, 0]]},
        {"id": "комфортно", "points": [[18, 0], [22, 1], [24, 1], [26, 0]]},
        {"id": "жарко", "points": [[24, 0], [26, 1], [40, 1], [50, 0]]}
    ]
}

default_heat_mf = {
        "уровень нагрева": [
            {"id": "слабый", "points": [[0, 0], [0, 1], [5, 1], [8, 0]]},
            {"id": "умеренный", "points": [[5, 0], [8, 1], [13, 1], [16, 0]]},
            {"id": "интенсивный", "points": [[13, 0], [18, 1], [23, 1], [26, 0]]}
        ]
    }

default_rules = [
        ['холодно', 'интенсивный'],
        ['комфортно', 'умеренный'],
        ['жарко', 'слабый']
    ]

temp_mf_json = load_json(args.temp_file, default_temp_mf)
heat_mf_json = load_json(args.heat_file, default_heat_mf)
rules_json = load_json(args.rules_file, default_rules)

try:
    optimal_heating = main(json.dumps(temp_mf_json), json.dumps(heat_mf_json),
                           json.dumps(rules_json), args.current_temp)
    print(f"Оптимальный уровень нагрева: {optimal_heating:.2f}")
except ValueError as e:
    print(f"Ошибка: {e}")
