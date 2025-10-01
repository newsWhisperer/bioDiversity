import secrets
#pip3 install newsapi-python
import pandas as pd

from pathlib import Path
import os.path

import requests
from urllib.parse import urlparse
import json
import time
import smtplib
import random

import datetime
from dateutil import parser

import re
from bs4 import BeautifulSoup

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import deep_translator
from deep_translator import GoogleTranslator
from deep_translator import MyMemoryTranslator
from deep_translator import LingueeTranslator


DATA_PATH = Path.cwd()


df = pd.read_csv(DATA_PATH / "en" / "news_2021_09.csv", delimiter=',',index_col='index')
df = pd.read_csv(DATA_PATH / "en" / "news_2021_10.csv", delimiter=',',index_col='index')

newsapiLanguages =  ["ar","de","en","es","fr","he","it","nl","no","pt","ru","sw","ur","zh"]
#newsapiLanguages = ["ar","de","en","es","fr","he","it","nl","no","pt","ru","se","ud","zh"]   ##ud vs ur, se vs sv
#DONE ------------->  **   **   **   **   **   __   **   **   __   **   **   __   __   **   

#sv vs sw???  svedish vs suaheli 
# sw no support ...
#jp,ja,...
#ud

#api2
newsapiLanguages =  ["ar","de","en","es","fr","he","it","nl","no","pt","ru","sw","zh",   "el","ja"]
#,"ud"

