import os, importlib
from settings import LANGUAGE_CODE
lex_name = "en"
if os.path.exists("i18n/%s.py"%LANGUAGE_CODE.lower()):
    lex_name = LANGUAGE_CODE.lower()
lq_lex_module = importlib.import_module("i18n.%s"%lex_name)
lq_lexicon = lq_lex_module.Lexicon

def var_exists(smth,obj=None):
    if not obj is None:
        return hasattr(obj,smth)
    return smth in locals() or smth in globals()
    
def get_function(fname,obj=None):
    if not obj is None:
        if hasattr(obj,fname):
            return getattr(obj,fname)
    if fname in locals():
        return locals()[fname]
    if fname in globals():
        return globals()[fname]
    return lambda *x: None
    
    
#CLASSES
class LQ_C(BaseConstants):
    # BLOCPAGEDATA_IN_PARTICIPANT = True
    TAGS_IN_TEXT = True
    APP_NAME=os.path.basename(os.path.dirname(__file__))
    LQ_PATH=os.path.join(os.getcwd(),APP_NAME,"leepquest.xlsx")
    if not os.path.exists(LQ_PATH): LQ_PATH=os.path.join(os.getcwd(),APP_NAME,APP_NAME+".xlsx")
    if os.path.exists(LQ_PATH):
        LQ_XLSX = pandas.ExcelFile(LQ_PATH)
        BLOCPAGES=[]
        for sheet in LQ_XLSX.sheet_names:
            if sheet[0] != '#':
                BLOCPAGES.append(sheet.upper())
                sh_df=LQ_XLSX.parse(sheet)
                for scol in list(sh_df.columns):
                    if scol[0] != '#':
                        cvarname=sheet.upper()+'_'+scol.upper()
                        tempvar=list(sh_df[scol])
                        ne_found=False
                        for i, x in reversed(list(enumerate(tempvar))):
                            # print(i,x)
                            if isinstance(x,str) and scol.upper() in ['LIST'] and x=='-':
                                ne_found=True
                                tempvar[i]=''
                            if isinstance(x,str) and scol.upper() in ['TYPES']:
                                tempvar[i]=x.lower()
                            if i==0 or scol.upper() in ['OPTS']: ne_found=True
                            if isinstance(x,float) and math.isnan(x):
                                if not ne_found: del tempvar[i]
                                else: tempvar[i]=''
                            else:
                                ne_found=True
                        del i,x,ne_found       
                        tempvar=[str(int(x) if isinstance(x,float) else x) for x in tempvar]
                        if scol.upper() in ['TYPES','OPTS','DEPS']:
                            tempvar=[[z.strip() for z in y] for y in [x.split(':') for x in tempvar]]
                        elif scol.upper() in ['BY', 'TITLE']:
                            if len(tempvar) == 1: 
                                tempvar = tempvar[0]
                                if scol.upper() in ['BY'] and str(tempvar).isnumeric() and int(tempvar)==0 : tempvar=sh_df.shape[0]
                        elif scol.upper() in ['RANDOMORDERS_SHOWNUMBERS', 'SAME_ORDERS_IN_ALL_ROUNDS']:
                            tempvar=[bool(int(str(x).lower().replace('false','0').replace('true','1'))) for x in tempvar]
                        elif scol.upper() in ['RANDOMORDERS']:
                            tempvar=[x.split(';') if ';' in x else sheet.upper()+"_"+x for x,sheet in zip(tempvar,[sheet]*len(tempvar))]
                        locals()[cvarname]=tempvar
                        # print(cvarname,tempvar)
                        del tempvar
                del scol, sh_df
        del sheet, LQ_XLSX
        TRACK_BLOCPAGE_LOADS = BLOCPAGES
    else:
        if var_exists('CUSTOM_LQ_C'):
            # an optional class CUSTOM_LQ_C should be added inside __init__.py of the app, above PlayerVariables class if there is no excel file for the parameters. The structure of the CUSTOM_LQ_C should be the same as in the else block below.
            cpdict=CUSTOM_LQ_C.__dict__
            for cpkey in cpdict:
                locals()[cpkey]=cpdict[cpkey]
            del cpkey,cpdict,__dict__
        else:
            # this is an example
            BLOCPAGES="A;B".split(';')
            TRACK_BLOCPAGE_LOADS = "A;B".split(';')
            A_LIST = "How old are you?;What is the highest degree you have obtained?;Please also answer the following question:;What is your gender?;What is your country of birth?;How many people are there in your household? ;Optional question: What percentage of your total income…;Are you a student?;If yes, what is your field of study?;If other, please specify...".split(';')
            A_TYPES = [x.split(':') for x in "slider:int;radio;info;hradio;select;int;slider:float:optional:vertical/350px;radio;radio;stext;radio".split(';')]
            A_OPTS = [x.split(':') for x in "99:18:1:18;No diploma:Primary education certificate:Old BEPC certificate:Vocational Training Certificate (CAP):Professional Education Certificate (BEP):Technical and Vocational High School Diploma:General High School Diploma:BAC +2 (DUT, BTS, DEUG):Higher education degree (Master’s or Grandes Écoles) ;;Man:Woman:I prefer <b><u>not</u></b> to answer;France:Abroad;:0:suff=person(s);0:100:0.1:inv:%:None at all/All income:0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100/1;Yes:No;Economics:Law:Other;".split(';')]
            A_VARS = "age;diploma;a_info_1;genre;pays;household_size;savings_perc;student;study_domain;study_domain_other".split(";")
            A_BY=2
            A_BY_INTRO=["Example without excel file"]
            # A_NO_SCREEN_TIME = True
            A_TITLE="Questionnaire"
            B_ACTIVITIES_LIST="job_satisfaction;volunteer_charity;community_events;sports_club;environmental_initiatives;student_organizations;nonprofit_donations;neighborhood_meetings;youth_mentoring;political_rallies;cultural_events;reading_clubs;online_activism".split(";")
            B_LIST = "On a scale from 1 (very dissatisfied) to 5 (very satisfied), how satisfied are you with your current job?;Volunteering for local charities;Attending community events;Participating in sports clubs;Taking part in environmental initiatives;Involvement in student organizations;Regular donations to non-profit causes;Participation in neighborhood meetings;Mentoring youth programs;Attendance at political rallies;Organizing cultural events;Membership in reading clubs;Taking part in online activism;I think I am a person of worth, at least equal to anyone else.;I think I have a number of good qualities;All things considered, I am inclined to view myself as a failure;I am able to do things as well as most people;I feel little reason to be proud of myself;I have a positive attitude toward myself;Overall, I am satisfied with myself;I wish I could have more respect for myself;Sometimes I feel really useless;I sometimes think I am a good-for-nothing".split(";")
            B_TYPES = [x.split(':') for x in ["radioline:1-5"]+["checkbox:inline"]*len(B_ACTIVITIES_LIST)+"radiotable:first;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable:last".split(';')]
            B_OPTS = [x.split(':') for x in ["(very dissatisfied)::::(very satisfied)"]+["YES:NO"]*len(B_ACTIVITIES_LIST)+["Strongly disagree:Somewhat disagree:Somewhat agree:Strongly agree"]*10]
            B_VARS = ["job_satisfaction"]+B_ACTIVITIES_LIST+"self_estim_01;self_estim_02;self_estim_03;self_estim_04;self_estim_05;self_estim_06;self_estim_07;self_estim_08;self_estim_09;self_estim_10".split(";")
            B_BY = "1;12;10".split(';')
            B_BY_INTRO = "Example without excel file;Which of the following activities do you regularly participate in?;For each of the following characteristics or descriptions, indicate how true each one is for you.".split(';')
            B_RANDOMORDERS=["B_ACTIVITIES_LIST","self_estim_01;self_estim_02;self_estim_03;self_estim_04;self_estim_05;self_estim_06;self_estim_07;self_estim_08;self_estim_09;self_estim_10".split(';')]
            B_RANDOMORDERS_SHOWNUMBERS=[True,False]
            # B_SAME_ORDERS_IN_ALL_ROUNDS=[False]
    for i in range(len(BLOCPAGES)):
        locals()[BLOCPAGES[i]+"_QNUMS"]=list(range(1,len(locals()[BLOCPAGES[i]+"_LIST"])+1))
        if i==len(BLOCPAGES)-1: del i  

