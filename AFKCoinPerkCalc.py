import random
import numpy as np
import matplotlib.pyplot as plt

def PWR_Wave(PWR, R, ban, x):
    """
    Calculate the value based on the piecewise mathematical expressions
    for the given values of PWR, R, ban, and x.
    """
    if 0 <= x < 21:
        return np.floor((200 - PWR) * (1 - R)) * np.floor(x)
    
    elif 21 <= x < 31:
        return (
            np.floor((250 - PWR) * (1 - R)) * np.floor(x)
            - (
                -np.floor((250 - PWR) * (1 - R))
                + np.floor((250 - PWR) * (1 - R)) * np.floor(21)
                - np.floor((200 - PWR) * (1 - R)) * np.floor(20)
            )
        )
    
    elif 31 <= x < 41:
        return (
        np.floor((300 - PWR) * (1 - R)) * np.floor(x)
        - (
            np.floor((300 - PWR) * (1 - R)) * np.floor(31)
            - (
                np.floor((250 - PWR) * (1 - R)) * np.floor(30)
                - (
                    -np.floor((250 - PWR) * (1 - R))
                    + np.floor((250 - PWR) * (1 - R)) * np.floor(21)
                    - np.floor((200 - PWR) * (1 - R)) * np.floor(20)
                )
            )
            - np.floor((300 - PWR) * (1 - R))
        )
    )
    
    elif 41 <= x <= 79 - ban:
        return (
            np.floor((350 - PWR) * (1 - R)) * np.floor(x)
            - (
                np.floor((350 - PWR) * (1 - R)) * np.floor(41)
                - (
                    np.floor((300 - PWR) * (1 - R)) * np.floor(40)
                    - (
                        np.floor((300 - PWR) * (1 - R)) * np.floor(31)
                        - (
                            np.floor((250 - PWR) * (1 - R)) * np.floor(30)
                            - (
                                -np.floor((250 - PWR) * (1 - R))
                                + np.floor((250 - PWR) * (1 - R)) * np.floor(21)
                                - np.floor((200 - PWR) * (1 - R)) * np.floor(20)
                            )
                        )
                    )
                )
                - np.floor((300 - PWR) * (1 - R))
                - np.floor((350 - PWR) * (1 - R))
            )
        )
    
    else:
        return None  # Return None if x doesn't fall within any of the defined ranges

def weighted_draw(bag, num_draws):
    if not bag:
        return []  # Return an empty list if the bag is empty

    # Define base weights for the perk categories
    base_weights = {1: 65, 2: 20, 3: 15}
    
    # Check if perks with specific seventh values exist
    counts = {key: sum(1 for perk in bag if perk[6] == key) for key in base_weights}
    
    # Active categories
    active_keys = [key for key, count in counts.items() if count > 0]

    # Adjust weights if some categories are missing
    adjusted_weights = base_weights.copy()
    for key in base_weights:
        if key not in active_keys:
            # Add this category's weight to the lowest numeric key among active categories
            lowest_key = min(active_keys)
            adjusted_weights[lowest_key] += base_weights[key]
            adjusted_weights[key] = 0

    # Assign weights to each perk in the bag
    weights = [adjusted_weights.get(perk[6], 0) for perk in bag]
    
    # Check if weights are valid (non-zero sum)
    total_weight = sum(weights)
    if total_weight == 0:
        return []  # Return an empty list if all weights are zero

    # Normalize weights to ensure the sum equals 1 for random.choices
    normalized_weights = [w / total_weight for w in weights]
    # print(normalized_weights)

    # Use random.choices to select `num_draws` unique perks
    selected_perks = []
    while len(selected_perks) < num_draws:
        perk = random.choices(bag, weights=normalized_weights, k=1)[0]  # Draw one perk at a time
        if perk not in selected_perks:  # Ensure uniqueness
            selected_perks.append(perk)

    return selected_perks


def draw_perks(bag, round_number, num_options):
    if round_number == 1:
        # Force perks with sixth value 1 into the first-round draw
        forced_perks = [perk for perk in bag if perk[5] == 1]
        remaining_perks = [perk for perk in bag if perk not in forced_perks and perk[1] in [1, 2]]
        return weighted_draw(forced_perks, min(num_options, len(forced_perks))) + \
               weighted_draw(remaining_perks, min(num_options - len(forced_perks), len(remaining_perks)))
    else:
        # Normal draw
        filtered_bag = [perk for perk in bag if perk[1] in [1, 2]]
        return weighted_draw(filtered_bag, min(num_options, len(filtered_bag)))

