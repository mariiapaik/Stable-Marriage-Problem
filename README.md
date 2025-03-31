Stable Marriage Problem Solver

Overview
This Python script solves the Stable Marriage Problem, where the goal is to match pairs (traditionally men and women) based on their preferences in a stable way. A stable match means there are no two individuals who would both rather have each other over their current partners.
How It Works
The program follows these key steps:
Load Preferences:
Reads the preferences of males and females from an input file (Paik.txt).
Generate CNF:
Translates the preference data into a CNF (Conjunctive Normal Form) file named cnf.txt.
This CNF file is designed to be used with a SAT solver to find stable pairings.
Solve with SAT Solver:
The user provides the output from a SAT solver in a file named sat.txt.
Process Results:
Parses the SAT solver output to identify stable pairs.
Writes the results to result.txt.
Files
Paik.txt: Input file containing participant preferences.
cnf.txt: CNF format file generated by the program for use with a SAT solver.
sat.txt: Output file from a SAT solver (user provided).
result.txt: Output file with final stable pairs.
variable_map.txt: Mapping file generated to decode the SAT solver output.
