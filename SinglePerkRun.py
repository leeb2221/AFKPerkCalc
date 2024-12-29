import random

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
    # Name, Type, Amount, Priority, Misc, First Perk Selected
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
        ("Perk Wave Requ",      1, 3, 9, 3, 0, 1), 
        ("Orbs",                1, 2, 1, 2, 0, 1), 
        ("Random Ult",          1, 2, 4, 2, 1, 1), 
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
    last_round_misc_2 = None
    rounds_with_PWR = []
    rounds_with_avoid_perks = []

    while bag:
        print(f"Round {round_number}:")
        
        # Draw perks
        drawn_perks = draw_perks(bag, round_number, Num_Options)
        if not drawn_perks:
            print("No valid perks to draw. Game over!")
            break
        
        print(f"Drawn perks: {[perk[0] for perk in drawn_perks]}")
        
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
        
        print(f"Selected perk: {selected_perk[0]} (Health Points: {selected_perk[2]-1}, Priority: {selected_perk[3]})")

        # Track rounds where avoid perks (Misc=1) were selected
        if selected_perk[4] == 1:
            rounds_with_avoid_perks.append(round_number)
        
        # Track last round for Misc=2 and Misc=3
        if selected_perk[4] == 2:
            last_round_misc_2 = round_number
        elif selected_perk[4] == 3:
            rounds_with_PWR.append(round_number)
        
        # Subtract 1 from health
        updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5], selected_perk[6])
        if selected_perk[0] == "Random Ult":
            updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5], 2)

        # Remove or update the selected perk in the bag
        bag = [perk for perk in bag if perk != selected_perk]
        if updated_perk[2] > 0:
            bag.append(updated_perk)
        
        print("\n")
        round_number += 1
    
    print("Game over! No perks left in the bag.")
    print(f"Last round a perk to max was selected:     {last_round_misc_2}")
    print(f"Rounds where PWR was selected:             {rounds_with_PWR}")
    print(f"Rounds where a perk to avoid was selected: {rounds_with_avoid_perks}\n")

if __name__ == "__main__":
    play_game()
