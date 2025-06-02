import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import interval_scheduling
from datetime import datetime

class IntervalSchedulingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Agendador de Eventos - Interval Scheduling")
        self.master.configure(bg="#f0f0f0")

        self.events = []

        # Frame principal
        frame = ttk.Frame(master, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        # Labels e Entradas
        ttk.Label(frame, text="Data Início (dd/mm/yyyy):").grid(row=0, column=0, sticky="e", pady=4)
        ttk.Label(frame, text="Hora Início (HH:MM):").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Label(frame, text="Data Fim (dd/mm/yyyy):").grid(row=2, column=0, sticky="e", pady=4)
        ttk.Label(frame, text="Hora Fim (HH:MM):").grid(row=3, column=0, sticky="e", pady=4)

        self.start_date_entry = ttk.Entry(frame, width=20)
        self.start_time_entry = ttk.Entry(frame, width=20)
        self.end_date_entry = ttk.Entry(frame, width=20)
        self.end_time_entry = ttk.Entry(frame, width=20)

        self.start_date_entry.grid(row=0, column=1, pady=4, padx=5)
        self.start_time_entry.grid(row=1, column=1, pady=4, padx=5)
        self.end_date_entry.grid(row=2, column=1, pady=4, padx=5)
        self.end_time_entry.grid(row=3, column=1, pady=4, padx=5)

        # Botões
        self.add_button = ttk.Button(frame, text="Adicionar Evento", command=self.add_event)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.solve_button = ttk.Button(frame, text="Executar Algoritmo", command=self.solve)
        self.solve_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Canvas com borda e fundo branco
        self.canvas_frame = ttk.Frame(master, padding=(20, 0, 20, 20))
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")
        self.canvas = tk.Canvas(self.canvas_frame, width=700, height=300, bg="white", highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack()

    def add_event(self):
        try:
            start_str = f"{self.start_date_entry.get()} {self.start_time_entry.get()}"
            end_str = f"{self.end_date_entry.get()} {self.end_time_entry.get()}"

            start = datetime.strptime(start_str, "%d/%m/%Y %H:%M")
            end = datetime.strptime(end_str, "%d/%m/%Y %H:%M")

            if start >= end:
                raise ValueError("A data de início deve ser anterior à data de fim.")

            self.events.append((start, end))

            # Limpa campos
            self.start_date_entry.delete(0, tk.END)
            self.start_time_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
            self.end_time_entry.delete(0, tk.END)

            self.draw_events()

        except ValueError as ve:
            messagebox.showerror("Erro de entrada", str(ve))

    def draw_events(self, selected=[]):
        self.canvas.delete("all")
        width = 600
        offset_x = 50
        offset_y = 30

        if not self.events:
            return

        min_time = min(start for start, _ in self.events)
        max_time = max(end for _, end in self.events)
        total_minutes = int((max_time - min_time).total_seconds() / 60)

        for i, (start, end) in enumerate(self.events):
            start_min = int((start - min_time).total_seconds() / 60)
            end_min = int((end - min_time).total_seconds() / 60)

            x1 = offset_x + (start_min / total_minutes) * width
            x2 = offset_x + (end_min / total_minutes) * width
            y = offset_y + i * 35

            color = "lightgreen" if (start, end) in selected else "lightblue"
            self.canvas.create_rectangle(x1, y, x2, y + 25, fill=color, outline="black")
            self.canvas.create_text((x1 + x2) / 2, y + 12, font=("Arial", 9),
                text=f"{start.strftime('%d/%m %H:%M')} - {end.strftime('%H:%M')}")

    def solve(self):
        selected = interval_scheduling(self.events)
        self.draw_events(selected)
        messagebox.showinfo("Resultado", f"Eventos selecionados: {len(selected)}")