def play_game():

    Num_Options = 4 # How many perk options you get during a pick

    Max_wave = 1810 # Max wave you expect in run
    PWR = 3  # Perk Wave Reduction Lab
    SPB = 9  # Standard Perk Bonus in %
    ban = 2  # How many bans

    # Name,       Type, Amount, Priority, Misc, First Pick Perk, Rarity, coin tracker
    # Type Key: 0=Banned, 1=Auto, 2=Neither (just a normal perk)
    # Priority Key: Highest number is higher priority
    # Misc Key: 
    #   1 = Avoid tracker
    #   2 = Perks to max tracker, outputs round you got all perks to max
    #   3 = Track last round of perk wave requirement
    # First Pick Key: 1 for first pick, if none the 0 for all.
    # Rarity key: 1 standard, 2 ults, 3 trade offs
    # Coin bounus tracker 1 if it boosts coin, 0 if not
    bag = [
        ("Max Health",          1, 5, 5, 0, 0, 1, 0), 
        ("Damage",              2, 5, 0, 0, 0, 1, 0), 
        ("Coins",               1, 5, 8, 0, 0, 1, 1), 
        ("Defense Abso",        2, 5, 0, 0, 0, 1, 0), 
        ("Cash",                2, 5, 0, 0, 0, 1, 0), 
        ("Health Reg",          2, 5, 0, 0, 0, 1, 0), 
        ("Interest",            2, 5, 0, 0, 0, 1, 0), 
        ("Land Mine Dam",       2, 5, 0, 0, 0, 1, 0), 
        ("Free Upgrades",       1, 5, 4, 0, 0, 1, 0), 
        ("Defense Percent",     1, 5, 3, 0, 0, 1, 0), 
        ("Bounce Shot",         2, 3, 0, 0, 0, 1, 0), 
        ("Perk Wave Requ",      1, 3, 9, 3, 1, 1, 0), 
        ("Orbs",                2, 2, 0, 0, 0, 1, 0), 
        ("Random Ult",          1, 2, 1, 0, 0, 1, 0), 
        ("Game Speed",          1, 1, 2, 0, 0, 1, 0), 
        ("Smart Missile",   0, 1, 0, 0, 0, 2, 0), 
        ("Swamp",           0, 1, 0, 0, 0, 2, 0), 
        ("Death Wave",      0, 1, 0, 0, 0, 2, 0), 
        ("Inner Mine",      2, 1, 0, 0, 0, 2, 0), 
        ("Gold Tower",      1, 1, 7, 0, 0, 2, 2), 
        ("Chain Light",     2, 1, 0, 0, 0, 2, 0), 
        ("Chrono",          0, 1, 0, 0, 0, 2, 0), 
        ("Black Hole",      2, 1, 0, 0, 0, 2, 0),
        ("Spot Light",      2, 1, 0, 0, 0, 2, 0),  
        ("Tow Dam / Boss Hp",       2, 1, 0, 0, 0, 3, 0), 
        ("Coin / Hp",               2, 1, 0, 0, 0, 3, 3), 
        ("Eme Hp / Tow Reg",        2, 1, 0, 0, 0, 3, 0), 
        ("Eme Dam / Tow Dam",       1, 1, 6, 0, 0, 3, 0),
        ("Ranged / Rang Dam",       2, 1, 0, 0, 0, 3, 0),
        ("Eme Sped / Eme Dam",      0, 1, 0, 0, 0, 3, 0), 
        ("Cash Wave / Cash Kill",   2, 1, 0, 0, 0, 3, 0), 
        ("Tow Reg / Tow Hp",        0, 1, 0, 0, 0, 3, 0), 
        ("Boss Hp / Boss Sped",     2, 1, 0, 0, 0, 3, 0), 
        ("Life Steal / Knockback",  2, 1, 0, 0, 0, 3, 0)
    ]

    round_number = 1
    rounds_with_PWR = []
    rounds_with_coins = []
    round_with_GT = 0
    round_with_CTO = 0
    drop_wave = 0

    while bag:

        if len(rounds_with_PWR) == 0:
            R = 0
            wave = PWR_Wave(PWR, R, ban, round_number)
        elif len(rounds_with_PWR) == 1:
            R = 0.2*1*(1+SPB/100)
            wave = PWR_Wave(PWR, R, ban, round_number)
        elif len(rounds_with_PWR) == 2:
            R = 0.2*2*(1+SPB/100)
            wave = PWR_Wave(PWR, R, ban, round_number)
        elif len(rounds_with_PWR) == 3:
            R = 0.2*3*(1+SPB/100)
            wave = PWR_Wave(PWR, R, ban, round_number)
  


        if wave > Max_wave:
            if [perk for perk in bag if perk[4] == 2]:
                last_round_max = None
            if not rounds_with_PWR:
                rounds_with_PWR.append(None)
            wave = drop_wave
            break

        drop_wave = wave
        
        # Draw perks
        drawn_perks = draw_perks(bag, round_number, Num_Options)
        if not drawn_perks:
            break
        
        
        # First-round special selection
        if round_number == 1:
            if all(perk[3] == 0 for perk in drawn_perks):  # Check if all priorities are 0
                selected_perk = next((perk for perk in drawn_perks if perk[5] == 1), random.choice(drawn_perks))
            else:
                perks_with_priority = [perk for perk in drawn_perks if perk[3] > 0]
                selected_perk = max(perks_with_priority, key=lambda m: m[3]) if perks_with_priority else random.choice(drawn_perks)
        else:
            # Normal selection rules
            perks_with_1 = [m for m in drawn_perks if m[1] == 1]
            if perks_with_1:
                selected_perk = max(perks_with_1, key=lambda m: m[3])
            else:
                selected_perk = random.choice(drawn_perks)
        
        if selected_perk[4] == 3:
            rounds_with_PWR.append(round_number)
        if selected_perk[7] == 1:
            rounds_with_coins.append(wave)
        if selected_perk[7] == 2:
            round_with_GT = wave
        if selected_perk[7] == 3:
            round_with_CTO = wave
        
        # Subtract 1 from health
        updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5], selected_perk[6], selected_perk[7])
        if selected_perk[0] == "Random Ult":
            updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5], 2, selected_perk[7])

        # Remove or update the selected perk in the bag
        bag = [perk for perk in bag if perk != selected_perk]
        if updated_perk[2] > 0:
            bag.append(updated_perk)
        round_number += 1

    if len(rounds_with_coins) != 5:
        # Extend the list with zeros to make its length 5
        rounds_with_coins.extend([0] * (5 - len(rounds_with_coins)))

    
    return round_with_GT, round_with_CTO, rounds_with_coins, Max_wave

