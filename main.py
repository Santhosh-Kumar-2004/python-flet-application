import flet as ft

def main(page: ft.Page):
    # Set up the window properties
    page.title = "My Flet App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Add a simple text element to the screen
    page.add(ft.Text(value="Environment is ready!", size=30, weight="bold"))

# This launches the app
ft.app(target=main)