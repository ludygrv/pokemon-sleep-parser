import itertools

def arena_outcomes(win_rate, rewards):
    """
    Simulate all possible Arena outcomes, their probabilities, and net rewards.

    Args:
        win_rate (float): Probability of winning a match (0.0 - 1.0).
        rewards (list): Reward for each number of wins (index = wins).

    Returns:
        list of dict: Each dict contains 'wins', 'losses', 'probability', 'reward'.
    """
    max_wins = len(rewards) - 1
    max_losses = 3
    results = []

    # Each run ends at 2 losses or 5 wins
    # We enumerate all possible (wins, losses) pairs that end a run
    for wins in range(0, max_wins + 1):
        for losses in range(0, max_losses + 1):
            if wins == max_wins and losses < max_losses:
                # Ended by reaching max wins before 2 losses
                # Only valid if losses < 2
                total_games = wins + losses
                # The last game must be a win
                if wins > 0:
                    # Number of ways to arrange (wins-1) wins and losses in (total_games-1) games
                    ways = itertools.combinations(range(total_games-1), wins-1)
                    count = sum(1 for _ in ways)
                    prob = (win_rate ** wins) * ((1 - win_rate) ** losses) * count
                    results.append({
                        'wins': wins,
                        'losses': losses,
                        'probability': prob,
                        'reward': rewards[wins]
                    })
            elif losses == max_losses and wins < max_wins:
                # Ended by reaching 2 losses before max wins
                total_games = wins + losses
                # The last game must be a loss
                if losses > 0:
                    # Number of ways to arrange wins and (losses-1) losses in (total_games-1) games
                    ways = itertools.combinations(range(total_games-1), wins)
                    count = sum(1 for _ in ways)
                    prob = (win_rate ** wins) * ((1 - win_rate) ** losses) * count
                    results.append({
                        'wins': wins,
                        'losses': losses,
                        'probability': prob,
                        'reward': rewards[wins]
                    })
    return results

# Add a column for Reward * Probability
def print_arena_table_with_expected(win_rate, rewards):
    outcomes = arena_outcomes(win_rate, rewards)
    print(f"{'Wins':>4} {'Losses':>6} {'Probability':>12} {'Reward':>8} {'Reward*P':>12}")
    print("-" * 52)
    expected = 0
    for o in outcomes:
        reward_p = o['probability'] * o['reward']
        print(f"{o['wins']:>4} {o['losses']:>6} {o['probability']:12.5%} {o['reward']:8} {reward_p:12.2f}")
        expected += reward_p
    print("-" * 52)
    print(f"Expected net value: {expected:.2f}")


# Example usage:
if __name__ == "__main__":
    # Example: win rate 0.5, rewards for 0-5 wins
    win_rate = 0.6
    # Cost = 300
    
    rewards = [-150, -150, -68, # 0, 1, 2
               -38, 5, 25, # 3, 4, 5
               125, 125, 200, # 6, 7, 8
                190, 450, 500, # 9, 10, 11
                800]

    print_arena_table_with_expected(win_rate, rewards)