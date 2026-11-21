import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from services.audit_service import get_all_audit_logs

BG = "#080F1C"
PANEL = "#111F33"
CARD = "#16263D"
BORDER = "#263B55"
CYAN = "#20D4D0"
GREEN = "#31D69A"
RED = "#FF5B6E"
ORANGE = "#FFB454"
WHITE = "#F1F5F9"
MUTED = "#8496AD"

class AuditLogsView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.all_logs = []
        self.action_filter = "ALL"

        self.create_widgets()
        self.load_logs()

    def create_widgets(self):

        # Page heading
        ctk.CTkLabel(
            self,
            text="Audit Logs",
            font=("Arial", 28, "bold"),
            text_color=WHITE
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            self,
            text="Track user actions and maintain a complete security audit trail.",
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
            "TOTAL RECORDS", CYAN
        )

        self.success_label = self.create_stat_card(
            "LOGIN SUCCESS", GREEN
        )

        self.failed_label = self.create_stat_card(
            "LOGIN FAILURES", RED
        )

        self.other_label = self.create_stat_card(
            "OTHER ACTIONS", ORANGE
        )

        # Main panel
        panel = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        panel.pack(
            fill="both",
            expand=True,
            pady=15
        )

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
            text="Security Audit Trail",
            font=("Arial", 17, "bold"),
            text_color=WHITE
        ).pack(side="left")

        ctk.CTkButton(
            toolbar,
            text="↻ Refresh",
            width=100,
            fg_color="#19384A",
            hover_color="#24546A",
            command=self.load_logs
        ).pack(side="right")

        # Search and filter
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
            placeholder_text="Search action, user ID or details...",
            width=300,
            height=35
        )
        self.search_entry.pack(
            side="left",
            padx=(0, 12)
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        self.filter_control = ctk.CTkOptionMenu(
            controls,
            values=["ALL"],
            width=170,
            height=35,
            fg_color="#19384A",
            button_color="#24546A",
            button_hover_color="#326B82",
            command=self.change_filter
        )
        self.filter_control.pack(side="left")

        # Table
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
            "ID",
            "ACTOR ID",
            "ACTION",
            "TARGET TYPE",
            "TARGET ID",
            "DETAILS",
            "TIMESTAMP"
        )

        style = ttk.Style()

        style.configure(
            "Audit.Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=40,
            font=("Arial", 10)
        )

        style.configure(
            "Audit.Treeview.Heading",
            background="#193047",
            foreground=CYAN,
            font=("Arial", 10, "bold")
        )

        style.map(
            "Audit.Treeview",
            background=[("selected", "#24546A")],
            foreground=[("selected", WHITE)]
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Audit.Treeview"
        )

        widths = {
            "ID": 55,
            "ACTOR ID": 80,
            "ACTION": 145,
            "TARGET TYPE": 115,
            "TARGET ID": 85,
            "DETAILS": 270,
            "TIMESTAMP": 180
        }

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        # Scrollbars
        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.table.tag_configure(
            "success",
            foreground=GREEN
        )

        self.table.tag_configure(
            "failed",
            foreground=RED
        )

        self.table.tag_configure(
            "other",
            foreground=ORANGE
        )

        # Footer
        self.record_count = ctk.CTkLabel(
            self,
            text="Showing 0 records",
            font=("Arial", 10),
            text_color=MUTED
        )

        self.record_count.pack(
            anchor="w",
            pady=(0, 8)
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

    def load_logs(self):

        try:
            logs = get_all_audit_logs()

            if logs is None or logs is False:
                raise RuntimeError("Unable to retrieve audit records.")

            self.all_logs = logs

            # Calculate summary statistics
            total = len(logs)

            successful = sum(
                1 for log in logs
                if log[2] == "LOGIN_SUCCESS"
            )

            failed = sum(
                1 for log in logs
                if log[2] in ("LOGIN_FAILED", "LOGIN_BLOCKED")
            )

            other = total - successful - failed

            self.total_label.configure(text=str(total))
            self.success_label.configure(text=str(successful))
            self.failed_label.configure(text=str(failed))
            self.other_label.configure(text=str(other))

            # Get actual action names from database
            actions = sorted(set(
                log[2] for log in logs if log[2]
            ))

            self.filter_control.configure(
                values=["ALL"] + actions
            )

            if self.action_filter not in ["ALL"] + actions:
                self.action_filter = "ALL"

            self.filter_control.set(self.action_filter)

            self.apply_filters()

        except Exception as e:
            print("Audit Log Error:", e)

            messagebox.showerror(
                "Database Error",
                "Unable to load audit logs."
            )

    def change_filter(self, selected):

        self.action_filter = selected
        self.apply_filters()

    def apply_filters(self):

        # Clear existing table rows
        for item in self.table.get_children():
            self.table.delete(item)

        search_text = self.search_entry.get().strip().lower()

        displayed = 0

        for log in self.all_logs:

            audit_id = log[0]
            actor_id = log[1]
            action = log[2]
            target_type = log[3]
            target_id = log[4]
            details = log[5]
            timestamp = log[6]

            # Apply action filter
            if self.action_filter != "ALL":
                if action != self.action_filter:
                    continue

            # Search across ALL audit log fields
            searchable = " ".join(
                str(value) for value in log
                if value is not None
            ).lower()

            if search_text and search_text not in searchable:
                continue

            if hasattr(timestamp, "strftime"):
                timestamp = timestamp.strftime(
                    "%d %b %Y, %I:%M %p"
                )

            if action == "LOGIN_SUCCESS":
                tag = "success"
            elif action in ("LOGIN_FAILED", "LOGIN_BLOCKED"):
                tag = "failed"
            else:
                tag = "other"

            self.table.insert(
                "",
                "end",
                values=(
                    audit_id,
                    actor_id if actor_id is not None else "-",
                    action,
                    target_type,
                    target_id,
                    details,
                    timestamp
                ),
                tags=(tag,)
            )

            displayed += 1

        self.record_count.configure(
            text=f"Showing {displayed} of {len(self.all_logs)} records"
        )

