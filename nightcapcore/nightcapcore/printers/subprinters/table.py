import textwrap
from typing import List
from colorama import Fore, Style
from math import ceil, floor
from os import get_terminal_size
from nightcapcore.printers import PrinterBase
from nightcapcore.printers.subprinters.schemas.base.table_schema import TableBaseSchema
from nightcapcore.printers.subprinters.schemas.default_schema import TableDefaultSchema

class TablePrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    #region Get Header/Column Max Sizes
    def _get_max_sizes(self, 
                        headers: List[str], 
                        data: dict, 
                        max_terminmal_size: int, 
                        max_column_count: int) -> dict:

        _modified_tsize = max_terminmal_size - 20 # 20 would be fine for tabs on the left size
        _column_size = _modified_tsize / max_column_count
        _requested_size = {}

        try:
            if data != None:
                for h, dl in data.items():
                    if dl == None or dl == []:
                        _requested_size[h] = {'header_size' : len(h), 'column_size' : _column_size,  'cell_size' : 0}
                    else:
                        if h in headers:
                            _requested_size[h] = {'header_size' : len(h), 'column_size' : _column_size - len(h),  'cell_size' : len(max(dl, key=len))}
            else:
                for h in headers:
                    _requested_size[h] = {'header_size' : len(h), 'column_size' : _column_size - len(h)}

            return _requested_size 
        except Exception as e:
            raise Exception("ERROR GETTING HEADER/COLUMN MAX SIZES :: %s" % e)
    #endregion 

    #region Determine Max Size, Metadata, Number of tables to print, and Organize row data
    def _get_combined_data(self, title:str, sizes: dict, headers_list: list, tdata: dict, min: int, max: int, max_columns: int) -> dict:
        _header_count = len(sizes.keys())
        _headers = headers_list
        _column_count = _header_count if _header_count <= max_columns else max_columns
        _column_size_f_columns = floor(max/_column_count) if floor(max/_column_count) % 2 == 0 else floor(max/_column_count) - 1
        
        _allowed = {
                    "table_count": 1,
                    "title": {'title': title, 'side_spaces': 0},
                    "table_headers": [_headers],
                    "column_data" : {},
                    "column_metadata": {

                    }
                }
        try:

            if _column_size_f_columns * _header_count > max:
                if _header_count > max_columns:
                    if (_header_count % max_columns) == 0:
                        _allowed['table_count'] = (_header_count / max_columns)
                    else:
                        _allowed['table_count'] = int(float(ceil(_header_count / max_columns)))

                    _chunked_headers = []
                    for i in range(0, _header_count, max_columns):
                        _chunked_headers.append(_headers[i:i+max_columns])
                    
                    _allowed['table_headers'] = _chunked_headers

            _allowed['column_data'] = tdata
            for header in _headers:
                _c_size = None
                try:
                    if "header_size" in sizes[header] and "column_size" in sizes[header]:
                        _c_size = sizes[header]['header_size'] if sizes[header]['header_size'] > sizes[header]['column_size'] else sizes[header]['column_size']
                        
                    elif "header_size" not in sizes[header] and "column_size" in sizes[header]:
                        _c_size = sizes[header]['column_size']
                    
                    elif "header_size" in sizes[header] and "column_size" not in sizes[header]:
                        _c_size = sizes[header]['header_size']
                except Exception as e:
                    raise e
            
                if _c_size != None:
                    if _c_size >= _column_size_f_columns:
                        _c_size = int(_column_size_f_columns)
                    elif _c_size < min:
                        _c_size = int(min)


                _tmp_count = None
                if tdata != None:
                    if (tdata[header] != {} and tdata[header] != None) :
                        _tmp_count = len(tdata[header])
                    else:
                        _tmp_count = 0     
                else:
                    _tmp_count = 0 


                _tmp = {
                        'width' : int(_c_size), 
                        'count' : _tmp_count, #(len(tdata[header]) if tdata[header] != {} or tdata[header] != None else 0) if tdata != None else 0,
                        'side_spaces' : int(((_c_size - len(header))/2))
                        }
                _allowed['column_metadata'][header] = _tmp

            _header_metadata = {}
            _tb_count = 0
            for theaders in _allowed['table_headers']:
                _tb_count += 1
                _hwidth = 0
                for header in theaders:
                    _hwidth += (_allowed['column_metadata'][header]['width'])
                _header_metadata[_tb_count] = {'width' : _hwidth}
                
            _allowed['header_metadata'] = _header_metadata


            try:
                _rows = {} 
                _tb_count = 0
                for theaders in _allowed['table_headers']:
                    _header_num = 0
                    _has_data = False
                    for header in theaders:
                        _row_count = 0
                        if str(_tb_count) not in _rows:
                            _rows[str(_tb_count)] = {}
                        
                        if str(_row_count) not in _rows[str(_tb_count)]:
                            _rows[str(_tb_count)][str(_row_count)] = []
                        
                        if _allowed['column_metadata'][header]['count'] == 0:
                            _rows[str(_tb_count)][str(_row_count)].append({'header' : header, "width" : _allowed['column_metadata'][header]['width'], "value": "N/A", "multi_line" : False})
                        else:
                            _has_data = True
                    
                    if _has_data:
                        _max_size = 0
                        for header in theaders:
                            try:
                                _current = len(_allowed['column_data'][header])
                                if _current > _max_size:
                                    _max_size = _current
                            except Exception as e:
                                raise Exception("MISS MATCH DATA :: MISSING HEADER FOR DATA")
                        
                        for index in range(0, _max_size):
                            if str(_row_count) not in _rows[str(_tb_count)]:
                                _rows[str(_tb_count)][str(_row_count)] = []

                            for header in theaders:
                                try:
                                    _tmp = {
                                            'header' : header,
                                            "width" : _allowed['column_metadata'][header]['width'], 
                                            "value": _allowed['column_data'][header][index], 
                                            "multi_line" : False if len(_allowed['column_data'][header][index]) < _allowed['column_metadata'][header]['width'] else True
                                            }
                                except Exception as e:
                                    _tmp = {
                                            'header' : header,
                                            "width" : _allowed['column_metadata'][header]['width'], 
                                            "value": "N/A", 
                                            "multi_line" : False
                                            }
                                finally:
                                    _rows[str(_tb_count)][str(_row_count)].append(_tmp)
                            _row_count += 1
                    _tb_count += 1
                _allowed['row_data'] = _rows
            except Exception as e:
                raise e

            return _allowed
        except Exception as e:
            raise Exception("ERROR GETTING HEADER/COLUMN ALLOWED SIZES :: %s" % e)
    #endregion
    
    #region Cell Check
    def _check_cells_ready(self, positional_data: dict) -> dict:
        try:
            _ready = True
            for pos, data in positional_data.items():
                if data['extra_values'] != None:
                    _ready = False
                    data['value'] = data['extra_values'][0]
                    if len(data['extra_values']) == 1:
                        positional_data[pos]['extra_values'] = None
                    else:
                        positional_data[pos]['extra_values'] = data['extra_values'][1:]
            
            return _ready
        except Exception as e:
            raise e
    #endregion

    #region Print All Cells
    def _print_cells(self, positional_data: dict, max_positions: int, master_table: list, cell_outside_left: str,
                            cell_outside_right: str, cell_divider: str, cell_text_color: Fore,  
                            h_boarder_color: str, h_boarder: str, color_reset: Style) -> List[str]:
            try:
                row_data = []
                empty_data = []
                
                for pos, data in positional_data.items():
                    _cell_size = len(data['value']) if len(data['value']) % 2 == 0 else len(data['value']) + 1
                    _side_spaces = int(((data['width'] - _cell_size)/2))
                    _cell_value = None
                    if len(data['value']) % 2 == 0:
                        _cell_value = data['value']
                    else:
                        _cell_value = f"{data['value']} "
                    
                    _cell_format = f"{' ' * _side_spaces}{cell_text_color}{_cell_value}{color_reset}{' ' * _side_spaces}"
                    _empty_cell_formt = f"{' ' * _side_spaces}{cell_text_color}{' ' * len(_cell_value)}{color_reset}{' ' * _side_spaces}"
                    if pos == 0 and max_positions == 1:
                        row_data.append(f"{cell_outside_left}{_cell_format}{cell_divider}")
                        empty_data.append(f"{cell_outside_left}{_empty_cell_formt}{cell_divider}")
                    elif pos == 0 and pos != max_positions:
                        row_data.append(f"{cell_outside_left}{_cell_format}{cell_divider}")
                        empty_data.append(f"{cell_outside_left}{_empty_cell_formt}")
                    elif pos == 0 and pos == max_positions:
                        row_data.append(f"{cell_outside_left}{_cell_format}{cell_outside_right}")
                        empty_data.append(f"{cell_outside_left}{_empty_cell_formt}{cell_outside_right}")
                    elif pos == max_positions:
                        row_data.append(f"{_cell_format}{cell_outside_right}")
                        empty_data.append(f"{_empty_cell_formt}{cell_outside_right}")
                    else:
                            row_data.append(f"{_cell_format}{cell_divider}")
                            empty_data.append(f"{_empty_cell_formt}{cell_divider}")
                    data['value'] = ''

                master_table.append(row_data)
                            
                if self._check_cells_ready(positional_data) == False:
                    self._print_cells(positional_data, max_positions, master_table, cell_outside_left, 
                                cell_outside_right, cell_divider, cell_text_color, h_boarder_color, h_boarder, color_reset)
            except Exception as e:
                raise e
    #endregion 

    #region Print Header Row
    def _print_table(self, 
                table_data: dict, 
                schema: TableBaseSchema):
        try:
            title_text_color:Fore = schema.title_text_color
            v_boarder:str = schema.v_boarder
            v_boarder_color:Fore = schema.v_boarder_color
            h_boarder:str = schema.h_boarder
            h_cell_boarder:str = schema.h_boarder
            cell_divider:str = schema.cell_divider
            cell_divider_color:Fore = schema.cell_divider_color
            cell_text_color:Fore = schema.cell_text_color
            header_text_color:Fore = schema.header_text_color
            header_divider_color:Fore = schema.header_divider_color
            h_boarder_color:Fore = schema.h_boarder_color
            indent:int = schema.left_tindent
            color_reset:Style = Style.RESET_ALL


            _header_outside_left = f"{color_reset}{v_boarder_color}{v_boarder}{color_reset}"
            _header_divider = f"{color_reset}{header_divider_color}{cell_divider}{color_reset}"
            _header_outside_right = f"{color_reset}{v_boarder_color}{v_boarder}{color_reset}"
            
            _table_num = 0
            _column_sizes = {}
            _leading_row_format = ("%s" % ('\t' * indent))

            for theaders in table_data['table_headers']:
                _header_str = ""
                _itter = 0
                _top_len = 0   
                _table_data = []

                for header in theaders:       
                    header_metadata = table_data['column_metadata']
                    _side_spaces = header_metadata[header]['side_spaces']

                    _local_len = len(header)
                    _local_len += _side_spaces
                    _local_len += _side_spaces
                    _top_len += _local_len
                    _column_sizes[header] = _local_len

                    _cell_format = f"{' ' * _side_spaces}{header_text_color}{header}{color_reset}{' ' * _side_spaces}"
                    if _itter == 0 and (len(theaders)) == 2:
                        _header_str += f"{_header_outside_left}{_cell_format}{_header_divider}"
                        _top_len += 2
                    elif _itter == 0 and _itter != (len(theaders) - 1):
                        _header_str += f"{_header_outside_left}{_cell_format}{_header_divider}"
                        _top_len += 2
                    elif _itter == 0 and _itter == (len(theaders) - 1):
                        _header_str += f"{_header_outside_left}{_cell_format}{_header_outside_right}"
                        _top_len += 2
                    elif _itter == (len(theaders) - 1):
                        _header_str += f"{_cell_format}{_header_outside_right}"
                        _top_len += 1
                    else:
                        _header_str += f"{_cell_format}{_header_divider}"
                        _top_len += 1
                    
                    _itter += 1

                _h = f"{h_boarder_color}{(h_boarder * _top_len)}{color_reset}"

                if table_data['title']['title'] != None:
                    _title = str(table_data['title']['title'])
                    _title = f'{_title} ' if len(_title) % 2 == 0 else _title

                    _title_max = (_top_len - 2)
                    _title_len = len(_title)
                    
                    _title_side_spaces = int( floor(((_title_max - _title_len)/2)))

                    _title_left = f"{color_reset}{v_boarder_color}{v_boarder}{color_reset}"
                    _cell_format = f"{' ' * _title_side_spaces}{title_text_color}{_title}{color_reset}{' ' * _title_side_spaces}"
                    _title_right = f"{color_reset}{v_boarder_color}{v_boarder}{color_reset}"

                    _title_str = f"{_title_left}{_cell_format}{_title_right}"

                    _table_data.append("%s" % _h)
                    _table_data.append("%s" % _title_str)
                _table_data.append("%s" % _h)
                _table_data.append("%s" % _header_str)
                _table_data.append("%s" % _h)


                _cell_outside_left = f"{color_reset}{v_boarder_color}{v_boarder}{color_reset}"
                _cell_divider = f"{color_reset}{cell_divider_color}{cell_divider}{color_reset}"
                _cell_outside_right = f"{color_reset}{v_boarder_color}{v_boarder}{color_reset}"
                
                _tcolumns = []
                for row_num, row_data in table_data['row_data'][str(_table_num)].items():
                    _positional_data = {} # {position : data}
                    for x in range(0, len(row_data)):
                        if str(row_data[x]['header']) not in _tcolumns:
                            _tcolumns.append(str(row_data[x]['header']))
                            
                        if row_data[x]['multi_line'] == False:
                            _positional_data[x] = row_data[x]
                            _positional_data[x]['extra_values'] = None
                            _positional_data[x]['finished'] = True
                            _positional_data[x]['has_ruler'] = False
                        else:
                            _split_cell_values = textwrap.wrap(text=row_data[x]['value'], width=(row_data[x]['width'] - 4))
                            row_data[x]['value'] = _split_cell_values[0]
                            _positional_data[x] = row_data[x]
                            _positional_data[x]['extra_values'] = [] 
                            _positional_data[x]['extra_values'] = _split_cell_values[1:]
                            _positional_data[x]['finished'] = False
                            _positional_data[x]['has_ruler'] = False

                    self._print_cells(_positional_data, len(_tcolumns)-1, 
                                        _table_data, _cell_outside_left, _cell_outside_right, _cell_divider, 
                                        cell_text_color, h_boarder_color, h_cell_boarder, color_reset)
                    _table_data.append(f"{_h}")

                _table_num += 1
                
                for _rdata in _table_data:
                    print(("%s%s") % (_leading_row_format, "".join(_rdata)))
        except Exception as e:
            raise e
    #endregion

    #region Clean Headers
    def _clean_data(self, data: dict):
        try:
            _tmp = {}
            for key, value in data.items():
                if len(key) % 2 == 0:
                    _tmp[key] = value
                else:
                    _nkey = ("%s " % key)
                    _tmp[_nkey] = value
            return _tmp
        except Exception as e:
            raise e 

    def _clean_columns(self, columns: List[str]):
        try:
            _tmp = []
            for column in columns:
                if len(column) % 2 == 0:
                    _tmp.append(column)
                else:
                    _ncol = ("%s " % column)
                    _tmp.append(_ncol)
            return _tmp
        except Exception as e:
            raise e 
    #endregion

    #region Print Table
    def table(self, 
                columns: List[str] = None, 
                data: dict = None, 
                title: str = None,
                schema: TableBaseSchema = TableDefaultSchema(),
                newlines_after_table: int = 2,
                newlines_before_table: int = 2):
        try: 
            if (columns == None or columns == []) and (data == None or data == {}):
                raise Exception(f"UNABLE TO PRINT TABLE :: NO DATA :: COLUMNS ({columns}) :: DATA ({data})")
            else:
                _t_size = get_terminal_size()

                if data != None:
                    _cleaned_data = self._clean_data(data)
                else:
                    _cleaned_data = None
                
                if columns == None or columns == []:
                    _cleaned_columns = self._clean_columns(data.keys())
                else:
                    _cleaned_columns = self._clean_columns(columns)

                _requested_size =  self._get_max_sizes(
                                                        headers=_cleaned_columns, 
                                                        data=_cleaned_data, 
                                                        max_terminmal_size=_t_size.columns, 
                                                        max_column_count=schema.column_count
                                                    )

                _table_data = self._get_combined_data(
                                                        title=title,
                                                        sizes=_requested_size,
                                                        headers_list=_cleaned_columns,
                                                        tdata=_cleaned_data,
                                                        min=schema.min_cell_size,
                                                        max=_t_size.columns,
                                                        max_columns=schema.column_count
                                                    )

                print("\n" * newlines_before_table)
                self._print_table(
                    table_data=_table_data,
                    schema=schema
                )
                print("\n" * newlines_after_table)
        except Exception as e:
            raise e
    #endregion
    