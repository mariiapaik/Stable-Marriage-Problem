"""
Účel kódu:
Kód rieši problém stabilného párovania medzi mužmi a ženami na základe ich preferencií. 
Cieľom je vytvoriť maximálny počet stabilných párov, pričom stabilita znamená, že neexistujú 
"blokujúce páry", ktoré by mohli rozbiť existujúce párovanie.

Spôsob práce:
1. Načíta preferencie mužov a žien zo vstupného súboru.
2. Vytvorí CNF reprezentáciu problému so stabilnými párovaniami.
3. Zapíše CNF do súboru `cnf.txt` pre použitie SAT solvera.
4. Spracuje výstup SAT solvera a dekóduje stabilné páry.
5. Výsledné páry zapíše do súboru `result.txt` vo formáte podľa špecifikácie.
"""


import itertools
import re

def load_preferences(file_path):
    males = {}
    females = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('m'):
                parts = line.split(':')
                male_id = int(parts[0][1:])
                preferences = list(map(int, parts[1].strip().split()))
                males[male_id] = preferences
            elif line.startswith('w'):
                parts = line.split(':')
                female_id = int(parts[0][1:])
                preferences = list(map(int, parts[1].strip().split()))
                females[female_id] = preferences

    return males, females

def create_cnf(males, females, output_file='cnf.txt'):
    female_ids = list(females.keys())
    male_ids = list(males.keys())
    no_match_1 = 'w_none1'
    no_match_2 = 'w_none2'
    variable_mapping = {}
    var_counter = 1

    for female in female_ids + [no_match_1] + [no_match_2]:
        for male in male_ids:
            variable_mapping[(female, male)] = var_counter
            var_counter += 1

    total_vars = var_counter - 1
    conditions = []

    for female in female_ids:
        female_vars = [variable_mapping[(female, male)] for male in male_ids]
        conditions.append(female_vars)
        for comb in itertools.combinations(female_vars, 2):
            conditions.append([-comb[0], -comb[1]])

    for male in male_ids:
        male_vars = [variable_mapping[(female, male)] for female in female_ids + [no_match_1] + [no_match_2]]
        conditions.append(male_vars)
        for comb in itertools.combinations(male_vars, 2):
            conditions.append([-comb[0], -comb[1]])

    for female in female_ids:
        female_prefs = females[female]
        for rank, preferred_male in enumerate(female_prefs):
            better_ranked = female_prefs[:rank]
            for better_male in better_ranked:
                for competitor in female_ids + [no_match_1] + [no_match_2]:
                    if competitor == female:
                        continue
                    male_prefs = males[better_male]
                    if female in male_prefs:
                        competitor_rank = (
                            len(male_prefs) if (competitor == no_match_1 or competitor == no_match_2) else male_prefs.index(competitor)
                        )
                        if male_prefs.index(female) < competitor_rank:
                            conditions.append([
                                -variable_mapping[(female, preferred_male)],
                                -variable_mapping[(competitor, better_male)]
                            ])


    with open(output_file, 'w') as cnf_out:
        cnf_out.write(f"p cnf {total_vars} {len(conditions)}\n")
        for condition in conditions:
            cnf_out.write(' '.join(map(str, condition)) + '\n')

    with open('variable_map.txt', 'w') as var_map_out:
        for (male, female), var_id in variable_mapping.items():
            var_map_out.write(f"{var_id} {female}_{male}\n")


def process_solver_output(sat_result_file='sat.txt', map_file='variable_map.txt'):
    variable_dict = {}
    with open(map_file, 'r') as map_in:
        for line in map_in:
            var_id, pairing = line.strip().split()
            variable_dict[int(var_id)] = pairing

    solution = {}
    with open(sat_result_file, 'r') as sat_in:
        for line in sat_in:
            match = re.match(r'x(\d+)\s*=\s*(\d+)', line.strip())
            if match:
                var_id = int(match.group(1))
                value = int(match.group(2))
                solution[var_id] = value

    matches = []
    for var_id, value in solution.items():
        if value == 1:
            pair = variable_dict.get(var_id)
            if pair:
                parts = pair.split('_')
                if len(parts) == 2:
                    male = parts[0]
                    female_part = parts[1]
                    if female_part.startswith('w_none'):
                        matches.append((male, None))
                    else:
                        matches.append((male, female_part))
                else:
                    male = parts[0]
                    female_part = '_'.join(parts[1:])
                    if female_part.startswith('w_none'):
                        matches.append((male, None))
                    else:
                        matches.append((male, female_part))

    print("Processed pairs:", matches)
    return matches

def main():
    male_prefs, female_prefs = load_preferences('Paik.txt')
    create_cnf(male_prefs, female_prefs)
    print("Generated 'cnf.txt'. Upload SAT solver output to 'sat.txt'.")
    input("Press Enter to continue...")
    result_pairs = process_solver_output()
    if result_pairs:
        print("Final matching results:")
        with open("result.txt", "w") as result_file:
            for pair in result_pairs:
                if isinstance(pair, tuple) and len(pair) == 2: 
                    male, female = pair
                    result = f"m{male} w{female}"
                else: 
                    result = pair
                result_file.write(result + "\n")
        print("Results have been saved to 'result.txt'.")

    else:
        print("No results to display. Ensure 'sat.txt' is uploaded correctly.")

if __name__ == "__main__":
    main()