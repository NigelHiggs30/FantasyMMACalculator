class FantasyPointsCalculator:
    def __init__(self, *args) -> None:
        (
            self.fight_results_dic, 
            self.fighter_1_name, 
            self.fighter_2_name, 
            self.fight_method, 
            self.fight_round, 
            self.fight_time, 
            self.fight_format
        ) = args

    def calculate_points(self, *args) -> tuple:
        # Example logic to calculate points using args
        (
            strikes_fighter1, strikes_fighter2,
            significant_strikes_fighter1, significant_strikes_fighter2,
            control_time_fighter1, control_time_fighter2,
            takedown_fighter1, takedown_fighter2,
            reversal_sweep_fighter1, reversal_sweep_fighter2,
            knockdown_fighter1, knockdown_fighter2
        ) = args

        # Same calculation logic as before
        fighter_1_score = (
            int(strikes_fighter1) * 0.2 +
            int(significant_strikes_fighter1) * 0.2 +
            int(control_time_fighter1) * 0.03 +
            int(takedown_fighter1) * 5 +
            int(reversal_sweep_fighter1) * 5 +
            int(knockdown_fighter1) * 10
        )

        fighter_2_score = (
            int(strikes_fighter2) * 0.2 +
            int(significant_strikes_fighter2) * 0.2 +
            int(control_time_fighter2) * 0.03 +
            int(takedown_fighter2) * 5 +
            int(reversal_sweep_fighter2) * 5 +
            int(knockdown_fighter2) * 10
        )

        # print(fighter_1_score, fighter_2_score)
        return fighter_1_score, fighter_2_score
    
    def calculate_fantasy_points_with_bonus(self) -> tuple:

        pass
        # # Determine the winner
        # winner = None
        # if fight_results_dic[fighter_1_name] == "W":
        #     winner = fighter_1_name
        # elif fight_results_dic[fighter_2_name] == "W":
        #     winner = fighter_2_name
