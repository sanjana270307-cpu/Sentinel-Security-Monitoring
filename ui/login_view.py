
import customtkinter as ctk


# SENTINEL COLOUR PALETTE
BG = "#080F1C"
SIDEBAR = "#0D1728"
PANEL = "#111F33"
CARD = "#16263D"
BORDER = "#263B55"

CYAN = "#20D4D0"
BLUE = "#438BFF"
GREEN = "#31D69A"
RED = "#FF5B6E"

WHITE = "#F1F5F9"
MUTED = "#8496AD"


class LoginView(ctk.CTkFrame):

    def __init__(self, master, on_login, on_signup=None):

        super().__init__(
            master,
            fg_color=BG
        )

        self.on_login = on_login
        self.on_signup = on_signup

        self.current_mode = "login"

        self.login_button = None
        self.signup_button = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_login()

    # ==========================================
    # MAIN SPLIT SCREEN
    # ==========================================

    def create_layout(self):

        for widget in self.winfo_children():
            widget.destroy()

        self.grid_columnconfigure(0, weight=11)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        # LEFT BRANDING PANEL

        self.left_panel = ctk.CTkFrame(
            self,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(1, weight=1)

        # BRAND

        brand_frame = ctk.CTkFrame(
            self.left_panel,
            fg_color="transparent"
        )

        brand_frame.pack(
            anchor="w",
            padx=55,
            pady=(45, 0)
        )

        ctk.CTkLabel(
            brand_frame,
            text="◈",
            font=("Arial", 36, "bold"),
            text_color=CYAN
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            brand_frame,
            text="SENTINEL",
            font=("Arial", 27, "bold"),
            text_color=WHITE
        ).pack(side="left")

        ctk.CTkLabel(
            self.left_panel,
            text="SECURITY OPERATIONS CENTER",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=105,
            pady=(0, 10)
        )

        # MAIN BRAND CONTENT

        content = ctk.CTkFrame(
            self.left_panel,
            fg_color="transparent"
        )

        content.pack(
            expand=True,
            fill="both",
            padx=55,
            pady=20
        )

        ctk.CTkLabel(
            content,
            text="Your security.\nOur priority.",
            font=("Arial", 37, "bold"),
            text_color=WHITE,
            justify="left"
        ).pack(
            anchor="w",
            pady=(30, 15)
        )

        ctk.CTkLabel(
            content,
            text=(
                "Monitor your environment, detect suspicious "
                "behaviour and stay ahead of potential threats."
            ),
            font=("Arial", 14),
            text_color=MUTED,
            justify="left",
            wraplength=390
        ).pack(
            anchor="w",
            pady=(0, 35)
        )

        # SECURITY STATUS CARD

        status_card = ctk.CTkFrame(
            content,
            fg_color=PANEL,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )

        status_card.pack(
            fill="x",
            pady=10
        )

        ctk.CTkLabel(
            status_card,
            text="SYSTEM STATUS",
            font=("Arial", 10, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        status_row = ctk.CTkFrame(
            status_card,
            fg_color="transparent"
        )

        status_row.pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

        ctk.CTkLabel(
            status_row,
            text="●",
            font=("Arial", 17),
            text_color=GREEN
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            status_row,
            text="SECURITY MONITORING ACTIVE",
            font=("Arial", 11, "bold"),
            text_color=WHITE
        ).pack(side="left")

        # FEATURES

        features = [
            ("◈", "Intelligent Threat Detection"),
            ("⌁", "Real-time Activity Monitoring"),
            ("✓", "Secure Access Management")
        ]

        for symbol, feature in features:

            row = ctk.CTkFrame(
                content,
                fg_color="transparent"
            )

            row.pack(
                anchor="w",
                pady=9
            )

            ctk.CTkLabel(
                row,
                text=symbol,
                font=("Arial", 17, "bold"),
                text_color=CYAN,
                width=28
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=feature,
                font=("Arial", 12),
                text_color="#CBD5E1"
            ).pack(side="left")

        # FOOTER

        ctk.CTkLabel(
            self.left_panel,
            text="SENTINEL SECURITY  •  VERSION 1.0",
            font=("Arial", 9, "bold"),
            text_color="#52657E"
        ).pack(
            anchor="w",
            padx=55,
            pady=25
        )

        # RIGHT AUTHENTICATION PANEL

        self.right_panel = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)

        self.form_container = ctk.CTkFrame(
            self.right_panel,
            fg_color="transparent"
        )

        self.form_container.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=55,
            pady=35
        )

        self.form_container.grid_columnconfigure(0, weight=1)

    # ==========================================
    # INPUT FIELD
    # ==========================================

    def create_input(self, label, placeholder, show=None):

        ctk.CTkLabel(
            self.form_container,
            text=label,
            font=("Arial", 11, "bold"),
            text_color="#CBD5E1"
        ).pack(
            anchor="w",
            pady=(12, 7)
        )

        entry = ctk.CTkEntry(
            self.form_container,
            height=48,
            corner_radius=9,
            placeholder_text=placeholder,
            fg_color=PANEL,
            border_color=BORDER,
            text_color=WHITE,
            placeholder_text_color="#64748B",
            show=show,
            font=("Arial", 13)
        )

        entry.pack(
            fill="x"
        )

        return entry

    # ==========================================
    # ERROR MESSAGE
    # ==========================================

    def create_error_label(self):

        self.error_label = ctk.CTkLabel(
            self.form_container,
            text="",
            font=("Arial", 11),
            text_color=RED,
            wraplength=350
        )

        self.error_label.pack(
            anchor="w",
            pady=(10, 0)
        )

    # ==========================================
    # LOGIN SCREEN
    # ==========================================

    def show_login(self):

        self.current_mode = "login"

        self.create_layout()

        ctk.CTkLabel(
            self.form_container,
            text="Welcome back!",
            font=("Arial", 31, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            pady=(30, 5)
        )

        ctk.CTkLabel(
            self.form_container,
            text="Sign in to continue to your workspace.",
            font=("Arial", 13),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        self.username_entry = self.create_input(
            "USERNAME",
            "Enter your username"
        )

        self.password_entry = self.create_input(
            "PASSWORD",
            "Enter your password",
            show="*"
        )

        # PASSWORD OPTIONS

        options = ctk.CTkFrame(
            self.form_container,
            fg_color="transparent"
        )

        options.pack(
            fill="x",
            pady=(13, 5)
        )

        self.show_password = ctk.CTkCheckBox(
            options,
            text="Show password",
            font=("Arial", 11),
            text_color=MUTED,
            fg_color=CYAN,
            hover_color="#0E7490",
            checkbox_width=17,
            checkbox_height=17,
            command=self.toggle_password
        )

        self.show_password.pack(
            side="left"
        )

        self.create_error_label()

        self.login_button = ctk.CTkButton(
            self.form_container,
            text="SIGN IN  →",
            height=49,
            corner_radius=9,
            fg_color="#0891B2",
            hover_color="#0E7490",
            font=("Arial", 13, "bold"),
            text_color="white",
            command=self.submit_login
        )

        self.login_button.pack(
            fill="x",
            pady=(20, 15)
        )

        ctk.CTkLabel(
            self.form_container,
            text="Don't have an account?",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkButton(
            self.form_container,
            text="CREATE AN ANALYST ACCOUNT",
            height=42,
            corner_radius=9,
            fg_color=CARD,
            hover_color="#19384A",
            border_width=1,
            border_color=BORDER,
            text_color=CYAN,
            font=("Arial", 11, "bold"),
            command=self.show_signup
        ).pack(
            fill="x"
        )

        self.username_entry.bind(
            "<Return>",
            lambda event: self.password_entry.focus()
        )

        self.password_entry.bind(
            "<Return>",
            lambda event: self.submit_login()
        )

        self.username_entry.focus()

    # ==========================================
    # SIGNUP SCREEN
    # ==========================================

    def show_signup(self):

        self.current_mode = "signup"

        self.create_layout()

        ctk.CTkLabel(
            self.form_container,
            text="Create account",
            font=("Arial", 30, "bold"),
            text_color=WHITE
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self.form_container,
            text="Join the Sentinel security operations team.",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        self.signup_username = self.create_input(
            "USERNAME",
            "Choose a username"
        )

        self.signup_password = self.create_input(
            "PASSWORD",
            "Create a password",
            show="*"
        )

        self.confirm_password = self.create_input(
            "CONFIRM PASSWORD",
            "Re-enter your password",
            show="*"
        )

        # ROLE DISPLAY

        ctk.CTkLabel(
            self.form_container,
            text="ACCOUNT TYPE",
            font=("Arial", 11, "bold"),
            text_color="#CBD5E1"
        ).pack(
            anchor="w",
            pady=(15, 7)
        )

        role_frame = ctk.CTkFrame(
            self.form_container,
            fg_color=PANEL,
            corner_radius=9,
            border_width=1,
            border_color=BORDER,
            height=45
        )

        role_frame.pack(
            fill="x"
        )

        role_frame.pack_propagate(False)

        ctk.CTkLabel(
            role_frame,
            text="ANALYST",
            font=("Arial", 12, "bold"),
            text_color=CYAN
        ).pack(
            side="left",
            padx=15
        )

        ctk.CTkLabel(
            role_frame,
            text="Standard access",
            font=("Arial", 11),
            text_color=MUTED
        ).pack(
            side="right",
            padx=15
        )

        ctk.CTkLabel(
            self.form_container,
            text="Admin accounts are created by authorised administrators.",
            font=("Arial", 10),
            text_color=MUTED,
            wraplength=350
        ).pack(
            anchor="w",
            pady=(8, 0)
        )

        self.create_error_label()

        self.signup_button = ctk.CTkButton(
            self.form_container,
            text="CREATE ACCOUNT  →",
            height=49,
            corner_radius=9,
            fg_color="#0891B2",
            hover_color="#0E7490",
            font=("Arial", 13, "bold"),
            text_color="white",
            command=self.submit_signup
        )

        self.signup_button.pack(
            fill="x",
            pady=(15, 10)
        )

        ctk.CTkButton(
            self.form_container,
            text="← BACK TO SIGN IN",
            height=40,
            corner_radius=9,
            fg_color="transparent",
            hover_color=CARD,
            text_color=CYAN,
            font=("Arial", 11, "bold"),
            command=self.show_login
        ).pack(
            fill="x",
            pady=(5, 0)
        )

        self.signup_username.bind(
            "<Return>",
            lambda event: self.signup_password.focus()
        )

        self.signup_password.bind(
            "<Return>",
            lambda event: self.confirm_password.focus()
        )

        self.confirm_password.bind(
            "<Return>",
            lambda event: self.submit_signup()
        )

        self.signup_username.focus()

    # ==========================================
    # PASSWORD VISIBILITY
    # ==========================================

    def toggle_password(self):

        if self.show_password.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    # ==========================================
    # LOGIN VALIDATION
    # ==========================================

    def submit_login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:

            self.show_error(
                "Please enter both username and password."
            )

            return

        self.error_label.configure(text="")

        self.on_login(username, password)

    # ==========================================
    # SIGNUP VALIDATION
    # ==========================================

    def submit_signup(self):

        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        confirm = self.confirm_password.get()

        if not username or not password or not confirm:

            self.show_error(
                "Please complete all fields."
            )

            return

        if len(username) < 3:

            self.show_error(
                "Username must contain at least 3 characters."
            )

            return

        if len(password) < 8:

            self.show_error(
                "Password must contain at least 8 characters."
            )

            return

        if password != confirm:

            self.show_error(
                "Passwords do not match."
            )

            self.confirm_password.delete(0, "end")
            self.confirm_password.focus()

            return

        if not self.on_signup:

            self.show_error(
                "Signup is not connected yet."
            )

            return

        self.error_label.configure(text="")

        self.on_signup(username, password)

    # ==========================================
    # ERROR DISPLAY
    # ==========================================

    def show_error(self, message):

        self.error_label.configure(
            text=message
        )

    # ==========================================
    # LOADING STATE
    # ==========================================

    def set_loading(self, loading):

        if self.current_mode == "login" and self.login_button:

            if loading:

                self.login_button.configure(
                    state="disabled",
                    text="SIGNING IN..."
                )

            else:

                self.login_button.configure(
                    state="normal",
                    text="SIGN IN  →"
                )

        elif self.current_mode == "signup" and self.signup_button:

            if loading:

                self.signup_button.configure(
                    state="disabled",
                    text="CREATING ACCOUNT..."
                )

            else:

                self.signup_button.configure(
                    state="normal",
                    text="CREATE ACCOUNT  →"
                )
