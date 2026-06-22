#!/usr/bin/env python
"""Construct legal solution to liars 1-4 make 10 puzzle.

- Allowed operations: +, -, /, *, parentheses
- Digits: 1, 2, 3, 4 (but the 1 is lying; it is a 0)
- Make 1-10 with 1-4 such that it still works when the liar is revealed

Within the main "puzzle-scripts" directory, run:
./find_liar_expr.py
"""

import itertools # Quick combination making
from typing import Dict, List # Type hints

def add_parens(pre_paren: List[str], open_parens: int,
               allow_open: bool) -> List[List[str]]:
    """Add parentheses to a list that is [digit, op, digit, ... digit]
    
    Some open parentheses from before may have to be closed.
    Output all possible result lists.
    Only one open paren ever is allowed.
    """
    if len(pre_paren) == 1:
        # Base case: only one number left, just have to close all the parens
        return [pre_paren + [')'] * open_parens]
    
    # First try not adding any parens
    post_parens = [pre_paren[:2] + ending for ending
                   in add_parens(pre_paren[2:], open_parens, allow_open)]
    # Then try adding only a close paren
    if open_parens > 0:
        post_parens += [ [pre_paren[0], ')', pre_paren[1]] + ending for ending
                        in add_parens(pre_paren[2:], open_parens - 1, allow_open)]
    # Then try adding only an open paren
    if allow_open:
        post_parens += [['('] + pre_paren[:2] + ending for ending
                        in add_parens(pre_paren[2:], open_parens + 1, False)]
    return post_parens

def generate_expr(digits: List[str], results: List[int], operations: List[str]
                  ) -> Dict[int, Dict[int, List[str]]]:
    """Generate all expressions with valid orig/liar results.
    
    Try all digit orders, with all operation combinations inserted in,
    and with all valid parentheses as well.

    Return a dict with [orig_val][liar_val] = ['expr1', 'expr2', ...]
    """
    pairs = {orig: {liar: [] for liar in results} for orig in results}
    # For all possible orderings of the digits
    for cur_order in itertools.permutations(digits):
        # For all possible sequences of operations
        for cur_ops in itertools.product(operations, operations, operations):
            # Construct an expression
            pre_paren = [cur_order[0], cur_ops[0], cur_order[1], cur_ops[1],
                         cur_order[2], cur_ops[2], cur_order[3]]
            # For all possible ways to add parentheses to this expression
            for post_paren in add_parens(pre_paren, 0, True):
                # Convert list to a string like 1+2+3+4
                orig_expr = ''.join(post_paren)
                # Convert original expression to liar version (swap 1 for 0)
                liar_expr = orig_expr.replace('1', '0')

                try:
                    # Try to evaluate these (guranteed safe since only nums/ops)
                    orig_value = eval(orig_expr)
                    liar_value = eval(liar_expr)
                    orig_int = int(orig_value)
                    liar_int = int(liar_value)
                    # If both versions evaluate to something valid, save them
                    if (orig_int == orig_value and orig_value in results
                        and liar_int == liar_value and liar_value in results):
                        pairs[orig_int][liar_int].append(orig_expr)
                except ZeroDivisionError:
                    # If we try to divide by zero that's not a valid expression!
                    continue
    return pairs

def print_possibility_matrix(expr: Dict[int, Dict[int, List[str]]]) -> None:
    """Print a grid of whether certain result combinations are possible.
    
    Rows are the original (i.e. 1=1) expression result.
    Cols are the liar (i.e. 1=0) expresion result.

    If a combo is impossible it is `.`,
    possible with parentheses is `y`,
    and possible without parentheses is `Y`.
    """

    for orig in sorted(expr.keys()):
        for liar in sorted(expr[orig].keys()):
            cur_expr = expr[orig][liar]
            if cur_expr:
                # Are there any non-paren expressions here?
                if any(not '(' in e for e in cur_expr):
                    print('Y', end='')
                else:
                    print('y', end='')
            else:
                # No expressions at all are possible
                print('.', end='')
        # Finished a row, newline
        print()

def print_expressions(expr: Dict[int, Dict[int, List[str]]]) -> None:
    """Print valid expressions as (orig val, liar val): list of expr."""
    for orig in sorted(expr.keys()):
        for liar in sorted(expr[orig].keys()):
            cur_expr = expr[orig][liar]
            if cur_expr:
                print(orig, '/', liar, ':', ' '.join(cur_expr))

if __name__ == '__main__':
    goals = list(range(1, 11))
    expr = generate_expr(['1', '2', '3', '4'], # Digits 1-4
                         list(range(1, 11)), # Make numbers 1-10
                         ['+', '-', '/', '*']) # Using 4-function operations
    # Used to figure out which orig/liar result pairs to use
    print_possibility_matrix(expr)
    # Used to get legal expressions for those pairs
    print_expressions(expr)