import tkinter as tk
from tkinter import messagebox
import random

def simulate_match(team1, team2, overs):
    def play_innings(team_name, overs):
        score = 0
        wickets = 0
        runs_per_ball = [0, 1, 2, 3, 4, 5, 6]
        while overs > 0 and wickets < 10:
            for _ in range(6):
                if wickets == 10:
                    break

                if random.randint(1, 100) <= 8:
                    wickets += 1
                else:
                    score += random.choice(runs_per_ball)
                
            overs -= 1
        return score, wickets
    
    team1_score, team1_wkts = play_innings(team1, overs)
    team2_score, team2_wkts = play_innings(team2, overs)

    if team1_score > team2_score:
        winner = team1
    elif team2_score > team1_score:
        winner = team2
    else:
        winner = "Tie"

    return {
        "team1_score": team1_score,
        "team2_score": team2_score,
        "team1_wickets": team1_wkts,
        "team2_wickets": team2_wkts,
        "winner": winner
    }

root = tk.Tk()
root.title("Cricket Match Simulator")
root.geometry("400x400")
root.resizable(False, False)

title_label = tk.Label(root,
                       text="Cricket Match Simulator",
                       font=("Arial", 14, "bold")
                       )
title_label.pack(pady=10)

team1_frame = tk.Frame(root)
team1_frame.pack(pady=5)
tk.Label(team1_frame, text="Team 1 Name:").grid(row=0, column=0, padx=5, pady=2)
team1_name = tk.Entry(team1_frame)
team1_name.grid(row=0, column=1, padx=5, pady=2)
tk.Label(team1_frame, text="Captain:").grid(row=1, column=0, padx=5, pady=2)
team1_captain = tk.Entry(team1_frame)
team1_captain.grid(row=1, column=1, padx=5, pady=2)

team2_frame = tk.Frame(root)
team2_frame.pack(pady=5)
tk.Label(team2_frame, text="Team 2 Name:").grid(row=0, column=0, padx=5, pady=2)
team2_name = tk.Entry(team2_frame)
team2_name.grid(row=0, column=1, padx=5, pady=2)
tk.Label(team2_frame, text="Captain:").grid(row=1, column=0, padx=5, pady=2)
team2_captain = tk.Entry(team2_frame)
team2_captain.grid(row=1, column=1, padx=5, pady=2)

overs_label = tk.Label(root, text="Select Overs:", font=("Arial", 12))
overs_label.pack(pady=10)

overs_var = tk.StringVar(value="10")
overs_frame = tk.Frame(root)
overs_frame.pack()
for over in [10, 20, 50]:
    tk.Radiobutton(overs_frame, text=f"{over} Overs", variable=overs_var, value=str(over)).pack(side=tk.LEFT, padx=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

def exit_app():
    root.destroy()

exit_button = tk.Button(buttons_frame, text="Exit", command=exit_app, width=10, bg="red", fg="white")
exit_button.grid(row=0, column=0, padx=10)

def start_simulation():
    t1 = team1_name.get()
    t2 = team2_name.get()
    overs = int(overs_var.get())

    if not t1 or not t2:
        messagebox.showerror("Input error", "Please enter both team names!")
        return
    
    result = simulate_match(t1, t2, overs)

    message = (
        f"{t1}: {result['team1_score']}/{result['team1_wickets']}\n"
        f"{t2}: {result['team2_score']}/{result['team2_wickets']}\n\n"
        f"Winner: {result['winner']}"
    )

    messagebox.showinfo("Match Result", message)

start_button = tk.Button(buttons_frame, text="Start SImulation", command=start_simulation, width=15, bg="green", fg="white")
start_button.grid(row=0, column=1, padx=10)

root.mainloop()