import os
import sys
import webbrowser
from tkinter import Event

import customtkinter as ctk

from .keygen import WingKeygen


class Application(ctk.CTk, WingKeygen):
    def __init__(self) -> None:
        super().__init__()

        self.__version__ = "9.0.2"
        self.__build__ = "2023.01.05"
        self.__github__ = "https://github.com/rodriguez-moon/wing-ide-keygen-gui"

        print("[+] Wing IDE Pro Keygen GUI is running!")
        self.iconbitmap(self.get_icon())
        self.title(f"Wing IDE Pro Keygen GUI v{self.__version__}")
        self.minsize(350, 250)
        self.create_widgets()

    @staticmethod
    def get_theme(key: str) -> tuple | None:
        # TODO: move to custom "theme.json" file
        colours = {
            "background": ("white", "#37383a"),
            "readonly": ("lightgrey", "#2d2d2d"),
            "dark": ("grey", "#202020"),
            "blue": ("#027cff", "#4c8cd4"),
            "darkblue": ("#0266d1", "#3c6ea6"),
            "darkdarkblue": ("#0254ab", "#32577d"),
            "red": ("#d73343", "#d73343"),
            "darkred": ("#B70000", "#830000"),
            "green": ("#38a851", "#2f8d44"),
            "darkgreen": ("#2B8400", "#206300"),
            "grey": ("#7d7d7d", "#666666"),
        }
        return colours.get(key)

    @staticmethod
    def get_icon() -> str | None:
        # TODO: implement cross-platform icons
        if sys.platform != "win32":
            return None

        parent_directory = os.path.abspath(
            os.path.join(sys.argv[0], os.path.pardir, os.path.pardir)
        )
        icon_path = os.path.join(parent_directory, "assets", "wing.ico")
        return icon_path

    @staticmethod
    def open_href(event: Event, href: str) -> None:
        # TODO: modify the widget to give visual response when clicked
        # widget = event.widget
        webbrowser.open_new_tab(href)

    def close_top_view(self, window: ctk.CTkToplevel) -> None:
        window.destroy()

        # Re-enable button
        self.about_button._state = "normal"
        self.about_button._fg_color = self.get_theme("blue")
        self.about_button._draw()

    def create_about_view(self) -> None:
        window = ctk.CTkToplevel(self)
        window.iconbitmap(self.get_icon())
        window.title("About")
        window.minsize(300, 260)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_top_view(window))

        for n in range(4):
            window.grid_columnconfigure(n, weight=1)
            window.grid_rowconfigure(n, weight=1)

        values = {
            "Author": "rodriguez-moon",
            "Build Date": self.__build__,
            "Program Version": self.__version__,
            "GUI Version": ctk.__version__,
        }

        current_col = 1
        current_row = 0

        # Github link
        variable = ctk.StringVar()
        github = ctk.CTkEntry(
            master=window,
            textvariable=variable,
            width=200,
            state="readonly",
            fg_color=self.get_theme("readonly"),
            text_color="#6ba3f0",
            font=ctk.CTkFont(weight="bold", underline=True),
            justify="center",
        )
        github.grid(padx=5, pady=5, row=current_row, column=current_col, columnspan=2)
        github.bind(
            "<Button-1>",
            (lambda event, href=self.__github__: self.open_href(event, href)),
        )
        variable.set("GitHub Repository")
        current_row += 1

        # Create a label and entry for each item
        for key, value in values.items():
            label = ctk.CTkLabel(master=window, text=key)
            label.grid(padx=5, pady=5, row=current_row, column=current_col)
            variable = ctk.StringVar()
            entry = ctk.CTkEntry(
                master=window,
                textvariable=variable,
                width=120,
                state="readonly",
                fg_color=self.get_theme("readonly"),
            )
            entry.grid(padx=5, pady=5, row=current_row, column=current_col + 1)
            variable.set(value)
            current_row += 1

        # Close button
        close_button = ctk.CTkButton(
            master=window,
            text="Close",
            command=lambda: self.close_top_view(window),
            fg_color=self.get_theme("red"),
            hover_color=self.get_theme("darkred"),
        )
        window.grid_rowconfigure(current_row, weight=1)
        close_button.grid(pady=10, row=current_row, column=1, columnspan=2)

        # Disable button
        self.about_button._state = "disabled"
        self.about_button._fg_color = self.get_theme("grey")
        self.about_button._draw()

    def create_widgets(self) -> None:
        current_row = 0
        current_col = 0

        # Version
        self.label0 = ctk.CTkLabel(master=self, text="Wing IDE Pro Version")
        self.label0.grid(padx=5, pady=5, row=current_row, column=current_col)
        self.version_info = ctk.StringVar()
        self.version_selection = ctk.CTkOptionMenu(
            master=self,
            variable=self.version_info,
            values=list(self.version_magics),
            fg_color=self.get_theme("blue"),
            button_color=self.get_theme("darkblue"),
            button_hover_color=self.get_theme("darkdarkblue"),
        )
        self.version_selection.grid(
            padx=5, pady=1, row=current_row, column=current_col + 1
        )
        self.version_selection.set(next(iter(self.version_magics)))
        current_row += 1

        # License Type
        self.label1 = ctk.CTkLabel(master=self, text="License Type")
        self.label1.grid(padx=5, pady=5, row=current_row, column=current_col)
        self.license_type = ctk.StringVar()
        self.license_selection = ctk.CTkOptionMenu(
            master=self,
            variable=self.license_type,
            values=list(self.license_types),
            fg_color=self.get_theme("blue"),
            button_color=self.get_theme("darkblue"),
            button_hover_color=self.get_theme("darkdarkblue"),
        )
        self.license_selection.grid(
            padx=5, pady=1, row=current_row, column=current_col + 1
        )
        self.license_selection.set(next(iter(self.license_types)))
        self.license_type.trace_add(
            "write",
            lambda *_: self.license_id.set(
                self.create_license_id(self.license_selection.get())
            ),
        )
        current_row += 1

        # License ID
        self.label2 = ctk.CTkLabel(master=self, text="License ID")
        self.label2.grid(padx=5, pady=5, row=current_row, column=current_col)
        self.license_id = ctk.StringVar()
        self.license_id_entry = ctk.CTkEntry(
            master=self,
            textvariable=self.license_id,
            width=220,
            state="readonly",
            fg_color=self.get_theme("readonly"),
        )
        self.license_id_entry.grid(
            padx=5, pady=5, row=current_row, column=current_col + 1
        )
        self.license_id.set(self.create_license_id(self.license_selection.get()))
        current_row += 1

        # Request Code
        self.label3 = ctk.CTkLabel(master=self, text="Request Code")
        self.label3.grid(padx=5, pady=5, row=current_row, column=current_col)
        self.request_code = ctk.StringVar()
        self.request_code_entry = ctk.CTkEntry(
            master=self, textvariable=self.request_code, width=220
        )
        self.request_code_entry.grid(
            padx=5, pady=5, row=current_row, column=current_col + 1
        )
        self.request_code_entry.bind(
            "<Return>", command=lambda event: self.generate_license(self)
        )
        current_row += 1

        # Activation Code
        self.label4 = ctk.CTkLabel(master=self, text="Activation Code")
        self.label4.grid(padx=5, pady=5, row=current_row, column=current_col)
        self.activation_code = ctk.StringVar()
        self.request_code_entry = ctk.CTkEntry(
            master=self,
            textvariable=self.activation_code,
            width=220,
            state="readonly",
            fg_color=self.get_theme("readonly"),
        )
        self.request_code_entry.grid(
            padx=5, pady=5, row=current_row, column=current_col + 1
        )
        current_row += 1

        # Button Frame
        self.button_frame = ctk.CTkFrame(
            master=self,
        )
        self.button_frame.grid(
            padx=10, pady=5, row=current_row, column=current_col, columnspan=2
        )

        # About Button
        self.about_button = ctk.CTkButton(
            master=self.button_frame,
            text="About",
            width=80,
            command=self.create_about_view,
            fg_color=self.get_theme("blue"),
            hover_color=self.get_theme("darkblue"),
        )
        self.about_button.grid(padx=5, pady=5, row=current_row, column=current_col)

        # Reroll Button
        self.reroll_button = ctk.CTkButton(
            master=self.button_frame,
            text="Reroll ID",
            width=80,
            command=lambda: self.license_id.set(
                self.create_license_id(self.license_selection.get())
            ),
            fg_color=self.get_theme("blue"),
            hover_color=self.get_theme("darkblue"),
        )
        self.reroll_button.grid(padx=5, pady=5, row=current_row, column=current_col + 1)

        # Generate button
        self.gen_button = ctk.CTkButton(
            master=self.button_frame,
            text="Generate",
            width=80,
            command=lambda: self.generate_license(self),
            fg_color=self.get_theme("green"),
            hover_color=self.get_theme("darkgreen"),
        )
        self.gen_button.grid(padx=5, pady=5, row=current_row, column=current_col + 2)

        # Exit button
        self.exit_button = ctk.CTkButton(
            master=self.button_frame,
            text="Exit",
            width=80,
            command=self.destroy,
            fg_color=self.get_theme("red"),
            hover_color=self.get_theme("darkred"),
        )
        self.exit_button.grid(padx=5, pady=5, row=current_row, column=current_col + 3)


if __name__ == "__main__":
    raise SystemExit("[x] Please run 'main.py'!")
