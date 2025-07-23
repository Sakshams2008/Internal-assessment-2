import tkinter as tk
from tkinter import messagebox

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