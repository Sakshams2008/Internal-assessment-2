import tkinter as tk
from tkinter import messagebox
import random

def simulate_match(team1, team2, overs):
    def play_innings(team_name, overs):
        score = 0
        wickets = 0
        players = [{"name": f"{team_name}_Player{i+1}", "runs": 0} for i in range(11)]
        current_player = 0
        runs_per_ball = [0, 1, 2, 3, 4, 5, 6]

        while overs > 0 and wickets < 10:
            for _ in range(6):
                if wickets == 10:
                    break
                if random.randint(1, 100) <= 8:
                    wickets += 1
                    current_player += 1
                else:
                    run = random.choice(runs_per_ball)
                    players[current_player]["runs"] += run
            overs -= 1

        top_player = max(players, key=lambda x:x["runs"])
        return score, wickets, top_player
    
    team1_score, team1_wkts, top1 = play_innings(team1, overs)
    team2_score, team2_wkts, top2 = play_innings(team2, overs)

    if team1_score > team2_score:
        winner = team1
    elif team2_score > team1_score:
        winner = team2
    else:
        winner = "Tie"

    overall_top = top1 if top1["runs"] >= top2["runs"] else top2

    rating1 = min(10, team1_score // 30)
    rating2 = min(10, team2_score // 30)

    return {
        "team1_score": team1_score,
        "team2_score": team2_score,
        "team1_wickets": team1_wkts,
        "team2_wickets": team2_wkts,
        "winner": winner,
        "top_scorer": overall_top,
        "rating1": rating1,
        "rating2": rating2
    }

root = tk.Tk()
root.title("Cricket Match Simulator")
root.geometry("480x400")
root.resizable(False, False)

team1_name = ""
team1_captain = ""
team2_name = ""
team2_captain = ""
overs_var = tk.StringVar(value="10")

tk.Label(root, text="Cricket Match Simulator", font=("Arial", 16, "bold")).pack(pady=10)
tk.Label(root, text="Simulate a cricket match with detailed stats.\nEnter team info and start the game!", font=("Arial", 11)).pack(pady=5)

tk.Label(root, text="Select Overs:", font=("Arial", 12)).pack(pady=10)
overs_frame = tk.Frame(root)
overs_frame.pack()
for over in [10, 20, 50]:
    tk.Radiobutton(overs_frame, text=f"{over} Overs", variable=overs_var, value=str(over)).pack(side=tk.LEFT, padx=10)

def open_team1_window():
