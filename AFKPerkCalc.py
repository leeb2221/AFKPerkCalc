import random
import numpy as np

def draw_perks(bag, round_number):
    if round_number == 1:
        # Force perks with sixth value 1 into the first-round draw
        forced_perks = [perk for perk in bag if perk[5] == 1]
        remaining_perks = [perk for perk in bag if perk not in forced_perks and perk[1] in [1, 2]]
        return random.sample(forced_perks, min(4, len(forced_perks))) + \
               random.sample(remaining_perks, min(4 - len(forced_perks), len(remaining_perks)))
    else:
        # Normal draw
        filtered_bag = [perk for perk in bag if perk[1] in [1, 2]]
        return random.sample(filtered_bag, min(4, len(filtered_bag)))

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
        ("Max Health",      1, 5, 8, 2, 0), 
        ("Damage",          2, 5, 0, 0, 0), 
        ("Coins",           1, 5, 7, 2, 0), 
        ("Defense Abso",    2, 5, 0, 0, 0), 
        ("Cash",            2, 5, 0, 0, 0), 
        ("Health Reg",      2, 5, 0, 0, 0), 
        ("Interest",        2, 5, 0, 0, 0), 
        ("Land Mine Dam",   2, 5, 0, 0, 0), 
        ("Free Upgrades",   1, 5, 6, 2, 0), 
        ("Defense Percent", 1, 5, 5, 2, 0), 
        ("Bounce Shot",     2, 3, 0, 0, 0), 
        ("Perk Wave Requ",  1, 3, 9, 3, 1), 
        ("Orbs",            2, 2, 0, 0, 0), 
        ("Random Ult",      2, 2, 0, 0, 0), 
        ("Game Speed",      1, 1, 4, 2, 0), 
        ("Smart Missile",   0, 1, 0, 0, 0), 
        ("Swamp",           0, 1, 0, 0, 0), 
        ("Death Wave",      0, 1, 0, 0, 0), 
        ("Inner Mine",      2, 1, 0, 0, 0), 
        ("Gold Tower",      1, 1, 3, 2, 0), 
        ("Chain Light",     2, 1, 0, 0, 0), 
        ("Chrono",          0, 1, 0, 0, 0), 
        ("Black Hole",      1, 1, 2, 2, 0),
        ("Spot Light",      2, 1, 0, 0, 0),  
        ("Tow Dam / Boss Hp",       2, 1, 0, 1, 0), 
        ("Coin / Hp",               2, 1, 0, 0, 0), 
        ("Eme Hp / Tow Reg",        2, 1, 0, 0, 0), 
        ("Eme Dam / Tow Dam",       1, 1, 1, 2, 0),
        ("Ranged / Rang Dam",       2, 1, 0, 1, 0),
        ("Eme Sped / Eme Dam",      0, 1, 0, 1, 0), 
        ("Cash Wave / Cash Kill",   2, 1, 0, 0, 0), 
        ("Tow Reg / Tow Hp",        0, 1, 0, 1, 0), 
        ("Boss Hp / Boss Sped",     2, 1, 0, 0, 0), 
        ("Life Steal / Knockback",  2, 1, 0, 1, 0)
    ]
    
    round_number = 1
    last_round_max = None
    rounds_with_PWR = []
    rounds_with_avoid_perks = []

    while bag:
        
        # Draw perks
        drawn_perks = draw_perks(bag, round_number)
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
        if selected_perk[4] == 2:
            last_round_max = round_number
        elif selected_perk[4] == 3:
            rounds_with_PWR.append(round_number)
        
        # Subtract 1 from health
        updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5])
        
        # Remove or update the selected perk in the bag
        bag = [perk for perk in bag if perk != selected_perk]
        if updated_perk[2] > 0:
            bag.append(updated_perk)
        round_number += 1

    # if not rounds_with_avoid_perks:
    #     rounds_with_avoid_perks.append(round_number)
    
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

    return avg_last_round_max, avg_last_round_PWR, avg_fist_round_avoid, std_max_out, std_PWR_out, std_avoid_out

if __name__ == "__main__":
    num_games = 10000
    avg_last_round_max, avg_PWR_rounds, avg_avoid_perk_rounds, std_max, std_PWR, std_avoid = run_simulation(num_games)
    print(f"\nAverage,std last round a perk to max was selected: {avg_last_round_max}, {std_max}")
    print(f"Average,std last round PWR was selected:             {avg_PWR_rounds}, {std_PWR}")
    print(f"Average,std first round perks to avoid was selected: {avg_avoid_perk_rounds}, {std_avoid}\n")
