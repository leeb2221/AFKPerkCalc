import random
import numpy as np
import matplotlib.pyplot as plt

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
    # Name,       Type, Amount, Priority, Misc, First Pick Perk
    # Type Key: 0=Banned, 1=Auto, 2=Neither (just a normal perk)
    # Priority Key: Highest number is higher priority
    # Misc Key: 
    #   1 = Avoid tracker
    #   2 = Perks to max tracker, outputs round you got all perks to max
    #   3 = Track last round of perk wave requirement
    # First Pick Key: 1 for first pick, if none the 0 for all.
    bag = [
        ("Max Health",          1, 5, 8, 2, 0, 1), 
        ("Damage",              2, 5, 0, 0, 0, 1), 
        ("Coins",               1, 5, 6, 2, 0, 1), 
        ("Defense Abso",        2, 5, 0, 0, 0, 1), 
        ("Cash",                2, 5, 0, 0, 0, 1), 
        ("Health Reg",          2, 5, 0, 0, 0, 1), 
        ("Interest",            2, 5, 0, 0, 0, 1), 
        ("Land Mine Dam",       2, 5, 0, 0, 0, 1), 
        ("Free Upgrades",       1, 5, 5, 2, 0, 1), 
        ("Defense Percent",     1, 5, 7, 2, 0, 1), 
        ("Bounce Shot",         2, 3, 0, 0, 0, 1), 
        ("Perk Wave Requ",      1, 3, 9, 3, 1, 1), 
        ("Orbs",                1, 2, 1, 2, 0, 1), 
        ("Random Ult",          1, 2, 4, 2, 0, 1), 
        ("Game Speed",          2, 1, 0, 0, 0, 1), 
        ("Smart Missile",   0, 1, 0, 0, 0, 2), 
        ("Swamp",           0, 1, 0, 0, 0, 2), 
        ("Death Wave",      0, 1, 0, 0, 0, 2), 
        ("Inner Mine",      2, 1, 0, 0, 0, 2), 
        ("Gold Tower",      1, 1, 2, 2, 0, 2), 
        ("Chain Light",     2, 1, 0, 0, 0, 2), 
        ("Chrono",          0, 1, 0, 0, 0, 2), 
        ("Black Hole",      2, 1, 0, 0, 0, 2),
        ("Spot Light",      2, 1, 0, 0, 0, 2),  
        ("Tow Dam / Boss Hp",       2, 1, 0, 0, 0, 3), 
        ("Coin / Hp",               2, 1, 0, 0, 0, 3), 
        ("Eme Hp / Tow Reg",        2, 1, 0, 0, 0, 3), 
        ("Eme Dam / Tow Dam",       1, 1, 3, 2, 0, 3),
        ("Ranged / Rang Dam",       2, 1, 0, 0, 0, 3),
        ("Eme Sped / Eme Dam",      0, 1, 0, 1, 0, 3), 
        ("Cash Wave / Cash Kill",   2, 1, 0, 0, 0, 3), 
        ("Tow Reg / Tow Hp",        0, 1, 0, 1, 0, 3), 
        ("Boss Hp / Boss Sped",     2, 1, 0, 0, 0, 3), 
        ("Life Steal / Knockback",  2, 1, 0, 1, 0, 3)
    ]
    
    Num_Options = 4

    round_number = 1
    last_round_max = None
    rounds_with_PWR = []
    rounds_with_avoid_perks = []

    while bag:
        
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

        # Track rounds where avoid perks (Misc=1) were selected
        if selected_perk[4] == 1:
            rounds_with_avoid_perks.append(round_number)
        
        # Track last round for Misc=2 and Misc=3
        if selected_perk[4] == 2 or selected_perk[4] == 3:
            last_round_max = round_number
        if selected_perk[4] == 3:
            rounds_with_PWR.append(round_number)
        
        # Subtract 1 from health
        updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5], selected_perk[6])
        if selected_perk[0] == "Random Ult":
            updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5], 2)

        # Remove or update the selected perk in the bag
        bag = [perk for perk in bag if perk != selected_perk]
        if updated_perk[2] > 0:
            bag.append(updated_perk)
        round_number += 1

    if not rounds_with_avoid_perks:
        rounds_with_avoid_perks.append(round_number)
    
    return last_round_max, max(rounds_with_PWR), min(rounds_with_avoid_perks)

def run_simulation(num_games):
    total_last_round_max = 0
    total_PWR_rounds = 0
    total_avoid_perk_rounds = 0

    std_max = []
    std_PWR = []
    std_avoid = []

    for _ in range(num_games):
        last_round_max, last_round_PWR, first_round_avoid = play_game()
        if last_round_max is not None:
            std_max.append(last_round_max)
            total_last_round_max += last_round_max
        if last_round_PWR is not None:
            std_PWR.append(last_round_PWR)
            total_PWR_rounds += last_round_PWR
        if first_round_avoid is not None:
            std_avoid.append(first_round_avoid)
            total_avoid_perk_rounds += first_round_avoid
        


    avg_last_round_max = total_last_round_max / num_games
    avg_last_round_PWR = total_PWR_rounds / num_games
    avg_fist_round_avoid = total_avoid_perk_rounds / num_games

    std_max_out = np.std(std_max)
    std_PWR_out = np.std(std_PWR)
    std_avoid_out = np.std(std_avoid)

    return avg_last_round_max, avg_last_round_PWR, avg_fist_round_avoid, std_max_out, std_PWR_out, std_avoid_out, std_max, std_PWR, std_avoid

if __name__ == "__main__":
    num_games = 100000
    avg_last_round_max, avg_PWR_rounds, avg_avoid_perk_rounds, std_max, std_PWR, std_avoid, max_data, PWR_data, avoid_data = run_simulation(num_games)
    print(f"\nAverage,std last round a perk to max was selected: {avg_last_round_max}, {std_max}")
    print(f"Average,std last round PWR was selected:             {avg_PWR_rounds}, {std_PWR}")
    print(f"Average,std first round perks to avoid was selected: {avg_avoid_perk_rounds}, {std_avoid}\n")

    bin_edge = np.arange(80)

    figure , axis = plt.subplots(3,1)

    axis[0].hist(max_data,bins=bin_edge)
    axis[0].set_xticks(np.arange(0, 90, 2))
    axis[0].set_title("Round when you max all wanted perks Dist")
    axis[1].hist(PWR_data,bins=bin_edge)
    axis[1].set_xticks(np.arange(0, 90, 2))
    axis[1].set_title("Round when you get all 3 PWR Dist")
    axis[2].hist(avoid_data,bins=bin_edge)
    axis[2].set_xticks(np.arange(0, 90, 2))
    axis[2].set_title("Round when you first hit a perk you want to avoid Dist")

    figure.tight_layout(pad=1.1)
    plt.show()