searchWords = {


 "'άγονη'":"el", "'Ακρίδες'":"el", "'Χαίρε'":"el", "'Ηφαιστειακή έκρηξη'":"el", "'καταρρακτώδεις βροχές'":"el", "'Μαύρο πάγο'":"el", "'Μουσώνας'":"el", 
 "'Αμμοθύελλα'":"el", "'Αναταραχή χιονιού'":"el", "'Ανεμοθύελλα'":"el", "'Ανεμοστρόβιλος'":"el", "'άνθιση φυκιών'":"el", "'άνθιση φυκών'":"el", 
 "'Αργός παγετός'":"el", "'Αρχή του χειμώνα'":"el", "'Βόρεια φώτα'":"el", "'Βόρειο Σέλας'":"el", "'Βόρειο Φως'":"el", "'Βροχή με παγωμένο νερό'":"el", 
 "'Βροχή με παγωνιά'":"el", "'Βροχή που παγώνει'":"el", "'Δασική πυρκαγιά'":"el", "'δασική πυρκαγιά'":"el", "'Διαρκής βροχή'":"el", "'Εκρήξεις ηφαιστείων'":"el", 
 "'Έκρηξη ηφαιστείου'":"el", "'Έναρξη της χειμερινής περιόδου'":"el", "'Έναρξη του χειμώνα'":"el", "'Έναρξη χειμώνα'":"el", "'Έντονη βροχή'":"el", 
 "'Επιπλέων πάγος'":"el", "'Η ηλιακή καταιγίδα'":"el", "'Ηλιακές καταιγίδες'":"el", "'Ηλιακή θύελλα'":"el", "'Ηλιακή καταιγίδα'":"el", 
 "'Ηφαίστειο'":"el", "'Θέρμανση'":"el", "'Θερμοκύμα'":"el", "'Θερμότητα'":"el", "'Θερμότητας'":"el", "'Θύελλα'":"el", "'Θύελλα ανέμου'":"el", 
 "'Θύελλα χιονιού'":"el", "'Ισχυρή βροχή'":"el", "'Ισχυρή βροχόπτωση'":"el", "'Καθίζηση'":"el", "'Καθυστερημένος παγετός'":"el", "'Καλοκαίρι αιώνα'":"el", 
 "'Καλοκαίρι του αιώνα'":"el", "'Καταιγίδα'":"el", "'κατακλυσμιαία βροχή'":"el", "'Κατακλυσμός'":"el", "'Καταπτώσεις βράχων'":"el", "'Ακρίτες'":"el", 
 "'καταρρακτώδη βροχή'":"el", "'καταρρακτώδης βροχή'":"el", "'Καταρρεύσεις βράχων'":"el", "'Κατολισθήσεις'":"el", "'Κατολίσθηση'":"el", "'Καύσωνας'":"el", 
 "'Κεραυνός'":"el", "'Κρύο κύμα'":"el", "'Κρύο κύμα ψύχους'":"el", "'Κρύο ψύχος'":"el", "'Κρυοπαγήματα'":"el", "'Κυκλώνα'":"el", "'Κυκλώνας'":"el", 
 "'Κύμα καταιγίδας'":"el", "'Κύμα καταιγίδων'":"el", "'Κύμα καύσωνα'":"el", "'Κύματα καύσωνα'":"el", "'Λαχάρ'":"el", "'Λιώσιμο χιονιού'":"el",  
 "'Μαύρος πάγος'":"el", "'Μέλανος πάγος'":"el", "'Μονσούν'":"el", "'Μονσούντα'":"el", "'Νυχτερινή παγωνιά'":"el", "'Νυχτερινός παγετός'":"el", 
 "'Νυχτερινός πάγος'":"el", "'Ξηρασία'":"el", "'ξηρασία'":"el", "'Ξηρότητα'":"el", "'ξηρότητα'":"el", "'ξηρότητας'":"el", "'Ο μαύρος πάγος'":"el", 
 "'Όψιμος παγετός'":"el", "'Παγετός'":"el", "'Παγετός της νύχτας'":"el", "'Παγόβουνα'":"el", "'Πάγοι'":"el", "'Παγοκύστες'":"el", "'Παγοπέδιλα'":"el", 
 "'Πάγος'":"el", "'Παγωμένη βροχή'":"el", "'Παγωμένος'":"el", "'Παλίρροια καταιγίδας'":"el", "'Πανούκλα ακρίδες'":"el", "'Πανούκλα από ακρίδες'":"el", 
 "'παράκτια πλημμύρα'":"el", "'παράκτιες κατακλύσεις'":"el", "'παράκτιες πλημμύρες'":"el", "'Παροχή ιλύος'":"el", "'Περμαφρόδιο'":"el", "'Περμαφρόδιτος'":"el", 
 "'Πληγή ακριδών'":"el", "'Πληγή ακρίδων'":"el", "'Πλήγμα κεραυνού'":"el", "'Πλημμύρα'":"el", "'πλημμύρα ποταμού'":"el", "'πλημμύρα ποταμών'":"el", 
 "'πλημμύρες'":"el", "'πλημμύρες από ποτάμια'":"el", "'πλημμύρες από ποταμούς'":"el", "'πλημμύρες ποταμού'":"el", "'πλημμύρες ποταμών'":"el", 
 "'Πλημμύρισμα'":"el", "'πλουβιακές πλημμύρες'":"el", "'Πτώση βράχου'":"el", "'Πτώση βράχων'":"el", "'πυρκαγιά'":"el", "'Πυρκαγιά δάσους'":"el", 
 "'Πυρκαγιά σε δάσος'":"el", "'πυρκαγιά σε θάμνους'":"el", "'Πυρκαγιά στο δάσος'":"el", "'πυρκαγιάς'":"el", "'πυρκαγιές'":"el", "'Ρεύματα θραυσμάτων'":"el", 
 "'Ροές απορριμμάτων'":"el", "'Ροές θραυσμάτων'":"el", "'Ροές συντριμμιών'":"el", "'Ροή απορριμμάτων'":"el", "'Ροή θραυσμάτων'":"el", "'Ροή ιλύος'":"el", 
 "'Ροή λάσπης'":"el", "'Ροή συντριμμάτων'":"el", "'Ροή συντριμμιών'":"el", "'Ροή της ιλύος'":"el", "'Σάντστορμ'":"el", "'Σεισμοί'":"el", "'Σεισμός'":"el", 
 "'Σνόου'":"el", "'Στεγνότητα'":"el", "'Συνεχή βροχή'":"el", "'Συνεχής βροχή'":"el", "'Συνεχόμενη βροχή'":"el", "'Σφοδρή βροχή'":"el", "'Ταϊφούνι'":"el", 
 "'Τήξη χιονιού'":"el", "'Το χάος του χιονιού'":"el", "'Τσουνάμι'":"el", "'Τυφώνα'":"el", "'Τυφώνες'":"el", "'Ύστερος παγετός'":"el", "'Χάιλ'":"el", 
 "'Χαίρετε'":"el", "'Χαμηλή στάθμη νερού'":"el", "'Χαμηλή στάθμη του νερού'":"el", "'Χαμηλή στάθμη ύδατος'":"el", "'Χαμηλό νερό'":"el", "'Χάος με χιόνι'":"el", 
 "'Χάος στο χιόνι'":"el", "'Χιόνι'":"el", "'Χιόνι ομίχλη'":"el", "'Χιόνι που λιώνει'":"el", "'Χιόνι χάος'":"el", "'χιονοθύελλα'":"el", "'Χιονόπτωση'":"el", 
 "'Χιονοστιβάδα'":"el", "'Χιονοστρωμνή'":"el", "'Χιονοστρώσεις'":"el", "'Χτύπημα από κεραυνό'":"el", "'Χτύπημα αστραπής'":"el", "'Χτύπημα κεραυνού'":"el", 


 "'tsunami'":"fr", "'inondation'":"fr", "'sécheresse'":"fr", "'permafrost'":"fr", "'tempête'":"fr", 
 "'incendie de forêt'":"fr", "'tremblement de terre'":"fr", "'hurricane'":"fr", "'typhon'":"fr", "'cyclone'":"fr", "'gelée'":"fr", "'neige'":"fr", 
 "l'orage":"fr", "'basses eaux'":"fr", "l'avalanche":"fr", "'glaçon'":"fr", "'volcan'":"fr", "'gelée à pierre fendre'":"fr", "'niche de départ'":"fr", 
 "niche d'arrachement":"fr", "'coulée de boue'":"fr", "'grêle'":"fr", "'pluie battante'":"fr", "'chaleur'":"fr", "'tornade'":"fr", "'tourbillon'":"fr", 
 "'plaque de glace flottante'":"fr", "'feu de brousse'":"fr", "'lahar'":"fr", "'neiges'":"fr", "'canicule'":"fr", "l'ouragan":"fr", "'bloc de glace'":"fr", 
 "'éruption volcanique'":"fr", "'flétrissement estival'":"fr", "'secousse tellurique'":"fr", "l'iceberg":"fr", "'épisode caniculaire'":"fr", 
 "'chute de pierres'":"fr", "'raz de marée'":"fr", "l'ouragan":"fr", "'pluie persistante'":"fr", "'tourmente de neige'":"fr", "'verglas'":"fr", 
 "'grésil'":"fr", "'mousson'":"fr", "'tourmente'":"fr", "'neige fondante'":"fr", "'congère'":"fr", "'bourrasque de neige'":"fr", "'gelée nocturne'":"fr", 
 "offensive de l'hiver":"fr", "'vague de froid'":"fr", "'séisme'":"fr", "'feu de forêt'":"fr", "'gel'":"fr", "'givre'":"fr", "'gelée à pierre fendre'":"fr", 
 "'sauterelle'":"fr", "'premières gelées'":"fr", "l'étiage":"fr", "'glissement de terrain'":"fr", "'locuste'":"fr", "'raz de marée'":"fr", 
 "'pergélisol'":"fr", "'pluie violente'":"fr", "'chaleur torride'":"fr", "l'ardeur":"fr", "'chaleur accablante'":"fr", "'chaleur caniculaire'":"fr", 
 "'touffeur'":"fr", "trombe d'eau":"fr", "'vague de chaleur'":"fr", "'pluie verglaçante'":"fr", "'tempête de sable'":"fr", "'effervescence algale'":"fr",

 "Tsunami":"de","Hochwasser":"de","Dürre":"de","Waldbrand":"de","Erdbeben":"de","Hurrikane":"de","Taifun":"de", "'Überschwemmung'":"de", "'Bergsturz'":"de",
 "Zyklon":"de","Spätfrost":"de","Schnee":"de","Unwetter":"de","Niedrigwasser":"de","Lawine":"de","Eisberg":"de","Vulkanausbruch":"de", "'Flut'":"de",
 "Frost":"de","Sturm":"de","Erdrutsch":"de","Mure":"de","Hagel":"de","Starkregen":"de","Hitze":"de","Tornado":"de","Windhose":"de","Eisschollen":"de",
 "Schlammstrom ":"de","Murenabgang":"de","Lahar":"de","Wirbelsturm":"de","Vulkanausbruch":"de","Hitzewelle":"de","Steinschlag":"de","Sturmflut":"de","Orkan":"de",
 "Trogorkan":"de","Dauerregen":"de","Schneechaos":"de","Glatteis":"de","Eisregen":"de","Monsun":"de","Schneematsch":"de","Schneeverwehung":"de",
 "Schneegestöber":"de","Nachtfrost":"de","Jahrhundertsommer":"de","Kältewelle":"de","Wintereinbruch":"de","Heuschreckenplage":"de","Permafrost":"de",
 "Sandsturm":"de","Algenblüte":"de","Trockenheit":"de","Blitzeinschlag":"de","Schneeschmelze":"de","Gewitter":"de","Nordlicht":"de","Sonnensturm":"de",
 "Algenteppich":"de", "Hungersteine":"de",
 

 "tsunami":"en", "flooding":"en", "drought":"en", "'lightning strike'":"en", "lahar":"en", "iceberg":"en", "'snow squall'":"en",
 "wildfire":"en", "earthquake":"en", "hurricane":"en", "typhoon":"en", "cyclone":"en", "freezing":"en", "snow":"en", "thunderstorm":"en", 
 "'low tide'":"en", "avalanche":"en", "growler":"en", "volcano":"en", "frost":"en", "windstorm":"en", "landslide":"en", "mudflow":"en", "hail":"en",
 "'torrential rain'":"en", "heat":"en", "tornado":"en", "'ice floe'":"en", "bushfire":"en", "freezing":"en", "frost":"en", "storm":"en", "'severe weather'":"en",
 "'volcano eruption'":"en", "'heavy rain'":"en", "'heat dome'":"en", "'dust devil'":"en", "whirlwind":"en", "'heat wave'":"en", "'winter gale'":"en",
 "blizzard":"en", "sludge":"en", "'snow slush'":"en", "'blowing snow'":"en", "'snow flurry'":"en", "'night frost'":"en", "megadrought":"en", "'cold snap'":"en",
 "'cold spell'":"en", "'pluvial flooding'":"en", "locusts":"en", "grasshopper":"en", "haboob":"en", "permafrost":"en", "sandstorm":"en", "'algae blooms'":"en",
 "'algal bloom'":"en", "aridity":"en", "dryness":"en", "'coastal flooding'":"en", "'river flooding'":"en", "'pluvial flooding'":"en", "lightning":"en",
 "'debris flow'":"en", "'bomb cyclone'":"en", "'atmospheric river'":"en", "'mudslide'":"en", "'glacier lake outbreak'":"en", "'soil moisture'":"en", 
 "'evapotranspiration'":"en", "'river runoff'":"en", "'extreme heat exposure'":"en", "'crop yields'":"en", "'crop failure'":"en", "'snowstorm'":"en",
 "'temperature plummet'":"en", "'jellyfish storm'":"en", "'water restrictions'":"en", "'flash drought'":"en", "'dust bowls'":"en", "'dust blizzard'":"en",
 "'dust storm'":"en", 

 "'熱波'":"ja", "'干ばつ'":"ja", "'山火事'":"ja", "'エン'":"ja", "'津波'":"ja", "'洪水'":"ja", 
"'地震'":"ja", "'ハリケーン'":"ja", "'台風'":"ja", "'サイクロン'":"ja", "'凍結'":"ja", "'雪'":"ja", "'雷雨'":"ja", "'干潮'":"ja", "'雪崩'":"ja", "'グローラー'":"ja", 
"'火山'":"ja", "'霜'":"ja", "'暴風'":"ja", "'土砂崩れ'":"ja", "'土石流'":"ja", "'雹（ひょう'":"ja", "'豪雨'":"ja", "'熱'":"ja", "'竜巻'":"ja", "'流氷'":"ja", 
"'ラハール'":"ja", "'凍てつく霜'":"ja", "'嵐'":"ja", "'悪天候'":"ja", "'氷山'":"ja", "'火山噴火'":"ja", "'大雨'":"ja", "'ヒートドーム'":"ja", 
"'ダストデビル'":"ja", "'つむじ風'":"ja", "'冬の強風'":"ja", "'ブリザード'":"ja", "'スラッジ'":"ja", "'スノースラッシュ'":"ja", "'吹雪'":"ja", 
"'雪が舞う'":"ja", "'夜霜'":"ja", "'大干ばつ'":"ja", "'コールドスナップ'":"ja", "'寒波'":"ja", "'沖積氾濫'":"ja", "'イナゴ'":"ja", "'バッタ'":"ja", "'ハボタン'":"ja", 
"'永久凍土'":"ja", "'砂嵐'":"ja", "'アオコの花'":"ja", "'アオコ'":"ja", "'乾燥'":"ja", "'海岸洪水'":"ja", "'河川氾濫'":"ja", "'沖積氾濫'":"ja", "'雷'":"ja", 

"'हीटवेव'":"hi", "'सूखा'":"hi", "'जंगल की आग'":"hi", "'कम ज्वार'":"hi", "'सुनामी'":"hi", "'बाढ़'":"hi", "'भूकंप'":"hi", 
"'जमना'":"hi", "'बर्फ'":"hi", "'आंधी तूफान'":"hi", "'हिमस्खलन'":"hi", "'ग्राउलर'":"hi", "'ज्वालामुखी'":"hi", "'ठंढ'":"hi", "'आन्धी'":"hi", "'चक्रवात'":"hi", 
"'भूस्खलन'":"hi", "'मडफ्लो'":"hi", "'ओला'":"hi", "'मूसलधार बारिश'":"hi", "'गर्मी'":"hi", "'बवंडर'":"hi", "'हिम खंड'":"hi", "'झाड़ी में आग लगी'":"hi", "'लहरी'":"hi", 
"'जमने वाला पाला'":"hi", "'आंधी'":"hi", "'बहुत बुरा मौसम'":"hi", "'हिमशैल'":"hi", "'ज्वालामुखी उद्भेदन'":"hi", "'भारी वर्षा'":"hi", "'गर्मी गुंबद'":"hi", "'धूल का शैतान'":"hi", 
"'गर्मी की लहर'":"hi", "'सर्दी की आंधी'":"hi", "'बर्फानी तूफान'":"hi", "'कीचड़'":"hi", "'बर्फ का कीचड़'":"hi", "'उड़ाने बर्फ'":"hi", "'बर्फ घबराहट'":"hi", "'आंधी'":"hi", 
"'रात का ठंढ'":"hi", "'ठंडी तस्वीर'":"hi", "'कोल्ड स्पेल'":"hi", "'टिड्डियों'":"hi", "'टिड्डी'":"hi", "'हबूब'":"hi", "'बालू का तूफ़ान'":"hi", 
"'शैवाल खिलता है'":"hi", "'शैवाल का फलना'":"hi", "'शुष्कता'":"hi", "'समुद्र तटीय बाढ़'":"hi", "'नदी बाढ़'":"hi", "'बाढ़'":"hi", "'आकाशीय बिजली'":"hi", 

 "tsunami ":"es", "marea alta":"es", "sequía":"es", "'incendio forestal'":"es", "terremoto":"es", "huracán":"es", "tifón":"es", "ciclón":"es",
 "'ciclo de deshielo'":"es", "nieve":"es", "'tiempo severo'":"es", "'marea baja'":"es", "avalancha":"es", "iceberg":"es", "volcán":"es", "helada":"es",
 "tempestad":"es", "'corrimiento de tierras'":"es", "'desplazamiento de tierras'":"es", "granizo":"es", "'lluvia intensa'":"es", "quemazón":"es", "tornado":"es", 
 "'manga de viento'":"es", "témpano":"es", "cortafuego":"es", "lazar":"es", "temporal":"es", "meteotsunami":"es", "rissaga":"es", "'erupción volcánica'":"es",
 "'lluvias torrenciales'":"es", "aridez":"es", "ciclón":"es", "torbellino":"es", "ola de calor":"es", "pedrisco":"es", "turbión":"es", "corrimiento":"es",
 "deslizamiento":"es", "vendaval":"es", "delantera":"es", "borrasca":"es", "procela":"es", "'agua baja'":"es", "tempestad":"es", "aguanieve":"es",
 "nevisca":"es", "'ventisca de nieve'":"es", "'helada nocturna'":"es", "seísmo":"es", "'temblor de tierra'":"es", "sismo":"es", "remezón":"es",
 "contrafuegos":"es", "crecida":"es", "inundación":"es", "'tormenta de arena'":"es", "'floración de algas'":"es", "'proliferación de algas'":"es",

"'tsunami '":"pt", "'cheia'":"pt", "'seca'":"pt", "aixa'":"pt", "'avalanche'":"pt", "'icebergue'":"pt", "'vulcão'":"pt", "'Geada tardia'":"pt", "'tormenta'":"pt", 
"'aluimento de terrenos'":"pt", "'escorregamento de terras'":"pt", "'chuva de pedra'":"pt", "'chuva forte'":"pt", "'calor'":"pt", "'tornado'":"pt", 
"'vendaval'":"pt", "'bloco de gelo flutuante'":"pt", "'fluxo de lama'":"pt", "'lahar'":"pt", "'iceberg'":"pt", "'ciclone violento'":"pt", "'temporal'":"pt", 
"'intempérie'":"pt", "'erupção vulcânica'":"pt", "'vaga de calor'":"pt", "'onda de calor'":"pt", "'maré ciclónica'":"pt", "'erupção freática'":"pt", 
"'maré ciclônica'":"pt", "'queda de ped'incêndio florestal'":"pt", "'sismo'":"pt", "'furacão'":"pt", "'tufão'":"pt", "'ciclone'":"pt", "'geada'":"pt", 
"'neve'":"pt", "'tempestade'":"pt", "'maré bras'":"pt", "'maré de tempestade'":"pt", "'furacão'":"pt", "'nevasca'":"pt", "'chuva contínua'":"pt", 
"'saraivada'":"pt", "'gelo preto'":"pt", "'saraiva'":"pt", "'monção'":"pt", "'calor insuportável'":"pt", "'calor abrasador'":"pt", "'calor escaldante'":"pt", 
"'calor sufocante'":"pt", "'calorão'":"pt", "'ardor'":"pt", "'onda de frio'":"pt", "'chegada repentina do inverno'":"pt", "'derreter'":"pt", "'desabamento'":"pt", 
"'deslizamento'":"pt", "'neve derretida e suja'":"pt", "'gafanhoto'":"pt", "'permafrost '":"pt", "'tempestade de areia'":"pt", "'florescimento de algas'":"pt", 
"'chuva torrencial'":"pt", "'inundação'":"pt", "'tremor de terra'":"pt", "'terremoto'":"pt", "'terramoto'":"pt", "'granizo'":"pt", "'aridez'":"pt", "'degelo'":"pt", 
"'descongelamento'":"pt", "'inundações costeiras'":"pt", "'inundação do rio'":"pt", "'inundação pluvial'":"pt", "'raio'":"pt", "'relâmpago'":"pt", "'corisco'":"pt", 


 "'tsunami  '":"it", "'acqua alta'":"it", "'secca'":"it", "'incendio di bosco'":"it", "'terremoto'":"it", "'iceberg'":"it", "'burrasca'":"it",
 "l'uragano":"it", "'tifone'":"it", "'ciclone'":"it", "'gelo'":"it", "'neve'":"it", "'intemperie'":"it", "'acqua bassa'":"it", "'lavina'":"it", 
 "'vulcano'":"it", "'gelidezza'":"it", "'tempesta'":"it", "'smottamento'":"it", "'colata detritica'":"it", "'gragnola'":"it", "'canicola'":"it",
 "'calura'":"it", "'tornado'":"it", "tromba d'aria":"it", "'lastra di ghiaccio'":"it", "'lahar'":"it", "'frana'":"it", "'bufera'":"it", 
 "'eruzione vulcanica'":"it", "'maltempo'":"it", "'magra'":"it", "'neve papposa'":"it", "'neve bagnata'":"it", "'caldo'":"it", "'valanga'":"it",
 "'slavina'":"it","l'arsura":"it", "'siccità'":"it", "l'aridità":"it", "'colmo'":"it", "'piena'":"it", "l'esondazione":"it", "l'inondazione":"it",
 "'arsura'":"it", "'neve fradicia'":"it", "'ondata di caldo'":"it", "'caldana'":"it", "'vampata'":"it", "'gragnuola'":"it", "'ondata di freddo'":"it",
 "'sisma'":"it", "'grandine'":"it", "'locusta'":"it", "'cavalletta'":"it", "'saltabecca'":"it", "'permafrost'":"it", "'tempesta di sabbia'":"it",
 "'eutrofizzazione'":"it", "'proliferazione di alghe'":"it", "'arsura'":"it", "'aridità'":"it", "'siccità'":"it", "'secchezza'":"it", "'secca'":"it",


"'tsunami   '":"nl", "'overstroming'":"nl", 
"'droogte'":"nl", "'bosbrand'":"nl", "'aardbeving'":"nl", "'orkanen'":"nl", "'tyfoon'":"nl", "'cycloon'":"nl", "'late vorst'":"nl", "'sneeuw'":"nl", 
"'storm'":"nl", "'laagwater'":"nl", "'lawine'":"nl", "'ijsberg'":"nl", "'vulkaan'":"nl", "'vorst'":"nl", "'onweer'":"nl", "'aardverschuiving'":"nl", 
"'brokstukken'":"nl", "'wees gegroet'":"nl", "'zware regen'":"nl", "'warmte'":"nl", "'tornado'":"nl", "'windbroek'":"nl", "'Ijsschotsen'":"nl", 
"'modderstroom'":"nl", "'lahar'":"nl", "'Vulkaanuitbarsting'":"nl", "'Koude golf'":"nl", "'Hittegolf'":"nl", "'hitte'":"nl", "'vallende stenen'":"nl", 
"'stormvloed'":"nl", "'orkaan'":"nl", "'aanhoudende regen'":"nl", "'sneeuw chaos'":"nl", "'zwart ijs'":"nl", "'ijs regen'":"nl", "'moesson'":"nl", 
"'slush'":"nl", "'nachtvorst'":"nl", "'begin van de winter'":"nl", "'sprinkhanen'":"nl", "'permafrost'":"nl", "'Zandstorm'":"nl", "'Algen bloeien'":"nl", 
"'algenbloei'":"nl", "'onweer'":"nl", "'blikseminslag'":"nl", "'Smeltende sneeuw'":"nl", "'onweersbui'":"nl", "'Noorderlicht'":"nl", "'zonnestorm'":"nl", 


 "'تسونامي'":"ar", "'فيضان'":"ar", "'جفاف'":"ar", "'حريق الغابة'":"ar",  "'اعصار'":"ar",  "'حطام'":"ar",
 "'هزة أرضية'":"ar", "'الأعاصير'":"ar", "'اعصار'":"ar", "'الصقيع'":"ar", "'الصقيع المتأخر'":"ar", "'الثلج'":"ar", "'عاصفه'":"ar", "'مد وجزر طفيف'":"ar", 
 "'انهيار ثلجي'":"ar", "'جبل جليد'":"ar", "'بركان'":"ar", "'الصقيع'":"ar", "'عاصفه'":"ar", "'انهيار أرضي'":"ar", "'وابل'":"ar", "'مطر غزير'":"ar", 
 "'الحرارة'":"ar", "'إعصار'":"ar", "'زوبعة'":"ar", "'الجليد الطافي'":"ar", "'تيار الطين'":"ar", "'تدفق الحطام'":"ar", "'لاهار'":"ar", "'الطقس القاسي'":"ar", 
 "'انفجار بركاني'":"ar", "'قبة الحرارة'":"ar", "'موجة حرارية'":"ar", "'سقوط الصخور'":"ar", "'العواصف'":"ar", "'مطر مستمر'":"ar", "'فوضى الثلج'":"ar", 
 "'عاصفة ثلجية'":"ar", "'المطر الجليد'":"ar", "'الرياح الموسمية'":"ar", "'طين'":"ar", "'عاصفة ثلجية'":"ar", "'ثلج'":"ar", "'الصقيع الليلي'":"ar", 
 "'موجة باردة'":"ar", "'موجة حر'":"ar", "'عاصفة ثلجية'":"ar", "'الجراد'":"ar", "'دائمة التجمد'":"ar", "'عاصفة رملية'":"ar", "'تتفتح الطحالب'":"ar", 
 "'الطحالب ازهر'":"ar", "'جفاف'":"ar", "'صاعقة'":"ar", "'ذوبان الثلوج'":"ar", "'عاصفة رعدية'":"ar", "'الاضواء الشمالية'":"ar", "'عاصفة شمسية'":"ar", 

 "'лесной пожар'":"ru", "'землетрясение'":"ru", "'смерч'":"ru", "'торнадо'":"ru", "'тайфун'":"ru", "'циклон'":"ru", "'мороз'":"ru", "'ненастье'":"ru", 
 "'ненастная погода'":"ru",  "'плохая погода'":"ru", "'плохие погодные условия'":"ru", "'прилив'":"ru", "'лайсберг'":"ru", "'снег'":"ru",
 "'градобой'":"ru",  "'нагрев'":"ru",  "'тепла'":"ru",  "'жара'":"ru", "'волны горячего воздуха'":"ru", "'волну горячего воздуха'":"ru", 
 "'буря'":"ru", "'гроза'":"ru", "'ураган'":"ru", "'землетрясений'":"ru", "'обвал'":"ru", "'оползни'":"ru", "'град'":"ru", "'здравствуйте'":"ru",
 "'отлив'":"ru", "'Лоуин'":"ru", "'айсберг'":"ru", "'вулкан'":"ru", "'обморожение'":"ru", "'шторм'":"ru", "'землетрясения'":"ru", "'оползень'":"ru", 
 "'грязевой поток'":"ru", "'поток шлама'":"ru", "'поток раствора'":"ru", "'селевый поток'":"ru", "'селевые потоки'":"ru", "'сельский поток'":"ru", 
 "'тепло'":"ru",  "'волна горячего воздуха'":"ru", "'льдина'":"ru", "'поток грязи'":"ru", "'селевой поток'":"ru", "'глазурь'":"ru", 
 "'айсинг'":"ru", "'глазировка'":"ru", "'Обрушение скал'":"ru", "'Камнепад'":"ru", "'непогода'":"ru", "'вулканическое извержение'":"ru",
 "'извержение вулканов'":"ru", "'малая вода'":"ru", "'низкий уровень воды'":"ru", "'низкое содержание воды'":"ru",
 "'щебень'":"ru",  "'сопка'":"ru", "'извержение вулкана'":"ru", "'низкая вода'":"ru", 

 #"'треску́чий моро́з'":"ru", "'ни́зкая вода́'":"ru", "'меже́нная вода́'":"ru", "'по́лая вода́'":"ru", "'меже́нь'":"ru", "'гололёд'":"ru", "'си́льный ве́тер'":"ru", 
 #"'сне́жный покро́в'":"ru", "'ночны́е за́морозки'":"ru", "'муссо́н'":"ru", "'полово́дье'":"ru", "'высо́кая вода́'":"ru", "'по́лная вода́'":"ru", 
 #"'снежо́к'":"ru", "'сне́жный зано́с'":"ru", "'сне́жный перемёт'":"ru", "'сту́жа'":"ru", "'сля́коть'":"ru", "'Дед Моро́з'":"ru", "'жесто́кий моро́з'":"ru", 
 #"'свире́пый моро́з'":"ru", "'треску́чий моро́з'":"ru", "'кре́пкий моро́з'":"ru", "'жесто́кий моро́з'":"ru", "'урага́н'":"ru", "'сдвиг'":"ru", "'о́сыпь'":"ru", 
 #"'ве́чная мерзлота́'":"ru", "'многоле́тняя мерзлота́'":"ru", "'цвете́ние воды́'":"ru", "'песча́ная бу́ря'":"ru", "'Хохвасер'":"ru", "'Лоуине'":"ru", "'засушливость'":"ru", 
 #"'сухость'":"ru", "'засушливости'":"ru", "'прибрежное наводнение'":"ru", "'затопление побережья'":"ru", "'наводнение в прибрежной зоне'":"ru", "'цуна́ми'":"ru", 
 #"'наводнение реки'":"ru", "'разливы рек'":"ru", "'паводок на реке'":"ru", "'наводнение на реке'":"ru", "'речное наводнение'":"ru", "'за́суха'":"ru", 
 #"'речные наводнения'":"ru", "'речные паводки'":"ru", "'флювиальные наводнения'":"ru", "'саранча'":"ru", "'саранчи'":"ru", "'саранчой'":"ru", "'Хохвассер'":"ru", 

 "'世纪之夏'":"zh", "'世纪的夏天'":"zh", "'世纪的夏季'":"zh", "'丛林之火'":"zh",  "'寒潮'":"zh", "'黑冰'":"zh", "'干旱'":"zh", "'坠落'":"zh", "'热波'":"zh", 
 "'丛林大火'":"zh", "'丛林火'":"zh", "'丛林火灾'":"zh", "'严寒'":"zh", "'严寒天气'":"zh", "'低水'":"zh", "'低水位'":"zh", "'低水分'":"zh", "'冬天的到来'":"zh", 
 "'冬天的开始'":"zh", "'冬天的来临'":"zh", "'冬季的到来'":"zh", "'冰山'":"zh", "'冰山一族'":"zh", "'冰山一角'":"zh", "'冰山上'":"zh", "'冻人'":"zh", "'冻伤'":"zh", 
 "'冻伤的雨'":"zh", "'冻土'":"zh", "'冻疮'":"zh", "'冻结的雨'":"zh", "'冻结的雨水'":"zh", "'冻雨'":"zh", "'北方之光'":"zh", "'北方的光'":"zh", "'北极光'":"zh", 
 "'北极星'":"zh", "'台风'":"zh", "'啸天'":"zh", "'地质灾害'":"zh", "'地震'":"zh", "'坠落的岩石'":"zh", "'塌方'":"zh", "'夜晚的霜冻'":"zh", "'夜间结霜'":"zh", 
 "'夜间霜冻'":"zh", "'夜霜'":"zh", "'大暴雨'":"zh", "'大雨'":"zh", "'大雨倾盆'":"zh", "'大雨天气'":"zh", "'大雨滂沱'":"zh", "'大雪纷飞'":"zh", "'太阳暴'":"zh", 
 "'太阳能风暴'":"zh", "'太阳风暴'":"zh", "'季候风'":"zh", "'季节性'":"zh", "'季风'":"zh", "'寒流'":"zh", "'寒流来袭'":"zh", "'寒潮来袭'":"zh", "'山体滑坡'":"zh", 
 "'山崩 地裂'":"zh", "'山崩地裂'":"zh", "'山火'":"zh", "'崩坏'":"zh", "'干旱化'":"zh", "'干旱化程度'":"zh", "'干旱性'":"zh", "'干旱问题'":"zh", "'干燥'":"zh", 
 "'干燥度'":"zh", "'干燥性'":"zh", "'干燥症'":"zh", "'弗罗斯特'":"zh", "'扬州的'":"zh", "'沙尘暴'":"zh", "'拉哈尔'":"zh", "'拉哈爾'":"zh", "'旋风'":"zh", "'旋风型'":"zh", 
 "'旋风式'":"zh", "'旋风系列'":"zh", "'日照风暴'":"zh", "'旱情'":"zh", "'旱灾'":"zh", "'晚霜'":"zh", "'晚霜期'":"zh", "'暴洪'":"zh", "'暴雨'":"zh", "'暴雨洪水'":"zh", 
 "'暴雪'":"zh", "'暴雪天气'":"zh", "'暴风雨'":"zh", "'暴风雪'":"zh", "'本世纪的夏天'":"zh", "'杜儿'":"zh", "'杜勒'":"zh", "'杜埃尔'":"zh", "'杜尔'":"zh", "'森林大火'":"zh", 
 "'森林火灾'":"zh", "'森林火警'":"zh", "'森林防火'":"zh", "'欢呼'":"zh", "'欢呼吧'":"zh", "'欢呼声'":"zh", "'水位低'":"zh", "'水患'":"zh", "'水灾'":"zh", "'永久冻土'":"zh", 
 "'永久性冻土'":"zh", "'永久性冻土层'":"zh", "'永冻土'":"zh", "'污泥流动'":"zh", "'污泥流向'":"zh", "'污泥流量'":"zh", "'沙尘暴'":"zh", "'沙暴'":"zh", "'河水氾滥'":"zh", 
 "'河水泛滥'":"zh", "'河流泛滥'":"zh", "'河流洪水'":"zh", "'沿海地区洪水'":"zh", "'沿海地区的洪水'":"zh", "'沿海洪水'":"zh", "'沿海洪灾'":"zh", "'泥沙'":"zh", 
 "'泥泞'":"zh", "'泥浆'":"zh", "'泥石流'":"zh", "'洪水'":"zh", "'洪水泛滥'":"zh", "'洪水灾害'":"zh", "'浮冰'":"zh", "'浮动冰'":"zh", "'浮动冰层'":"zh", "'海啸'":"zh", 
 "'海藻蓝'":"zh", "'海藻蓝调'":"zh", "'淤泥'":"zh", "'v淤泥流量'":"zh", "'混乱的大雪'":"zh", "'混乱的雪'":"zh", "'混乱的雪地'":"zh", "'混乱的雪景'":"zh", "'滑坡'":"zh", 
 "'漂流的雪'":"zh", "'漂流雪'":"zh", "'漂雪'":"zh", "'火山喷发'":"zh", "'火山爆发'":"zh", "'火山爆發'":"zh", "'火山爆裂'":"zh", "'热力'":"zh", "'热度'":"zh",
 "'热浪'":"zh", "'热浪滚滚'":"zh", "'热潮'":"zh", "'热能'":"zh", "'热量'":"zh", "'砂暴'":"zh", "'碎屑流'":"zh", "'碎片流'":"zh", "'碎片流动'":"zh", "'落石'":"zh", 
 "'落石事件'":"zh", "'藻华'":"zh", "'藻类大量繁殖'":"zh", "'藻类的蓝调'":"zh", "'藻类繁殖'":"zh", "'藻类蓝调'":"zh", "'蝗灾'":"zh", "'蝗虫'":"zh", "'蝗虫之灾'":"zh", 
 "'蝗虫灾'":"zh", "'蝗虫灾害'":"zh", "'蝗虫的危害'":"zh", "'蝗虫的危害性'":"zh", "'融雪'":"zh", "'融雪剂'":"zh", "'诗尼戈尔'":"zh", "'诗尼格罗伯'":"zh", "'诗篇》杂志'":"zh", 
 "'诗篇》杂志社'":"zh", "'连续下雨'":"zh", "'连续的雨'":"zh", "'连续的雨水'":"zh", "'连续降雨'":"zh", "'迟来的霜冻'":"zh", "'迟来的霜降'":"zh", "'野火'":"zh", 
 "'野生火'":"zh", "'野生火灾'":"zh", "'雪'":"zh", "'雪地'":"zh", "'雪崩'":"zh", "'雪崩事件'":"zh", "'雪景'":"zh", "'雪灾'":"zh", "'雪花'":"zh", "'雪花纷飞'":"zh", 
 "'雪花飘飘'":"zh", "'雪花飞舞'":"zh", "'雪融化'":"zh", "'雪融化了'":"zh", "'雷击'":"zh", "'雷击事件'":"zh", "'雷击事故'":"zh", "'雷暴'":"zh", "'雷电袭击'":"zh", 
 "'雷雨'":"zh", "'雷雨天'":"zh", "'雷雨天气'":"zh", "'雹子'":"zh", "'霜冻'":"zh", "'霜淇淋'":"zh", "'霜降'":"zh", "'颱風'":"zh", "'风暴'":"zh", "'风暴暴涨'":"zh", 
 "'风暴浪涌'":"zh", "'风暴浪潮'":"zh", "'风暴潮'":"zh", "'飓风'":"zh", "'飓风来临时'":"zh", "'飓风来了'":"zh", "'飓风来袭'":"zh", "'飘雪'":"zh", "'龙卷风'":"zh", 


 "'צונאמי'":"he", "'שיטפון'":"he", 
 "'הצפה'":"he",  "'בַּצוֹרֶת'":"he",  "'שריפת יער'":"he", "'רעידת אדמה'":"he",  "'הוריקנים'":"he",  "'טַיִפוּן'":"he",  "'צִיקלוֹן'":"he",  "'כפור מאוחר'":"he",  "'שֶׁלֶג'":"he", 
 "'סערה'":"he",  "'גאות נמוכה'":"he",  "'מַפּוֹלֶת שְׁלָגִים'":"he",  "'קַרחוֹן'":"he",  "'הַר גַעַשׁ'":"he",  "'כְּפוֹר'":"he",  "'סערה'":"he",  "'רוֹב מוֹחֵץ'":"he",  "'דְאָגָה'":"he", 
 "'בָּרָד'":"he",  "'גֶשֶׁם כָּבֵד'":"he",  "'חוֹם'":"he",  "'טוֹרנָדוֹ'":"he",  "'מכנסי רוח'":"he",  "'קרחונים'":"he",  "'זרם בוץ'":"he",  "'לָבָה'":"he",  "'התפרצות געשית'":"he", 
 "'גַל חוֹם'":"he",  "'אבנים נופלות'":"he",  "'סער סערה'":"he",  "'הוֹרִיקָן'":"he",  "'גל הסערה'":"he",  "'גשם רציף'":"he",  "'סוּפַת שֶׁלֶג'":"he",  "'גשם קרח'":"he", 
 "'כפור לילה'":"he",  "'קאלטוול'":"he",  "'תחילת החורף'":"he",  "'טוֹרנָאדוֹ'":"he",  "'מַפּוֹלֶת הַרִים'":"he",  "'לְהִסְתַעֵר'":"he",  "'ארבה'":"he",  "'לְזַגֵג'":"he",  "'פרפרוסט'":"he", 
 "'סופת חול'":"he",  "'פריחת אצות'":"he",  "'יוֹבֶשׁ'":"he",  "'לְהַצִיף'":"he",  "'שִׁיטָפוֹן'":"he",  "'מַבּוּל'":"he",  "'לְהִסְתַעֵר'":"he",  "'מַפּוֹלֶת שֶׁלֶג'":"he",  "'יוֹבֶשׁ'":"he", 

 #suaheli
 "'ukame'":"sw", "'mafuriko'":"sw", "'kimbunga'":"sw", "'barafu'":"sw", "'mafuriko'":"sw", "'moto wa nyika'":"sw", "'tetemeko la ardhi'":"sw", "'kuganda'":"sw", 
"'theluji'":"sw", "'dhoruba ya radi'":"sw", "'wimbi la chini'":"sw", "'Banguko'":"sw", "'mkulima'":"sw", "'baridi'":"sw", "'dhoruba ya upepo'":"sw", 
"'maporomoko ya ardhi'":"sw", "'mtiririko wa matope'":"sw", "'mvua ya mawe'":"sw", "'mvua kubwa'":"sw", "'joto'":"sw", "'kimbunga'":"sw", "'moto wa msituni'":"sw", 
"'baridi ya kufungia'":"sw", "'dhoruba'":"sw", "'hali ya hewa kali'":"sw", "'mlipuko wa volcano'":"sw", "'mvua kubwa'":"sw", "'kuba joto'":"sw", 
"'shetani wa vumbi'":"sw", "'wimbi la joto'":"sw", "'upepo wa baridi'":"sw", "'dhoruba ya theluji'":"sw", "'uchafu'":"sw", "'theluji ya theluji'":"sw", 
"'theluji inayovuma'":"sw", "'mteremko wa theluji'":"sw", "'baridi ya usiku'":"sw", "'ukame mkubwa'":"sw", "'snap baridi'":"sw", "'uchawi wa baridi'":"sw", 
"'mafuriko ya maji'":"sw", "'nzige'":"sw", "'panzi'":"sw", "'haboob'":"sw", "'dhoruba ya mchanga'":"sw", "'mwani huchanua'":"sw", "'maua ya mwani'":"sw", 
## "'permafrost'":"sw", "'tsunami'":"sw", "'volkano'":"sw", "'lahar'":"sw", 
}

