import random
import time

def binary_search_strategy(min_val, max_val, feedback=None):
    """
    Implements binary search strategy for the number guessing game.
    Returns the next guess based on previous feedback.
    """
    # Store min and max values as static variables if this is the first call
    if not hasattr(binary_search_strategy, 'current_min'):
        binary_search_strategy.current_min = min_val
        binary_search_strategy.current_max = max_val
    
    if feedback is None:  # First guess
        # Reset the range for a new game
        binary_search_strategy.current_min = min_val
        binary_search_strategy.current_max = max_val
        return (binary_search_strategy.current_min + binary_search_strategy.current_max) // 2
    
    guess, result = feedback
    if result == "low":
        binary_search_strategy.current_min = guess + 1
    elif result == "high":
        binary_search_strategy.current_max = guess - 1
    
    return (binary_search_strategy.current_min + binary_search_strategy.current_max) // 2

def linear_search_strategy(min_val, max_val, feedback=None):
    """
    Implements linear search strategy for the number guessing game.
    Simply starts at min_val and increments by 1.
    """
    # Initialize current value if this is the first run
    if not hasattr(linear_search_strategy, 'current'):
        linear_search_strategy.current = min_val
    
    if feedback is None:  # First guess
        # Reset for a new game
        linear_search_strategy.current = min_val
        return linear_search_strategy.current
    
    guess, result = feedback
    if result == "low":
        linear_search_strategy.current = guess + 1
    # If too high, we stick with our current value (shouldn't happen in proper linear search)
    
    return linear_search_strategy.current

def random_search_strategy(min_val, max_val, feedback=None):
    """
    Implements random search strategy for the number guessing game.
    Makes random guesses, avoiding previously guessed numbers.
    """
    # Initialize static variables if first run
    if not hasattr(random_search_strategy, 'tried_values'):
        random_search_strategy.tried_values = set()
        random_search_strategy.current_min = min_val
        random_search_strategy.current_max = max_val
    
    if feedback is None:  # First guess
        # Reset for a new game
        random_search_strategy.tried_values = set()
        random_search_strategy.current_min = min_val
        random_search_strategy.current_max = max_val
        guess = random.randint(min_val, max_val)
        random_search_strategy.tried_values.add(guess)
        return guess
    
    guess, result = feedback
    # Update our range based on feedback
    if result == "low":
        random_search_strategy.current_min = guess + 1
    elif result == "high":
        random_search_strategy.current_max = guess - 1
    
    # Find an untried value in the range
    valid_options = [n for n in range(random_search_strategy.current_min, 
                                     random_search_strategy.current_max + 1) 
                   if n not in random_search_strategy.tried_values]
    
    if not valid_options:
        # If we've somehow tried all values or have an invalid range, reset
        random_search_strategy.tried_values = set()
        if random_search_strategy.current_min <= random_search_strategy.current_max:
            guess = random.randint(random_search_strategy.current_min, 
                                 random_search_strategy.current_max)
        else:
            # Fallback if min > max (shouldn't happen)
            guess = min_val
    else:
        guess = random.choice(valid_options)
    
    random_search_strategy.tried_values.add(guess)
    return guess

def manual_strategy(min_val, max_val, feedback=None):
    """
    Allows the user to manually guess numbers.
    """
    while True:
        try:
            guess_str = input("Enter your guess (1-100): ")
            if not guess_str:  # Handle empty input
                print("Please enter a number.")
                continue
            guess = int(guess_str)
            
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
                continue
            
            return guess
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def play_number_guessing_game(strategy_func=manual_strategy, min_val=1, max_val=100, 
                             show_secret=False, delay=0.5):
    """
    Plays a number guessing game using the specified strategy.
    
    Args:
        strategy_func: Function that implements a guessing strategy
        min_val: Minimum value for the secret number
        max_val: Maximum value for the secret number
        show_secret: Whether to show the secret number at the start
        delay: Time delay between guesses (for automated strategies)
        
    Returns:
        dict: Statistics about the game (attempts, success, etc.)
    """
    secret_number = random.randint(min_val, max_val)
    attempts = 0
    feedback = None
    strategy_name = strategy_func.__name__.replace('_strategy', '').replace('_', ' ')
    
    print(f"\nStarting new game with {strategy_name} strategy!")
    print(f"I'm thinking of a number between {min_val} and {max_val}.")
    
    if show_secret:
        print(f"[SECRET: The number is {secret_number}]")
    
    start_time = time.time()
    
    while True:
        try:
            guess = strategy_func(min_val, max_val, feedback)
            attempts += 1
            
            if guess < min_val or guess > max_val:
                print(f"Invalid guess {guess} outside range ({min_val}-{max_val}). Adjusting...")
                guess = max(min_val, min(guess, max_val))
            
            print(f"Guess #{attempts}: {guess}")
            
            if strategy_func != manual_strategy:
                time.sleep(delay)  # Add delay for automated strategies
            
            if guess < secret_number:
                print("Too low!")
                feedback = (guess, "low")
            elif guess > secret_number:
                print("Too high!")
                feedback = (guess, "high")
            else:
                elapsed_time = time.time() - start_time
                print(f"Correct! The number was {secret_number}.")
                print(f"It took {attempts} attempts and {elapsed_time:.2f} seconds.")
                return {
                    "strategy": strategy_name,
                    "attempts": attempts,
                    "success": True,
                    "time": elapsed_time,
                    "range_size": max_val - min_val + 1
                }
                
            # Theoretical check for impossible situation
            if min_val > max_val:
                print("Something went wrong! The range is impossible.")
                return {
                    "strategy": strategy_name,
                    "attempts": attempts,
                    "success": False,
                    "time": time.time() - start_time,
                    "range_size": max_val - min_val + 1
                }
                
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {
                "strategy": strategy_name,
                "attempts": attempts,
                "success": False,
                "time": time.time() - start_time,
                "range_size": max_val - min_val + 1
            }

