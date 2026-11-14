import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan
from utils.validation import parse_inputs
from results.formatter import format_result


# ==================================================
# DISKFLOW DESIGN SYSTEM
# ==================================================

BG = "#F2F4F5"
WHITE = "#FFFFFF"
DARK = "#263746"
NAVY = "#30485D"
BLUE = "#477A9F"
GREEN = "#39836B"
PURPLE = "#826BA4"
TEXT = "#344452"
MUTED = "#788692"
BORDER = "#DCE3E7"
SOFT = "#F7F9FA"


class DiskSchedulingApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("DiskFlow | Disk Scheduling Simulator")
        self.geometry("1200x850")
        self.minsize(900, 650)
        self.configure(bg=BG)

        self.total_labels = {}
        self.notebook = None
        self.result_frames = []

        self.create_variables()
        self.setup_styles()
        self.create_interface()

    # ==================================================
    # VARIABLES
    # ==================================================

    def create_variables(self):

        self.head_var = tk.StringVar(value="53")

        self.queue_var = tk.StringVar(
            value="98, 183, 37, 122, 14, 124, 65, 67"
        )

        self.minimum_var = tk.StringVar(value="0")
        self.maximum_var = tk.StringVar(value="199")

        self.direction_var = tk.StringVar(value="right")

        self.algorithm_var = tk.StringVar(
            value="Compare All Algorithms"
        )

        self.status_var = tk.StringVar(
            value="Ready | Configure your simulation."
        )

    # ==================================================
    # STYLES
    # ==================================================

    def setup_styles(self):

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Modern.TEntry",
            padding=9,
            font=("Segoe UI", 10),
            fieldbackground=WHITE
        )

        style.configure(
            "Modern.TCombobox",
            padding=8,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Primary.TButton",
            background=NAVY,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            padding=(18, 10),
            borderwidth=0
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", BLUE),
                ("pressed", DARK)
            ]
        )

        style.configure(
            "Secondary.TButton",
            background="#E8ECEE",
            foreground=DARK,
            font=("Segoe UI", 10),
            padding=(18, 10),
            borderwidth=0
        )

        style.map(
            "Secondary.TButton",
            background=[("active", "#DDE3E5")]
        )

        style.configure(
            "Modern.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=32,
            font=("Segoe UI", 9),
            borderwidth=0
        )

        style.configure(
            "Modern.Treeview.Heading",
            background="#E9EEF1",
            foreground=DARK,
            font=("Segoe UI", 9, "bold"),
            padding=9,
            borderwidth=0
        )

        style.map(
            "Modern.Treeview",
            background=[("selected", "#EAF1F6")],
            foreground=[("selected", DARK)]
        )

        # Horizontal result tabs

        style.configure(
            "Results.TNotebook",
            background=BG,
            borderwidth=0,
            tabmargins=(0, 0, 0, 0)
        )

        style.configure(
            "Results.TNotebook.Tab",
            background="#E5E9EB",
            foreground=DARK,
            padding=(25, 12),
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Results.TNotebook.Tab",
            background=[
                ("selected", NAVY),
                ("active", "#D5E0E7")
            ],
            foreground=[
                ("selected", WHITE),
                ("active", DARK)
            ]
        )

    # ==================================================
    # MAIN INTERFACE
    # ==================================================

    def create_interface(self):

        # Header
        header = tk.Frame(
            self,
            bg=DARK,
            height=105
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="diskflow.",
            font=("Segoe UI", 25, "bold"),
            bg=DARK,
            fg=WHITE
        ).pack(anchor="w", padx=30, pady=(16, 0))

        tk.Label(
            header,
            text="DISK SCHEDULING SIMULATOR"
                 "     /     FCFS  •  SSTF  •  SCAN",
            font=("Segoe UI", 9),
            bg=DARK,
            fg="#C4D0D9"
        ).pack(anchor="w", padx=30, pady=(2, 0))

        # Main scrollable area
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            container,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(
            self.canvas,
            bg=BG,
            padx=25,
            pady=20
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        # Main sections
        self.create_configuration()
        self.create_performance_cards()
        self.create_results_section()

        # Status bar
        status = tk.Frame(
            self,
            bg="#E6EAEB",
            height=32
        )

        status.pack(side="bottom", fill="x")
        status.pack_propagate(False)

        tk.Label(
            status,
            textvariable=self.status_var,
            bg="#E6EAEB",
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="left", padx=16, pady=6)

    # ==================================================
    # SCROLLING
    # ==================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_content(self, event):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==================================================
    # DESIGN HELPERS
    # ==================================================

    def create_card(self, parent, padding=18):

        return tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=padding,
            pady=padding
        )

    def section_heading(self, parent, number, title):

        frame = tk.Frame(parent, bg=BG)

        frame.pack(
            fill="x",
            pady=(0, 11)
        )

        tk.Label(
            frame,
            text=number,
            font=("Segoe UI", 9, "bold"),
            bg=BG,
            fg=BLUE
        ).pack(side="left")

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=DARK
        ).pack(side="left", padx=(9, 0))

    def add_field(
        self,
        parent,
        label,
        variable,
        row,
        column,
        width=22
    ):

        frame = tk.Frame(parent, bg=WHITE)

        frame.grid(
            row=row,
            column=column,
            sticky="w",
            padx=(0, 22),
            pady=9
        )

        tk.Label(
            frame,
            text=label.upper(),
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 6))

        entry = ttk.Entry(
            frame,
            textvariable=variable,
            width=width,
            style="Modern.TEntry"
        )

        entry.pack(anchor="w")

        return entry

    # ==================================================
    # SECTION 01 - CONFIGURATION
    # ==================================================

    def create_configuration(self):

        self.section_heading(
            self.content,
            "01",
            "Simulation Setup"
        )

        card = self.create_card(self.content, 20)
        card.pack(fill="x", pady=(0, 22))

        fields = tk.Frame(card, bg=WHITE)
        fields.pack(fill="x")

        fields.grid_columnconfigure(0, weight=1)
        fields.grid_columnconfigure(1, weight=2)

        self.add_field(
            fields,
            "Initial Head Position",
            self.head_var,
            0, 0, 20
        )

        self.add_field(
            fields,
            "Request Queue",
            self.queue_var,
            0, 1, 48
        )

        self.add_field(
            fields,
            "Minimum Cylinder",
            self.minimum_var,
            1, 0, 20
        )

        self.add_field(
            fields,
            "Maximum Cylinder",
            self.maximum_var,
            1, 1, 20
        )

        # SCAN direction
        direction_frame = tk.Frame(fields, bg=WHITE)

        direction_frame.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 22),
            pady=9
        )

        tk.Label(
            direction_frame,
            text="SCAN DIRECTION",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 6))

        ttk.Combobox(
            direction_frame,
            textvariable=self.direction_var,
            values=["right", "left"],
            state="readonly",
            width=18,
            style="Modern.TCombobox"
        ).pack(anchor="w")

        # Algorithm selection
        algorithm_frame = tk.Frame(fields, bg=WHITE)

        algorithm_frame.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(0, 22),
            pady=9
        )

        tk.Label(
            algorithm_frame,
            text="ALGORITHM",
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 6))

        ttk.Combobox(
            algorithm_frame,
            textvariable=self.algorithm_var,
            values=[
                "Compare All Algorithms",
                "FCFS",
                "SSTF",
                "SCAN"
            ],
            state="readonly",
            width=27,
            style="Modern.TCombobox"
        ).pack(anchor="w")

        # Action buttons
        actions = tk.Frame(card, bg=WHITE)

        actions.pack(
            fill="x",
            pady=(17, 0)
        )

        ttk.Button(
            actions,
            text="Run Simulation",
            style="Primary.TButton",
            command=self.run_simulation
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Reset",
            style="Secondary.TButton",
            command=self.reset_inputs
        ).pack(side="left", padx=10)

    # ==================================================
    # SECTION 02 - PERFORMANCE OVERVIEW
    # ==================================================

    def create_performance_cards(self):

        self.section_heading(
            self.content,
            "02",
            "Performance Overview"
        )

        container = tk.Frame(self.content, bg=BG)

        container.pack(
            fill="x",
            pady=(0, 22)
        )

        configurations = [
            ("FCFS", BLUE),
            ("SSTF", GREEN),
            ("SCAN", PURPLE)
        ]

        for index, (name, color) in enumerate(configurations):

            card = tk.Frame(
                container,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
                padx=17,
                pady=14
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=(0 if index == 0 else 7, 0)
            )

            container.grid_columnconfigure(
                index,
                weight=1
            )

            tk.Label(
                card,
                text=name,
                font=("Segoe UI", 9, "bold"),
                bg=WHITE,
                fg=color
            ).pack(anchor="w")

            value = tk.Label(
                card,
                text="—",
                font=("Segoe UI", 25, "bold"),
                bg=WHITE,
                fg=DARK
            )

            value.pack(anchor="w", pady=(4, 0))

            tk.Label(
                card,
                text="TOTAL HEAD MOVEMENT",
                font=("Segoe UI", 8),
                bg=WHITE,
                fg=MUTED
            ).pack(anchor="w")

            self.total_labels[name] = value

    # ==================================================
    # SECTION 03 - RESULTS AND TABS
    # ==================================================

    def create_results_section(self):

        self.section_heading(
            self.content,
            "03",
            "Computation Results"
        )

        self.results_container = tk.Frame(
            self.content,
            bg=BG
        )

        self.results_container.pack(
            fill="both",
            expand=True,
            pady=(0, 25)
        )

        self.show_empty_message()

    def show_empty_message(self):

        card = self.create_card(
            self.results_container,
            25
        )

        card.pack(fill="x")

        tk.Label(
            card,
            text="No simulation results yet.",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(pady=(5, 4))

        tk.Label(
            card,
            text="Configure your inputs and select Run Simulation to begin.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(pady=(0, 5))

    # ==================================================
    # SSTF EXPLANATION HELPER
    # ==================================================

    def build_sstf_steps(self, initial_head, requests, sequence):

        pending = list(enumerate(requests))
        current_head = initial_head
        steps = []

        for selected_request in sequence:

            candidates = []

            for index, request in pending:

                candidates.append({
                    "request": request,
                    "distance": abs(current_head - request),
                    "index": index
                })

            candidates.sort(
                key=lambda item: (
                    item["distance"],
                    item["index"]
                )
            )

            selected = min(
                pending,
                key=lambda item: (
                    abs(current_head - item[1]),
                    item[0]
                )
            )

            request = selected[1]

            steps.append({
                "current_head": current_head,
                "candidates": candidates,
                "selected": request,
                "distance": abs(current_head - request)
            })

            pending.remove(selected)
            current_head = request

        return steps

    # ==================================================
    # ALGORITHM RESULT SECTION
    # ==================================================

    def create_algorithm_section(
        self,
        parent,
        name,
        result,
        head,
        requests
    ):

        formatted = format_result(
            result,
            head
        )

        colors = {
            "FCFS": BLUE,
            "SSTF": GREEN,
            "SCAN": PURPLE
        }

        descriptions = {
            "FCFS": "First Come, First Serve",
            "SSTF": "Shortest Seek Time First",
            "SCAN": "Elevator Algorithm"
        }

        color = colors[name]

        card = self.create_card(parent, 18)
        card.pack(fill="x")

        self.result_frames.append(card)

        # Header
        header = tk.Frame(card, bg=WHITE)
        header.pack(fill="x")

        tk.Label(
            header,
            text=name,
            font=("Segoe UI", 15, "bold"),
            bg=WHITE,
            fg=color
        ).pack(side="left")

        tk.Label(
            header,
            text=f"{result['total_movement']} CYLINDERS",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(side="right")

        tk.Label(
            card,
            text=descriptions[name],
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 12))

        tk.Label(
            card,
            text=formatted["explanation"],
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=TEXT,
            wraplength=1000,
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        # Service sequence
        self.add_result_label(
            card,
            "SERVICE SEQUENCE",
            " → ".join(map(str, formatted["sequence"]))
        )

        # Movement table
        tk.Label(
            card,
            text="MOVEMENT PER STEP",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w", pady=(16, 7))

        table_frame = tk.Frame(card, bg=WHITE)
        table_frame.pack(fill="x")

        columns = (
            "step",
            "movement",
            "distance"
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=min(max(len(formatted["rows"]), 1), 8),
            style="Modern.Treeview"
        )

        table.heading("step", text="STEP")
        table.heading("movement", text="HEAD MOVEMENT")
        table.heading("distance", text="DISTANCE")

        table.column(
            "step",
            width=80,
            anchor="center"
        )

        table.column(
            "movement",
            width=300,
            anchor="center"
        )

        table.column(
            "distance",
            width=150,
            anchor="center"
        )

        for row in formatted["rows"]:

            table.insert(
                "",
                "end",
                values=(
                    row["step"],
                    row["head_movement"],
                    row["distance"]
                )
            )

        table.pack(fill="x")

        # Mathematical solution
        tk.Label(
            card,
            text="STEP-BY-STEP SOLUTION",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w", pady=(16, 7))

        solution_box = tk.Frame(
            card,
            bg=SOFT,
            padx=12,
            pady=10
        )

        solution_box.pack(fill="x")

        tk.Label(
            solution_box,
            text=formatted["equation"] or "0",
            font=("Consolas", 10),
            bg=SOFT,
            fg=TEXT,
            wraplength=1000,
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            solution_box,
            text=(
                f"TOTAL HEAD MOVEMENT = "
                f"{formatted['total']} CYLINDERS"
            ),
            font=("Segoe UI", 10, "bold"),
            bg=SOFT,
            fg=color
        ).pack(anchor="w", pady=(9, 0))

        # Algorithm-specific explanations
        if name == "SSTF":

            steps = self.build_sstf_steps(
                head,
                requests,
                result["sequence"]
            )

            self.create_sstf_explanation(
                card,
                steps
            )

        elif name == "SCAN":

            self.create_scan_explanation(
                card,
                formatted["scan_details"],
                formatted["scan_events"]
            )

    # ==================================================
    # RESULT LABEL
    # ==================================================

    def add_result_label(self, parent, title, value):

        tk.Label(
            parent,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            parent,
            text=value,
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT,
            wraplength=1000,
            justify="left"
        ).pack(anchor="w")

    # ==================================================
    # SSTF EXPLANATION
    # ==================================================

    def create_sstf_explanation(self, parent, steps):

        tk.Frame(
            parent,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=16)

        tk.Label(
            parent,
            text="NEAREST REQUEST SELECTION",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(anchor="w", pady=(0, 8))

        for number, detail in enumerate(steps, start=1):

            current = detail["current_head"]
            selected = detail["selected"]
            distance = detail["distance"]

            candidates = ", ".join(
                f'{item["request"]} ({item["distance"]})'
                for item in detail["candidates"]
            )

            text = (
                f"Step {number} | Current head: {current}\n"
                f"Candidates (cylinder / distance): {candidates}\n"
                f"Selected: {selected} | "
                f"|{current} - {selected}| = {distance}"
            )

            tk.Label(
                parent,
                text=text,
                font=("Consolas", 8),
                bg=WHITE,
                fg=TEXT,
                justify="left",
                wraplength=1000
            ).pack(anchor="w", pady=4)

    # ==================================================
    # SCAN EXPLANATION
    # ==================================================

    def create_scan_explanation(
        self,
        parent,
        details,
        events
    ):

        tk.Frame(
            parent,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=16)

        tk.Label(
            parent,
            text="SCAN DIRECTION AND BOUNDARY",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=PURPLE
        ).pack(anchor="w", pady=(0, 8))

        information = [
            f"Initial direction: {details['initial_direction'].upper()}",
            f"Disk boundary: {details['boundary']}",
            f"Reversal position: {details['reversed_at']}"
        ]

        for item in information:

            tk.Label(
                parent,
                text=f"• {item}",
                font=("Segoe UI", 9),
                bg=WHITE,
                fg=TEXT
            ).pack(anchor="w", pady=2)

        for event in events:

            tk.Label(
                parent,
                text=f"• {event['message']}",
                font=("Segoe UI", 9),
                bg=WHITE,
                fg=PURPLE
            ).pack(anchor="w", pady=2)

    # ==================================================
    # RUN SIMULATION
    # ==================================================

    def run_simulation(self):

        try:

            head, requests, minimum, maximum, direction = parse_inputs(
                self.head_var.get(),
                self.queue_var.get(),
                self.minimum_var.get(),
                self.maximum_var.get(),
                self.direction_var.get()
            )

            # Execute algorithms
            all_results = {

                "FCFS": fcfs(
                    head,
                    requests
                ),

                "SSTF": sstf(
                    head,
                    requests
                ),

                "SCAN": scan(
                    head,
                    requests,
                    minimum,
                    maximum,
                    direction
                )
            }

            selected = self.algorithm_var.get()

            if selected == "Compare All Algorithms":

                displayed_results = all_results

            else:

                displayed_results = {
                    selected: all_results[selected]
                }

            # Clear previous output
            self.clear_results()

            # Update overview cards
            for name, label in self.total_labels.items():

                if name in displayed_results:

                    total = displayed_results[name][
                        "total_movement"
                    ]

                    label.config(text=str(total))

                else:

                    label.config(text="—")

            # Create horizontal tabs
            self.notebook = ttk.Notebook(
                self.results_container,
                style="Results.TNotebook"
            )

            self.notebook.pack(
                fill="both",
                expand=True
            )

            # Separate result page for each algorithm
            for name, result in displayed_results.items():

                page = tk.Frame(
                    self.notebook,
                    bg=BG,
                    padx=8,
                    pady=10
                )

                self.notebook.add(
                    page,
                    text=f"  {name}  "
                )

                self.create_algorithm_section(
                    page,
                    name,
                    result,
                    head,
                    requests
                )

            self.status_var.set(
                f"Simulation completed | "
                f"Algorithm: {selected} | "
                f"Requests: {len(requests)}"
            )

            self.canvas.yview_moveto(0)

        except ValueError as error:

            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

            self.status_var.set(
                "Simulation failed | Check your inputs."
            )

        except Exception as error:

            messagebox.showerror(
                "Application Error",
                str(error)
            )

            self.status_var.set(
                "An unexpected error occurred."
            )

    # ==================================================
    # CLEAR RESULTS
    # ==================================================

    def clear_results(self):

        for widget in self.results_container.winfo_children():
            widget.destroy()

        self.result_frames.clear()
        self.notebook = None

        for label in self.total_labels.values():
            label.config(text="—")

    # ==================================================
    # RESET
    # ==================================================

    def reset_inputs(self):

        self.head_var.set("53")

        self.queue_var.set(
            "98, 183, 37, 122, 14, 124, 65, 67"
        )

        self.minimum_var.set("0")
        self.maximum_var.set("199")

        self.direction_var.set("right")

        self.algorithm_var.set(
            "Compare All Algorithms"
        )

        self.clear_results()
        self.show_empty_message()

        self.status_var.set(
            "Ready | Default configuration restored."
        )

        self.canvas.yview_moveto(0)


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================

if __name__ == "__main__":

    app = DiskSchedulingApp()
    app.mainloop()
