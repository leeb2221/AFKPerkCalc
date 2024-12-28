import random

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
    # Name, Type, Amount, Priority, Misc, First Perk Selected
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
    last_round_misc_2 = None
    rounds_with_PWR = []
    rounds_with_avoid_perks = []

    while bag:
        print(f"Round {round_number}:")
        
        # Draw perks
        drawn_perks = draw_perks(bag, round_number)
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
        updated_perk = (selected_perk[0], selected_perk[1], selected_perk[2] - 1, selected_perk[3], selected_perk[4], selected_perk[5])
        
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