def display_menu():
    """Displays the main menu for the game."""
    print("\n" + "="*50)
    print("NUMBER GUESSING GAME - STRATEGY ANALYZER")
    print("="*50)
    print("Select an option:")
    print("1. Play manually")
    print("2. Watch binary search strategy")
    print("3. Watch linear search strategy")
    print("4. Watch random search strategy")
    print("5. Compare all strategies")
    print("6. Exit")
    print("="*50)

def compare_strategies(num_games=5, min_val=1, max_val=100):
    """Compares the performance of different strategies over multiple games."""
    strategies = [
        binary_search_strategy,
        linear_search_strategy,
        random_search_strategy
    ]
    
    results = {s.__name__.replace('_strategy', '').replace('_', ' '): {
        'total_attempts': 0,
        'games_played': 0,
        'successful_games': 0,
        'min_attempts': float('inf'),
        'max_attempts': 0,
        'total_time': 0
    } for s in strategies}
    
    for strategy in strategies:
        print(f"\nTesting {strategy.__name__.replace('_strategy', '').replace('_', ' ')} strategy over {num_games} games...")
        
        for game in range(1, num_games + 1):
            print(f"\nGame {game}/{num_games}")
            stats = play_number_guessing_game(strategy, min_val, max_val, delay=0.1)
            
            strategy_name = stats['strategy']
            results[strategy_name]['total_attempts'] += stats['attempts']
            results[strategy_name]['games_played'] += 1
            results[strategy_name]['total_time'] += stats['time']
            
            if stats['success']:
                results[strategy_name]['successful_games'] += 1
                results[strategy_name]['min_attempts'] = min(
                    results[strategy_name]['min_attempts'], 
                    stats['attempts']
                )
                results[strategy_name]['max_attempts'] = max(
                    results[strategy_name]['max_attempts'], 
                    stats['attempts']
                )
    
    # Print summary
    print("\n" + "="*60)
    print("STRATEGY COMPARISON RESULTS")
    print("="*60)
    print(f"{'Strategy':<15} | {'Avg Attempts':<12} | {'Success Rate':<12} | {'Min':<5} | {'Max':<5} | {'Avg Time':<8}")
    print("-"*60)
    
    for strategy, data in results.items():
        if data['games_played'] > 0:
            avg_attempts = data['total_attempts'] / data['games_played']
            success_rate = (data['successful_games'] / data['games_played']) * 100
            avg_time = data['total_time'] / data['games_played']
            
            min_attempts = data['min_attempts'] if data['min_attempts'] != float('inf') else 'N/A'
            max_attempts = data['max_attempts'] if data['successful_games'] > 0 else 'N/A'
            
            print(f"{strategy:<15} | {avg_attempts:<12.2f} | {success_rate:<11.1f}% | {min_attempts!s:<5} | {max_attempts!s:<5} | {avg_time:<8.2f}s")
    
    return results

def main():
    """Main function to run the number guessing game with various strategies."""
    stats = []
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            stats.append(play_number_guessing_game(manual_strategy))
        elif choice == '2':
            stats.append(play_number_guessing_game(binary_search_strategy))
        elif choice == '3':
            stats.append(play_number_guessing_game(linear_search_strategy))
        elif choice == '4':
            stats.append(play_number_guessing_game(random_search_strategy))
        elif choice == '5':
            compare_strategies()
        elif choice == '6':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()