
# region Imports
from random import randint
from art import *
from colorama import Style, Fore
from nightcapcore.colors import NightcapColors
# endregion

class Splash(object):
    def __init__(self) -> None:
        # region Art String
        self.artString = '''
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
      
                                                                    
                   &                              &#                  
                   %:@                          #*:#                  
                   $..!&                      #%:.:#                  
                   $.:..*&                  #%:...:#                  
                   &::::.:*@              &%:.....%                   
                    $:..:::.!$&##&&&&##&$!:.:....*                    
                     #$*!:..:.::::::::::....:!*%&                     
                         #@%:.::::::::::.:%&                          
                             %::::::::::$                             
                     $        %#*::::*&$        $@                    
                 #  *%   *:!# &  !::!  # #!:*   &.# #                 
                **  :*   %!*# &  &..# #  #*!%   %.# *!#               
               *::@ @.@       &   **  #        $.$ @::!&              
              *:!!:$ &*%#     &   ##  ##     &**&#%::::!#             
             @:!!!!:!$##&##   %&      %%  ##&&&&%!::::::$             
             @:!!!!!!::*$&   &!!@    %::&  #@%!::!!:::::@             
              @!::::::::::!% &!!!$  *!!!&#%:::::::::::!$              
                #@@@$$$@$$%!!$!!!!#@!!!!%!!%$$$$$$$$@&                
                            #@*!!!$%!!!*$#                            
                               @!!!!!!$                               
                                #*!!*&                                
                                 &!!&                                 
                                  %%                                  
                                  &&                                  

                                  
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        '''
        # endregion

    # region Random Color
    def _randomColor(self) -> str:
        random = randint(0, 11)
        return NightcapColors().randomColor(random)
    # endregion

    def getSplash(self) -> str:
        # return NightcapBanner().Banner(artString~self.artString)
        rcolor = self._randomColor()
        print(Fore.LIGHTGREEN_EX)
        print(self.artString)
        print(Style.RESET_ALL)