from otree.api import *
import math, random, os

class C(BaseConstants):
    NAME_IN_URL = 'leepquest'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BLOCPAGES="A;B".split(';')
    # BLOCPAGEDATA_IN_PARTICIPANT = True
    TRACK_BLOCPAGE_LOADS = "A;B".split(';')
    A_LIST = "Quel âge avez-vous ?;Quel est le diplôme le plus élevé que vous avez obtenu ?;Veuillez également répondre à la question suivante :;Quel est votre genre ?;Quel est votre pays de naissance?".split(';')
    A_TYPES = [x.split(':') for x in "slider:int;radio;info;radio;select".split(';')]
    A_OPTS = [x.split(':') for x in "99:18:1:17;Sans diplôme:Certificat d’études primaires:Ancien brevet BEPC:Certificat d’aptitude professionnelle (CAP):Brevet d’enseignement professionnel (BEP):BAC d’enseignement technique et professionnel:BAC d’enseignement général:BAC +2 (DUT, BTS, D\EUG):Diplôme de l’enseignement supérieur (2ème ou 3ème cycles, grande école);;Homme:Femme;France:Etranger".split(';')]
    A_VARS = "age;diplome;a_info_1;genre;pays".split(";")
    A_BY=2
    A_BY_INTRO=[""]
    # A_NO_SCREEN_TIME = True
    A_TITLE="Questionnaire"
    B_ASSO_LIST="asso_gibiers;asso_neige;asso_petitsprinces;asso_armeschasse;asso_vehiculesepoque;asso_medecinsdumonde;asso_parachitistes;asso_medecinssansfrontiers;asso_industrienationale;asso_sourds;asso_ceramique;asso_yachtclub".split(";")
    B_LIST = "Sur une échelle de 1 (pas bénéfiques) à 5 (très bénéfiques), pensez-vous que les Associations Reconnues d’Utilité Publique (ARUP) sont généralement bénéfiques pour la société ?;Association nationale des chasseurs de grands gibiers;Association nationale pour l’étude de la neige et des avalanches ;Association des petits princes;Union nationale des propriétaires d’armes de chasse et de tir;Fédération française des véhicules d’époque;Médecins du monde;Union nationale des parachutistes;Médecins sans frontières;Société d’encouragement pour l’industrie nationale;Fédération nationale des sourds de France;Société française de céramique;Yacht club de France;Je pense que je suis une personne de valeur, au moins égale à n’importe qui d’autre;Je pense que je possède un certain nombre de belles qualités;Tout bien considéré, je suis porté-e à me considérer comme un-e raté-e;Je suis capable de faire les choses aussi bien que la majorité des gens;Je sens peu de raisons d’être fier-e de moi;J’ai une attitude positive vis-à-vis moi-même;Dans l’ensemble, je suis satisfait-e de moi;J’aimerais avoir plus de respect pour moi-même;Parfois je me sens vraiment inutile;Il m’arrive de penser que je suis un-e bon-ne à rien".split(";")
    B_TYPES = [x.split(':') for x in ["radioline:1-5"]+["checkbox:inline"]*len(B_ASSO_LIST)+"radiotable:first;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable;radiotable:last".split(';')]
    B_OPTS = [x.split(':') for x in ["(pas bénéfiques)::::(très bénéfiques)"]+["OUI:NON"]*len(B_ASSO_LIST)+["Tout à fait en désaccord:Plutôt en désaccord:Plutôt en accord:Tout à fait en accord"]*10]
    B_VARS = ["arup_benefiques"]+B_ASSO_LIST+"self_estim_01;self_estim_02;self_estim_03;self_estim_04;self_estim_05;self_estim_06;self_estim_07;self_estim_08;self_estim_09;self_estim_10".split(";")
    B_BY = "1;12;10".split(';')
    B_BY_INTRO = ";Lesquelles de ces associations sont selon vous des Associations Reconnues d’Utilité Publique ?;;Sur une échelle de « 1 » (jamais) à « 5 » (souvent), répondez aux affirmations suivantes :;Pour chacune des caractéristiques ou descriptions suivantes, indiquez à quel point chacune est vraie pour vous.".split(';')
    B_RANDOMORDERS=["B_ASSO_LIST","self_estim_01;self_estim_02;self_estim_03;self_estim_04;self_estim_05;self_estim_06;self_estim_07;self_estim_08;self_estim_09;self_estim_10".split(';')]
    B_RANDOMORDERS_SHOWNUMBERS=[True,False]
    # B_SAME_ORDERS_IN_ALL_ROUNDS=[False]
    for i in range(len(BLOCPAGES)):
        locals()[BLOCPAGES[i]+"_QNUMS"]=list(range(1,len(locals()[BLOCPAGES[i]+"_LIST"])+1))
        if i==len(BLOCPAGES)-1: del i  

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ### blocpage stuff below
    if not hasattr(C,"BLOCPAGEDATA_IN_PARTICIPANT") or not getattr(C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        blocpagedata=models.LongStringField(initial="")
        blocpageindex=models.IntegerField(initial=0)
    if hasattr(C,"TRACK_BLOCPAGE_LOADS"):
        for i in range(len(C.TRACK_BLOCPAGE_LOADS)):
           if C.TRACK_BLOCPAGE_LOADS[i].strip() != '': 
            locals()[C.TRACK_BLOCPAGE_LOADS[i]+"_nloads"]=models.IntegerField(initial=0)
            locals()[C.TRACK_BLOCPAGE_LOADS[i]+"_loadtime"]=models.FloatField(initial=-11,blank=True)
           if i==len(C.TRACK_BLOCPAGE_LOADS)-1: del i
    for bpi in range(len(C.BLOCPAGES)):
        cbp=C.BLOCPAGES[bpi]
        if hasattr(C,cbp+"_RANDOMORDERS"):
            for rpi in range(len(getattr(C,cbp+"_RANDOMORDERS"))):
                vars_for_orders = getattr(C,cbp+"_RANDOMORDERS")[rpi] if isinstance(getattr(C,cbp+"_RANDOMORDERS")[rpi], list) else getattr(C,getattr(C,cbp+"_RANDOMORDERS")[rpi])
                var_name=getattr(C,cbp+"_RANDOMORDERS")[rpi].lower()+"_orders" if not isinstance(getattr(C,cbp+"_RANDOMORDERS")[rpi], list) else  cbp+"_orders_"+str(rpi+1)
                locals()[var_name]=models.StringField()
                for i in list(range(1,len(vars_for_orders)+1)):
                    locals()[vars_for_orders[i-1]+"_order"]=models.IntegerField(initial=-11,blank=True)
                    if i == len(vars_for_orders): 
                        del i
                if rpi == len(getattr(C,cbp+"_RANDOMORDERS"))-1:
                    del rpi, vars_for_orders, var_name
        by_list=[getattr(C,cbp+'_BY')]*math.ceil(len(getattr(C,cbp+'_LIST'))/int(getattr(C,cbp+'_BY'))) if not isinstance(getattr(C,cbp+'_BY'),list) else getattr(C,cbp+'_BY')
        for i in getattr(C,cbp+"_QNUMS"):
            cblank=False
            for h in range(1,len(getattr(C,cbp+'_TYPES')[i-1])):
                if getattr(C,cbp+'_TYPES')[i-1][h]=="optional": cblank = True
                if h==len(getattr(C,cbp+'_TYPES')[i-1])-1: del h
            if getattr(C,cbp+"_TYPES")[i-1][0]=="radio":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1],choices=[[h+1,x] for h,x in enumerate(getattr(C,cbp+'_OPTS')[i-1])],widget=widgets.RadioSelect, blanc=cblank)
                locals()[getattr(C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(C,cbp+'_LIST')[i-1],choices=getattr(C,cbp+'_OPTS')[i-1],widget=widgets.RadioSelect,blank=True)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="hradio" or getattr(C,cbp+'_TYPES')[i-1][0]=="radiotable":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1],choices=[[h+1,x] for h,x in enumerate(getattr(C,cbp+'_OPTS')[i-1])],widget=widgets.RadioSelectHorizontal, blanc=cblank)
                locals()[getattr(C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(C,cbp+'_LIST')[i-1],choices=getattr(C,cbp+'_OPTS')[i-1],widget=widgets.RadioSelectHorizontal,blank=True)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="radioline":
                suph=1 if len(getattr(C,cbp+'_TYPES')[i-1]) == 1 else int(getattr(C,cbp+'_TYPES')[i-1][1].split('-')[0])
                ctypesvals=[]
                for h in range(0,len(getattr(C,cbp+'_OPTS')[i-1])): ctypesvals.append([str(h+suph)+"#line#"+getattr(C,cbp+'_OPTS')[i-1][h],suph])
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1],choices=[[h+x[1],x[0]] for h,x in enumerate(ctypesvals)],widget=widgets.RadioSelectHorizontal, blanc=cblank)
                locals()[getattr(C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(C,cbp+'_LIST')[i-1],choices=getattr(C,cbp+'_OPTS')[i-1],widget=widgets.RadioSelectHorizontal,blank=True)
                del suph,ctypesvals,h
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="checkbox":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.BooleanField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1], widget=widgets.CheckboxInput, blank=True, initial=False)
                locals()[getattr(C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(C,cbp+'_LIST')[i-1],choices=getattr(C,cbp+'_OPTS')[i-1],blank=True)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="select":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1],choices=[[h+1,x] for h,x in enumerate(getattr(C,cbp+'_OPTS')[i-1])], blanc=cblank)
                locals()[getattr(C,cbp+'_VARS')[i-1]+"_strval"]=models.StringField(label=getattr(C,cbp+'_LIST')[i-1],choices=getattr(C,cbp+'_OPTS')[i-1],blank=True)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="slider" and len(getattr(C,cbp+'_TYPES')[i-1])>1 and  getattr(C,cbp+'_TYPES')[i-1][1]=="int":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.IntegerField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1], blanc=cblank)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="slider" and (len(getattr(C,cbp+'_TYPES')[i-1])<=1 or getattr(C,cbp+'_TYPES')[i-1][1]=="float"):
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.FloatField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1], blanc=cblank)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="ltext" or getattr(C,cbp+'_TYPES')[i-1][0]=="longstring":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.LongStringField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1], blank=cblank)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="stext" or getattr(C,cbp+'_TYPES')[i-1][0]=="string":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.StringField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1], blanc=cblank)
            elif getattr(C,cbp+'_TYPES')[i-1][0]=="info":
                locals()[getattr(C,cbp+'_VARS')[i-1]]=models.BooleanField(variable=getattr(C,cbp+'_VARS')[i-1], label=getattr(C,cbp+'_LIST')[i-1], blank=True)
            if not (not isinstance(getattr(C,cbp+'_BY'),list) and str(getattr(C,cbp+'_BY')) == '0'):
                locals()[getattr(C,cbp+'_VARS')[i-1]+"_time"]=models.FloatField(blank=True, initial=-11)
            if i == len(getattr(C,cbp+"_QNUMS")): 
                del i, cblank
        for i in list(range(1,len(by_list)+1)):
            if not hasattr(C,cbp+'_NO_SCREEN_TIME') or not getattr(C,cbp+'_NO_SCREEN_TIME'):
                locals()[cbp+"_screen"+str(i)+"_time"]=models.FloatField(initial=-11,blank=True)
            if i == len(by_list): 
                del i
        if bpi == len(C.BLOCPAGES)-1:
            del bpi, cbp, by_list                  
    ### blocpage stuff above

