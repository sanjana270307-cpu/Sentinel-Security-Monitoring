import customtkinter as ctk
from services.dashboard_service import get_dashboard_stats
from services.activity_service import get_recent_activity

BG = "#080F1C"
SIDEBAR = "#0D1728"
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


class DashboardView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.create_dashboard()

    def create_dashboard(self):
        try:
            dashboard_stats = get_dashboard_stats()
        except Exception as e:
            print("Dashboard Error:", e)
            dashboard_stats = None

        try:
            recent_activity = get_recent_activity(10)
        except Exception as e:
            print("Activity Error:", e)
            recent_activity = []
        ctk.CTkLabel(
            self,
            text="Security Overview",
            font=("Arial", 29, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self,
            text="Monitor your environment and stay ahead of potential threats.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(0, 25)
        )

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        stats_frame.pack(
            fill="x",
            pady=10
        )
        if dashboard_stats:
            stats = [
                (
                    "TOTAL USERS",
                    str(dashboard_stats["total_users"]),
                    "Registered accounts",
                    CYAN
                ),
                (
                    "LOGIN EVENTS",
                    str(dashboard_stats["login_events"]),
                    "Recorded activity",
                    BLUE
                ),
                (
                    "ACTIVE ALERTS",
                    str(dashboard_stats["active_alerts"]),
                    "Awaiting investigation",
                    RED
                ),
                (
                    "THREATS DETECTED",
                    str(dashboard_stats["threats_detected"]),
                    "Total generated alerts",
                    ORANGE
                )
            ]

        else:

            stats = [
                ("TOTAL USERS", "--", "Database unavailable", CYAN),
                ("LOGIN EVENTS", "--", "Database unavailable", BLUE),
                ("ACTIVE ALERTS", "--", "Database unavailable", RED),
                ("THREATS DETECTED", "--", "Database unavailable", ORANGE)
            ]

        for title, value, description, color in stats:

            card = ctk.CTkFrame(
                stats_frame,
                fg_color=CARD,
                corner_radius=14,
                border_width=1,
                border_color=BORDER
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=6
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 10, "bold"),
                text_color=MUTED
            ).pack(
                anchor="w",
                padx=16,
                pady=(18, 8)
            )

            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 30, "bold"),
                text_color=color
            ).pack(
                anchor="w",
                padx=16
            )

            ctk.CTkLabel(
                card,
                text=description,
                font=("Arial", 10),
                text_color=MUTED
            ).pack(
                anchor="w",
                padx=16,
                pady=(5, 18)
            )

        lower_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        lower_frame.pack(
            fill="both",
            expand=True,
            pady=20
        )

        lower_frame.grid_columnconfigure(0, weight=3)
        lower_frame.grid_columnconfigure(1, weight=2)

        threat_panel = ctk.CTkFrame(
            lower_frame,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        threat_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            threat_panel,
            text="Threat Monitoring",
            font=("Arial", 18, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            threat_panel,
            text="Security detection overview",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        threat_types = [
            ("BRUTE FORCE", RED),
            ("SUSPICIOUS LOGIN", ORANGE),
            ("ACCOUNT LOCKOUT", BLUE)
        ]

        for threat, color in threat_types:

            row = ctk.CTkFrame(
                threat_panel,
                fg_color=PANEL,
                corner_radius=9
            )

            row.pack(
                fill="x",
                padx=18,
                pady=6
            )

            ctk.CTkLabel(
                row,
                text="●",
                text_color=color,
                font=("Arial", 15)
            ).pack(
                side="left",
                padx=12,
                pady=13
            )

            ctk.CTkLabel(
                row,
                text=threat,
                font=("Arial", 11, "bold"),
                text_color=WHITE
            ).pack(
                side="left",
                pady=13
            )

            ctk.CTkLabel(
                row,
                text="MONITORED",
                font=("Arial", 9, "bold"),
                text_color=GREEN
            ).pack(
                side="right",
                padx=12
            )

        activity_panel = ctk.CTkFrame(
            lower_frame,
            fg_color=CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER
        )

        activity_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        ctk.CTkLabel(
            activity_panel,
            text="Recent Activity",
            font=("Arial", 18, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            activity_panel,
            text="Latest security events",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        activity_list = ctk.CTkScrollableFrame(
            activity_panel,
            fg_color="transparent",
            height=350
        )

        activity_list.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        if recent_activity:

            for event in recent_activity:

                success = event["success"] == 1

                status = "SUCCESS" if success else "FAILED"
                status_color = GREEN if success else RED

                event_time = event["event_time"]

                if hasattr(event_time, "strftime"):
                    event_time = event_time.strftime(
                        "%d %b, %I:%M %p"
                    )

                activity_row = ctk.CTkFrame(
                    activity_list,
                    fg_color=PANEL,
                    corner_radius=9
                )

                activity_row.pack(
                    fill="x",
                    pady=5,
                    padx=3
                )

                ctk.CTkLabel(
                    activity_row,
                    text=event["attempted_username"],
                    font=("Arial", 11, "bold"),
                    text_color=WHITE
                ).pack(
                    anchor="w",
                    padx=12,
                    pady=(9, 2)
                )

                details_frame = ctk.CTkFrame(
                    activity_row,
                    fg_color="transparent"
                )

                details_frame.pack(
                    fill="x",
                    padx=12,
                    pady=(0, 3)
                )

                ctk.CTkLabel(
                    details_frame,
                    text=str(event_time),
                    font=("Arial", 9),
                    text_color=MUTED
                ).pack(side="left")

                ctk.CTkLabel(
                    details_frame,
                    text=status,
                    font=("Arial", 9, "bold"),
                    text_color=status_color
                ).pack(side="right")

                if not success and event["failure_reason"]:

                    ctk.CTkLabel(
                        activity_row,
                        text=event["failure_reason"],
                        font=("Arial", 9),
                        text_color=RED
                    ).pack(
                        anchor="w",
                        padx=12,
                        pady=(0, 8)
                    )

        else:

            ctk.CTkLabel(
                activity_list,
                text="No login activity found.",
                font=("Arial", 11),
                text_color=MUTED
            ).pack(pady=30)

        ctk.CTkLabel(
            self,
            text="SENTINEL SECURITY  •  THREAT VISIBILITY  •  SYSTEM MONITORING",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(15, 10)
        )
