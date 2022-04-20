import tkinter as tk
from tkinter import *
from tkinter import ttk


# Main tkinter window
class SoccerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # -- SEARCH HANDLING --
        self.search_handlers = {
            'Name': self.handle_search_name,
            'User': self.handle_search_user,
            'Top': self.handle_search_top,
            'Tags': self.handle_search_tags
        }
        self.n_of_players = 1000

        # -- WINDOW SETUP --

        self.title('CPD - Trabalho Final')
        self.geometry('800x250')
        self.resizable(False, False)

        # Frames
        self.input_frame = ttk.Frame(self)
        self.vert_bar = ttk.Separator(self, orient=VERTICAL)
        self.output_frame = ttk.Frame(self)
        self.output_frame['borderwidth'] = 2
        self.output_frame['relief'] = 'sunken'

        self.search_frame = ttk.Frame(self.input_frame)
        self.searchtype_frame = ttk.Frame(self.input_frame)
        self.logging_frame = ttk.Frame(self.input_frame)

        self.input_frame.grid(column=0, row=0, sticky='nw', padx=5, pady=5)
        self.vert_bar.grid(column=1, row=0, padx=20, ipady=180)
        self.output_frame.grid(column=2, row=0, sticky='ne', padx=5, pady=5)

        self.search_frame.grid(column=0, row=1, sticky='nw')
        self.searchtype_frame.grid(column=0, row=0, sticky='nw')
        self.logging_frame.grid(column=0, row=2, sticky='sw', pady=30)


        # StringVars
        self.searched = StringVar()
        self.searchtype = StringVar()
        self.top_value = IntVar()

        # -- Widgets --

        # Search
        self.label_search = ttk.Label(self.search_frame, text='Search:')
        self.label_search.grid(column=0, row=0, sticky='w')

        self.search = ttk.Entry(self.search_frame, textvariable=self.searched)
        self.search.grid(column=0, row=1, padx=2, pady=2)

        self.submit_button = ttk.Button(self.search_frame, text='Submit')
        self.submit_button.grid(column=1, row=1)

        # Search type
        self.label_searchtype = ttk.Label(self.searchtype_frame, text='Search type:')
        self.label_searchtype.grid(row=0, sticky='w')

        self.searchtype_box = ttk.Combobox(self.searchtype_frame, textvariable=self.searchtype)
        self.searchtype_box.grid(column=0, row=1, padx=2)
        self.searchtype_box['values'] = tuple(self.search_handlers.keys())
        self.searchtype_box.bind('<<ComboboxSelected>>', self.set_search_type)
        self.searchtype_spinbox = ttk.Spinbox(self.searchtype_frame, from_=1, to=self.n_of_players,
                                              textvariable=self.top_value)
        self.searchtype_spinbox.grid(column=1, row=1)


        # Logging
        self.label_log = ttk.Label(self.logging_frame, text='Log:')
        self.label_log.grid(row=0, sticky='w')

        self.log_textbox = Text(self.logging_frame, width=50, height=5, wrap=NONE)
        self.log_textbox.grid(row=1, pady=2,padx=2)
        self.log_textbox['state'] = DISABLED

        # Output

        self.output_tree = ttk.Treeview(self.output_frame, show='headings', columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        for column in self.output_tree['columns']:
            self.output_tree.column(column, stretch=False, width=64)
        self.output_tree.grid(column=0)
        # self.output_scroll = ttk.Scrollbar(self.output_frame, orient=VERTICAL, command=self.output_tree.xview())
        # self.output_scroll.grid(column=1)

    def write_to_log(self, msg):
        self.log_textbox['state'] = NORMAL
        self.log_textbox.insert(END, msg + '\n')
        self.log_textbox.see(END)
        self.log_textbox['state'] = DISABLED

    def set_search_type(self, event):
        string = self.searchtype.get()

        # Set button command
        self.submit_button['command'] = self.search_handlers[string]

        # Clear treeview
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)

    def handle_search_name(self):
        player_name = self.searched.get()
        if not len(player_name):
            return

        self.write_to_log(f'Searching for player \'{player_name}\'...')

    def handle_search_user(self):
        user_name = self.searched.get()
        if not len(user_name):
            return

        self.write_to_log(f'Searching for user \'{user_name}\'...')

    def handle_search_top(self):
        tag = self.searched.get()
        if not len(tag):
            return

        value = max(1, min(self.n_of_players, self.top_value.get()))
        self.top_value.set(value)

        self.write_to_log(f'Searching for the top {value} players with tag {tag}...')

    def handle_search_tags(self):
        tags = self.searched.get()
        if not len(tags):
            return

        tags = tags.split(' ')

        self.write_to_log(f'Searching for players under tags \'{", ".join(tags)}\'...')