from otree.api import (
    models, BasePlayer
)

class Player(BasePlayer):
    if var_exists('PlayerVariables'):
        cpdict=PlayerVariables.__dict__
        for cpkey in cpdict:
            locals()[cpkey]=cpdict[cpkey]
        del cpkey,cpdict,__dict__
    ### blocpage stuff below
    if not hasattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT") or not getattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        blocpagedata=models.LongStringField(initial="")
        blocpageindex=models.IntegerField(initial=0)
        blocpagelasttime=models.FloatField(initial=0.0)
    if hasattr(LQ_C,"TRACK_BLOCPAGE_LOADS"):
        for i in range(len(LQ_C.TRACK_BLOCPAGE_LOADS)):
           if LQ_C.TRACK_BLOCPAGE_LOADS[i].strip() != '': 
            locals()[LQ_C.TRACK_BLOCPAGE_LOADS[i]+"_nloads"]=models.IntegerField(initial=0)
            locals()[LQ_C.TRACK_BLOCPAGE_LOADS[i]+"_loadtime"]=models.FloatField(initial=-11,blank=True)
           if i==len(LQ_C.TRACK_BLOCPAGE_LOADS)-1: del i
    for bpi in range(len(LQ_C.BLOCPAGES)):
        cbp=LQ_C.BLOCPAGES[bpi]
        if hasattr(LQ_C,cbp+"_RANDOMORDERS"):
            for rpi in range(len(getattr(LQ_C,cbp+"_RANDOMORDERS"))):
                vars_for_orders = getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi] if isinstance(getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi], list) else getattr(LQ_C,getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi])
                var_name=getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi].lower()+"_orders" if not isinstance(getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi], list) else  cbp+"_orders_"+str(rpi+1)
                locals()[var_name]=models.StringField()
                for i in list(range(1,len(vars_for_orders)+1)):
                    locals()[vars_for_orders[i-1]+"_order"]=models.IntegerField(initial=-11,blank=True)
                    if i == len(vars_for_orders): 
                        del i
                if rpi == len(getattr(LQ_C,cbp+"_RANDOMORDERS"))-1:
                    del rpi, vars_for_orders, var_name
        by_list=[getattr(LQ_C,cbp+'_BY')]*math.ceil(len(getattr(LQ_C,cbp+'_LIST'))/int(getattr(LQ_C,cbp+'_BY'))) if not isinstance(getattr(LQ_C,cbp+'_BY'),list) else getattr(LQ_C,cbp+'_BY')
        for i in getattr(LQ_C,cbp+"_QNUMS"):
            cblank=False
            min_index=1; max_index=0
            if getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="int" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="float" or (getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="slider" and len(getattr(LQ_C,cbp+'_TYPES')[i-1])>1 and getattr(LQ_C,cbp+'_TYPES')[i-1][1] in ["int","float"]):
                if len(getattr(LQ_C,cbp+'_OPTS')[i-1])>1 and getattr(LQ_C,cbp+'_OPTS')[i-1][0].strip()!="" and getattr(LQ_C,cbp+'_OPTS')[i-1][1].strip()!="" :
                    if float(getattr(LQ_C,cbp+'_OPTS')[i-1][0].strip())<float(getattr(LQ_C,cbp+'_OPTS')[i-1][1].strip()):
                        max_index = 1; min_index = 0
            # print(getattr(LQ_C,cbp+'_TYPES')[i-1][0])
            for h in range(1,len(getattr(LQ_C,cbp+'_TYPES')[i-1])):
                if getattr(LQ_C,cbp+'_TYPES')[i-1][h] in ["optional", "readonly", "disabled"]: cblank = True
                if h==len(getattr(LQ_C,cbp+'_TYPES')[i-1])-1: del h
            if not cblank and hasattr(LQ_C,cbp+"_DEPS"):
                for h in range(len(getattr(LQ_C,cbp+'_DEPS'))):
                    if getattr(LQ_C,cbp+'_DEPS')[h][0]==getattr(LQ_C,cbp+'_VARS')[i-1]: cblank = True
                    if h==len(getattr(LQ_C,cbp+'_DEPS'))-1: del h
            if getattr(LQ_C,cbp+"_TYPES")[i-1][0]=="radio":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=[[h+1,x] for h,x in enumerate(getattr(LQ_C,cbp+'_OPTS')[i-1])],widget=widgets.RadioSelect, blank=cblank)
                # print(getattr(LQ_C,cbp+'_VARS')[i-1],cblank)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=getattr(LQ_C,cbp+'_OPTS')[i-1],widget=widgets.RadioSelect,blank=True)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="hradio" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radiotable":
                # print(getattr(LQ_C,cbp+'_VARS')[i-1])
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=[[h+1,x] for h,x in enumerate(getattr(LQ_C,cbp+'_OPTS')[i-1])],widget=widgets.RadioSelectHorizontal, blank=cblank)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=getattr(LQ_C,cbp+'_OPTS')[i-1],widget=widgets.RadioSelectHorizontal,blank=True)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radioline":
                suph=1 if len(getattr(LQ_C,cbp+'_TYPES')[i-1]) == 1 else int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[0]) if getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[0].strip() != '' else -int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[1])
                ctypesvals=[]
                cstep=1 if len(getattr(LQ_C,cbp+'_TYPES')[i-1]) ==1 or len(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')) == 1 or int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[1 if suph<0 else 0])<=int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[-1]) else -1
                for h in range(0,len(getattr(LQ_C,cbp+'_OPTS')[i-1])): ctypesvals.append([(str(h*cstep+suph)+"#line#" if not 'nonumbers' in getattr(LQ_C,cbp+'_TYPES')[i-1] and (len(getattr(LQ_C,cbp+'_TYPES')[i-1]) ==1 or len(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')) == 1 or (h*cstep+suph>=min([suph,int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[-1])]) and h*cstep+suph<=max([suph,int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[-1])]))) else '')+getattr(LQ_C,cbp+'_OPTS')[i-1][h],suph,cstep])
                # print("ctypesvals = ",ctypesvals)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=[[x[2]*h+x[1],x[0]] for h,x in enumerate(ctypesvals)],widget=widgets.RadioSelectHorizontal, blank=cblank)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=getattr(LQ_C,cbp+'_OPTS')[i-1],widget=widgets.RadioSelectHorizontal,blank=True)
                del suph,ctypesvals,cstep,h
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="checkbox":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.BooleanField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], widget=widgets.CheckboxInput, blank=True, initial=False)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=getattr(LQ_C,cbp+'_OPTS')[i-1],blank=True)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="select":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=[[h+1,x] for h,x in enumerate(getattr(LQ_C,cbp+'_OPTS')[i-1])], blank=cblank)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(LQ_C,cbp+'_LIST')[i-1],choices=getattr(LQ_C,cbp+'_OPTS')[i-1],blank=True)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="slider" and len(getattr(LQ_C,cbp+'_TYPES')[i-1])>1 and  getattr(LQ_C,cbp+'_TYPES')[i-1][1]=="int":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], max=int(getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()) if getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()!="" else None, min=int(getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()) if len(getattr(LQ_C,cbp+'_OPTS')[i-1])>1 and getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()!="" else None, blank=cblank)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="slider" and (len(getattr(LQ_C,cbp+'_TYPES')[i-1])<=1 or getattr(LQ_C,cbp+'_TYPES')[i-1][1]=="float"):
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.FloatField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], max=float(getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()) if getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()!="" else None, min=float(getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()) if len(getattr(LQ_C,cbp+'_OPTS')[i-1])>1 and getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()!="" else None, blank=cblank)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="ltext" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="longstring":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.LongStringField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], blank=cblank)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="stext" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="string":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.StringField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], blank=cblank)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="int":
                # print(getattr(LQ_C,cbp+'_VARS')[i-1],cblank)
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], max=int(getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()) if getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()!="" else None, min=int(getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()) if len(getattr(LQ_C,cbp+'_OPTS')[i-1])>1 and getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()!="" else None, blank=cblank)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="float":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.FloatField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], max=float(getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()) if getattr(LQ_C,cbp+'_OPTS')[i-1][max_index].strip()!="" else None, min=float(getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()) if len(getattr(LQ_C,cbp+'_OPTS')[i-1])>1 and getattr(LQ_C,cbp+'_OPTS')[i-1][min_index].strip()!="" else None, blank=cblank)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="info":
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]]=models.BooleanField(variable=getattr(LQ_C,cbp+'_VARS')[i-1], label=getattr(LQ_C,cbp+'_LIST')[i-1], blank=True)
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="nothing":
                pass
            if not (not isinstance(getattr(LQ_C,cbp+'_BY'),list) and str(getattr(LQ_C,cbp+'_BY')) == '0') and getattr(LQ_C,cbp+'_TYPES')[i-1][0] not in ["info","nothing"]:
                locals()[getattr(LQ_C,cbp+'_VARS')[i-1]+"_time"]=models.FloatField(blank=True, initial=-11)
            if i == len(getattr(LQ_C,cbp+"_QNUMS")): 
                del i, cblank
        for i in list(range(1,len(by_list)+1)):
            if not hasattr(LQ_C,cbp+'_NO_SCREEN_TIME') or not getattr(LQ_C,cbp+'_NO_SCREEN_TIME'):
                locals()[cbp+"_screen"+str(i)+"_time"]=models.FloatField(initial=-11,blank=True)
            if i == len(by_list): 
                del i
        if hasattr(LQ_C,cbp+"_BY_ERRORVARS"):
            for i in range(len(getattr(LQ_C,cbp+"_BY_ERRORVARS"))):
               if getattr(LQ_C,cbp+"_BY_ERRORVARS")[i].strip() != '': 
                locals()[getattr(LQ_C,cbp+"_BY_ERRORVARS")[i]]=models.IntegerField(initial=0,blank=True)
               if i==len(getattr(LQ_C,cbp+"_BY_ERRORVARS"))-1: del i    
        if hasattr(LQ_C,cbp+"_ANSWERS_VARS"):
            for i in range(len(getattr(LQ_C,cbp+"_ANSWERS_VARS"))):
               if getattr(LQ_C,cbp+"_ANSWERS_VARS")[i].strip() != '': 
                locals()[getattr(LQ_C,cbp+"_ANSWERS_VARS")[i]]=models.StringField(initial='',blank=True)
               if i==len(getattr(LQ_C,cbp+"_ANSWERS_VARS"))-1: del i    
        if bpi == len(LQ_C.BLOCPAGES)-1:
            del bpi, cbp, by_list, min_index, max_index
    participant_startpageindex=models.IntegerField(initial=-1)# FUNCTIONS
    ### blocpage stuff above

