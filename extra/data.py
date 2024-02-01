import requests
from bs4 import BeautifulSoup
import random



#----------------------------------------------------------------------------------------------------------------------------------------
def newword():
    words=["able ","about ","above ","absolute ","accent ","as ","ashamed ","aside ","ask ","asleep ","assist ","associate ","assume ","assure ","at ","background ","bacon ","bad ","bag ","bake ","balance ","ball ","banana ","band ","bang ","bank ","bar ","bare ","beyond ","big ","bike ","bill ","billion ","bin ","bind ","bird ","birth ","biscuit ","bit ","blow ","blue ","board ","boat ","body ","boil ","bomb ","bond ","bone ","book ","branch ","brand ","brave ","bread ","break ","breakfast ","breast ","breath ","breathe ","breed ","brick ","bush ","business ","busy ","but ","butter ","button ","buy ","by ","cable ","cage ","cake ","calculate ","call ","calm ","camera ","chain ","chew ","chicken ","chief ","child ","chip ","chocolate ","choice ","choose ","chop ","christmas ","church ","cigarette ","coast ","community ","company ","compare ","competition ","complain ","complete ","curl ","current ","customer ","cut ","dad ","damage ","dance ","danger ","desk ","directed ","direction ","dirty ","disappear ","disappoint ","discipline ","discover ","discuss ","disease ","disgust ","dish ","distance ","district ","disturb ","dive ","divide ","divorce ","do ","doctor ","dog ","doll ","dollar ","door ","double ","doubt ","dump ","during ","dust ","duty ","each ","ear ","early ","earn ","earth ","ease ","east ","easy ","eleven ","else ","email ","embarrass ","emotion ","empire ","employ ","empty ","encourage ","end ","enemy ","energy ","engage ","engine ","engineer ","enjoy ","enormous ","enough ","enter ","entertain ","entire ","envelope ","environment ","equal ","equipment ","escape ","especially ","establish ","estate ","flame ","flash ","flat ","flight ","flip ","float ","flood ","floor ","flow ","flower ","fly ","fold ","folk ","follow ","food ","fool ","foot ","football ","for ","force ","foreign ","forest ","forget ","forgive ","form ","forth ","fortnight ","fortunate ","fortune ","forward ","four ","fox ","frame ","frankly ","free ","freeze ","fresh ","friday ","friend ","fright ","frog ","from ","front ","frost ","fruit ","frustrate ","fry ","full ","fun ","fund ","fur ","furniture ","further ","future ","gain ","game ","garage ","give ","glad ","glance ","glass ","glory ","go ","group ","grow ","guarantee ","guard ","guess ","guest ","guide ","guilty ","gun ","guy ","heap ","hear ","heart ","heat ","heaven ","heavy ","hedge ","height ","hell ","hello ","help ","here ","hero ","hesitate ","hide ","high ","hill ","hire ","history ","hit ","hobby ","hold ","hole ","holiday ","home ","honest ","honey ","honour ","hook ","hope ","ice ","idea ","identify ","idiot ","if ","ignore ","ill ","illustrate ","image ","imagine ","immediate ","important ","impress ","improve ","in ","inch ","include ","income ","increase ","incredible ","indeed ","indicate ","individual ","industry ","influence ","inform ","injure ","innocent ","inside ","insist ","library ","licence ","lid ","lie ","life ","lift ","light ","mrs ","much ","mud ","mum ","murder ","muscle ","music ","must ","mystery ","nail ","name ","nanny ","nest ","never ","new ","news ","newspaper ","next ","nice ","night ","nine ","no ","nobody ","noise ","non ","none ","nor ","normal ","north ","northern ","nose ","not ","note ","nothing ","notice ","november ","now ","nowhere ","number ","nurse ","nut ","oak ","object ","panic ","paper ","pardon ","parent ","park ","part ","particular ","partner ","party ","pass ","past ","pat ","patch ","path ","patient ","pattern ","pause ","pay ","peace ","pen ","penny ","pension ","pleasant ","please ","pleasure ","plenty ","plug ","plus ","pocket ","poem ","poet ","point ","poison ","pole ","police ","pride ","prime ","prince ","print ","prison ","privacy ","private ","pump ","punch ","punish ","pup ","purchase ","pure ","purple ","purpose ","push ","put ","qualify ","quality ","quarter ","queen ","question ","quick ","quiet ","quit ","quite ","quote ","rabbit ","race ","radio ","rain ","raise ","range ","rapid ","ring ","rip ","rise ","risk ","river ","road ","roar ","rob ","rock ","role ","sad ","safe ","shoot ","shop ","shore ","short ","should ","shoulder ","shout ","shove ","show ","shower ","shut ","shy ","sick ","side ","sight ","sign ","signal ","silence ","silly ","silver ","similar ","simple ","since ","smile ","smoke ","smooth ","snake ","snap ","snow ","so ","social ","society ","species ","specific ","speech ","speed ","spell ","spend ","tone ","tongue ","tonight ","too ","travel ","tray ","treat ","tree ","trial ","type ","typical ","wind ","window ","wine ","wing ","winter ","wipe ","wire ","wise ","wish ","with ","within ","without ","witness ","wolf ","woman ","zero"]
    sword = random.choice(words)
    datais={}
    datais["word"]=sword
    searchword=sword
    url = f"https://www.merriam-webster.com/dictionary/{searchword}"
    response = requests.get(url)
    meaning=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        meanings = soup.find_all("span", class_="dtText")
        a=0
        for i in meanings:
            if a==3:
                break
            else:
                meaning.append(i.text.strip())
                a+=1
    datais["meanings"]=meaning

    u=f"https://sentencedict.com/{sword}.html"
    res = requests.get(u)
    if res.status_code == 200:
        sou = BeautifulSoup(res.text, 'html.parser')
    
    example=sou.find(id="all").find_all('div')
    k=0
    ex=[]
    for i in example:
        k+=1
        if k<=7:
            e=i.text
            ex.append(e)
    datais["examples"]=ex
    return datais