#searchWords = {"'petropolis'":"de", "'petropolis'":"en", "'storm eunice'":"en", "'Sturm Ylenia'":"de", "'Sturm Zeynep'":"de", 
#  "'Sturm Antonia'":"de", "'Tempete Eunice'":"fr", "'ice jam'":"en", "'storm franklin'":"en", "'emnati'":"en"
#  }    
# 

#searchWords = {"'Hochwasser Südafrika'":"de", "'Überschwemmung Südafrika'":"de", "'KZN flood'":"en", "'KZN floods'":"en", "'KZN flooding'":"en",
#               "'Hochwasser KwaZulu'":"de", "'KwaZulu flood'":"en", "'SA flood'":"en", "'South Africa flood'":"en", "'India heatwave'":"en",
#               "'Hitzewelle Indien'":"de", "'Hitzewelle Pakistan'":"de",  "'California drought'":"en", "'Utah drought'":"en"
#  }     

#searchWords = {"'Dürre Italien'":"de", "'Dürre Frankreich'":"de","'Dürre Portugal'":"de", "'Dürre Polen'":"de", 
#               "'Dürre USA'":"de", "'Dürre Iran'":"de", "'japan heatwave'":"en", "'drought italy'":"en",
#               "'aridità'":"it", "'siccità'":"it", "'secchezza'":"it", "'secca'":"it", "'Tornado Niederlande'":"de",
#               "'Hochwasser Sidney'":"de", "'Flooding Sidney'":"de", "'Tornado Holland'":"de", "'Grossbrand Rom'":"de", "'Gletscher Dolomiten'":"de",
#               "'Dürre China'":"de", "'Hochwasser China'":"de", "'Hitze China'":"de", "'china heatwave'":"en", "'drought china'":"en", "'flooding china'":"en",
#               "'Waldbrand Griechenland'":"de", "'wildfire greece'":"en", 
# }