# FUNCTIONS
def LQ_creating_session(subsession):
    session = subsession.session
    period = subsession.round_number
    players=subsession.get_players()
    import random
    for player in players :
        ### blocpage stuff below
        for i,cbp in enumerate(LQ_C.BLOCPAGES):
            if hasattr(LQ_C,cbp+"_RANDOMORDERS"):
               for ovi,ov in enumerate(getattr(LQ_C,cbp+"_RANDOMORDERS")):
                make_random_orders(player,i,ov,ovi,period)
        if hasattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT"):
            player.participant.blocpagedata=""
            player.participant.blocpageindex=0
            player.participant.blocpagelasttime=0.0
        ### blocpage stuff above

### blocpage stuff below        
def make_random_orders(player, cbpi: int, var_name_or_list, roi : int, period : int):
    import random
    cbp=LQ_C.BLOCPAGES[cbpi]
    init_list=getattr(LQ_C,var_name_or_list) if not isinstance(var_name_or_list, list) else var_name_or_list
    orders=list(range(1,len(init_list)+1))
    random.shuffle(orders)
    orders_list=str.join(',',[str(o) for o in orders])
    var_name=var_name_or_list.lower()+"_orders" if not isinstance(var_name_or_list, list) else  cbp+"_orders_"+str(roi+1)
    if(hasattr(LQ_C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")):
        if (isinstance(getattr(LQ_C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS"),bool) and getattr(LQ_C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")) or (isinstance(getattr(LQ_C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS"),list) and cbpi<len(getattr(LQ_C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")) and getattr(LQ_C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")[cbpi]):
            if period>1:
                orders_list = getattr(player.in_round(1),var_name)
    setattr(player,var_name,orders_list)
def get_random_orders(player, var_name_or_list, roi : int, cbp : str):
    var_name=var_name_or_list.lower()+"_orders" if not isinstance(var_name_or_list, list) else  cbp+"_orders_"+str(roi+1)
    orders=[int(o) for o in getattr(player,var_name).split(',')]
    init_list=getattr(LQ_C,var_name_or_list) if not isinstance(var_name_or_list, list) else var_name_or_list
    var_orders=[]
    for i,o in enumerate(orders): 
        var_orders.append(init_list[o-1])
        setattr(player,init_list[o-1]+"_order",0) #i+1
    return var_orders

def track_reloads(player, page):
    if hasattr(LQ_C,"TRACK_BLOCPAGE_LOADS") and page in LQ_C.TRACK_BLOCPAGE_LOADS:
        setattr(player,page+"_nloads",getattr(player,page+"_nloads",0)+1)

def get_current_blocpage(player, shift=0):
    blocpageindex = get_blocpage_index(player) + shift
    return LQ_C.BLOCPAGES[blocpageindex%len(LQ_C.BLOCPAGES)]

def get_blocpage_index(player):
    if player.participant_startpageindex < 0:
        my_start_index=0
        for i in range(len(page_sequence)):
            if page_sequence[i].__name__ == 'BlocPage': break
            my_start_index+=1
        player.participant_startpageindex = player.participant._index_in_pages - my_start_index
    cindex=-1
    if hasattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        cindex = player.participant.blocpageindex
    else:
        cindex = player.blocpageindex
    return cindex


def increment_blocpage_index(player, cthreshold=-1):
    import time
    ctime=time.time()
    done=False
    debug=hasattr(LQ_C,"DEBUG") and getattr(LQ_C,"DEBUG")
    if hasattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        if ctime-player.participant.blocpagelasttime>cthreshold:
            player.participant.blocpageindex+=1
            done=True
            if debug: print("incrementing participant.blocpageindex new is", player.participant.blocpageindex, end=". ")
        else:
            if debug: print("not incrementing participant.blocpageindex current is", player.participant.blocpageindex, end=". ")
            pass
        if debug and cthreshold>-1: print("prevtime",player.participant.blocpagelasttime, "current time", ctime, "diff", ctime-player.participant.blocpagelasttime, "threshold", cthreshold)
        if done: player.participant.blocpagelasttime=ctime;
    else:
        if ctime-player.blocpagelasttime>cthreshold:
            player.blocpageindex+=1
            done=True
            if debug: print("incrementing player.blocpageindex new is", player.blocpageindex, end=". ")
        else:
            if debug: print("not incrementing player.blocpageindex current is", player.blocpageindex, end=". ")
            pass
        if debug and cthreshold>-1: print("prevtime",player.blocpagelasttime, "current time", ctime, "diff", ctime-player.blocpagelasttime, "threshold", cthreshold)
        if done: player.blocpagelasttime=ctime;

def get_blocpage_data(player):
    if hasattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        return player.participant.blocpagedata.strip()
    else:
        return player.blocpagedata.strip()
def set_blocpage_data(player,data):
    if hasattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(LQ_C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        player.participant.blocpagedata = data
    else:
        player.blocpagedata = data

def blocpage_live_method(player, data):
    cbp=get_current_blocpage(player)
    status=data[:data.find('|')]
    if status=='load':
        # print('loading page...')
        track_reloads(player,cbp)
        if get_blocpage_data(player) != "":
            # print('apply',player.blocpagedata)
            return {player.id_in_group: 'apply|'+get_blocpage_data(player)}
        else: 
            set_blocpage_data(player,data[data.find('|')+1:])
            return {player.id_in_group: 'ok|'}
    if status=='update':
        blocpagedata=data[data.find('|')+1:]
        set_blocpage_data(player,blocpagedata)
    if status=='custom':
       eventdata=data[data.find('|')+1:]
       return bp_live_event(player,cbp,eventdata)


def get_opts_by_var(cbp,varname,what = "OPTS"):
    for i in getattr(LQ_C,cbp+"_QNUMS"):
        if getattr(LQ_C,cbp+'_VARS')[i-1] == varname:
            return getattr(LQ_C,cbp+'_'+what)[i-1]
# PAGES
class BlocPage(Page):
    form_model = 'player'
    live_method = blocpage_live_method
    @staticmethod
    def is_displayed(player):
        if player.participant_startpageindex < 0:
            my_start_index=0
            for i in range(len(page_sequence)):
                if page_sequence[i] == __class__: break
                my_start_index+=1
            player.participant_startpageindex = player.participant._index_in_pages - my_start_index
        cbp=get_current_blocpage(player)
        res=True
        # blockpages exlusions below
        supfunc='bp_is_displayed'
        if var_exists(supfunc):
            res = get_function(supfunc)(player,cbp)
        # blockpages exlusions above
        debug = hasattr(LQ_C,"DEBUG") and getattr(LQ_C,"DEBUG")
        cblocpageindex=get_blocpage_index(player)
        if debug : print("\nis_displayed, cbp is",cbp, ",round is", player.round_number, ", display",res,", cbp index:", get_blocpage_index(player), ", page index:", player.participant._index_in_pages, ", participant_startpageindex:", player.participant_startpageindex, ', len(page_sequence)',len(page_sequence))
        if not res:
            index_should_be=-1
            for i in range((player.participant._index_in_pages-player.participant_startpageindex)%len(page_sequence)+1):
                if page_sequence[i] == __class__: index_should_be+=1
            if debug : print("bp index_should_be",index_should_be, "bp index is",cblocpageindex)
            if index_should_be == cblocpageindex: increment_blocpage_index(player)
        if get_blocpage_index(player)>=page_sequence.count(__class__): res=False
        return res #player.round_number == LQ_C.NUM_ROUNDS #1
    @staticmethod
    def get_timeout_seconds(player):
        cbp=get_current_blocpage(player)
        res = None
        # blockpages timer conditions below
        res = get_function('bp_get_timeout_seconds')(player,cbp)
        # blockpages timer conditions above
        return res
    @staticmethod
    def get_form_fields(player):
        cbp=get_current_blocpage(player)
        res = []
        for i in getattr(LQ_C,cbp+"_QNUMS"):
            if getattr(LQ_C,cbp+"_TYPES")[i-1][0] != "nothing":
                if get_function('skip_some_bp_quests')(player,cbp,i,getattr(LQ_C,cbp+"_VARS")[i-1],"get_form_fields") or get_function('hide_some_bp_quests')(player,getattr(LQ_C,cbp+'_VARS')[i-1]): continue
                res.append(getattr(LQ_C,cbp+"_VARS")[i-1])
                if getattr(LQ_C,cbp+"_TYPES")[i-1][0] != "info": res.append(getattr(LQ_C,cbp+"_VARS")[i-1]+'_time')
        if not hasattr(LQ_C,cbp+'_NO_SCREEN_TIME') or not getattr(LQ_C,cbp+'_NO_SCREEN_TIME'):
            by_list=[getattr(LQ_C,cbp+'_BY')]*math.ceil(len(getattr(LQ_C,cbp+'_LIST'))/int(getattr(LQ_C,cbp+'_BY'))) if not isinstance(getattr(LQ_C,cbp+'_BY'),list) else getattr(LQ_C,cbp+'_BY')
            for h in range(1,len(by_list)+1):
                res.append(cbp+"_screen"+str(h)+"_time")
        if hasattr(LQ_C,cbp+"_RANDOMORDERS"):
           for rpi,ov in enumerate(getattr(LQ_C,cbp+"_RANDOMORDERS")):
            vars_for_orders = getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi] if isinstance(getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi], list) else getattr(LQ_C,getattr(LQ_C,cbp+"_RANDOMORDERS")[rpi])
            for x in vars_for_orders: res.append(x+'_order')
        if hasattr(LQ_C,cbp+"_ANSWERS_VARS"):
            for w in range(len(getattr(LQ_C,cbp+"_ANSWERS_VARS"))):
               if getattr(LQ_C,cbp+"_ANSWERS_VARS")[w].strip() != '': 
                res.append(getattr(LQ_C,cbp+"_ANSWERS_VARS")[w])
               if w==len(getattr(LQ_C,cbp+"_ANSWERS_VARS"))-1: del w
        if hasattr(LQ_C,"TRACK_BLOCPAGE_LOADS") and cbp in LQ_C.TRACK_BLOCPAGE_LOADS: res.append(cbp+"_loadtime")
        supfunc='bp_get_form_fields'
        if var_exists(supfunc):
            res += get_function(supfunc)(player,cbp)
        return res
    @staticmethod
    def before_next_page(player, timeout_happened):
        cbp=get_current_blocpage(player)
        next_cbp=get_current_blocpage(player,1)
        if hasattr(LQ_C,"DEBUG") and getattr(LQ_C,"DEBUG") : print("before_next_page, cbp is",cbp)
        set_blocpage_data(player,"")
        for i in getattr(LQ_C,cbp+"_QNUMS"):
            if get_function('skip_some_bp_quests')(player,cbp,i,getattr(LQ_C,cbp+"_VARS")[i-1],"before_next_page") or get_function('hide_some_bp_quests')(player,getattr(LQ_C,cbp+'_VARS')[i-1]): continue
            if getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radio" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="hradio" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="select" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radioline" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radiotable":
                if not player.field_maybe_none(getattr(LQ_C,cbp+'_VARS')[i-1]) is None:
                    # print(i,getattr(LQ_C,cbp+'_VARS')[i-1],getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]));
                    cindex=getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1])-1
                    if getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radioline" and len(getattr(LQ_C,cbp+'_TYPES')[i-1])>1 and len(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-'))>1:
                        firstrlval = int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[0]) if getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[0].strip() != '' else -int(getattr(LQ_C,cbp+'_TYPES')[i-1][1].split('-')[1])
                        lastrlval = int(getattr(LQ_C,cbp+'_TYPES')[i-1][-1].split('-')[-1])
                        if firstrlval>lastrlval:
                            cindex=lastval-getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1])
                        else:
                            cindex=getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1])-firstrlval
                    if var_exists('%s_choices'%getattr(LQ_C,cbp+'_VARS')[i-1]):
                        choices=get_function('%s_choices'%getattr(LQ_C,cbp+'_VARS')[i-1])(player)
                        for ch in choices:
                            if ch[0] == cindex + 1:
                               cstringval = ch[1]
                               break
                    else:
                        cstringval=getattr(LQ_C,cbp+'_OPTS')[i-1][cindex] if getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1])>0 else ""
                    setattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval",cstringval if cstringval != "" else "("+str(getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]))+")")
            if getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="checkbox":
                # print(getattr(LQ_C,cbp+'_VARS')[i-1],":",getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]))
                cstringval=getattr(LQ_C,cbp+'_OPTS')[i-1][1-int(getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]))] if len(getattr(LQ_C,cbp+'_OPTS')[i-1])>1 else ['Y','N'][1-int(getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]))]
                setattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]+"_strval",cstringval if cstringval != "" else "("+str(getattr(player,getattr(LQ_C,cbp+'_VARS')[i-1]))+")")
        get_function('bp_before_next_page')(player, timeout_happened, cbp,next_cbp)
        increment_blocpage_index(player)
            
    @staticmethod
    def vars_for_template(player):
        cbp=get_current_blocpage(player)
        slidervars=[]
        slideropts=[]
        vsliders=[]
        disabledsliders=[]
        vslider_height=400
        hslider_width='50%'
        radiolines=[]
        nonumbers=[]
        radiotable_headers=[]
        radiotable_bottoms=[]
        radiotable_rows=[]
        singleline=[]
        onlyinfo=[]
        suffixvars=[]
        suffixes=[]
        prefixvars=[]
        prefixes=[]
        title=""
        questtags=[]
        deps=[]
        if(hasattr(LQ_C,cbp+"_TITLE")): title=getattr(LQ_C,cbp+"_TITLE")
        presentation_template=""
        if os.path.exists(LQ_C.APP_NAME+"/include_"+cbp+".html"): presentation_template=LQ_C.APP_NAME+"/include_"+cbp+".html"
        # print("vars_for_template")
        for i in getattr(LQ_C,cbp+"_QNUMS"):
            if get_function('skip_some_bp_quests')(player,cbp,i,getattr(LQ_C,cbp+"_VARS")[i-1],"vars_for_template"): continue
            if getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="info" or getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="nothing" or get_function('hide_some_bp_quests')(player,getattr(LQ_C,cbp+'_VARS')[i-1]):
                onlyinfo.append(getattr(LQ_C,cbp+'_VARS')[i-1])
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="slider":
                slidervars.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                slideropts.append(str.join(':',getattr(LQ_C,cbp+'_OPTS')[i-1]))
                for h in range(1,len(getattr(LQ_C,cbp+'_TYPES')[i-1])):
                    if getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/')[0]=="vertical": 
                        vsliders.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                        if len(getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/'))>1 :
                            vslider_height=getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/')[1]
                    elif getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/')[0].startswith("hor") and len(getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/'))>1:
                        hslider_width=getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/')[1]
                for h in range(1,len(getattr(LQ_C,cbp+'_TYPES')[i-1])):
                    if getattr(LQ_C,cbp+'_TYPES')[i-1][h].split('/')[0] in ["readonly", "disabled"]: 
                        disabledsliders.append(getattr(LQ_C,cbp+'_VARS')[i-1])
            elif getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radioline":
                radiolines.append(getattr(LQ_C,cbp+'_VARS')[i-1])
            for h in range(1,len(getattr(LQ_C,cbp+'_TYPES')[i-1])):
                if getattr(LQ_C,cbp+'_TYPES')[i-1][h]=="inline":
                    singleline.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                if getattr(LQ_C,cbp+'_TYPES')[i-1][h]=="nonumbers":
                    nonumbers.append(getattr(LQ_C,cbp+'_VARS')[i-1])
            for h in range(1,len(getattr(LQ_C,cbp+'_OPTS')[i-1])):
                if getattr(LQ_C,cbp+'_OPTS')[i-1][h][:5]=="suff=":
                    suffixvars.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    suffixes.append(dict(var=getattr(LQ_C,cbp+'_VARS')[i-1], val=getattr(LQ_C,cbp+'_OPTS')[i-1][h][5:]))
                if getattr(LQ_C,cbp+'_OPTS')[i-1][h][:5]=="pref=":
                    prefixvars.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    prefixes.append(dict(var=getattr(LQ_C,cbp+'_VARS')[i-1], val=getattr(LQ_C,cbp+'_OPTS')[i-1][h][5:]))
            if getattr(LQ_C,cbp+'_TYPES')[i-1][0]=="radiotable":
                if len(getattr(LQ_C,cbp+'_TYPES')[i-1]) <= 1 or getattr(LQ_C,cbp+'_TYPES')[i-1][1] == "row":
                    radiotable_rows.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                elif len(getattr(LQ_C,cbp+'_TYPES')[i-1]) > 1 and getattr(LQ_C,cbp+'_TYPES')[i-1][1] == "first":
                    radiotable_headers.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    radiotable_rows.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                elif len(getattr(LQ_C,cbp+'_TYPES')[i-1]) > 1 and getattr(LQ_C,cbp+'_TYPES')[i-1][1] == "last":
                    radiotable_bottoms.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    radiotable_rows.append(getattr(LQ_C,cbp+'_VARS')[i-1])
            cqtag='h5' if not getattr(LQ_C,cbp+'_VARS')[i-1] in radiotable_rows else 'th'
            if(hasattr(LQ_C,cbp+"_QUESTTAG")):
                cqtag_cand = getattr(LQ_C,cbp+"_QUESTTAG")[i-1] if i <= len(getattr(LQ_C,cbp+"_QUESTTAG")) else getattr(LQ_C,cbp+"_QUESTTAG")[-1]
                if str(cqtag_cand)!='' and str(cqtag_cand)!='-' and str(cqtag_cand)!='0': cqtag=cqtag_cand
            questtags.append(dict(var=getattr(LQ_C,cbp+'_VARS')[i-1],tag=cqtag))
        if hasattr(LQ_C,cbp+"_DEPS"):
            for h in range(len(getattr(LQ_C,cbp+'_DEPS'))):
                deps.append(str.join(':',getattr(LQ_C,cbp+'_DEPS')[h]))
        mintime_text=lq_lexicon['next_button_will_appear_soon']
        allvars=[]
        for vi,v in enumerate(getattr(LQ_C,cbp+'_VARS')): 
            if get_function('skip_some_bp_quests')(player,cbp,vi+1,v,"vars_for_template"): continue
            if getattr(LQ_C,cbp+'_TYPES')[vi][0]=="nothing" or get_function('hide_some_bp_quests')(player,v) : allvars.append("__info__");
            else: allvars.append(getattr(LQ_C,cbp+'_VARS')[vi])
        res = dict(
            questtags=questtags,
            deps=deps,
            slidervars=slidervars,
            radiolines=radiolines,
            nonumbers=nonumbers,
            vsliders=vsliders,
            readonlysliders=disabledsliders,
            vslider_height=str(vslider_height)+('px' if not any(sub in str(vslider_height) for sub in ('px', '%')) else ''),
            hslider_width=str(hslider_width)+('px' if not any(sub in str(hslider_width) for sub in ('px', '%')) else ''),
            onlyinfo=onlyinfo,
            radioline_width=getattr(LQ_C,cbp+"_RADIOLINE_WIDTH")[0] if hasattr(LQ_C,cbp+"_RADIOLINE_WIDTH") and getattr(LQ_C,cbp+"_RADIOLINE_WIDTH")[0] != '' else "120px",
            radioline_width_nonumbers=getattr(LQ_C,cbp+"_RADIOLINE_WIDTH_NONUMBERS")[0] if hasattr(LQ_C,cbp+"_RADIOLINE_WIDTH_NONUMBERS") and getattr(LQ_C,cbp+"_RADIOLINE_WIDTH_NONUMBERS")[0] != '' else getattr(LQ_C,cbp+"_RADIOLINE_WIDTH")[0] if hasattr(LQ_C,cbp+"_RADIOLINE_WIDTH") and getattr(LQ_C,cbp+"_RADIOLINE_WIDTH")[0] != '' else "50px",
            radioline_leftright_width_px=int(getattr(LQ_C,cbp+"_RADIOLINE_LEFTRIGH_PX")[0]) if hasattr(LQ_C,cbp+"_RADIOLINE_LEFTRIGH_PX") and getattr(LQ_C,cbp+"_RADIOLINE_LEFTRIGH_PX")[0] != '' else 0, #100
            quest_width_px=int(getattr(LQ_C,cbp+"_QUEST_WIDTH_PX")[0]) if hasattr(LQ_C,cbp+"_QUEST_WIDTH_PX") and getattr(LQ_C,cbp+"_QUEST_WIDTH_PX")[0] != '' else 0, #600
            separate_line=getattr(LQ_C,cbp+"_SEPARATE_LINE")[0] if hasattr(LQ_C,cbp+"_SEPARATE_LINE") and getattr(LQ_C,cbp+"_SEPARATE_LINE")[0] != "0" else False, #600
            choice_label_tag=getattr(LQ_C,cbp+"_OPTS_TAG")[0] if hasattr(LQ_C,cbp+"_OPTS_TAG") and getattr(LQ_C,cbp+"_OPTS_TAG")[0] != "0" else "", #600
            singleline=singleline,
            waitnext_text=mintime_text,
            radiotable_headers=radiotable_headers,
            radiotable_rows=radiotable_rows,
            radiotable_bottoms=radiotable_bottoms,
            cslidervars=str.join(';',slidervars),
            cslideropts=str.join(';',slideropts),
            cvsliders=str.join(';',vsliders),
            cdisabledsliders=str.join(';',disabledsliders),
            all_vars=[v for v in allvars if v != "__info__"],
            allvars=str.join(';',allvars),
            by=str.join(',',[str(getattr(LQ_C,cbp+'_BY'))]*math.ceil(len(getattr(LQ_C,cbp+'_LIST'))/int(getattr(LQ_C,cbp+'_BY'))) if not isinstance(getattr(LQ_C,cbp+'_BY'),list) else getattr(LQ_C,cbp+'_BY')),
            title=title,
            suffixvars=suffixvars,
            suffixes=suffixes,
            prefixvars=prefixvars,
            prefixes=prefixes,
            presentation_template=presentation_template,
            lq_lexicon = lq_lexicon,
        )
        if hasattr(LQ_C,cbp+"_ANSWERS_VARS"): res['answers_vars']=';'.join(getattr(LQ_C,cbp+"_ANSWERS_VARS"))
        supfunc='bp_vars_for_template'
        if var_exists(supfunc):
            res |= get_function(supfunc)(player,cbp)
        # print(cbp,res)
        return res
    @staticmethod
    def js_vars(player):
        cbp=get_current_blocpage(player)
        firstrandoms=[]
        randomorders=[]
        shownumbers=[]
        confirm_empty=[]
        optionals=[]
        disabledvars=[]
        fixedsum_sliders=[]
        withtags=[]
        withouttags=[]
        for i in getattr(LQ_C,cbp+"_QNUMS"):
            for h in range(1,len(getattr(LQ_C,cbp+'_TYPES')[i-1])):
                if getattr(LQ_C,cbp+'_TYPES')[i-1][h] in ["optional", "readonly", "disabled"]: 
                    optionals.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    if getattr(LQ_C,cbp+'_TYPES')[i-1][h] in ["readonly", "disabled"]:
                        disabledvars.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    break
        if hasattr(LQ_C,cbp+"_RANDOMORDERS"):
           for ovi,ov in enumerate(getattr(LQ_C,cbp+"_RANDOMORDERS")):
            firstrandoms.append(ov[0] if isinstance(ov,list) else getattr(LQ_C,ov)[0])
            randomorders.append(get_random_orders(player,ov,ovi,cbp))
            if hasattr(LQ_C,cbp+"_RANDOMORDERS_SHOWNUMBERS"):
                if isinstance(getattr(LQ_C,cbp+"_RANDOMORDERS_SHOWNUMBERS"),bool): shownumbers.append(getattr(LQ_C,cbp+"_RANDOMORDERS_SHOWNUMBERS"))
                elif isinstance(getattr(LQ_C,cbp+"_RANDOMORDERS_SHOWNUMBERS"),list) and ovi<len(getattr(LQ_C,cbp+"_RANDOMORDERS_SHOWNUMBERS")):
                     shownumbers.append(getattr(LQ_C,cbp+"_RANDOMORDERS_SHOWNUMBERS")[ovi])                
        elif hasattr(LQ_C,cbp+"_SHOWNUMBERS"):
            for i in getattr(LQ_C,cbp+"_QNUMS"):
                if (isinstance(getattr(LQ_C,cbp+"_SHOWNUMBERS"),list)):
                    cshownumber = getattr(LQ_C,cbp+"_SHOWNUMBERS")[i-1] if i-1 < len(getattr(LQ_C,cbp+"_SHOWNUMBERS")) else getattr(LQ_C,cbp+"_SHOWNUMBERS")[-1]
                    shownumbers.append(cshownumber)
                elif int(getattr(LQ_C,cbp+"_SHOWNUMBERS")):
                    shownumbers.append(getattr(LQ_C,cbp+"_SHOWNUMBERS"))
        if hasattr(LQ_C,cbp+"_CONFIRM_BLANK"):
            for i in getattr(LQ_C,cbp+"_QNUMS"):
                if (isinstance(getattr(LQ_C,cbp+"_CONFIRM_BLANK"),list)):
                    c_confirm_empty = getattr(LQ_C,cbp+"_CONFIRM_BLANK")[i-1] if i-1 < len(getattr(LQ_C,cbp+"_CONFIRM_BLANK")) else getattr(LQ_C,cbp+"_CONFIRM_BLANK")[-1]
                    confirm_empty.append(c_confirm_empty)
                elif int(getattr(LQ_C,cbp+"_CONFIRM_BLANK")):
                    confirm_empty.append(getattr(LQ_C,cbp+"_CONFIRM_BLANK"))
        if hasattr(LQ_C,cbp+"_HASTAGS") or LQ_C.TAGS_IN_TEXT:
            for i in getattr(LQ_C,cbp+"_QNUMS"):
                chastags = LQ_C.TAGS_IN_TEXT
                if hasattr(LQ_C,cbp+"_HASTAGS"):
                    clastval = getattr(LQ_C,cbp+"_HASTAGS")[i-1] if i <= len(getattr(LQ_C,cbp+"_HASTAGS")) else getattr(LQ_C,cbp+"_HASTAGS")[-1]
                    chastags =  not (str(clastval) == '' or 'f' in str(clastval).lower() or str(clastval) == '0' or 'n' in str(clastval).lower())
                    if not chastags: withouttags.append(getattr(LQ_C,cbp+'_VARS')[i-1])
                    # print(getattr(LQ_C,cbp+'_VARS')[i-1],clastval,chastags,LQ_C.TAGS_IN_TEXT);
                if chastags: withtags.append(getattr(LQ_C,cbp+'_VARS')[i-1])
        res = dict(
            hide_initial=False,
            bys_intro=getattr(LQ_C,cbp+"_BY_INTRO") if hasattr (LQ_C,cbp+"_BY_INTRO") else [""],
            prev_buttons=getattr(LQ_C,cbp+"_PREV_BUTTONS") if hasattr (LQ_C,cbp+"_PREV_BUTTONS") else [0],
            min_times=getattr(LQ_C,cbp+"_MIN_TIMES") if hasattr (LQ_C,cbp+"_MIN_TIMES") else [0],
            confirm_blank=confirm_empty,
            randomorders=randomorders,
            firstrandoms=firstrandoms,
            shownumbers=shownumbers,
            screentime_prefix=cbp+"_",
            fixedsum_sliders=fixedsum_sliders,
            withtags=withtags,
            withouttags=withouttags,
            optional_vars=optionals,
            disabled_vars=disabledvars,
            lq_lexicon = lq_lexicon,
            debug=False,
        )
        if hasattr(LQ_C,"TRACK_BLOCPAGE_LOADS") and cbp in LQ_C.TRACK_BLOCPAGE_LOADS: res['loadtimevar']=cbp+"_loadtime"
        supfunc='bp_js_vars'
        if var_exists(supfunc):
            res |= get_function(supfunc)(player,cbp)
        return res

