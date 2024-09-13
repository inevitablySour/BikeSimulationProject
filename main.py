// Step 1: Initialize the utility matrix and strategies
UTILITY_MATRIX = {
    ('C', 'C'): (6, 6),
    ('C', 'D'): (2, 9),
    ('D', 'C'): (9, 2),
    ('D', 'D'): (3, 3)
}

STRATEGIES = ['Random', 'Hawk', 'Dove', 'Tit-for-Tat']
RESULTS_TABLE = CreateEmptyTable(STRATEGIES)

// Step 2: Run a round-robin tournament
FOR each strategy_1 IN STRATEGIES:
FOR each strategy_2 IN STRATEGIES:
IF strategy_1 != strategy_2:
(score1, score2) = SimulateGame(strategy_1, strategy_2, 100)
// Step 4: Record results
IF score1 > score2:
RESULTS_TABLE[strategy_1][strategy_2] += 1
ELSE IF score2 > score1:
RESULTS_TABLE[strategy_2][strategy_1] += 1
ELSE:
// It's a draw, no winner

// Step 3: Simulate a game of 100 rounds
FUNCTION SimulateGame(strategy_1, strategy_2, rounds):
score1 = 0
score2 = 0
previous_move1 = None
previous_move2 = None

FOR round IN 1 to rounds:
move1 = GetMove(strategy_1, previous_move2)
move2 = GetMove(strategy_2, previous_move1)

(utility1, utility2) = UTILITY_MATRIX[move1, move2]
score1 += utility1
score2 += utility2

previous_move1 = move1
previous_move2 = move2

RETURN (score1, score2)

// Step 5: Output the results
DisplayResults(RESULTS_TABLE)