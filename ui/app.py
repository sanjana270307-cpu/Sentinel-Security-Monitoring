import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import login_user, register_user
from ui.login_view import LoginView
from ui.dashboard_view import DashboardView
from ui.alerts_view import AlertsView
from ui.login_activity_view import LoginActivityView
from ui.audit_logs_view import AuditLogsView
from ui.user_management_view import UserManagementView
from ui.threat_detection_view import ThreatDetectionView

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


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SentinelApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("SENTINEL | Security Operations")
        self.geometry("1350x850")
        self.minsize(1100, 700)
        self.configure(fg_color=BG)
        self.session = None
        self.show_login()


    def show_login(self):

        for widget in self.winfo_children():
            widget.destroy()
        self.configure(menu="")
        self.session = None

        self.login_view = LoginView(
            self,
            on_login=self.authenticate_user,
            on_signup=self.register_account
        )
        self.login_view.pack(
            fill="both",
            expand=True
        )

    def authenticate_user(self, username, password):
        self.login_view.set_loading(True)
        try:

            user = login_user(username, password)

            if not user:

                self.login_view.set_loading(False)

                self.login_view.show_error(
                    "Invalid username/password or account temporarily locked."
                )

                return

            role = str(user.get("role", "")).strip().lower()

            if role not in ("admin", "analyst"):

                self.login_view.set_loading(False)

                self.login_view.show_error(
                    "This account does not have a valid application role."
                )

                return

            self.session = {
                "user_id": user["user_id"],
                "username": user["username"],
                "role": role
            }

            self.open_workspace()

        except Exception as e:

            print("Login error:", e)

            self.login_view.set_loading(False)

            self.login_view.show_error(
                "Unable to authenticate right now. Please check the database connection."
            )

    def register_account(self, username, password):

        self.login_view.set_loading(True)

        try:

            success = register_user(username, password)

            self.login_view.set_loading(False)

            if success:

                messagebox.showinfo(
                    "Registration Successful",
                    "Your Analyst account has been created!\n\nPlease log in."
                )

                self.login_view.show_login()

            else:

                self.login_view.show_error(
                    "Registration failed. This username may already exist."
                )

        except Exception as e:

            print("Registration Error:", e)

            self.login_view.set_loading(False)

            self.login_view.show_error(
                "Unable to create account. Please try again."
            )


    def open_workspace(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.create_menu()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.active_page = "Dashboard"

        self.create_sidebar()
        self.create_main_area()

        self.navigate("Dashboard")

    def create_menu(self):

        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )

        file_menu.add_command(
            label="Refresh Dashboard",
            command=self.show_dashboard
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Logout",
            command=self.logout
        )

        file_menu.add_command(
            label="Exit",
            command=self.destroy
        )

        menu_bar.add_cascade(
            label="File",
            menu=file_menu
        )

        tools_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )

        tools_menu.add_command(
            label="Run Threat Detection",
            command=self.run_detection
        )

        menu_bar.add_cascade(
            label="Tools",
            menu=tools_menu
        )

        help_menu = tk.Menu(
            menu_bar,
            tearoff=0
        )

        help_menu.add_command(
            label="About Sentinel",
            command=lambda: messagebox.showinfo(
                "About Sentinel",
                "Sentinel Security Operations Platform\nVersion 1.0"
            )
        )

        menu_bar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.configure(menu=menu_bar)

    def run_detection(self):

        self.navigate("Threat Detection")

        self.after(
            200,
            lambda: self.threat_detection_view.start_scan()
            if hasattr(self, "threat_detection_view")
            else None
        )

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=245,
            fg_color=SIDEBAR,
            corner_radius=0,
            border_width=1,
            border_color=BORDER
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)
        brand = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand.pack(
            fill="x",
            padx=22,
            pady=(30, 35)
        )

        ctk.CTkLabel(
            brand,
            text="◈",
            font=("Arial", 35, "bold"),
            text_color=CYAN
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            brand,
            text="SENTINEL",
            font=("Arial", 22, "bold"),
            text_color=WHITE
        ).pack(side="left")

        ctk.CTkLabel(
            self.sidebar,
            text="WORKSPACE",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 12)
        )

        self.nav_buttons = {}

        navigation = [
            ("Dashboard", "◫"),
            ("Login Activity", "◷"),
            ("Threat Detection", "⌘"),
            ("Security Alerts", "⚠")
        ]

        if self.session["role"] == "admin":

            navigation.extend([
                ("Audit Logs", "▤"),
                ("User Management", "♙")
            ])

        for page, symbol in navigation:

            button = ctk.CTkButton(
                self.sidebar,
                text=f"   {symbol}     {page}",
                height=46,
                corner_radius=10,
                anchor="w",
                font=("Arial", 13),
                fg_color="transparent",
                hover_color=CARD,
                text_color=MUTED,
                command=lambda p=page: self.navigate(p)
            )

            button.pack(
                fill="x",
                padx=15,
                pady=4
            )

            self.nav_buttons[page] = button

        self.sidebar_bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color=PANEL,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        self.sidebar_bottom.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        ctk.CTkLabel(
            self.sidebar_bottom,
            text="SIGNED IN AS",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=15,
            pady=(13, 4)
        )

        ctk.CTkLabel(
            self.sidebar_bottom,
            text=self.session["username"],
            font=("Arial", 14, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 3)
        )

        ctk.CTkLabel(
            self.sidebar_bottom,
            text=self.session["role"].upper(),
            font=("Arial", 10, "bold"),
            text_color=CYAN
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            self.sidebar_bottom,
            text="●  Monitoring Ready",
            font=("Arial", 11, "bold"),
            text_color=GREEN
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        ctk.CTkButton(
            self.sidebar_bottom,
            text="LOG OUT",
            height=35,
            fg_color="#26384F",
            hover_color="#394F6B",
            text_color=WHITE,
            font=("Arial", 11, "bold"),
            command=self.logout
        ).pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

    def create_main_area(self):

        self.main_area = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_area.grid_rowconfigure(
            1,
            weight=1
        )

        self.topbar = ctk.CTkFrame(
            self.main_area,
            height=75,
            fg_color=PANEL,
            corner_radius=0,
            border_width=1,
            border_color=BORDER
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.topbar.grid_columnconfigure(
            0,
            weight=1
        )

        self.page_title = ctk.CTkLabel(
            self.topbar,
            text="Dashboard",
            font=("Arial", 21, "bold"),
            text_color=WHITE
        )

        self.page_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=30,
            pady=20
        )

        ctk.CTkLabel(
            self.topbar,
            text="● SYSTEM ONLINE",
            font=("Arial", 11, "bold"),
            text_color=GREEN
        ).grid(
            row=0,
            column=1,
            padx=25
        )
        self.content = ctk.CTkScrollableFrame(
            self.main_area,
            fg_color=BG,
            corner_radius=0
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=20
        )

    def navigate(self, page):

        admin_only_pages = [
            "Audit Logs",
            "User Management"
        ]

        if (
            page in admin_only_pages
            and self.session["role"] != "admin"
        ):

            messagebox.showwarning(
                "Access Denied",
                "This section is available to Admin users only."
            )

            return

        if page not in self.nav_buttons:
            return

        self.active_page = page
        for name, button in self.nav_buttons.items():

            if name == page:

                button.configure(
                    fg_color="#19384A",
                    text_color=CYAN
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color=MUTED
                )

        self.page_title.configure(text=page)

        self.clear_content()

        if page == "Dashboard":

            self.show_dashboard()

        elif page == "Security Alerts":

            self.alerts_view = AlertsView(self.content)

            self.alerts_view.pack(
                fill="both",
                expand=True
            )

        elif page == "Login Activity":

            self.login_activity_view = LoginActivityView(
                self.content
            )

            self.login_activity_view.pack(
                fill="both",
                expand=True
            )

        elif page == "Audit Logs":

            self.audit_logs_view = AuditLogsView(
                self.content
            )

            self.audit_logs_view.pack(
                fill="both",
                expand=True
            )

        elif page == "User Management":

            self.user_management_view = UserManagementView(
                self.content
            )

            self.user_management_view.pack(
                fill="both",
                expand=True
            )
        
        elif page == "Threat Detection":

            self.threat_detection_view = ThreatDetectionView(
                self.content
            )

            self.threat_detection_view.pack(
                fill="both",
                expand=True
            )

        else:

            self.show_placeholder(page)

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        if not self.session:
            return

        self.clear_content()

        self.dashboard_view = DashboardView(
            self.content
        )

        self.dashboard_view.pack(
            fill="both",
            expand=True
        )

    def show_placeholder(self, page):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text=page,
            font=("Arial", 28, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            pady=(15, 10)
        )

        ctk.CTkLabel(
            self.content,
            text=f"The {page} module will be connected to the Sentinel backend.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=10
        )

        ctk.CTkLabel(
            self.content,
            text="MODULE UNDER DEVELOPMENT",
            font=("Arial", 11, "bold"),
            text_color=CYAN
        ).pack(
            anchor="w",
            pady=20
        )

    def logout(self):

        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out of Sentinel?"
        )

        if confirm:
            self.show_login()

if __name__ == "__main__":

    app = SentinelApp()
    app.mainloop()
