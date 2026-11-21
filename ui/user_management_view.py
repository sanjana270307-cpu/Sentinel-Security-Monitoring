import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

from services.user_service import (
    get_all_users,
    unlock_user,
    update_user_role
)

class UserManagementView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.all_users = []

        self.create_widgets()
        self.load_users()

    def create_widgets(self):

        heading = ctk.CTkLabel(
            self,
            text="User Management",
            font=("Arial", 26, "bold")
        )
        heading.pack(anchor="w", padx=25, pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Monitor registered users and manage account access",
            text_color="gray"
        )
        subtitle.pack(anchor="w", padx=25, pady=(0, 20))

        # Summary cards
        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.pack(fill="x", padx=25, pady=10)

        self.total_label = self.create_card(
            cards, "TOTAL USERS", "0"
        )
        self.admin_label = self.create_card(
            cards, "ADMINISTRATORS", "0"
        )
        self.locked_label = self.create_card(
            cards, "LOCKED ACCOUNTS", "0"
        )
        self.analyst_label = self.create_card(
            cards, "ANALYSTS", "0"
        )

        # Search and refresh
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=25, pady=15)

        self.search_entry = ctk.CTkEntry(
            controls,
            placeholder_text="Search username or user ID...",
            width=280,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 12))

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        refresh_btn = ctk.CTkButton(
            controls,
            text="Refresh",
            width=100,
            command=self.load_users
        )
        refresh_btn.pack(side="left")

        # Table
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 15)
        )

        columns = (
            "ID", "USERNAME", "ROLE",
            "FAILED ATTEMPTS", "ACCOUNT STATUS", "LOCKED UNTIL"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14
        )

        widths = [60, 150, 110, 140, 150, 180]

        for col, width in zip(columns, widths):
            self.table.heading(col, text=col)
            self.table.column(
                col,
                width=width,
                anchor="center"
            )

        self.table.tag_configure(
            "locked",
            foreground="#FF6464"
        )

        self.table.tag_configure(
            "active",
            foreground="#38D9A9"
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
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10
        )

        # Actions
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=25, pady=(0, 20))

        unlock_btn = ctk.CTkButton(
            actions,
            text="Unlock Account",
            fg_color="#168A70",
            hover_color="#106B57",
            command=self.handle_unlock
        )
        unlock_btn.pack(side="left", padx=(0, 10))

        role_btn = ctk.CTkButton(
            actions,
            text="Change Role",
            command=self.handle_role_change
        )
        role_btn.pack(side="left")

        self.record_count = ctk.CTkLabel(
            actions,
            text="Showing 0 users",
            text_color="gray"
        )
        self.record_count.pack(side="right")

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            corner_radius=12
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="gray",
            font=("Arial", 11, "bold")
        ).pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 25, "bold")
        )
        value_label.pack(pady=(0, 15))

        return value_label

    def load_users(self):

        self.all_users = get_all_users()

        total = len(self.all_users)
        admins = sum(1 for user in self.all_users
            if user["role"].lower() == "admin")

        analysts = sum(1 for user in self.all_users
            if user["role"].lower() == "analyst")

        locked = sum(
            1 for user in self.all_users
            if user["locked_until"] is not None
            and user["locked_until"] > datetime.now()
        )

        self.total_label.configure(text=str(total))
        self.admin_label.configure(text=str(admins))
        self.analyst_label.configure(text=str(analysts))
        self.locked_label.configure(text=str(locked))

        self.apply_filters()

    def apply_filters(self):

        for item in self.table.get_children():
            self.table.delete(item)

        search = self.search_entry.get().strip().lower()
        displayed = 0

        for user in self.all_users:

            user_id = user["user_id"]
            username = user["username"]
            role = user["role"]
            failed = user["failed_attempts"]
            locked_until = user["locked_until"]

            if search not in str(user_id).lower() and search not in username.lower():
                continue

            is_locked = (
                locked_until is not None
                and locked_until > datetime.now()
            )

            status = "LOCKED" if is_locked else "ACTIVE"

            if locked_until is not None:
                lock_text = locked_until.strftime(
                    "%d %b %Y, %I:%M %p"
                )
            else:
                lock_text = "—"

            tag = "locked" if is_locked else "active"

            self.table.insert(
                "",
                "end",
                values=(
                    user_id,
                    username,
                    role,
                    failed,
                    status,
                    lock_text
                ),
                tags=(tag,)
            )

            displayed += 1

        self.record_count.configure(
            text=f"Showing {displayed} of {len(self.all_users)} users"
        )

    def get_selected_user_id(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a user first."
            )
            return None

        values = self.table.item(selected[0], "values")

        return int(values[0])

    def handle_unlock(self):

        user_id = self.get_selected_user_id()

        if user_id is None:
            return

        if not messagebox.askyesno(
            "Confirm Unlock",
            "Are you sure you want to unlock this account?"
        ):
            return

        if unlock_user(user_id):
            messagebox.showinfo(
                "Success",
                "Account unlocked successfully."
            )
            self.load_users()
        else:
            messagebox.showwarning(
                "Notice",
                "Account was not updated. It may already be unlocked."
            )

    def handle_role_change(self):

        user_id = self.get_selected_user_id()

        if user_id is None:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Change User Role")
        dialog.geometry("320x200")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Select New Role",
            font=("Arial", 18, "bold")
        ).pack(pady=(25, 15))

        role_menu = ctk.CTkOptionMenu(
            dialog,
            values=["Analyst", "Admin"]
        )
        role_menu.pack(pady=10)

        def save_role():

            new_role = role_menu.get()

            if not messagebox.askyesno(
                "Confirm Role Change",
                f"Change user {user_id}'s role to {new_role}?",
                parent=dialog
            ):
                return

            if update_user_role(user_id, new_role):
                messagebox.showinfo(
                    "Success",
                    "User role updated successfully.",
                    parent=dialog
                )
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showwarning(
                    "Notice",
                    "Role was not changed. It may already have this role.",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="Save Changes",
            command=save_role
        ).pack(pady=15)
