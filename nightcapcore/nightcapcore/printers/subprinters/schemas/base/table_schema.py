from abc import ABC
from colorama import Fore

class TableBaseSchema(ABC):
    def __init__(self, 
                    cell_divider:str = '|', 
                    v_boarder:str = '|', 
                    h_boarder:str = '-', 
                    min_cell_size:int = 20, 
                    left_tindent:int = 2, 
                    column_count:int = 3,
                    indent_text:str = '\t',
                    title_text_color:Fore = Fore.LIGHTYELLOW_EX,
                    v_boarder_color:Fore = Fore.MAGENTA, 
                    h_boarder_color:Fore = Fore.MAGENTA,
                    cell_divider_color:Fore = Fore.BLUE,
                    header_divider_color:Fore = Fore.BLUE,
                    cell_text_color:Fore = Fore.LIGHTGREEN_EX, 
                    header_text_color:Fore = Fore.LIGHTYELLOW_EX) -> None:
        super().__init__()

        self.title_text_color = title_text_color
        self.cell_divider = cell_divider
        self.v_boarder = v_boarder
        self.h_boarder = h_boarder
        self.min_cell_size = min_cell_size
        self.left_tindent = left_tindent
        self.column_count = column_count
        self.indent_text = indent_text
        self.v_boarder_color = v_boarder_color
        self.h_boarder_color = h_boarder_color
        self.cell_divider_color = cell_divider_color
        self.cell_text_color = cell_text_color
        self.header_text_color = header_text_color
        self.header_divider_color = header_divider_color
