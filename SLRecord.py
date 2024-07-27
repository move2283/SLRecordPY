import tkinter as tk

class ButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button App")

        self.main_buttons = []
        self.sub_buttons = []
        self.click_order = []
        self.round_number = 1
        self.recent_actions = []

        self.create_sub_buttons_placeholder()
        self.create_main_buttons()
        self.create_end_button()
        self.create_reset_button()
        self.create_input_field()
        self.create_recent_actions_label()

    def create_sub_buttons_placeholder(self):
        # Create placeholders for the sub-buttons
        for i in range(3):
            for j in range(8):
                placeholder = tk.Label(self.root, text="", width=3, height=2)
                placeholder.grid(row=i, column=j, padx=5, pady=5)

    def create_main_buttons(self):
        for i in range(10):
            btn = tk.Button(
                self.root,
                text=f"{i+1}",
                command=lambda i=i: self.on_main_button_click(i),
                width=3,
                height=1
            )
            btn.grid(row=3, column=i, padx=5, pady=5)
            self.main_buttons.append(btn)

    def create_end_button(self):
        end_button = tk.Button(self.root, text="结束", command=self.end_round, width=3,
                height=3)
        end_button.grid(row=3, column=10, padx=5, pady=5)

    def create_reset_button(self):
        reset_button = tk.Button(self.root, text="sl", command=self.reset_round, width=3, height=1)
        reset_button.grid(row=0, column=10, padx=5, pady=5)

    def create_input_field(self):
        self.input_field = tk.Entry(self.root, width=10)
        self.input_field.grid(row=1, column=10, padx=5, pady=5)

    def create_recent_actions_label(self):
        self.recent_actions_label = tk.Label(self.root, text="最近三次操作:", justify='left', anchor='w')
        self.recent_actions_label.grid(row=4, column=0, columnspan=11, sticky='w', padx=5, pady=5)

    def update_recent_actions_label(self):
        recent_actions_text = "最近三次操作: " + "   ".join(self.recent_actions[-3:])
        self.recent_actions_label.config(text=recent_actions_text)

    def on_main_button_click(self, index):
        main_action = f"{index+1}->"
        self.click_order.append(f"{index+1}->")
        if not self.sub_buttons:
            for i in range(3):
                row_buttons = []
                for j in range(8):
                    btn = tk.Button(
                        self.root,
                        text=f"{3-i}.{j+1}",
                        command=lambda i=i, j=j: self.on_sub_button_click(i, j, main_action),
                    )
                    btn.grid(row=i, column=j, padx=5, pady=5)
                    row_buttons.append(btn)
                self.sub_buttons.append(row_buttons)

    def on_sub_button_click(self, row, col, main_action):
        sub_action = f"{3-row}.{col+1}"
        full_action = f"{main_action}{sub_action}"
        self.click_order.append(f"{3-row}.{col+1} ")
        self.recent_actions.append(full_action)
        self.update_recent_actions_label()
        self.destroy_sub_buttons()

    def destroy_sub_buttons(self):
        for row_buttons in self.sub_buttons:
            for btn in row_buttons:
                btn.destroy()
        self.sub_buttons = []

    def end_round(self):
        if self.click_order:
            record = f"第{self.round_number}回合: " + "".join(self.click_order) + "结束回合"
            self.recent_actions.append(f"第{self.round_number}回合结束")
            self.update_recent_actions_label()
            self.save_click_order_to_file(record)
            self.click_order = []
            for row_buttons in self.sub_buttons:
                for btn in row_buttons:
                    btn.destroy()
            self.round_number += 1
            self.sub_buttons = []

    def reset_round(self):

        if self.click_order:
            record = f"第{self.round_number}回合: " + "".join(self.click_order) + "结束回合"
            self.recent_actions.append(f"第{self.round_number}回合结束")
            self.update_recent_actions_label()
            self.save_click_order_to_file(record)
            self.click_order = []
            self.round_number += 1
            self.destroy_sub_buttons()

        input_value = self.input_field.get()
        if not input_value:
            input_value = "0"
        record = f"重新开始战斗, 薪火受到伤害: {input_value}"
        self.recent_actions.append(record)
        self.update_recent_actions_label()
        self.save_click_order_to_file(record, add_newlines=True)
        self.click_order = []
        for row_buttons in self.sub_buttons:
            for btn in row_buttons:
                btn.destroy()
        self.sub_buttons = []
        self.round_number = 1

    def save_click_order_to_file(self, record, add_newlines=False):
        with open("click_order.txt", "a", encoding='utf-8') as file:
            if add_newlines:
                file.write(f"\n{record}\n\n")
            else:
                file.write(record + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()

    