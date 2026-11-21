import customtkinter as ctk
from tkinter import ttk, messagebox

from services.alert_service import (
    get_all_alerts,
    update_alert_status,
    delete_alert
)

BG = "#080F1C"
PANEL = "#111F33"
CARD = "#16263D"
BORDER = "#263B55"
CYAN = "#20D4D0"
RED = "#FF5B6E"
ORANGE = "#FFB454"
GREEN = "#31D69A"
WHITE = "#F1F5F9"
MUTED = "#8496AD"


class AlertsView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.create_widgets()
        self.load_alerts()

    def create_widgets(self):

        # Heading
        ctk.CTkLabel(
            self,
            text="Security Alerts",
            font=("Arial", 28, "bold"),
            text_color=WHITE
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            self,
            text="Monitor, investigate and manage detected threats.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Summary cards
        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.summary_frame.pack(fill="x", pady=10)

        self.new_label = self.create_stat_card(
            "NEW ALERTS", CYAN
        )

        self.investigating_label = self.create_stat_card(
            "INVESTIGATING", ORANGE
        )

        self.resolved_label = self.create_stat_card(
            "RESOLVED", GREEN
        )

        self.dismissed_label = self.create_stat_card(
            "DISMISSED", RED
        )

        # Alert table panel
        table_panel = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )
        table_panel.pack(
            fill="both",
            expand=True,
            pady=15
        )

        # Table heading
        heading_frame = ctk.CTkFrame(
            table_panel,
            fg_color="transparent"
        )
        heading_frame.pack(
            fill="x",
            padx=18,
            pady=15
        )

        ctk.CTkLabel(
            heading_frame,
            text="Detected Threats",
            font=("Arial", 17, "bold"),
            text_color=WHITE
        ).pack(side="left")

        ctk.CTkButton(
            heading_frame,
            text="↻ Refresh",
            width=100,
            fg_color="#19384A",
            hover_color="#24546A",
            command=self.load_alerts
        ).pack(side="right")

        # Table
        columns = (
            "ID",
            "RULE",
            "SEVERITY",
            "DESCRIPTION",
            "USER ID",
            "STATUS"
        )

        style = ttk.Style()

        style.configure(
            "Sentinel.Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=38,
            font=("Arial", 10)
        )

        style.configure(
            "Sentinel.Treeview.Heading",
            background="#193047",
            foreground=CYAN,
            font=("Arial", 10, "bold")
        )

        style.map(
            "Sentinel.Treeview",
            background=[("selected", "#24546A")],
            foreground=[("selected", WHITE)]
        )

        self.table = ttk.Treeview(
            table_panel,
            columns=columns,
            show="headings",
            style="Sentinel.Treeview"
        )

        widths = {
            "ID": 55,
            "RULE": 145,
            "SEVERITY": 85,
            "DESCRIPTION": 300,
            "USER ID": 75,
            "STATUS": 120
        }

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # Action buttons
        action_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        action_frame.pack(
            fill="x",
            pady=10
        )

        ctk.CTkButton(
            action_frame,
            text="Investigate",
            fg_color="#B66A20",
            hover_color="#94531A",
            command=lambda: self.change_status("investigating")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            action_frame,
            text="Resolve",
            fg_color="#168B68",
            hover_color="#106C50",
            command=lambda: self.change_status("resolved")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            action_frame,
            text="Dismiss",
            fg_color="#475569",
            hover_color="#334155",
            command=lambda: self.change_status("dismissed")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            action_frame,
            text="Delete",
            fg_color="#A52C40",
            hover_color="#7F2030",
            command=self.remove_alert
        ).pack(side="right", padx=5)

    def create_stat_card(self, title, color):

        card = ctk.CTkFrame(
            self.summary_frame,
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
        ).pack(anchor="w", padx=14, pady=(14, 5))

        value_label = ctk.CTkLabel(
            card,
            text="0",
            font=("Arial", 26, "bold"),
            text_color=color
        )

        value_label.pack(anchor="w", padx=14, pady=(0, 14))

        return value_label

    def load_alerts(self):

        for item in self.table.get_children():
            self.table.delete(item)

        alerts = get_all_alerts()

        if alerts is False:
            messagebox.showerror(
                "Database Error",
                "Unable to load security alerts."
            )
            return

        counts = {
            "new": 0,
            "investigating": 0,
            "resolved": 0,
            "dismissed": 0
        }

        for alert in alerts:

            alert_id = alert[0]
            rule_code = alert[1]
            severity = alert[2]
            description = alert[3]
            user_id = alert[4]
            status = alert[6]

            counts[status] = counts.get(status, 0) + 1

            self.table.insert(
                "",
                "end",
                values=(
                    alert_id,
                    rule_code,
                    severity.upper(),
                    description,
                    user_id if user_id is not None else "-",
                    status.upper()
                ),
                tags=(severity,)
            )

        self.new_label.configure(text=str(counts["new"]))
        self.investigating_label.configure(
            text=str(counts["investigating"])
        )
        self.resolved_label.configure(text=str(counts["resolved"]))
        self.dismissed_label.configure(text=str(counts["dismissed"]))

    def get_selected_alert(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an alert first."
            )
            return None

        values = self.table.item(selected[0], "values")

        return values[0]

    def change_status(self, new_status):

        alert_id = self.get_selected_alert()

        if alert_id is None:
            return

        success = update_alert_status(
            int(alert_id),
            new_status
        )

        if success:
            messagebox.showinfo(
                "Sentinel",
                "Alert status updated successfully."
            )
            self.load_alerts()
        else:
            messagebox.showerror(
                "Error",
                "Unable to update alert status."
            )

    def remove_alert(self):

        alert_id = self.get_selected_alert()

        if alert_id is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to permanently delete this alert?"
        )

        if confirm:

            if delete_alert(int(alert_id)):
                messagebox.showinfo(
                    "Sentinel",
                    "Alert deleted successfully."
                )
                self.load_alerts()
            else:
                messagebox.showerror(
                    "Error",
                    "Unable to delete alert."
                )