# FUNCTIONS
def creating_session(subsession: Subsession):
    session = subsession.session
    period = subsession.round_number
    players=subsession.get_players()
    for player in players :
        ### blocpage stuff below
        for i,cbp in enumerate(C.BLOCPAGES):
            if hasattr(C,cbp+"_RANDOMORDERS"):
               for ovi,ov in enumerate(getattr(C,cbp+"_RANDOMORDERS")):
                make_random_orders(player,i,ov,ovi,period)
        if hasattr(C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(C,"BLOCPAGEDATA_IN_PARTICIPANT"):
            player.participant.blocpagedata=""
            player.participant.blocpageindex=""
        ### blocpage stuff above

### blocpage stuff below        
def make_random_orders(player: Player, cbpi: int, var_name_or_list, roi : int, period : int):
    import random
    cbp=C.BLOCPAGES[cbpi]
    init_list=getattr(C,var_name_or_list) if not isinstance(var_name_or_list, list) else var_name_or_list
    orders=list(range(1,len(init_list)+1))
    random.shuffle(orders)
    orders_list=str.join(',',[str(o) for o in orders])
    var_name=var_name_or_list.lower()+"_orders" if not isinstance(var_name_or_list, list) else  cbp+"_orders_"+str(roi+1)
    if(hasattr(C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")):
        if (isinstance(getattr(C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS"),bool) and getattr(C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")) or (isinstance(getattr(C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS"),list) and cbpi<len(getattr(C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")) and getattr(C,cbp+"_SAME_ORDERS_IN_ALL_ROUNDS")[cbpi]):
            if period>1:
                orders_list = getattr(player.in_round(1),var_name)
    setattr(player,var_name,orders_list)
def get_random_orders(player: Player, var_name_or_list, roi : int, cbp : str):
    var_name=var_name_or_list.lower()+"_orders" if not isinstance(var_name_or_list, list) else  cbp+"_orders_"+str(roi+1)
    orders=[int(o) for o in getattr(player,var_name).split(',')]
    init_list=getattr(C,var_name_or_list) if not isinstance(var_name_or_list, list) else var_name_or_list
    var_orders=[]
    for i,o in enumerate(orders): 
        var_orders.append(init_list[o-1])
        setattr(player,init_list[o-1]+"_order",0) #i+1
    return var_orders

def track_reloads(player: Player, page):
    if hasattr(C,"TRACK_BLOCPAGE_LOADS") and page in C.TRACK_BLOCPAGE_LOADS:
        setattr(player,page+"_nloads",getattr(player,page+"_nloads",0)+1)

def get_current_blocpage(player: Player):
    if hasattr(C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        return C.BLOCPAGES[player.participant.blocpageindex]
    else:
        return C.BLOCPAGES[player.blocpageindex]

def get_blocpage_data(player: Player):
    if hasattr(C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(C,"BLOCPAGEDATA_IN_PARTICIPANT"):
        return player.participant.blocpagedata.strip()
    else:
        return player.blocpagedata.strip()
def set_blocpage_data(player: Player,data):
    if hasattr(C,"BLOCPAGEDATA_IN_PARTICIPANT") and getattr(C,"BLOCPAGEDATA_IN_PARTICIPANT"):
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
            return {player.id_in_group: 'apply|'+player.blocpagedata}
        else: 
            set_blocpage_data(player,data[data.find('|')+1:])
            return {player.id_in_group: 'ok|'}
    if status=='update':
        blocpagedata=data[data.find('|')+1:]
        set_blocpage_data(player,blocpagedata)
        # for sb in blocpagedata.split('|'):
            # bundle=sb.split(';')
            # if(len(bundle)>1):
                # print(bundle[0],str(player.__table__.columns[bundle[0]].type))
                #setattr(player,bundle[0],bundle[1])
        # print('update',data)
### blocpage stuff above

# PAGES
class BlocPage(Page):
    form_model = 'player'
    # form_fields = getattr(C,cbp+'_VARS')+list(map(lambda x : x+'_time', getattr(C,cbp+'_VARS')))+list(map(lambda x : x+'_order', C.B_ASSO_LIST))+["blocD_screen"+str(i+1)+"_time" for i,v in enumerate(getattr(C,cbp+'_BY'))]
    live_method = blocpage_live_method
    @staticmethod
    def get_form_fields(player):
        cbp=get_current_blocpage(player)
        res = []
        for i in getattr(C,cbp+"_QNUMS"):
            res.append(getattr(C,cbp+"_VARS")[i-1])
            if getattr(C,cbp+"_TYPES")[i-1][0] != "info": res.append(getattr(C,cbp+"_VARS")[i-1]+'_time')
        if not hasattr(C,cbp+'_NO_SCREEN_TIME') or not getattr(C,cbp+'_NO_SCREEN_TIME'):
            by_list=[getattr(C,cbp+'_BY')]*math.ceil(len(getattr(C,cbp+'_LIST'))/int(getattr(C,cbp+'_BY'))) if not isinstance(getattr(C,cbp+'_BY'),list) else getattr(C,cbp+'_BY')
            for h in range(1,len(by_list)+1):
                res.append(cbp+"_screen"+str(h)+"_time")
        if hasattr(C,cbp+"_RANDOMORDERS"):
           for rpi,ov in enumerate(getattr(C,cbp+"_RANDOMORDERS")):
            vars_for_orders = getattr(C,cbp+"_RANDOMORDERS")[rpi] if isinstance(getattr(C,cbp+"_RANDOMORDERS")[rpi], list) else getattr(C,getattr(C,cbp+"_RANDOMORDERS")[rpi])
            for x in vars_for_orders: res.append(x+'_order')
        if hasattr(C,"TRACK_BLOCPAGE_LOADS") and cbp in C.TRACK_BLOCPAGE_LOADS: res.append(cbp+"_loadtime")
        return res
    @staticmethod
    def before_next_page(player, timeout_happened):
        cbp=get_current_blocpage(player)
        set_blocpage_data(player,"")
        for i in getattr(C,cbp+"_QNUMS"):
            if getattr(C,cbp+'_TYPES')[i-1][0]=="radio" or getattr(C,cbp+'_TYPES')[i-1][0]=="hradio" or getattr(C,cbp+'_TYPES')[i-1][0]=="select" or getattr(C,cbp+'_TYPES')[i-1][0]=="radioline" or getattr(C,cbp+'_TYPES')[i-1][0]=="radiotable":
                cstringval=getattr(C,cbp+'_OPTS')[i-1][getattr(player,getattr(C,cbp+'_VARS')[i-1])-1]
                setattr(player,getattr(C,cbp+'_VARS')[i-1]+"_strval",cstringval if cstringval != "" else "("+str(getattr(player,getattr(C,cbp+'_VARS')[i-1]))+")")
            if getattr(C,cbp+'_TYPES')[i-1][0]=="checkbox":
                # print(getattr(C,cbp+'_VARS')[i-1],":",getattr(player,getattr(C,cbp+'_VARS')[i-1]))
                cstringval=getattr(C,cbp+'_OPTS')[i-1][1-int(getattr(player,getattr(C,cbp+'_VARS')[i-1]))] if len(getattr(C,cbp+'_OPTS')[i-1])>1 else ['Y','N'][1-int(getattr(player,getattr(C,cbp+'_VARS')[i-1]))]
                setattr(player,getattr(C,cbp+'_VARS')[i-1]+"_strval",cstringval if cstringval != "" else "("+str(getattr(player,getattr(C,cbp+'_VARS')[i-1]))+")")
        player.blocpageindex+=1
    @staticmethod
    def vars_for_template(player: Player):
        cbp=get_current_blocpage(player)
        slidervars=[]
        slideropts=[]
        radiolines=[]
        radiotable_headers=[]
        radiotable_bottoms=[]
        radiotable_rows=[]
        singleline=[]
        onlyinfo=[]
        title=""
        if(hasattr(C,cbp+"_TITLE")): title=getattr(C,cbp+"_TITLE")
        presentation_tepmplate=""
        if os.path.exists(C.NAME_IN_URL+"/include_"+cbp+".html"): presentation_tepmplate=C.NAME_IN_URL+"/include_"+cbp+".html"
        # print("vars_for_template")
        for i in getattr(C,cbp+"_QNUMS"):
            if getattr(C,cbp+'_TYPES')[i-1][0]=="slider":
                slidervars.append(getattr(C,cbp+'_VARS')[i-1])
                slideropts.append(str.join(':',getattr(C,cbp+'_OPTS')[i-1]))
            if getattr(C,cbp+'_TYPES')[i-1][0]=="radioline":
                radiolines.append(getattr(C,cbp+'_VARS')[i-1])
            if getattr(C,cbp+'_TYPES')[i-1][0]=="info":
                onlyinfo.append(getattr(C,cbp+'_VARS')[i-1])
            for h in range(1,len(getattr(C,cbp+'_TYPES')[i-1])):
                if getattr(C,cbp+'_TYPES')[i-1][h]=="inline":
                    singleline.append(getattr(C,cbp+'_VARS')[i-1])
            if getattr(C,cbp+'_TYPES')[i-1][0]=="radiotable":
                if len(getattr(C,cbp+'_TYPES')[i-1]) <= 1 or getattr(C,cbp+'_TYPES')[i-1][1] == "row":
                    radiotable_rows.append(getattr(C,cbp+'_VARS')[i-1])
                elif len(getattr(C,cbp+'_TYPES')[i-1]) > 1 and getattr(C,cbp+'_TYPES')[i-1][1] == "first":
                    radiotable_headers.append(getattr(C,cbp+'_VARS')[i-1])
                    radiotable_rows.append(getattr(C,cbp+'_VARS')[i-1])
                elif len(getattr(C,cbp+'_TYPES')[i-1]) > 1 and getattr(C,cbp+'_TYPES')[i-1][1] == "last":
                    radiotable_bottoms.append(getattr(C,cbp+'_VARS')[i-1])
                    radiotable_rows.append(getattr(C,cbp+'_VARS')[i-1])
        return  dict(
            slidervars=slidervars,
            radiolines=radiolines,
            onlyinfo=onlyinfo,
            radioline_width="120px",
            singleline=singleline,
            radiotable_headers=radiotable_headers,
            radiotable_rows=radiotable_rows,
            radiotable_bottoms=radiotable_bottoms,
            cslidervars=str.join(';',slidervars),
            cslideropts=str.join(';',slideropts),
            allvars=str.join(';',getattr(C,cbp+'_VARS')),
            by=str.join(',',[str(getattr(C,cbp+'_BY'))]*math.ceil(len(getattr(C,cbp+'_LIST'))/int(getattr(C,cbp+'_BY'))) if not isinstance(getattr(C,cbp+'_BY'),list) else getattr(C,cbp+'_BY')),
            title=title,
            presentation_tepmplate=presentation_tepmplate,
        )     
    @staticmethod
    def js_vars(player):
        cbp=get_current_blocpage(player)
        firstrandoms=[]
        randomorders=[]
        shownumbers=[]
        if hasattr(C,cbp+"_RANDOMORDERS"):
           for ovi,ov in enumerate(getattr(C,cbp+"_RANDOMORDERS")):
            firstrandoms.append(ov[0] if isinstance(ov,list) else getattr(C,ov)[0])
            randomorders.append(get_random_orders(player,ov,ovi,cbp))
            if hasattr(C,cbp+"_RANDOMORDERS_SHOWNUMBERS"):
                if isinstance(getattr(C,cbp+"_RANDOMORDERS_SHOWNUMBERS"),bool): shownumbers.append(getattr(C,cbp+"_RANDOMORDERS_SHOWNUMBERS"))
                elif isinstance(getattr(C,cbp+"_RANDOMORDERS_SHOWNUMBERS"),list) and ovi<len(getattr(C,cbp+"_RANDOMORDERS_SHOWNUMBERS")):
                     shownumbers.append(getattr(C,cbp+"_RANDOMORDERS_SHOWNUMBERS")[ovi])                
        res = dict(
            hide_initial=False,
            bys_intro=getattr(C,cbp+"_BY_INTRO"),
            randomorders=randomorders,
            firstrandoms=firstrandoms,
            shownumbers=shownumbers,
            screentime_prefix=cbp+"_",
        )
        if hasattr(C,"TRACK_BLOCPAGE_LOADS") and cbp in C.TRACK_BLOCPAGE_LOADS: res['loadtimevar']=cbp+"_loadtime"
        return res

page_sequence = [BlocPage,BlocPage]