import numpy as np

import numpy as np

def run_simulation(num_games):
    round_GT_data = []
    round_CTO_data = []
    round_coins_data = []  # Collect rounds when coins are selected

    for _ in range(num_games):
        round_with_GT, round_with_CTO, rounds_with_coins, max_wave = play_game()
        if round_with_GT is not None:
            round_GT_data.append(round_with_GT)
        if round_with_CTO is not None:
            round_CTO_data.append(round_with_CTO)
        if rounds_with_coins is not None:
            round_coins_data.append(rounds_with_coins)

    # Convert to numpy array for element-wise operations
    round_coins_data = np.array(round_coins_data)

    # Mask zeros in round_coins_data for averaging
    coin_mask = round_coins_data != 0
    avg_coin_rounds = np.sum(round_coins_data * coin_mask, axis=0) / np.sum(coin_mask, axis=0)

    # Convert to numpy arrays for GT and CTO data
    round_GT_data = np.array(round_GT_data)
    round_CTO_data = np.array(round_CTO_data)

    # Mask zeros in round_GT_data and round_CTO_data for averaging
    gt_mask = round_GT_data != 0
    cto_mask = round_CTO_data != 0

    avg_GT_wave = np.sum(round_GT_data * gt_mask) / np.sum(gt_mask)
    avg_CTO_wave = np.sum(round_CTO_data * cto_mask) / np.sum(cto_mask)

    return avg_GT_wave, avg_CTO_wave, avg_coin_rounds, round_GT_data, round_CTO_data, round_coins_data, max_wave



if __name__ == "__main__":
    num_games = 100000
    avg_GT_wave, avg_CTO_wave, avg_coin_rounds, round_GT_data, round_CTO_data, round_coins_data, max_wave = run_simulation(num_games)
    print(f"\nAssuming max wave:  {max_wave}")
    print(f"Simulating {num_games} games\n")

    print(f"Average wave for Gold Tower:     {avg_GT_wave:.1f}")
    print(f"Average wave for Coin Trade off: {avg_CTO_wave:.1f}")
    print(f"Average waves for coin perks:")
    print(f"    Rank 1: {avg_coin_rounds[0]:.1f}")
    print(f"    Rank 2: {avg_coin_rounds[1]:.1f}")
    print(f"    Rank 3: {avg_coin_rounds[2]:.1f}")
    print(f"    Rank 4: {avg_coin_rounds[3]:.1f}")
    print(f"    Rank 5: {avg_coin_rounds[4]:.1f}\n")


    # Calculate the percentage of non-zero entries for GT
    non_zero_GT_count = np.count_nonzero(round_GT_data)  # Count of non-zero elements
    total_count_GT = round_GT_data.size                 # Total number of elements
    percentage_non_GT_zero = (non_zero_GT_count / total_count_GT) * 100
    # Calculate the percentage of non-zero entries for CTO
    non_zero_CTO_count = np.count_nonzero(round_CTO_data)  # Count of non-zero elements
    total_count_CTO = round_CTO_data.size                 # Total number of elements
    percentage_non_CTO_zero = (non_zero_CTO_count / total_count_CTO) * 100 
    # Calculate the percentage of non-zero entries for each coin perk rank
    non_zero_coin_counts = np.count_nonzero(round_coins_data, axis=0)  # Count of non-zero elements in each column
    total_counts_coin = round_coins_data.shape[0]                     # Total number of rows
    percentage_non_coin_zero = (non_zero_coin_counts / total_counts_coin) * 100

    print(f"Percentage of time got Golden Tower Perk: {percentage_non_GT_zero:.2f}%")
    print(f"Percentage of time got Coin T/O Perk:     {percentage_non_CTO_zero:.2f}%")
    print(f"Percentage of time got Coin Perk:")
    print(f"    Rank 1: {percentage_non_coin_zero[0]:.2f}%")
    print(f"    Rank 2: {percentage_non_coin_zero[1]:.2f}%")
    print(f"    Rank 3: {percentage_non_coin_zero[2]:.2f}%")
    print(f"    Rank 4: {percentage_non_coin_zero[3]:.2f}%")
    print(f"    Rank 5: {percentage_non_coin_zero[4]:.2f}%\n")


