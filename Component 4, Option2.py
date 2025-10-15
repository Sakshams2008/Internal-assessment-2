import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import os
from collections import Counter

RESULTS_FILE = "match_results.txt"

def simulate_match(team1, team2, overs):
    def play_innings(team_name, overs):
        remaining_overs = overs
        score = 0
        wickets = 0
        players = [{"name": f"{team_name}_Player{i+1}", "runs": 0, "wickets": 0} for i in range(11)]
        current_player = 0
        runs_per_ball = [0, 1, 2, 3, 4, 5, 6]

        while remaining_overs > 0 and wickets < 10:
            for _ in range(6):
                if wickets == 10:
                    break
                if random.randint(1, 100) <= 8:
                    wickets += 1
                    current_player += 1
                    bowler = random.choice(players)
                    bowler["wickets"] += 1
                else:
                    run = random.choice(runs_per_ball)
                    players[current_player]["runs"] += run
                    score += run
            remaining_overs -= 1

        top_player = max(players, key=lambda x:x["runs"])
        return score, wickets, top_player, players
    
    team1_score, team1_wkts, top1, players1 = play_innings(team1, overs)
    team2_score, team2_wkts, top2, players2 = play_innings(team2, overs)

    if team1_score > team2_score:
        winner = team1
    elif team2_score > team1_score:
        winner = team2
    else:
        winner = "Tie"

    overall_top = top1 if top1["runs"] >= top2["runs"] else top2

    rating1 = min(10, team1_score // 30)
    rating2 = min(10, team2_score // 30)

    if winner == team1:
        winning_players = players1
    elif winner == team2:
        winning_players = players2
    else:
        winning_players = []
    
    player_of_match = None
    if winning_players:
        player_of_match = max(
            winning_players,
            key=lambda p: p["runs"] + (p["wickets"] * 25)
        )

    return {
        "team1_score": team1_score,
        "team2_score": team2_score,
        "team1_wickets": team1_wkts,
        "team2_wickets": team2_wkts,
        "winner": winner,
        "top_scorer": overall_top,
        "rating1": rating1,
        "rating2": rating2,
        "player_of_match": player_of_match 
    }

def save_match_result(data):
    with open(RESULTS_FILE, "a") as file:
        file.write(data + "\n" + ("-"*40) + "\n")

def view_previous_matches():
    if not os.path.exists(RESULTS_FILE):
        messagebox.showinfo("No Matches", "No previous match found.")
        return
    
    view_win = tk.Toplevel(root)
    view_win.title("Previous Matches")
    view_win.geometry("500x400")

    with open(RESULTS_FILE, "r") as file:
        content = file.read()
    
    text_area = scrolledtext.ScrolledText(view_win, wrap=tk.WORD, width=60, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)

def view_statistics_simple():
    if not os.path.exists(RESULTS_FILE):
        messagebox.showinfo("No Matches", "No match data available for statistics.")
        return
    
    with open(RESULTS_FILE, "r") as file:
        content = file.read().strip()

    if not content:
        messagebox.showinfo("No Matches", "No match data available for statistics.")
        return

    matches = content.split("-" * 40 + "\n")
    matches = [m.strip() for m in matches if m.strip()]

    total_matches = len(matches)
    wins = Counter()
    top_scorers = Counter()
    ties = 0

    for match in matches:
        lines = match.splitlines()
        for line in lines:
            if line.startswith("Winner"):
                winner = line.split("Winner:")[1].strip()
                if winner == "Tie":
                    ties += 1
                else:
                    wins[winner] += 1
            if line.startswith("Top Scorer:"):
                scorer = line.split("Top Scorer:")[1].strip().split("-")[0].strip()
                top_scorers[scorer] += 1
    
    # Show ALL top scorers instead of just one
    if top_scorers:
        all_top_scorers = "\n".join([f"{player}: {count} times" for player, count in top_scorers.items()])
    else:
        all_top_scorers = "None"

    stats_message = (
        f"Match Statistics\n\n"
        f"Total Matches: {total_matches}\n"
        f"Ties: {ties}\n\n"
        + "\n".join([f"{team} Wins: {count}" for team, count in wins.items()])
        + f"\n\nTop Scorers Across All Matches:\n{all_top_scorers}"
    )

    messagebox.showinfo("Match Statistics", stats_message)

root = tk.Tk()
root.title("Cricket Match Simulator")
root.geometry("480x460")
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
    def save_team1():
        nonlocal t1_name_entry, t1_captain_entry
        global team1_name, team1_captain
        team1_name = t1_name_entry.get()
        team1_captain = t1_captain_entry.get()

        if not team1_name:
            messagebox.showerror("Error", "Please enter Team 1 Name.")
            return
        
        if not team1_captain:
            messagebox.showerror("Error", "Please enter Team 1 Captain Name.")
            return

        if not team1_name.isalpha():
            messagebox.showerror("Error", "The team name must only contain letters.")
            return
        
        if not team1_captain.isalpha():
            messagebox.showerror("Error", "The team captain name must only contain letters.")
            return
        
        messagebox.showinfo("Saved", f"Team 1 Info Saved: {team1_name}")
        team1_win.destroy()
    
    team1_win = tk.Toplevel(root)
    team1_win.title("Enter Team 1 Info")


    tk.Label(team1_win, text="Team 1 Name:").grid(row=0, column=0, padx=10, pady=5)
    t1_name_entry = tk.Entry(team1_win)
    t1_name_entry.grid(row=0, column=1)
    t1_name_entry.insert(0, team1_name)

    tk.Label(team1_win, text="Captain Name:").grid(row=1, column=0, padx=10, pady=5)
    t1_captain_entry = tk.Entry(team1_win)
    t1_captain_entry.grid(row=1, column=1)
    t1_captain_entry.insert(0, team1_captain)

    tk.Button(team1_win, text="Save", command=save_team1, bg="green", fg="white").grid(row=2, columnspan=2, pady=10)

def open_team2_window():
    def save_team2():
        nonlocal t2_name_entry, t2_captain_entry
        global team2_name, team2_captain
        team2_name = t2_name_entry.get()
        team2_captain = t2_captain_entry.get()

        if not team2_name:
            messagebox.showerror("Error", "Please enter Team 2 Name.")
            return

        if not team2_captain:
            messagebox.showerror("Error", "Please enter Team 2 captain name.")
            return

        if not team2_name.isalpha():
            messagebox.showerror("Error", "The team name must only contain letters.")
            return
        if not team2_captain.isalpha():
            messagebox.showerror("Error", "The team captain name must only contain letters.")
            return

        messagebox.showinfo("Saved", f"Team 2 Info Saved: {team2_name}")
        team2_win.destroy()
    
    team2_win = tk.Toplevel(root)
    team2_win.title("Enter Team 2 Info")

    tk.Label(team2_win, text="Team 2 Name:").grid(row=0, column=0, padx=10, pady=5)
    t2_name_entry = tk.Entry(team2_win)
    t2_name_entry.grid(row=0, column=1)
    t2_name_entry.insert(0, team2_name)

    tk.Label(team2_win, text="Captain Name:").grid(row=1, column=0, padx=10, pady=5)
    t2_captain_entry = tk.Entry(team2_win)
    t2_captain_entry.grid(row=1, column=1)
    t2_captain_entry.insert(0, team2_captain)

    tk.Button(team2_win, text="Save", command=save_team2, bg="green", fg="white").grid(row=2, columnspan=2, pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)
tk.Button(buttons_frame, text="Enter Team 1 Info", command=open_team1_window, width=18).grid(row=0, column=0, padx=10)
tk.Button(buttons_frame, text="Enter Team 2 Info", command=open_team2_window, width=18).grid(row=0, column=1, padx=10)

def start_simulation():
    if not team1_name or not team2_name:
        messagebox.showerror("Error", "Please enter info for both teams!")
        return
    
    if team1_name.lower() == team2_name.lower():
        messagebox.showerror("Error", "Team names must be different!")
        return
    
    overs = int(overs_var.get())
    result = simulate_match(team1_name, team2_name, overs)

    result_message = (
        f"{team1_name}: {result['team1_score']}/{result['team1_wickets']}  "
        f"(Rating: {result['rating1']}/10)\n"
        f"{team2_name}: {result['team2_score']}/{result['team2_wickets']}  "
        f"(Rating: {result['rating2']}/10)\n\n"
        f"Winner: {result['winner']}\n\n"
        f"Top Scorer: {result['top_scorer']['name']}  "
        f"- {result['top_scorer']['runs']} runs"
    )

    pom = result["player_of_match"]
    if pom:
        result_message += (
            f"\n\nPlayer of the Match: {pom['name']}\n"
            f"Performance: {pom['runs']} runs | {pom['wickets']} wickets"
        )
    messagebox.showinfo("Match Result", result_message)
    save_match_result(result_message)

def tournament_mode():
    if not team1_name or not team2_name:
        messagebox.showerror("Error", "Please enter info for both teams before starting a tournament!")
        return

    if team1_name.lower() == team2_name.lower():
        messagebox.showerror("Error", "Team names must be different!")
        return

    # Ask user for series length (3 or 5 matches)
    series_length = messagebox.askquestion(
        "Tournament Type",
        "Do you want to play Best of 5?\n(Click 'Yes' for Best of 5, 'No' for Best of 3)"
    )
    total_matches = 5 if series_length == "yes" else 3
    required_wins = (total_matches // 2) + 1

    overs = int(overs_var.get())
    match_results = []
    wins = {team1_name: 0, team2_name: 0}
    player_stats = {}

    for match_no in range(1, total_matches + 1):
        result = simulate_match(team1_name, team2_name, overs)

        winner = result["winner"]
        if winner != "Tie":
            wins[winner] += 1

        # track player stats for man of the series
        for p in [result["player_of_match"], result["top_scorer"]]:
            if p:
                if p["name"] not in player_stats:
                    player_stats[p["name"]] = {"runs": 0, "wickets": 0}
                player_stats[p["name"]]["runs"] += p["runs"]
                player_stats[p["name"]]["wickets"] += p["wickets"]

        # build match summary
        pom = result["player_of_match"]
        pom_text = f"(POTM: {pom['name']} - {pom['runs']} runs, {pom['wickets']} wickets)" if pom else ""
        summary = (
            f"Match {match_no}: "
            f"{team1_name} {result['team1_score']}/{result['team1_wickets']} "
            f"vs {team2_name} {result['team2_score']}/{result['team2_wickets']} "
            f"→ Winner: {winner} {pom_text}"
        )

        match_results.append(summary)

        # save each match as usual
        result_message = (
            f"{team1_name}: {result['team1_score']}/{result['team1_wickets']}  (Rating: {result['rating1']}/10)\n"
            f"{team2_name}: {result['team2_score']}/{result['team2_wickets']}  (Rating: {result['rating2']}/10)\n\n"
            f"Winner: {winner}\n\n"
            f"Top Scorer: {result['top_scorer']['name']}  - {result['top_scorer']['runs']} runs"
        )
        if pom:
            result_message += (
                f"\n\nPlayer of the Match: {pom['name']}\n"
                f"Performance: {pom['runs']} runs | {pom['wickets']} wickets"
            )
        save_match_result(result_message)

        # stop if one team already secured enough wins
        if wins[team1_name] == required_wins or wins[team2_name] == required_wins:
            break

    # Decide series winner
    if wins[team1_name] > wins[team2_name]:
        series_winner = f"{team1_name} ({wins[team1_name]}–{wins[team2_name]})"
    elif wins[team2_name] > wins[team1_name]:
        series_winner = f"{team2_name} ({wins[team2_name]}–{wins[team1_name]})"
    else:
        series_winner = "Series tied"

    # Decide man of the series
    man_of_series = None
    if player_stats:
        man_of_series = max(
            player_stats.items(),
            key=lambda kv: kv[1]["runs"] + kv[1]["wickets"] * 25
        )

    # Final tournament message
    final_message = "\n".join(match_results)
    final_message += f"\n\n🏆 Series Winner: {series_winner}"
    if man_of_series:
        stats = player_stats[man_of_series[0]]
        final_message += (
            f"\nMan of the Series: {man_of_series[0]} "
            f"({stats['runs']} runs, {stats['wickets']} wickets)"
        )

    results_win = tk.Toplevel(root)
    results_win.title("Tournament Results")
    results_win.geometry("600x400")  # you can adjust size

    text_area = scrolledtext.ScrolledText(
        results_win, wrap=tk.WORD, width=70, height=20, font=("Consolas", 11)
    )
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Insert formatted results
    text_area.insert(tk.END, "=== Tournament Results ===\n\n")
    text_area.insert(tk.END, final_message)

    # Make text read-only
    text_area.config(state=tk.DISABLED)

tk.Button(root, text="Start Simulation", command=start_simulation, width=18, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="Tournament Mode", command=tournament_mode, width=18, bg="orange", fg="black").pack(pady=5)
tk.Button(root, text="View Previous Matches", command=view_previous_matches, width=18, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="View Statistics", command=view_statistics_simple, width=18, bg="purple", fg="white").pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, width=18, bg="red", fg="white").pack(pady=5)

root.mainloop()
