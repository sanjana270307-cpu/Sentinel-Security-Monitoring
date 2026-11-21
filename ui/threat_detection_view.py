
import customtkinter as ctk
import threading
import queue

from detection.run_detection import run_all_detections


BG = "#080F1C"
PANEL = "#111F33"
CARD = "#16263D"
BORDER = "#263B55"

CYAN = "#20D4D0"
BLUE = "#438BFF"
GREEN = "#31D69A"
RED = "#FF5B6E"
ORANGE = "#FFB454"

WHITE = "#F1F5F9"
MUTED = "#8496AD"


class ThreatDetectionView(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.result_queue = queue.Queue()
        self.scanning = False
        self.scan_number = 0

        self.create_view()

    # ==========================================
    # MAIN VIEW
    # ==========================================

    def create_view(self):

        ctk.CTkLabel(
            self,
            text="Threat Detection Center",
            font=("Arial", 29, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self,
            text="Scan login activity and identify suspicious security patterns.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(0, 25)
        )

        # STATUS CARDS

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        stats_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.engine_card = self.create_stat_card(
            stats_frame,
            "DETECTION ENGINE",
            "READY",
            "Waiting for scan",
            CYAN,
            0
        )

        self.threat_card = self.create_stat_card(
            stats_frame,
            "THREATS FOUND",
            "--",
            "No scan completed",
            RED,
            1
        )

        self.scan_card = self.create_stat_card(
            stats_frame,
            "TOTAL SCANS",
            "0",
            "This session",
            BLUE,
            2
        )

        # DETECTION RULES PANEL

        rules_panel = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        rules_panel.pack(
            fill="x",
            pady=10
        )

        ctk.CTkLabel(
            rules_panel,
            text="Detection Rules",
            font=("Arial", 18, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            rules_panel,
            text="Security patterns monitored by Sentinel",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 12)
        )

        self.create_rule_row(
            rules_panel,
            "BRUTE FORCE DETECTION",
            "Identifies repeated failed login attempts",
            RED
        )

        self.create_rule_row(
            rules_panel,
            "SUSPICIOUS LOGIN DETECTION",
            "Identifies suspicious login patterns",
            ORANGE
        )

        # SCAN CONTROL

        control_panel = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        control_panel.pack(
            fill="x",
            pady=15
        )

        control_content = ctk.CTkFrame(
            control_panel,
            fg_color="transparent"
        )

        control_content.pack(
            fill="x",
            padx=20,
            pady=18
        )

        text_frame = ctk.CTkFrame(
            control_content,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            text_frame,
            text="Ready to scan?",
            font=("Arial", 16, "bold"),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Run the detection engine against recorded login events.",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        self.scan_button = ctk.CTkButton(
            control_content,
            text="▶  RUN THREAT SCAN",
            height=43,
            width=190,
            corner_radius=9,
            fg_color="#087E91",
            hover_color="#0E7490",
            font=("Arial", 12, "bold"),
            command=self.start_scan
        )

        self.scan_button.pack(
            side="right",
            padx=(15, 0)
        )

        self.progress = ctk.CTkProgressBar(
            self,
            height=7,
            corner_radius=5,
            progress_color=CYAN,
            fg_color=PANEL
        )

        self.progress.pack(
            fill="x",
            pady=(0, 15)
        )

        self.progress.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="●  ENGINE READY",
            font=("Arial", 11, "bold"),
            text_color=GREEN
        )

        self.status_label.pack(
            anchor="w",
            pady=(0, 12)
        )

        # RESULTS PANEL

        self.results_panel = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        self.results_panel.pack(
            fill="both",
            expand=True,
            pady=(5, 10)
        )

        ctk.CTkLabel(
            self.results_panel,
            text="Detection Results",
            font=("Arial", 18, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        self.results_subtitle = ctk.CTkLabel(
            self.results_panel,
            text="Results will appear here after a scan.",
            font=("Arial", 11),
            text_color=MUTED
        )

        self.results_subtitle.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.results_content = ctk.CTkFrame(
            self.results_panel,
            fg_color="transparent"
        )

        self.results_content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.show_initial_results()

    # ==========================================
    # STATISTIC CARDS
    # ==========================================

    def create_stat_card(
        self,
        parent,
        heading,
        value,
        description,
        color,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=13,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=heading,
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 25, "bold"),
            text_color=color
        )

        value_label.pack(
            anchor="w",
            padx=15
        )

        description_label = ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 10),
            text_color=MUTED
        )

        description_label.pack(
            anchor="w",
            padx=15,
            pady=(3, 15)
        )

        return {
            "value": value_label,
            "description": description_label
        }

    # ==========================================
    # DETECTION RULE ROWS
    # ==========================================

    def create_rule_row(
        self,
        parent,
        title,
        description,
        color
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=9
        )

        row.pack(
            fill="x",
            padx=18,
            pady=5
        )

        ctk.CTkLabel(
            row,
            text="●",
            font=("Arial", 15),
            text_color=color
        ).pack(
            side="left",
            padx=12,
            pady=12
        )

        text_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left",
            pady=9
        )

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text=description,
            font=("Arial", 10),
            text_color=MUTED
        ).pack(anchor="w")

        ctk.CTkLabel(
            row,
            text="ENABLED",
            font=("Arial", 9, "bold"),
            text_color=GREEN
        ).pack(
            side="right",
            padx=15
        )

    # ==========================================
    # INITIAL RESULTS
    # ==========================================

    def show_initial_results(self):

        ctk.CTkLabel(
            self.results_content,
            text="◈",
            font=("Arial", 32),
            text_color=CYAN
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.results_content,
            text="No scan results yet",
            font=("Arial", 14, "bold"),
            text_color=WHITE
        ).pack()

        ctk.CTkLabel(
            self.results_content,
            text="Click Run Threat Scan to analyse security events.",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(pady=(5, 20))

    # ==========================================
    # START SCAN
    # ==========================================

    def start_scan(self):

        if self.scanning:
            return

        self.scanning = True

        self.scan_button.configure(
            state="disabled",
            text="SCANNING..."
        )

        self.engine_card["value"].configure(
            text="RUNNING",
            text_color=ORANGE
        )

        self.status_label.configure(
            text="●  ANALYSING SECURITY EVENTS...",
            text_color=ORANGE
        )

        self.progress.start()

        self.results_subtitle.configure(
            text="The detection engine is analysing recorded login events..."
        )

        worker = threading.Thread(
            target=self.run_scan_worker,
            daemon=True
        )

        worker.start()

        self.after(100, self.check_scan_result)

    # ==========================================
    # BACKGROUND DETECTION
    # ==========================================

    def run_scan_worker(self):

        try:

            results = run_all_detections()

            self.result_queue.put(
                ("success", results)
            )

        except Exception as e:

            self.result_queue.put(
                ("error", str(e))
            )

    # ==========================================
    # CHECK SCAN RESULT
    # ==========================================

    def check_scan_result(self):

        try:

            result_type, result = self.result_queue.get_nowait()

        except queue.Empty:

            self.after(100, self.check_scan_result)
            return

        self.progress.stop()
        self.progress.set(1)

        self.scanning = False

        self.scan_button.configure(
            state="normal",
            text="▶  RUN THREAT SCAN"
        )

        if result_type == "error":

            self.engine_card["value"].configure(
                text="ERROR",
                text_color=RED
            )

            self.status_label.configure(
                text="●  SCAN FAILED",
                text_color=RED
            )

            self.results_subtitle.configure(
                text="Detection could not be completed."
            )

            self.show_scan_error(result)

            return

        self.display_results(result)

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    def display_results(self, results):

        brute_force = results.get("brute_force", [])
        suspicious = results.get("suspicious_login", [])

        total = len(brute_force) + len(suspicious)

        self.scan_number += 1

        self.engine_card["value"].configure(
            text="COMPLETED",
            text_color=GREEN
        )

        self.engine_card["description"].configure(
            text="Last scan completed"
        )

        self.threat_card["value"].configure(
            text=str(total),
            text_color=RED if total else GREEN
        )

        self.threat_card["description"].configure(
            text="Detection matches"
        )

        self.scan_card["value"].configure(
            text=str(self.scan_number)
        )

        self.scan_card["description"].configure(
            text="Completed this session"
        )

        self.status_label.configure(
            text="●  SCAN COMPLETED",
            text_color=GREEN
        )

        self.results_subtitle.configure(
            text="Latest detection engine results"
        )

        for widget in self.results_content.winfo_children():
            widget.destroy()

        self.create_result_section(
            "BRUTE FORCE DETECTION",
            brute_force,
            RED
        )

        self.create_result_section(
            "SUSPICIOUS LOGIN DETECTION",
            suspicious,
            ORANGE
        )

        if total == 0:

            ctk.CTkLabel(
                self.results_content,
                text="✓  No matching threats detected",
                font=("Arial", 13, "bold"),
                text_color=GREEN
            ).pack(
                anchor="w",
                padx=10,
                pady=15
            )

    # ==========================================
    # RESULT SECTION
    # ==========================================

    def create_result_section(
        self,
        title,
        users,
        color
    ):

        section = ctk.CTkFrame(
            self.results_content,
            fg_color=PANEL,
            corner_radius=9
        )

        section.pack(
            fill="x",
            pady=6,
            padx=3
        )

        ctk.CTkLabel(
            section,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=color
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        if users:

            for user_id in users:

                ctk.CTkLabel(
                    section,
                    text=f"Detected User ID: {user_id}",
                    font=("Arial", 11),
                    text_color=WHITE
                ).pack(
                    anchor="w",
                    padx=15,
                    pady=4
                )

        else:

            ctk.CTkLabel(
                section,
                text="No matching users detected.",
                font=("Arial", 10),
                text_color=MUTED
            ).pack(
                anchor="w",
                padx=15,
                pady=(2, 12)
            )

    # ==========================================
    # ERROR DISPLAY
    # ==========================================

    def show_scan_error(self, error):

        for widget in self.results_content.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.results_content,
            text="Detection Error",
            font=("Arial", 14, "bold"),
            text_color=RED
        ).pack(
            anchor="w",
            padx=10,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            self.results_content,
            text=str(error),
            font=("Arial", 11),
            text_color=MUTED,
            wraplength=700
        ).pack(
            anchor="w",
            padx=10,
            pady=5
        )
