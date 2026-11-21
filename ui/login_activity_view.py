import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from services.activity_service import get_recent_activity

BG = "#080F1C"
PANEL = "#111F33"
CARD = "#16263D"
BORDER = "#263B55"
CYAN = "#20D4D0"
GREEN = "#31D69A"
RED = "#FF5B6E"
WHITE = "#F1F5F9"
MUTED = "#8496AD"

class LoginActivityView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.all_events = []
        self.filter_value = "ALL"

        self.create_widgets()
        self.load_activity()

    def create_widgets(self):

        ctk.CTkLabel(
            self,
            text="Login Activity",
            font=("Arial", 28, "bold"),
            text_color=WHITE
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            self,
            text="Track and investigate authentication events across your system.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Summary cards
        self.stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.stats_frame.pack(fill="x", pady=10)

        self.total_label = self.create_stat_card(
            "TOTAL ATTEMPTS", CYAN
        )

        self.success_label = self.create_stat_card(
            "SUCCESSFUL", GREEN
        )

        self.failed_label = self.create_stat_card(
            "FAILED", RED
        )

        # Main activity panel
        panel = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )
        panel.pack(fill="both", expand=True, pady=15)

        # Toolbar
        toolbar = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        toolbar.pack(
            fill="x",
            padx=18,
            pady=15
        )

        ctk.CTkLabel(
            toolbar,
            text="Authentication Records",
            font=("Arial", 17, "bold"),
            text_color=WHITE
        ).pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="↻ Refresh",
            width=100,
            fg_color="#19384A",
            hover_color="#24546A",
            command=self.load_activity
        ).pack(side="right")

        # Search and filter controls
        controls = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        controls.pack(
            fill="x",
            padx=18,
            pady=(0, 12)
        )

        self.search_entry = ctk.CTkEntry(
            controls,
            placeholder_text="Search username...",
            width=220,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 12))

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        self.filter_control = ctk.CTkSegmentedButton(
            controls,
            values=["ALL", "SUCCESS", "FAILED"],
            command=self.change_filter
        )
        self.filter_control.set("ALL")
        self.filter_control.pack(side="left")

        # Table area
        table_frame = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columns = (
            "USERNAME",
            "STATUS",
            "TIMESTAMP",
            "REASON",
            "SOURCE"
        )

        style = ttk.Style()

        style.configure(
            "Login.Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=40,
            font=("Arial", 10)
        )

        style.configure(
            "Login.Treeview.Heading",
            background="#193047",
            foreground=CYAN,
            font=("Arial", 10, "bold")
        )

        style.map(
            "Login.Treeview",
            background=[("selected", "#24546A")],
            foreground=[("selected", WHITE)]
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Login.Treeview"
        )

        widths = {
            "USERNAME": 150,
            "STATUS": 110,
            "TIMESTAMP": 190,
            "REASON": 250,
            "SOURCE": 130
        }

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.tag_configure(
            "success",
            foreground=GREEN
        )

        self.table.tag_configure(
            "failed",
            foreground=RED
        )

    def create_stat_card(self, title, color):

        card = ctk.CTkFrame(
            self.stats_frame,
            fg_color=CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=14,
            pady=(14, 5)
        )

        value = ctk.CTkLabel(
            card,
            text="0",
            font=("Arial", 26, "bold"),
            text_color=color
        )

        value.pack(
            anchor="w",
            padx=14,
            pady=(0, 14)
        )

        return value

    def load_activity(self):

        try:
            self.all_events = get_recent_activity(200)

            if self.all_events is False:
                raise RuntimeError("Unable to retrieve login records.")

            successful = sum(
                1 for event in self.all_events
                if event["success"] == 1
            )

            failed = len(self.all_events) - successful

            self.total_label.configure(
                text=str(len(self.all_events))
            )

            self.success_label.configure(
                text=str(successful)
            )

            self.failed_label.configure(
                text=str(failed)
            )

            self.apply_filters()

        except Exception as e:
            print("Login Activity Error:", e)

            messagebox.showerror(
                "Database Error",
                "Unable to load login activity."
            )

    def change_filter(self, selected_filter):

        self.filter_value = selected_filter
        self.apply_filters()

    def apply_filters(self):

        for item in self.table.get_children():
            self.table.delete(item)

        search_text = self.search_entry.get().strip().lower()

        for event in self.all_events:

            success = event["success"] == 1

            status = "SUCCESS" if success else "FAILED"

            if self.filter_value != "ALL":
                if status != self.filter_value:
                    continue

            username = event["attempted_username"] or "Unknown"

            if search_text not in username.lower():
                continue

            timestamp = event["event_time"]

            if hasattr(timestamp, "strftime"):
                timestamp = timestamp.strftime("%d %b %Y, %I:%M %p")

            reason = (
                "Login successful"
                if success
                else event["failure_reason"] or "Failure reason unavailable"
            )

            source = event["source_label"] or "-"

            self.table.insert(
                "",
                "end",
                values=(
                    username,
                    status,
                    str(timestamp),
                    reason,
                    source
                ),
                tags=("success" if success else "failed",)
            )
