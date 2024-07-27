import tkinter as tk
from tkinter import messagebox
import os

class ButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button App")

        self.main_buttons = []
        self.sub_buttons = []
        self.click_order = []

        self.create_sub_buttons_placeholder()
        self.create_main_buttons()
        self.create_end_button()

    def create_sub_buttons_placeholder(self):
        # Create placeholders for the sub-buttons
        for i in range(3):
            for j in range(5):
                placeholder = tk.Label(self.root, text="", width=12, height=2)
                placeholder.grid(row=i, column=j, padx=5, pady=5)

    def create_main_buttons(self):
        for i in range(10):
            btn = tk.Button(
                self.root,
                text=f"Button {i+1}",
                command=lambda i=i: self.on_main_button_click(i),
            )
            btn.grid(row=3, column=i, padx=5, pady=5)
            self.main_buttons.append(btn)

    def create_end_button(self):
        end_button = tk.Button(self.root, text="End Round", command=self.end_round)
        end_button.grid(row=3, column=10, padx=5, pady=5)

    def on_main_button_click(self, index):
        self.click_order.append(f"Main Button {index+1}")
        if not self.sub_buttons:
            for i in range(3):
                row_buttons = []
                for j in range(5):
                    btn = tk.Button(
                        self.root,
                        text=f"Sub Button {i*5 + j+1}",
                        command=lambda i=i, j=j: self.on_sub_button_click(i, j),
                    )
                    btn.grid(row=i, column=j, padx=5, pady=5)
                    row_buttons.append(btn)
                self.sub_buttons.append(row_buttons)

    def on_sub_button_click(self, row, col):
        self.click_order.append(f"Sub Button {row*5 + col+1}")
        self.destroy_sub_buttons()

    def destroy_sub_buttons(self):
        for row_buttons in self.sub_buttons:
            for btn in row_buttons:
                btn.destroy()
        self.sub_buttons = []

    def end_round(self):
        if self.click_order:
            record = "\n".join(self.click_order)
            messagebox.showinfo("Click Order", f"The order of clicks:\n{record}")
            self.save_click_order_to_file(record)
            self.click_order = []
            for row_buttons in self.sub_buttons:
                for btn in row_buttons:
                    btn.destroy()
            self.sub_buttons = []

    def save_click_order_to_file(self, record):
        with open("sorted_click_order.txt", "w") as file:
            sorted_order = sorted(self.click_order)
            file.write("\n".join(sorted_order))

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()