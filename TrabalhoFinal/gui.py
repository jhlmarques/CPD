import tkinter as tk
import re
from tkinter import *
from tkinter import ttk



# Main tkinter window
class SoccerApp(tk.Tk):
    def __init__(self, searcher):
        super().__init__()

        # -- SEARCH HANDLING --
        self.searcher = searcher
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

        # Start up messages
        self.write_to_log(f'Built Trie and Players Hash Table in {searcher.t_players} seconds')
        self.write_to_log(f'Built Users Hash Table and Top 20 lists in {searcher.t_users} seconds')
        self.write_to_log(f'Built Tag Hash Tables in {searcher.t_tags} seconds')
        self.write_to_log(f'Sorted lists in {searcher.t_sorts}')


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

        self.output_tree.heading('col1')
        self.output_tree.heading('col2')
        self.output_tree.heading('col3')
        self.output_tree.heading('col4')
        self.output_tree.heading('col5')

    def handle_search_name(self):

        # Clear treeview
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)

        player_name = self.searched.get()
        if not len(player_name):
            return

        self.write_to_log(f'Searching for player \'{player_name}\'...')
        players = self.searcher.find_by_name(player_name)

        self.output_tree.heading('col1', text='ID')
        self.output_tree.heading('col2', text='Name')
        self.output_tree.heading('col3', text='Positions')
        self.output_tree.heading('col4', text='Rating')
        self.output_tree.heading('col5', text='Count')

        for player_data in players:
            self.output_tree.insert('', END, values=
                                    (player_data.id, player_data.name,
                                     ', '.join(player_data.positions),
                                     player_data.average,
                                     player_data.n_of_ratings))

    def handle_search_user(self):

        # Clear treeview
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)

        user_id = self.searched.get()
        if not len(user_id):
            return
        if not user_id.isnumeric():
            self.write_to_log('User IDs only use numbers')
            return


        self.write_to_log(f'Searching for user of id \'{user_id}\'...')
        ratings = self.searcher.find_by_user(int(user_id))

        if ratings is None:
            self.write_to_log('User ID not found')
            return

        for item in self.output_tree.get_children():
            self.output_tree.delete(item)


        self.output_tree.heading('col1', text='ID')
        self.output_tree.heading('col2', text='Name')
        self.output_tree.heading('col3', text='Global Rating')
        self.output_tree.heading('col4', text='Count')
        self.output_tree.heading('col5', text='Rating')

        for item in ratings:
            rating = item[0]
            player_data = item[1]
            self.output_tree.insert('', END, values=
                                    (player_data.id, player_data.name,
                                     player_data.average,
                                     player_data.n_of_ratings, rating))

    def handle_search_top(self):

        # Clear treeview
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)

        position = self.searched.get()
        if not len(position):
            return

        value = max(1, min(self.n_of_players, self.top_value.get()))
        self.top_value.set(value)

        self.write_to_log(f'Searching for the top {value} players in position {position}...')
        players = self.searcher.find_top(value, position)

        self.output_tree.heading('col1', text='ID')
        self.output_tree.heading('col2', text='Name')
        self.output_tree.heading('col3', text='Positions')
        self.output_tree.heading('col4', text='Rating')
        self.output_tree.heading('col5', text='Count')

        for player_data in players:

            self.output_tree.insert('', END, values=
                                    (player_data.id, player_data.name,
                                     ', '.join(player_data.positions),
                                     player_data.average,
                                     player_data.n_of_ratings))

    def handle_search_tags(self):

        # Clear treeview
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)

        tags_str = self.searched.get()
        if not len(tags_str):
            return

        tags = re.findall('\'([a-zA-Z ()]+)\'', tags_str)

        self.write_to_log(f'Searching for players under tags {", ".join(tags)}...')
        players = self.searcher.find_by_tags(tags)

        self.output_tree.heading('col1', text='ID')
        self.output_tree.heading('col2', text='Name')
        self.output_tree.heading('col3', text='Positions')
        self.output_tree.heading('col4', text='Rating')
        self.output_tree.heading('col5', text='Count')

        for player_data in players:
            self.output_tree.insert('', END, values=
                                    (player_data.id, player_data.name,
                                     ', '.join(player_data.positions),
                                     player_data.average,
                                     player_data.n_of_ratings))

