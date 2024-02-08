import keyboard
import os
import shutil
from colorama import init, Fore, Style

init()

class ConsoleUI:
    def __init__(self, center_page=False):
        self.pages = []
        self.current_page = 0
        self.selected_option = 0
        self.center = center_page

    def add_page(self, title, options, description=None, callback=None):
        """
        parameters:
            title: title of the page
            options: list of options (like buttons)
            description: description of the page
            callback: callback function to be called when page is selected

        returns:
            None
        """
        page = {"title": title, "description": description, "options": options, "callback": callback}
        self.pages.append(page)
    
    def get_current_page(self):
        """
        parameters:
            None

        returns:
            Current page that is shown
        """
        page = self.pages[self.current_page]
        if page:
            return page
        return None
    
    def print_page_build(self, page):
        """
        parameters:
            page: Enter an Integer for that page, you want to read

        returns:
            Console output: print all key's and value's of the current page
        """
        if type(page) is int:
            origin = self.pages[page]
            for i, j in enumerate(origin):
                print(i, j)
        else:
            return TypeError("Invalid Parameter, must be an integer/number. Mind, the pages are stored in a array")

    def display_current_page(self):
        """
        Its a function that prints the current page to the console. 

        parameters:
            None

        returns:
            None
        """
        current_page_data = self.pages[self.current_page]
        paddingTitle = self.center_text(current_page_data['title'])
        paddingDescription = ""
        paddingButtons = self.center_list_padding(current_page_data["options"])
        if not self.center:
            paddingTitle = ""
            paddingButtons = ""
            paddingDescription= ""

        print(f"{paddingTitle}{current_page_data['title']}")

        if current_page_data['description']:
            paddingDescription = self.center_text(current_page_data['description'])
            print(f"{paddingDescription}{Fore.LIGHTBLACK_EX + Style.BRIGHT}{current_page_data['description']}{Fore.RESET + Style.RESET_ALL}")

        for i, option in enumerate(current_page_data["options"]):
            prefix = f"{paddingButtons}{Fore.WHITE}> {Fore.LIGHTRED_EX}" if i == self.selected_option else f"{paddingButtons}{Fore.WHITE}"
            print(f"{prefix}{option}{Fore.RESET}")

    def next_page(self):
        """
        go to the next page
        
        parameters:
            None

        returns:
            IndexError: Limit reached
        """
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.selected_option = 0
        else:
            return IndexError("Limit reached")

    def prev_page(self):
        """
        go to the previous page

        parameters:
            None

        returns:
            None
        """
        if self.current_page > 0:
            self.current_page -= 1
            self.selected_option = 0
        else:
            print("Es gibt keine vorherige Seite.")

    def select_option(self):
        """
        A function that calls the current page callback. Its the callback method. 

        parameters:
            None

        returns:
            None
        """

        callback = self.pages[self.current_page]["callback"]
        if callback:
            callback(self)

    def scroll_index(self, direction):
        """
        Scroll through the current page

        parameters:
            direction: string type available direction's "up", "down"

        returns:
            None
        """

        current_page_data = self.pages[self.current_page]
        num_options = len(current_page_data["options"])

        if direction == "up":
            self.selected_option = (self.selected_option - 1) % num_options
        elif direction == "down":
            self.selected_option = (self.selected_option + 1) % num_options

    def center_text(self, text):
        """
        This function uses the Text lenght and the console size
        to return the padding for the given text

        parameters:
            text: Text that you want to center or calculateing the padding of it

        returns:
            padding: the needed space to center the text 
        """
        terminal_width, _ = shutil.get_terminal_size()
        padding = (terminal_width - len(text)) // 2
        centered_side = ' ' * padding

        return centered_side
    
    def center_list_padding(self, text_list):
        """
        This function uses the List lenght and the console size
        to return the padding for the given list

        parameters:
            text_list: A list that you want to center or calculating the padding of it

        returns:
            padding: the needed space to center the list 
        """
        terminal_width, _ = shutil.get_terminal_size()

        max_text_width = max(len(text[0]) for text in text_list)
        padding = (terminal_width - max_text_width) // 2

        centered_padding = ' ' * padding

        return centered_padding
    

    def create_logo(self, logo_array):
        """
        This function generate a string from a array that is written in Ascii letters
        Important to mention is the letters must be in a array, like
        logo = [
            " ██▓ ██▓███   ",
            "▓██▒▓██░  ██▒ ",
            "▒██▒▓██░ ██▓▒ ",
            "░██░▒██▄█▓▒ ▒ ",
            "░██░▒██▒ ░  ░ ",
            "░▓  ▒▓▒░ ░  ░ ",
            " ▒ ░░▒ ░      ",
            " ▒ ░░░        ",
            " ░            "
        ]

        parameters:
            logo_array: A array that has ASCII characters 

        returns:
            logo: A string that includes the ASCII characters in one string
        """
        max_line_length = max(len(line) for line in logo_array)        
        terminal_width, _ = shutil.get_terminal_size()
        centered_side = ''
        if self.center:
            padding = (terminal_width - max_line_length) // 2
            centered_side = ' ' * padding

        logo = ""
        for part in logo_array:
            logo += centered_side + Fore.RED + part + Fore.RESET + "\n"

        return logo
    
    def run(self):
        """
        This function is the start of the UI, it registers all Keyboard events for the navigation in the UI, for instance
        Enter: if available, calls the callback function
        - Arrow Up: scroll up
        - Arrow Down: scroll down
        - Arrow Left: Previous Page
        - Arrow Right: Next Page 

        parameters:
            None

        returns:
            if available, the callback function
        """
        while True:
            os.system("cls")
            self.display_current_page()

            key = keyboard.read_event(suppress=True)
            if key.event_type == keyboard.KEY_DOWN:
                if key.scan_code == 28: # Enter
                    self.select_option()
                    break
                elif key.scan_code == 72: # Up
                    self.scroll_index("up")
                elif key.scan_code == 80: # Down
                    self.scroll_index("down")
                elif key.scan_code == 1: # Esc
                    break
                elif key.scan_code == 75: # Left
                    self.prev_page()
                elif key.scan_code == 77: # right
                    self.next_page()


logoArray =[
    " ██▓ ██▓███   ",
    "▓██▒▓██░  ██▒ ",
    "▒██▒▓██░ ██▓▒ ",
    "░██░▒██▄█▓▒ ▒ ",
    "░██░▒██▒ ░  ░ ",
    "░▓  ▒▓▒░ ░  ░ ",
    " ▒ ░░▒ ░      ",
    " ▒ ░░░        ",
    " ░            "
]

def callback(ui):
    print(ui.title)

ui = ConsoleUI(True)

ui.add_page(ui.create_logo(logoArray), ["Option A", "Option B", "exit"], "", callback=callback)
ui.add_page(ui.create_logo(logoArray), ["OK"], "page 1")

ui.run()