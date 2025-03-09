import flet as ft
import bcrypt
from datetime import datetime, timedelta
from models import get_session, User, Device
from components.app_bar import NavBar,Info_SnackBar,Error_SnackBar,Warn_SnackBar
import json
import random

class SmartHomeApp:
    def __init__(self):
        self.session = get_session()
        self.current_user = None
        self.mqtt_client = None

    def route_change(self,route):
        print(route.data)
        if route.data=='/logout': 
            self.page.appbar=None 
            self.username_login.value=''
            self.password_login.value=''                
            self.current_user=""        
            self.show_login()

    def initialize(self, page: ft.Page):
        self.page = page
        self.page.title = "Hello moto"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.spacing = 20
        self.page.on_route_change=self.route_change
        
        self.setup_auth_views()
        self.show_login()

    def setup_auth_views(self):
        # Login View
        self.username_login = ft.TextField(
            label="Username",
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        self.password_login = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        self.login_view = ft.Column(
            controls=[
                ft.Text("Welcome!", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Login to your Dashboard", size=16, color=ft.Colors.GREY_400),
                self.username_login,
                self.password_login,
                ft.ElevatedButton(
                    text="Login",
                    width=300,
                    on_click=self.handle_login
                ),
                ft.TextButton(
                    text="Don't have an account? Register",
                    on_click=lambda _: self.show_register()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Register View
        self.username_register = ft.TextField(
            label="Username",
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        self.password_register = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        self.confirm_password = ft.TextField(
            label="Confirm Password",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        self.register_view = ft.Column(
            controls=[
                ft.Text("Create Account", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Register for Smart Home Access", size=16, color=ft.Colors.GREY_400),
                self.username_register,
                self.password_register,
                self.confirm_password,
                ft.ElevatedButton(
                    text="Register",
                    width=300,
                    on_click=self.handle_register
                ),
                ft.TextButton(
                    text="Already have an account? Login",
                    on_click=lambda _: self.show_login()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
   
    def show_login(self):
        self.page.clean()
        self.page.add(
            ft.Container(
                content=self.login_view,
                alignment=ft.alignment.center,                
            )
        )

    def show_register(self):
        self.page.clean()
        self.page.add(
            ft.Container(
                content=self.register_view,
                alignment=ft.alignment.center
            )
        )

    def show_home(self):
        """Show the home view."""
        self.page.appbar=NavBar(self.page)
        self.page.clean()
        # Add your main page here
        self.page.update()

    def handle_login(self, e):
        user = (
            self.session.query(User)
            .filter_by(username=self.username_login.value)
            .first()
        )
        
        if user and bcrypt.checkpw(
            self.password_login.value.encode('utf-8'),
            user.password_hash
        ):
            self.current_user = user
            self.show_home()
            self.page.open(Info_SnackBar(f"Welcome back, {user.username}!"))            
        else:
            self.page.open(Error_SnackBar("Invalid username or password"))

    def handle_register(self, e):
        if self.password_register.value != self.confirm_password.value:
            self.page.open(Error_SnackBar("Passwords do not match"))
            return

        existing_user = (
            self.session.query(User)
            .filter_by(username=self.username_register.value)
            .first()
        )
        
        if existing_user:
            self.page.open(Warn_SnackBar("Username already exists"))            
            return

        password_hash = bcrypt.hashpw(
            self.password_register.value.encode('utf-8'),
            bcrypt.gensalt()
        )
        
        new_user = User(
            username=self.username_register.value,
            password_hash=password_hash
        )
        self.session.add(new_user)
        self.session.commit()
        
        self.current_user = new_user
        self.show_home()
        self.page.open(Info_SnackBar("Registration successful!"))        

    def handle_logout(self, e):
        self.current_user = None
        self.show_login()
        self.page.open(Info_SnackBar("Logged out successfully"))        


def main(page: ft.Page):

    app = SmartHomeApp()
    app.initialize(page)

if __name__ == "__main__":
    ft.app(target=main)