'''
searchWords = {
               "'Erdbeben China'":"de", "'Hochwasser Pakistan'":"de", "'china earthquake'":"en", "'drought china'":"en", "'flooding pakistan'":"en", "'flooding'":"en",
               "'中国 热浪'":"zh", "'中国 旱灾'":"zh", "'中国 洪水'":"zh", "'热浪'":"zh", "'旱灾'":"zh", "'洪水'":"zh", "'地震'":"zh",  "'地 震'":"zh",  "'地质灾害'":"zh"
}


searchWords = {
               "'موجة حارة'":"ar", "'جفاف'":"ar", "'حرائق الغابات'":"ar", "'انخفاض مستوى الماء'":"ar", 
               "'Dürre'":"de", "'Hitzewelle'":"de", "'Waldbrand'":"de", "'Niedrigwasser'":"de",
               "'καύσωνας'":"el", "'ξηρασία'":"el", "'υγρό πύρ'":"el", "'χαμηλή στάθμη νερού'":"el",
               "'drought'":"en","'heatwave'":"en",  "'wildfire'":"en", "'low water level'":"en",
               "'ola de calor'":"es", "sequía":"es", "'incendio forestal'":"es", "'bajo nivel de agua'":"es", 
               "'vague de chaleur'":"fr", "'sécheresse'":"fr", "'incendies'":"fr", "'faible niveau d'eau'":"fr", 
               "'גל חום'":"he", "'בַּצוֹרֶת'":"he", "'אש בשדה קוצים'":"he", "'גאות נמוכה'":"he",
               "'हीटवेव'":"hi", "'सूखा'":"hi", "'जंगल की आग'":"hi", "'कम ज्वार'":"hi",   
               "'ondata di caldo'":"it", "'siccità'":"it", "'macchia d'olio'":"it", "'livello dell'acqua basso'":"it",
               "'熱波'":"ja", "'干ばつ'":"ja", "'山火事'":"ja", "'干潮'":"ja",
               "'hittegolf'":"nl", "'droogte'":"nl", "'wildvuur'":"nl", "'laagtij'":"nl",
               "'hetebølge'":"no", "'tørke'":"no", "'skogbrann'":"no", "'lavvann'":"no",
               "'onda de calor'":"pt", "'seca'":"pt", "'incêndios'":"pt", "'nível de água baixo'":"pt",   
               ##"'värmebölja'":"sv", "'torka'":"sv", "'löpeld'":"sv", "'lågvatten'":"sv",    
               "'ukame'":"sw", "'wimbi la joto'":"sw", "'Moto wa msitu maji'":"sw", "'ya chini'":"sw",                
               "'жара'":"ru", "'засуха'":"ru", "'лесной пожар'":"ru", "'отлив'":"ru",  
               "'گرمی کی لہر'":"ur", "'خشک سالی'":"ur", "'جنگل کی آگ'":"ur", "'کم جوار'":"ur",   
               "'热浪'":"zh", "'旱灾'":"zh", "'森林火灾'":"zh", "'低潮'":"zh", "'乾旱'":"zh", "'野火'":"zh",
               #"'हीटवेव'":"bn", 

}
'''




