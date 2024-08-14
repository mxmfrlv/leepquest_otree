from otree.api import *
import math, random, os, pandas

from typing import Union,Optional,Callable,List,Dict,Any #in order to annotate the return types of *bp_* functions

class PlayerVariables:
    # additional player variables should be defined here
    test = models.IntegerField(initial = 1)
    # pass

# import leepquest:
with open('LQ.py','r', encoding="utf-8") as f:
    content = f.read()
exec(content)

# STANDARD OTREE CLASSES (except Player which is inside LQ.py with (optional) additional variables in the PlayerVariables class above)
# (the C class should inherit from the leepquest's LQ_C class (which inherits from BaseConstants) )
class C(LQ_C):
    pass 

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# FUNCTIONS
def creating_session(subsession: Subsession):
    LQ_creating_session(subsession) ## leepquest stuff
    # put additional logic below

# skip_some_bp_quests is used to skip some questions inside blocpages (cbp is the current blocpage, n is the question number, var is the question's variable name (cbp+n and var are interchangeable), function can one of "get_form_fields","vars_for_template","before_next_page" )
def skip_some_bp_quests(player:Player,cbp:str,n:int,var:str,function:Optional[str]=None) -> bool:
    # example: if cbp == 'B2' and n > 1 and player.treatment > 3: return True
    return False
    
# make_bp_type_nothing is also used to skip some questions inside blocpages (var is the question's variable name) but this function does not remove the corresponding part from blocpage sequence if blocpage's BY argument equals 1
def make_bp_type_nothing(player:Player, var:str)->bool:
    # example: if var == "others_evaluation" and player.treatment != 2 and player.treatment != 3: return True
    return False

# bp_is_displayed is used to dynamically exclude some blocpages (cbp is the current blocpage's name)
def bp_is_displayed(player:Player, cbp:str)->bool:
    return True

# bp_get_timeout_seconds is used to add a timeout to some blocpages, in should return (cbp is the current blocpage's name)
def bp_get_timeout_seconds(player:Player, cbp:str) -> Union[int,None]:
    # example: if cbp == "RAVEN" : return 60*C.RAVEN_MINUTES
    return None

# bp_get_form_fields is used to add additional fields to blocpages (the additional fields should be defined in PlayerVariables class above, created before importing LQ.py)
def bp_get_form_fields(player:Player, cbp:str) -> List[str]:
    return []

# bp_before_next_page is used to execute additional code before passing to the next blocpage (cbp is the current blocpage's name, next_cbp is the next blocpage's name)
def bp_before_next_page(player:Player,timeout_happened:bool, cbp:str, next_cbp:str) -> None:
    pass

# bp_vars_for_template is used to to add additional variables for blocpage template (cbp is the current blocpage's name)
def bp_vars_for_template(player:Player,cbp:str) -> Dict[str,Any]:
    return {}

# bp_js_vars is used to to add additional variables to the otree's js_vars (cbp is the current blocpage's name)
def bp_js_vars(player:Player,cbp:str) -> Dict[str,Any]:
    return {}


#PAGES
# define additional pages in a standard way

# class MyPage(Page):
    # pass 

# compose the page sequence :

# page_sequence = [MyPage, BlocPage] ### in order to place custom pages before blocpages
page_sequence = [BlocPage]

# the code below adds the necessary number of blocpages in order to correspond to the leepquest.xlsx (or [appname].xlsx) confifuration file
if page_sequence.count(BlocPage) < len(C.BLOCPAGES):
    for i in range(len(C.BLOCPAGES)-page_sequence.count(BlocPage)):
        page_sequence.append(BlocPage)

### a way to place additional custom pages at the end :
# custom_page_sequence=[MyPage]        
# page_sequence +=custom_page_sequence
