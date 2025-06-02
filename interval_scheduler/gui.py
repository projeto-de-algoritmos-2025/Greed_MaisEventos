import tkinter as tk
from tkinter import ttk, messagebox
from scheduler import interval_scheduling
from datetime import datetime, timedelta

class IntervalSchedulingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Agendador de Eventos - Interval Scheduling")
        self.master.geometry("1000x750")
        self.master.configure(bg="#f0f0f0")
        self.events = []

        style = ttk.Style()
        style.theme_use("clam")

        container = ttk.Frame(master)
        container.pack(expand=True)

        title = ttk.Label(container, text="Agendador de Eventos", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        inputs_frame = ttk.LabelFrame(container, text="Adicionar novo evento", padding=15)
        inputs_frame.pack(pady=10)

        ttk.Label(inputs_frame, text="Data Início (dd/mm/yyyy):").grid(row=0, column=0, sticky="e", pady=4)
        ttk.Label(inputs_frame, text="Hora Início (HH:MM):").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Label(inputs_frame, text="Data Fim (dd/mm/yyyy):").grid(row=2, column=0, sticky="e", pady=4)
        ttk.Label(inputs_frame, text="Hora Fim (HH:MM):").grid(row=3, column=0, sticky="e", pady=4)

        self.start_date_entry = ttk.Entry(inputs_frame, width=25)
        self.start_time_entry = ttk.Entry(inputs_frame, width=25)
        self.end_date_entry = ttk.Entry(inputs_frame, width=25)
        self.end_time_entry = ttk.Entry(inputs_frame, width=25)

        self.start_date_entry.grid(row=0, column=1, pady=4, padx=5)
        self.start_time_entry.grid(row=1, column=1, pady=4, padx=5)
        self.end_date_entry.grid(row=2, column=1, pady=4, padx=5)
        self.end_time_entry.grid(row=3, column=1, pady=4, padx=5)

        self.add_button = ttk.Button(inputs_frame, text="Adicionar Evento", command=self.add_event)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.solve_button = ttk.Button(inputs_frame, text="Executar Algoritmo", command=self.solve)
        self.solve_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.reset_button = ttk.Button(container, text="Reiniciar Eventos", command=self.reset_events)
        self.reset_button.pack(pady=(0,10))

        self.event_listbox = tk.Listbox(container, height=10, width=100)
        self.event_listbox.pack(pady=5)

        self.result_label = ttk.Label(container, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)

        self.canvas_frame = ttk.Frame(container, padding=(20, 0, 20, 20))
        self.canvas_frame.pack()
        self.canvas = tk.Canvas(self.canvas_frame, width=920, height=400, bg="white", highlightthickness=1, highlightbackground="#cccccc")
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
            self.event_listbox.insert(tk.END, f"{start.strftime('%d/%m %H:%M')} → {end.strftime('%H:%M')}")

            self.start_date_entry.delete(0, tk.END)
            self.start_time_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
            self.end_time_entry.delete(0, tk.END)

            self.draw_events()

        except ValueError as ve:
            messagebox.showerror("Erro de entrada", str(ve))

    def draw_events(self, selected=[]):
        self.canvas.delete("all")
        width = 880
        offset_x = 20
        offset_y = 50 

        if not self.events:
            return

        min_time = min(start for start, _ in self.events)
        max_time = max(end for _, end in self.events)
        total_minutes = int((max_time - min_time).total_seconds() / 60)

        timeline_y = offset_y - 30
        self.canvas.create_line(offset_x, timeline_y, offset_x + width, timeline_y, fill="black")

        start_hour = min_time.replace(minute=0, second=0, microsecond=0)
        end_hour = max_time.replace(minute=0, second=0, microsecond=0)
        hours = int((end_hour - start_hour).total_seconds() / 3600) + 2 

        for i in range(hours):
            time_point = start_hour + timedelta(hours=i)
            if time_point > max_time:
                break
            minute_offset = int((time_point - min_time).total_seconds() / 60)
            x = offset_x + (minute_offset / total_minutes) * width
            self.canvas.create_line(x, timeline_y - 5, x, timeline_y + 5, fill="black")
            self.canvas.create_text(x, timeline_y - 10, text=time_point.strftime("%H:%M"), font=("Arial", 8), anchor="s")

        lines = []
        for event in self.events:
            placed = False
            for line in lines:
                if all(event[0] >= e[1] or event[1] <= e[0] for e in line):
                    line.append(event)
                    placed = True
                    break
            if not placed:
                lines.append([event])

        for line_index, line in enumerate(lines):
            for i, (start, end) in enumerate(line):
                start_min = int((start - min_time).total_seconds() / 60)
                end_min = int((end - min_time).total_seconds() / 60)

                x1 = offset_x + (start_min / total_minutes) * width
                x2 = offset_x + (end_min / total_minutes) * width
                y = offset_y + line_index * 40

                color = "lightgreen" if (start, end) in selected else "#90caf9"
                self.canvas.create_rectangle(x1, y, x2, y + 25, fill=color, outline="black")
                self.canvas.create_text((x1 + x2) / 2, y + 12, font=("Arial", 9),
                    text=f"{start.strftime('%d/%m %H:%M')} - {end.strftime('%H:%M')}")

        # Legenda
        legend_y = self.canvas.winfo_height() - 40
        self.canvas.create_rectangle(20, legend_y, 40, legend_y + 20, fill="#90caf9", outline="black")
        self.canvas.create_text(60, legend_y + 10, anchor="w", text="Evento não selecionado")

        self.canvas.create_rectangle(220, legend_y, 240, legend_y + 20, fill="lightgreen", outline="black")
        self.canvas.create_text(260, legend_y + 10, anchor="w", text="Evento selecionado")

    def solve(self):
        selected = interval_scheduling(self.events)
        self.draw_events(selected)
        self.result_label.config(text=f"Eventos selecionados: {len(selected)} de {len(self.events)}")

    def reset_events(self):
        self.events = []
        self.event_listbox.delete(0, tk.END)
        self.result_label.config(text="")
        self.canvas.delete("all")