stopDomains = ["www.mydealz.de", "www.techstage.de", "www.nachdenkseiten.de", "www.amazon.de", "www.4players.de", "www.netzwelt.de", "www.nextpit.de",
               "www.mein-deal.com", "www.sparbote.de", "www.xda-developers.com" "www.pcgames.de", "blog.google", "www.ingame.de", "playstation.com",
               "www.pcgameshardware.de", 
                ]



extractCodes = [
    {'trg':'published', 'tag':'meta', 'att':'property', 'idn':'article:modified_time', 'val':'content'},
    {'trg':'published', 'tag':'time', 'att':'class', 'idn':'atc-MetaTime', 'val':'datetime'},

    {'trg':'published', 'tag':'meta', 'att':'itemprop', 'idn':'dateModified', 'val':'content'},
    {'trg':'published', 'tag':'meta', 'att':'name', 'idn':'buildDate', 'val':'content'},

    {'trg':'description', 'tag':'meta', 'att':'property', 'idn':'og:description', 'val':'content'},   
    {'trg':'description', 'tag':'meta', 'att':'property', 'idn':'twitter:description', 'val':'content'},
    {'trg':'description', 'tag':'meta', 'att':'name', 'idn':'description', 'val':'content'},    
]

#https://github.com/theSoenke/news-crawler/blob/master/data/feeds_de.txt

                  
def dataIsNotBlocked(data):
    for blocked in stopDomains: 
        if blocked in data['domain']:
            return False
    return True         

