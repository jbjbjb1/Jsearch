# Program to search drive files and folders with a simple GUI.

import io
import os
import pickle
import time
from datetime import datetime

import PySimpleGUI as sg

sg.ChangeLookAndFeel('Dark')

class Gui:
    def __init__(self, default_drive):
        initial_path = f'{default_drive}:\\'
        self.layout = [
            [sg.Text('Search Term', size=(10,1)), 
            sg.Input(size=(45,1), focus=True, key="TERM"),
            sg.Button('Search', size=(6,1), bind_return_key=True, key='_SEARCH_'), 
            sg.Radio('Default', group_id='choice', key='DEFAULT', default=True), 
            sg.Radio('Files', group_id='choice', key='FILES'), 
            sg.Radio('Folders', group_id='choice', key='FOLDERS')],
            [sg.Text('Root Path', size=(10,1)), 
            sg.Input(initial_path, size=(45,1), key='PATH'), 
            sg.FolderBrowse('Browse', size=(6,1), target='PATH'), 
            sg.Button('Index', size=(12,1), key='_INDEX_'), 
            sg.Button('Load Index', size=(12,1), key='_LOADINDEX_')],
            [sg.Output(size=(120,20), key='-OUTPUT-')],
            [sg.Button('All records', size=(10,1), key='_OPENALL_'),
            sg.Button('History', size=(10,1), key='_HISTORY_'),
            sg.Button('Help', size=(10,1), key='_HELP_')]
        ]
        self.window = sg.Window('JSearch: File Search Engine').Layout(self.layout)


class SearchEngine:
    def __init__(self, default_drive):
        self.default_drive = default_drive
        self.file_index = []
        self.results = []
        self.matches = 0
        self.records = 0

        # create a search_records file if it does not exist and over write existing file if exists
        with io.open('search_records.txt', 'w', encoding="utf-8") as f:
            f.write('')
        # create a search_history file if it does not exist
        if not os.path.exists('search_history.txt'):
            with io.open('search_history.txt', 'w', encoding="utf-8") as f:
                f.write('')

    def create_new_index(self, values):
        ''' Create a new index and save to file. '''

        start_time = time.time()
        root_path = values['PATH']
        root_path_letter = root_path.split(':')[0]
        name = f'file_index_{root_path_letter}.pkl'
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        # save to file
        with open(name, 'wb') as f:
            pickle.dump(self.file_index, f)
        dur = time.time() - start_time
        print(f'New index created in {dur:.0f} sec.')        

    def load_existing_index(self, new_drive = None):
        ''' Load each time the program is started if it exists. '''
        # TODO change this to the first file in settings.txt (in future load all)

        # if the paramater new_drive is passed make that the default drive
        if new_drive:
            self.default_drive = new_drive

        try:
            with open(f'file_index_{self.default_drive}.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
        ''' Search for term based on search type. '''

        # reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0
        term_r = values['TERM']     # raw term

        # perform search
        # TODO Order results by lowest file depth first
        term = term_r.split(',')
        term = [i.strip() for i in term]
        
        if values['DEFAULT']:
            for path, files in self.file_index:
                for file in files:
                    self.records += 1
                    full_path = path + '\\' + file
                    if all(t.lower() in full_path.lower() for t in term):
                        self.results.append(full_path)
                        self.matches += 1
                    else:
                        continue
        if values['FOLDERS']:
            for path, files in self.file_index:
                self.records += 1
                if all(t.lower() in path.lower() for t in term):
                    self.results.append(path)
                    self.matches += 1              
                else:
                    continue
        if values['FILES']:
            for path, files in self.file_index:
                for file in files:
                    full_path = path + '\\' + file
                    self.records += 1
                    if all(t.lower() in file.lower() for t in term):
                        self.results.append(full_path)
                        self.matches += 1
                    else:
                        continue
        
        # save search results
        with io.open('search_records.txt', 'w', encoding="utf-8") as f:
            for row in self.results:
                f.write(row + '\n')
        
        # save search term to history
        with io.open('search_history.txt', 'r+', encoding="utf-8") as f:    # r+ is needed because we are reading whole file, not just appending
            content = f.read()
            f.seek(0, 0)
            new_line = datetime.now().strftime('%d/%m/%Y %H:%M:%S:  ') + term_r
            f.write(new_line.rstrip('\r\n') + '\n' + content) # add to top of file
            

def main():
    # Main function that runs events in the GUI

    # Load settings of default drive
    def load_indexes():
        try:
            with open('settings.txt') as f:
                for line in f:
                    fields = line.strip().split()
                    # for security only input these pre-defined variables
                    if fields[0] == 'default_drive':
                        return fields[2]
        except:
            # If the file does not exist or there is nothing valid there
            print('No settings found in settings.txt')
            return ''
    
    default_drive = load_indexes()
    g = Gui(default_drive)
    s = SearchEngine(default_drive)
    s.load_existing_index()

    while True:      
        # Start gui loop
        event, values = g.window.read()
        #print(event, values)   # debug

        if event is None:
            break
        elif event == '_INDEX_':
            a = sg.popup_ok_cancel('This may take some time. Are you sure you want to index?')  # Double check before re-indexing
            if a == 'OK':
                s.create_new_index(values)
                print()
                print('New index has been created.')      

        elif event == '_SEARCH_':
            g.window.FindElement('-OUTPUT-').Update('')
            if s.file_index == []:
                print('No index exists. Please re-index.')
            else:
                start = time.time()
                s.search(values)
                dur = time.time() - start
                # Print results to output element
                if len(s.results) == 0:
                    # Handle no results
                    print('There were no results.')
                else:
                    print('About {:,d} results ({:.2f} seconds) of {:,d} records: \n'.format(s.matches, dur, s.records))
                    num_results = 10
                    if len(s.results) < 10:
                        num_results = len(s.results)
                    for i in range(num_results):
                        print(s.results[i])

        elif event == '_LOADINDEX_':
            # TODO Make this to open a new index to search from
            try:
                fname = sg.popup_get_file('Index to open', default_path = "", file_types = (("PKL Index Files", "*.pkl"), ) )
                new_drive = fname.split('.pkl')[0].split('file_index_')[1]      # Get the drive letter
                s.load_existing_index(new_drive)
                g.window['PATH'].update(f'{new_drive}:\\')
                g.window.FindElement('-OUTPUT-').Update('')
                print('New index loaded.')
            except:
                pass

        elif event == '_OPENALL_':
            os.startfile('search_records.txt')

        elif event == '_HISTORY_':
            os.startfile('search_history.txt')

        elif event == '_HELP_':
            g.window.FindElement('-OUTPUT-').Update('Help notes:\n* To search multiple terms use a comma (,) in between terms.')

# Only run GUI if calling this script  
if __name__ == '__main__':
    main()