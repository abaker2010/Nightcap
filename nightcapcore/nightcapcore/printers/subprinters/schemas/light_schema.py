from nightcapcore.printers.subprinters.schemas.base.table_schema import TableBaseSchema
from colorama import Fore

class TableLightSchema(TableBaseSchema):
    def __init__(self, cell_divider: str = '|', v_boarder: str = '|', h_boarder: str = '-', min_cell_size: int = 20, \
                    left_tindent: int = 2, column_count: int = 3, indent_text: str = '\t', title_text_color: Fore = Fore.LIGHTWHITE_EX, v_boarder_color: Fore = Fore.LIGHTWHITE_EX, \
                    h_boarder_color: Fore = Fore.LIGHTWHITE_EX, cell_divider_color: Fore = Fore.LIGHTWHITE_EX, header_divider_color: Fore = Fore.LIGHTWHITE_EX, \
                    cell_text_color: Fore = Fore.LIGHTWHITE_EX, header_text_color: Fore = Fore.LIGHTWHITE_EX) -> None:

        super().__init__(cell_divider, v_boarder, h_boarder, min_cell_size, left_tindent, column_count, indent_text, title_text_color, \
                            v_boarder_color, h_boarder_color, cell_divider_color, header_divider_color, cell_text_color, header_text_color)