#replace/drop: "https://www.zeit.de/zustimmung?url="  

#get url data (inq)  -> check if keyword in title|description    and url equal
#see 'https://www.stern.de/panorama/weltgeschehen/news-heute---ocean-viking--rettet-mehr-als-40-menschen-aus-dem-mittelmeer-30598826.html'

def extractInfo(url):
    print(url)
    data = {}
    data['url'] = url
    data['published'] = '1970-01-01T00:00:00'
    domain = urlparse(url).netloc
    data['domain'] = domain
    content = ""
    try:
        page = requests.get(url, timeout=10)
        data['status'] = page.status_code
        if page.status_code == 200:
            content = page.content
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        data['status'] = 999  

    DOMdocument = BeautifulSoup(content, 'html.parser')
    #<html lang="de">
    htmlTag = DOMdocument.html
    if(htmlTag and htmlTag.has_attr('lang')):
        data['language'] = htmlTag['lang']
    if(DOMdocument.title):
        data['title'] = DOMdocument.title.string
    if(DOMdocument.description):
        data['description'] = DOMdocument.description.string
    # og:title
    title = DOMdocument.find('meta', attrs={'property': 'og:title'})
    if(title):
      if('content' in title):  
        data['title'] = title['content']

    title = DOMdocument.find('meta', attrs={'property': 'twitter:title'})
    if(title):
      if('content' in title):  
        data['title'] = title['content']

    image = DOMdocument.find('meta', attrs={'property': 'og:image'})
    if(image):
        if(image.get('content')):
            data['image'] = image.get('content')
    description = DOMdocument.find('meta', attrs={'name': 'description'})
    if(description):
        if(description.get('content')):
           data['description'] = description.get('content') 
        if(description.get('value')):
           data['description'] = description.get('value') 
    description = DOMdocument.find('meta', attrs={'property': 'og:description'})
    if(description):
      if(description.get('content')): 
        data['description'] = description.get('content')
    description = DOMdocument.find('meta', attrs={'property': 'twitter:description'})
    if(description):
      if(description.get('content')): 
        data['description'] = description.get('content')
    #extract date from url
    match = re.search(r'20\d{2}/\d{2}/\d{2}', url)
    if(match):
       data['published'] = match.group().replace('/','-')+'T12:00:00' 

    #extract date from archive
    #s2 = 'https://web.archive.org/web/20170817131154/h'
    #match2 = re.search(r'archive.org/web/(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})', s2)
    #print(match2.groupdict())

    updated = DOMdocument.find('meta', attrs={'property': 'og:updated_time'})
    if(updated):
        if(updated.get('content')):
           data['published'] = updated.get('content')  
    modified = DOMdocument.find('meta', attrs={'name': 'last-modified'})
    if(modified):
        if(modified.get('content')):
           data['published'] = modified.get('content')  
    modified2 = DOMdocument.find('meta', attrs={'property': 'article:modified_time'})
    if(modified2):
        if(modified2.get('content')):
           data['published'] = modified2.get('content')     
    published2 = DOMdocument.find('meta', attrs={'name': 'cXenseParse:publishtime'})
    if(published2):
        if(published2.get('content')):
           data['published'] = published2.get('content')  
    published3 = DOMdocument.find('meta', attrs={'itemprop': 'datePublished'})
    if(published3):
        if(published3.get('content')):
           data['published'] = published3.get('content')                             
    issued = DOMdocument.find('meta', attrs={'name': 'DC.date.issued'})
    if(issued):
        if(issued.get('content')):
           data['published'] = issued.get('content')          
    published = DOMdocument.find('meta', attrs={'property': 'article:published_time'})
    if(published):
        if(published.get('content')):
           data['published'] = published.get('content')  
    datum = DOMdocument.find('meta', attrs={'name': 'date'})
    if(datum):
        if(datum.get('content')):
           data['published'] = datum.get('content')  

    for code in extractCodes:
        identity = DOMdocument.find(code['trg'], attrs={code['att']: code['idn']})
        if(identity):
            if(identity.get(code['val'])):
                data[code['trg']] = identity.get(code['val'])         



