import numpy as np
from itertools import combinations
from tqdm import tqdm
import time


### TODO: I'd try to somehow incorporate grundy and period together, to maybe limit the max_n in calculations
### like the period must happen at least 3 times after some pre-period or sth

def calculate_grundy(S, max_n):
    """
    Calculate the Grundy numbers G(n) for a subtraction game with moves in set S.

    Parameters:
    - S (list): The allowed moves (subtraction values).
    - max_n (int): The maximum heap size to compute Grundy numbers for.

    Returns:
    - list: Grundy numbers G(0) to G(max_n).
    """
    grundy = [0] * (max_n + 1)  # Initialize Grundy numbers to 0

    for n in range(1, max_n + 1):
        # Determine reachable Grundy numbers
        reachable = {grundy[n - move] for move in S if n - move >= 0}
        # Minimum excluded value (mex)
        grundy[n] = next(x for x in range(len(reachable) + 1) if x not in reachable)

    return grundy


def find_period(grundy, max_a):
    """
    Find the pre-period (l) and period (p) of the Grundy sequence.

    Parameters:
    - grundy (list): Grundy numbers for the sequence.
    - max_a (int): Maximum move value (a).

    Returns:
    - tuple: (pre-period l, period p)
    """
    length = len(grundy)
    try:
        for l in range(max_a, length):  # Start searching from max_a
            for p in range(1, length - l):
                if grundy[l:l + p] == grundy[l + p:l + 2 * p]:  # Check for periodicity
                    # Verify periodicity according to Corollary 7.34
                    if all(grundy[n] == grundy[n + p] for n in range(l, min(l + p + max_a, length))):
                        return l, p
    except Exception:
        pass
    return None, None  # If no period is found

def find_period_iterative(S, max_n):
    if len(S) == 3:
        if S[0] == 1 and S[1] == 2:
            return None, S[2] + 1 if S[2] % 3 == 0 else 3
        if S[0] == 1 and S[1] == 3:
            return None, S[2] + 3 if S[2] % 2 == 0 else 2
        if S[0] == 1 and S[1] + 1 == S[2] and S[2] >= 3:
            return None, 2 * S[1] + 1 if S[1] % 2 == 0 else 2 * S[1]

    max_a = max(S)

    grundy = [0] * (max_n + 1)

    for n in range(1, max_n + 1):
        # Determine reachable Grundy numbers
        reachable = {grundy[n - move] for move in S if n - move >= 0}
        # Minimum excluded value (mex)
        tmp_val = 0
        while tmp_val in reachable:
            tmp_val += 1
        grundy[n] = tmp_val

        temp_grundy = grundy[:n]
        l, p = find_period(temp_grundy, max_a)

        if l is not None:
            return l, p
    
    return None, None


def max_period(S):
    k = len(S)
    a = np.max(S)

    return (k+1)**a


def generate_combinations(max_a, size_S):
    elements = list(range(1, max_a))
    results = []

    for comb in combinations(elements, size_S - 1):
        # Add max_a to the combination and sort
        results.append(tuple(sorted(comb + (max_a,))))
    
    return results


def worst_period(max_a, size_S):

    possible_moves = generate_combinations(max_a, size_S)
    period = 0
    worst_S = []
    max_period = (size_S + 1)**max_a
    max_n = min(max_period, 10000)


    with open(f'data/S={size_S}/max_a={max_a}', 'w') as file:
        file.write('S;p;l\n')
        for S in tqdm(possible_moves):
            # # how many steps should we check?
            # # let's say that period must happen at least 3 times
            # # so let's get 4 times, with pre-period in mind
            # max_per = max_period(S)
            l, p = find_period_iterative(S, max_n)

            #ZAPIS
            line = f'{S};{p};{l}'
            file.write(line + '\n')


            if l is None:
                return None, None

            if p > period:
                period = p
                worst_S = S

                if period == max_period:
                    break
    


    return period, worst_S


def worst_period_values_S(max_n, size_S):
    # max_n - up to which value do we want to check the period

    values = []
    max_time = 60*15

    with open(f'data/times/S={size_S}', 'w') as file:
        file.write('max_a;duration\n')

        for max_a in range(1, max_n+1):
            start_time = time.time()
            period, S = worst_period(max_a, size_S)
            end_time = time.time()
            duration = end_time - start_time

            line = f'{max_a};{duration}'
            file.write(line + '\n')

            values.append(period) 
            print(f"max_a: {max_a}, period: {period}, S: {S}")

            if duration > max_time:
                break

    return values