#get time of archive.org (earliest)
#get time of url:  yyyy/mm/dd


#<div class="date-published">19.03.2017 Stand 19.03.2017, 16:57 Uhr</div>

# script only
# https://www.cbc.ca/news/science/climate-change-india-farmer-suicides-1.4230510
# https://www.washingtonpost.com/news/worldviews/wp/2017/09/08/hurricane-jose-threatens-a-second-blow-to-caribbean-islands-devastated-by-irma/
# https://nationalpost.com/news/world/taiwan-earthquake-rescue-efforts-temporarily-suspended-after-building-tilting-at-45-degree-angle-begins-to-slide



    language = DOMdocument.find("meta",  property="og:locale")
    if(language and ('content' in language)):
        data['language'] = language['content']

    #<meta name="news_keywords" content="sierra leona, inundaciones"/>  
    #<meta property="og:locale" content="es_LA"/>    

    #data['author'] = DOMdocument.find("meta",  property="author")['content'] 
    # keywords content-language og:site_name 
    # twitter:title ...
    # rss-feeds:  <link rel="alternate" type="application/rss+xml" title="xxx" href="https://www.lvz.de/rss/feed/lvz_nachrichten" />
    return data




collectedNews = {}

def addNewsToCollection(data):
    global collectedNews
    pubDate = parser.parse(data['published'])
    if(not data['language'] in collectedNews):
        collectedNews[data['language']] = {}
    fileDate = 'news_'+pubDate.strftime('%Y_%m')+'.csv'
    if(not fileDate in collectedNews[data['language']]):
        if(os.path.isfile(DATA_PATH / data['language']/ fileDate)):
            #df = pd.read_csv(DATA_PATH / fileDate, delimiter=',' ,index_col='url')
            df = pd.read_csv(DATA_PATH / data['language'] / fileDate, delimiter=',',index_col='index')
            collectedNews[data['language']][fileDate] = df.to_dict('index')
        else:
            collectedNews[data['language']][fileDate] = {}
    if(not data['url'] in collectedNews[data['language']][fileDate]):
        data = translateNews(data)
        print(data['en'])
        data = archiveUrl(data)
        collectedNews[data['language']][fileDate][data['url']] = data
        return True
    return False

def storeCollection():
    global collectedNews
    cols = ['url','valid','domain','en','title','description','image','published','archive','content','language','keyword']
    for language in collectedNews:
        for dateFile in collectedNews[language]:
            df = pd.DataFrame.from_dict(collectedNews[language][dateFile], orient='index', columns=cols)
            #df.to_csv(DATA_PATH / dateFile, index=True) 
            if(not os.path.exists(DATA_PATH / language)):
                os.mkdir(DATA_PATH / language)
            df.to_csv(DATA_PATH / language / dateFile, index_label='index') 
    collectedNews = {}

# self.randomWordsDF = pd.DataFrame.from_dict(self.randomWords, orient='index', columns=self.randomBase.keys())  
# self.randomWordsDF.to_csv(DATA_PATH / self.category / "csv" / ("words_random_"+str(self.randomSize)+".csv"), index=True)

def sendNewsToMail(data): 
    sender_address = os.getenv('SENDER_EMAIL')
    sender_pass = os.getenv('SENDER_PASSWORD')
    receiver_address = os.getenv('RECEIVER_EMAIL')
    
    sender_address = "micha.kahle@gmail.com"
    sender_pass = "5chu55el_2017@Flixbu5"
    receiver_address = "climateWhisperer@gmail.com"
    #if( & & ):
      #if(sender_address == 'sender@gmail.com'):  print("Please edit 'SENDER_EMAIL' in secrets.py"); return None
      #if(sender_pass == 'secret_sender_password'):  print("Please edit 'SENDER_PASSWORD' in secrets.py"); return None
      #if(receiver_address == 'receiver@gmail.com'):  print("Please edit 'RECEIVER_EMAIL' in secrets.py"); return None
    message = MIMEMultipart()
    message['Subject'] = data['keyword'] + ': ' +data['title']
    message['From'] = receiver_address
    message['To'] = sender_address
    message.attach(MIMEText(data['url'], 'plain'))

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def translateNews(data):
    shortText = str(data['title'])+'. '+str(data['description'])
    if('en'==data['language']):
        data['en'] = shortText
    else:
        data['en'] = GoogleTranslator(source=data['language'], target='en').translate(shortText)
    return data

# https://www.cnbeta.com/articles/tech/1182049.htm

def archiveUrl(data):
    #timetravelDate = datetime.datetime.strptime(data['published'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
    #pubDate = datetime.datetime.fromisoformat(data['published'])
    #pubDate = parser.isoparse(data['published'])
    timetravelDate = '19700101'
    pubDate = None
    try:
        pubDate = parser.parse(data['published'])
    except:
        print('date parse error 1')
    if(not pubDate):
      try:
        pubDate = parser.isoparse(data['published'])
      except:
        print('date parse error 2')   
    if(pubDate):
        timetravelDate = pubDate.strftime('%Y%m%d')
    timetravelUrl = 'http://timetravel.mementoweb.org/api/json/'+timetravelDate+'/'+data['url']
    try:
        page = requests.get(timetravelUrl, timeout=10)
        if page.status_code == 200:
            content = page.content
            #print(content)
            if(content):
                print(content)
                jsonData = json.loads(content)
                if(jsonData and jsonData['mementos']):
                    data['archive'] = jsonData['mementos']['closest']['uri'][0]
                    if('1970-01-01T00:00:00' == data['published']):
                        data['published'] = jsonData['mementos']['closest']['datetime']
                #'closest'
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("not archived yet")
        saveUrl = 'https://web.archive.org/save/' + data['url'] # archive.org
        #saveUrl = 'https://archive.is/submit/'
        #saveUrl = 'https://archive.ph/submit/'
        try:
            page = requests.get(saveUrl, timeout=240)  # archive.org
            #page = requests.post(saveUrl, data = {'url':data['url']}, timeout=240)
            if page.status_code == 200:
                print('archived!')
        except requests.exceptions.RequestException as e2:
            print("not archivable: " + data['url'])
    return data 

def inqRandomNews():
    apiKey = os.getenv('NEWSAPI_KEY')
    apiKey = 'af24229d673d4b1ab546df8c4ca9f176'

    #keyWord = random.choice(searchWords)
    #language = 'de'
    #language = 'en'   
    #language = 'fr' 
    keyWord = random.choice(list(searchWords.keys()))
    language = searchWords[keyWord]
    newLanguage = random.choice(newsapiLanguages)
    if((not newLanguage == language) & (random.uniform(0.0, 100.0)>70.0)):
        print('language: '+language+'; keyword: '+keyWord)
        keyWord = keyWord.strip("'")
        translatorList = []
        # if  GoogleTranslator.get_supported_languages(as_dict=True).values()
        translatorList.append(GoogleTranslator(source=language, target=newLanguage))
        translatorList.append(MyMemoryTranslator(source=language, target=newLanguage))   #-ud(ur?),se(sv?)
        if((not language in ['ar','he','no','se','ud','ur']) and (not newLanguage in ['ar','he','no','se','ud','ur'])):
            translatorList.append(LingueeTranslator(source=language, target=newLanguage))
        #Yandex, Deepl, QCRI needs API
        someTranslator = random.choice(translatorList)
        try:
            newKeyWord = someTranslator.translate(keyWord)
            keyWord = "'" + newKeyWord + "'"
            language = newLanguage
        except deep_translator.exceptions.ElementNotFoundInGetRequest as e:
            print(['ElementNotFoundInGetRequest', e])
        except:
            print("Some exception in keyword translate - keep")
    if(not 'xx'==language):
        #searchWords.pop(keyWord)

        page = random.choice(['1','2','3','4','5'])  
        #page = '1'
        sort = random.choice(['relevancy', 'popularity', 'publishedAt'])
        #sort = 'relevancy'

        print('language: '+language+'; keyword: '+keyWord+'; Page: '+page)
        # https://newsapi.org/docs/endpoints/everything
        url = ('https://newsapi.org/v2/everything?'
            'q='+keyWord+'&'
            'language='+language+'&'
            'page='+page+'&'
            'sortBy='+sort+'&'
            'apiKey='+apiKey
            #'excludeDomains=www.zeit.de,www.reuters.com'
            )
            
            # sortBy=relevancy   : relevancy, popularity, publishedAt
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        #print(response.text)
        foundNew = False
        foundZero = True
        if(response.text):
            jsonData = json.loads(response.text)
            #see climate change....
            if (('ok'==jsonData['status']) and (jsonData['totalResults']>0)):
                foundZero = False
                for article in jsonData['articles']:
                    title = article['title']
                    description = article['description']
                    url = article['url']
                    #later use list...
                    url = url.replace('https://www.zeit.de/zustimmung?url=', '')
                    url = url.replace('https://www.golem.de/sonstiges/zustimmung/auswahl.html?from=', '')
                    url = url.replace('%3A', ':')
                    url = url.replace('%2F', '/')                

                    domain = urlparse(url).netloc

                    image = article['urlToImage']
                    published = article['publishedAt']
                    content = article['content']
                    print(article)



                    data = {'url':url, 'valid':0, 'domain':domain, 'en':'', 'published':published, 'description':description, 'title':title,
                           'image':image, 'content':content, 'language': language, 'keyword':keyWord}
                    if (dataIsNotBlocked(data)):                    
                        print(str(keyWord)+': '+str(title)+' '+str(url))
                        #data = archiveUrl(data)  #done in addNewsToCollection
                        if(addNewsToCollection(data)):
                            #mail
                            #time.sleep(random.uniform(160.5, 175.5))
                            foundNew = True
                            time.sleep(random.uniform(12.5, 14.55))
                            #time.sleep(10)
                            #sendNewsToMail(data) 
                        else:
                            time.sleep(17)
                storeCollection()
            else:
                print(response.text)   
                time.sleep(150) 
                #time.sleep(400) 
        if(not foundNew):
            print(["Nothing new", len(searchWords)])
        else:  
            print(["Found something", len(searchWords)])  
            searchWords.pop(keyWord, None)
        #foundZero    

#b'{"status":"ok","totalResults":1504,
# "articles":[{"source":{"id":null,"name":"heise online"},
#              "author":"Stefan Krempl",
#              "title":"Wissenschaftler: Klimawandel tr\xc3\xa4gt zum Starkregen bei\xe2\x80\x8b",
#              "description":"Die Wolkenbr\xc3\xbcche mit katastrophalen Folgen geh\xc3\xb6ren so nicht mehr zur \xc3\xbcblichen Wetter-Varianz, meinen Wissenschaftler. Sie fordern einen Umbau der Infrastruktur.",
#              "url":"https://www.heise.de/news/Wissenschaftler-Klimawandel-traegt-zum-Starkregen-bei-6140856.html",
#              "urlToImage":"https://heise.cloudimg.io/bound/1200x1200/q85.png-lossy-85.webp-lossy-85.foil1/_www-heise-de_/imgs/18/3/1/3/9/7/8/0/Ueberschwemmung-c06f751f2932e14b.jpeg",
#              "publishedAt":"2021-07-16T15:06:00Z",
#              "content":"Nach den langen und heftigen Regenf\xc3\xa4llen Mitte der Woche treten immer mehr katastrophale Folgen zutage: Die Zahl der Toten w\xc3\xa4chst, allein in Rheinland-Pfalz und Nordrhein-Westfalen sind \xc3\xbcber 100 Mens\xe2\x80\xa6 [+4840 chars]"}



 # se not supported....
 # hi only without language
def inqRandomNews2():
    apiKey = os.getenv('FREENEWS_API_KEY')
    apiKey = '27df9d0a81msh4d292fffabdafdcp145cb9jsndf9f7c9c702e'

    #keyWord = random.choice(searchWords)
    #language = 'de'
    #language = 'en'   
    #language = 'fr' 
    keyWord = random.choice(list(searchWords.keys()))
    language = searchWords[keyWord]
    newLanguage = random.choice(newsapiLanguages)
    if((not newLanguage == language) & (random.uniform(0.0, 100.0)>60.0) & (not 'free' == language)):
        print('language: '+language+'; keyword: '+keyWord)
        keyWord = keyWord.strip("'")
        translatorList = []
        # if  GoogleTranslator.get_supported_languages(as_dict=True).values()
        translatorList.append(GoogleTranslator(source=language, target=newLanguage))
        translatorList.append(MyMemoryTranslator(source=language, target=newLanguage))   #-ud(ur?),se(sv?)
        if((not language in ['ar','he','no','se','ud','hi','sw','ur']) and (not newLanguage in ['ar','he','no','se','ud','hi','sw','ur'])):
            translatorList.append(LingueeTranslator(source=language, target=newLanguage))
        #Yandex, Deepl, QCRI needs API
        someTranslator = random.choice(translatorList)
        # keyWord = GoogleTranslator(source=language, target=newLanguage).translate(keyWord)
        try:
            newKeyWord = someTranslator.translate(keyWord)
            keyWord = "'" + newKeyWord + "'"
            language = newLanguage
        except deep_translator.exceptions.ElementNotFoundInGetRequest as e:
            print(['ElementNotFoundInGetRequest', e])
        except:
            print("Some exception in keyword translate - keep")
    lang2 = language
    if('zh'==language):
        lang2 = 'cn'
    if('ud'==language):
        lang2 = 'ur'
    # if('sv'==language):
    #     lang2 = 'sw'

    if(language in ['hi']):
        lang2 = 'free'

    if(not 'xx'==lang2):
        #searchWords.pop(keyWord)

        page = random.choice(['1','2','3','4','5'])  
        #page = '1'
        sort = random.choice(['relevancy', 'popularity', 'publishedAt'])
        #sort = 'relevancy'

        print('keyword: '+keyWord+'; Page: '+page)

        # https://free-docs.newscatcherapi.com/#request-parameters
        url = "https://free-news.p.rapidapi.com/v1/search"

        
        querystring = {"q":keyWord,"lang":lang2,"page":page,"page_size":"20"}
        if ('free' == lang2):
            querystring = {"q":keyWord,"page":page,"page_size":"20"}

        headers = {
            'x-rapidapi-key': apiKey,
            'x-rapidapi-host': "free-news.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.status_code)
        response.encoding = response.apparent_encoding
        print(response.text)
        print(response.status_code)     #200
        foundNew = False
        foundZero = True
        if((response.text) and (not response.status_code in [204, 500, 504])):
            text = response.text
            #unless string: text = text.decode("utf-8")
            print(['string: ', isinstance(text,str)])
            if(not isinstance(text,str)):
                text = text.decode("utf-8")
            jsonData = json.loads(text)
            #print(jsonData)
            if (('ok'!=jsonData['status'])):
                    time.sleep(20) 
                    page = '1'
                    querystring = {"q":keyWord,"lang":lang2,"page":page,"page_size":"20"}
                    if ('free' == lang2):
                        querystring = {"q":keyWord,"page":page,"page_size":"20"}
                    response = requests.request("GET", url, headers=headers, params=querystring)
                    response.encoding = response.apparent_encoding
                    print(['string: ', isinstance(text,str)])
                    if(not isinstance(text,str)):
                        text = text.decode("utf-8")
                    jsonData = json.loads(response.text)   
                    #print(jsonData)
            if (('ok'==jsonData['status']) and (jsonData['total_hits']>0)):
                foundZero = False  
                for article in jsonData['articles']:
                    print(article)
                    title = article['title']
                    description = '' #  article['summary']
                    url = article['link']    # 'clean_url'
                    #later use list...
                    url = url.replace('https://www.zeit.de/zustimmung?url=', '')
                    url = url.replace('https://www.golem.de/sonstiges/zustimmung/auswahl.html?from=', '')
                    url = url.replace('%3A', ':')
                    url = url.replace('%2F', '/')                

                    domain = urlparse(url).netloc

                    data = extractInfo(url)
                    if('description' in data):
                        description = data['description']
                    else:
                        if(article['summary']):
                            description = article['summary'][0:500]   

                    image = article['media']
                    published = article['published_date']
                    # 'published_date': '2021-09-30 04:15:00', 'published_date_precision': 'full'


                    content = article['summary']
                    topic = article['topic']
                    country = article['country']
                    lang3 = article['language']
                    if(lang3):
                        if (lang2 == 'free'):
                            language = lang3
                            if('cn'==lang3):
                                language = 'zh'
                            #if('ur'==lang3):
                            #    language = 'ud'
                            if('sw'==lang3):
                                language = 'sv'
                            if('ca'==lang3):
                                language = 'fr'
                            if('af'==lang3):
                                language = 'en'                                                               

                    data = {'url':url, 'valid':0, 'domain':domain, 'en':'', 'published':published, 'description':description, 'title':title,
                           'image':image, 'content':content, 'language': language, 'keyword':keyWord, 'topic':topic, 'country':country}
                    if (dataIsNotBlocked(data)):                    
                        print(str(keyWord)+': '+str(title)+' '+str(url))
                        #data = archiveUrl(data)  #done in addNewsToCollection
                        if(addNewsToCollection(data)):
                            #mail
                            #time.sleep(random.uniform(160.5, 175.5))
                            foundNew = True
                            time.sleep(random.uniform(11.5, 14.55))
                            #time.sleep(10)
                            #sendNewsToMail(data) 
                        else:
                            time.sleep(35)
                storeCollection()
            else:
                print([language, lang2])
                print(response.text)   
                time.sleep(300) 
                #time.sleep(400) 
        if(not foundNew):
            print(["Nothing new", len(searchWords)])
        else:  
            print(["Found something", len(searchWords)])  
            #searchWords.pop(keyWord, None)
        #foundZero    

i=1
while True:
  print(i)  
  inqRandomNews2()
  i += 1
  time.sleep(1400) # unless drop none-french
  #time.sleep(20)