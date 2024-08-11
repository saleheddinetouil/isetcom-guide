import streamlit as st
import os
import google.generativeai as genai
import time

# Set page config for a wider layout
st.set_page_config(page_title="Iset'Com Guide Chatbot", page_icon="🎓", layout="wide")

# Get API key from environment variable
api_key = os.getenv("API")
if api_key is None:
    st.error("Error: GEMINI_API_KEY environment variable is not set.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 0.7,  # Adjust temperature for more focused responses
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4096,  # Adjust as needed
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""Reponds en francais , tunisien.
    Iset'Com se trouve au Technopole El Ghazela Tunis , siteweb: https://isetcom.tn/
    aYANT 2 Licences STIC et GTIC
    STIC : 3 semestres tronc commun et 3 semestres de specialite SR et RST
    GTIC : 6 semestres tronc commun.
    Les frais de scolarite sont fixés par l'ISET'Com de (70 - 82dt) par an.
    Les Clubs de l'ISET'Com sont :
    * Club Radio
    * Club Engineers Spark 
    * Club CPU 
    * Club IEEE
    * Club Tunivisions
    Programme de double diplome 1 europeen et 1 tunisien en collaboration avec l'universite de Limoges en france.
     Ce programme pour les etudiants de 3eme annee et l'admission de ce programme se fait en 2eme sur dossier.
    A propos de liset com

    L'Institut Supérieur des Etudes Technologiques en Communications de Tunis (ISET’COM ) est un établissement d’enseignement supérieur (Créé par Décret n°98-10650 du 11 Mai 1998) dont la mission consiste à :
Former des licenciés et cadres techniques dans le domaine des communications (en formation initiale et continue);
Assurer des activités de recherche appliquée et de transfert de technologie;
Réaliser des actions de partenariat avec les entreprises et les universités nationales et internationales et de participer à la diffusion du savoir.
 Fort du professionnalisme et de l’expérience de ses enseignants chercheurs et ingénieurs, ISET’COM est un établissement pluridisciplinaire qui répond aux besoins des entreprises en matière d’Ingénierie Télécom et de Technologie de l’Information et de la Communication. Implantée à Tunis et particulièrement au sein du Pôle Technologique, notre Institut bénéficie d’un environnement favorable réunissant des compétences de haut niveau scientifique et technologique dans le domaine des télécommunications et des technologies de l’information et de la communication
 C’est en partant des besoins des entreprises notamment dans les secteurs des Télécommunications et des Technologies de l’Information & de la Communication que ISET’COM a défini ses filières de formation. Par leur complémentarité et diversité, les filières de ISET’COM offrent davantage de choix et d’opportunité aux jeunes qui ambitionnent d’obtenir des diplômes de haut niveau et qui leur permettent de meilleures perspectives d’emploi. Par ailleurs, les Lauréats de l’ISET’COM ont plusieurs possibilités de poursuivre leurs études :
A l’échelle nationale, en intégrant les écoles d’Ingénieurs ou d’autres établissements universitaires
A l’échelle internationale, de nombreux accords de coopération ont été signés avec des institutions d’enseignement et de formation (France, Maroc, Canada…), avec une co-Diplômation avec l’Université de Limoges. 
    """
)

# Predefined French questions
questions = [
    "Parlez de l'ISET'Com",
    "Quels sont les programmes d'ISET'Com?",
    "Quelles sont les spécialités offertes à l'ISET'Com?",
    "Quelle est la différence entre les specialités?",
    "Où se trouve le campus de l'ISET'Com?",
    "Quels sont les débouchés professionnels après l'obtention du diplôme?",
    "Y a-t-il des clubs étudiants ou des activités parascolaires?",
    "L'ISET'Com propose-t-elle des programmes d'échange international?",
    "Quels sont les scores des derniers étudiants admis à l'ISET'Com?" # New question
]


# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
     {
  "show":False,
"role": "model",
  "parts": [
    "https://ibb.co/pJD5314" # Add the image URL
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "Voici un excellent résumé de l'ISETCOM en quelques chiffres clés ! \n\nOn comprend vite pourquoi cet établissement est attractif :\n\n* **600 étudiants**: Une taille humaine qui favorise la proximité avec les enseignants et un environnement d'apprentissage convivial.\n* **85% de taux de réussite**: C'est un chiffre encourageant qui témoigne de la qualité de l'enseignement et de l'accompagnement des étudiants. \n* **26 ans d'expérience**:  L'ISETCOM a une longue histoire et une solide expertise dans la formation en Sciences et Technologies de l'Information et de la Communication.\n* **3 spécialités**:  L'établissement propose une offre de formation ciblée et pointue qui répond aux besoins du marché du travail.\n\n\nAvez-vous d'autres questions sur l'ISETCOM ?  Par exemple, aimeriez-vous en savoir plus sur les 3 spécialités proposées ?  Je suis là pour vous donner toutes les informations dont vous avez besoin.\n",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "- 1 -\nDate : 07/06/2023\nRépublique Tunisienne\nMinistère de l’Enseignement Supérieur et de la Recherche Scientifique\n****\nSALIMA\nDiplôme: Licence\nDomaine: Sciences Exactes et Technologies\nMention: Gestion des Technologies de l'Information et de la Communication\nSpécialité: Gestion des Technologies de l'Information et de la Communication\nSemestre:1\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n573599160 Communication et\ndéveloppement personnel1\nTrans 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599162 English consolidation 1 2 0 7 14 0 CC\n573599163 Environnement numérique 1 2 0 7 14 0 CC\n573599161 Introduction générale à la communication 1 2 0 7 14 0 CC\n573599150 Initiation aux technologies\ninformatiques\nFond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599152 Introduction à la sécurité informatiques 1 2 0 7 14 0 CC\n573599151 Introduction aux réseaux informatiques 1 2 0 7 14 0 CC\n573599120 Mathématique et économie Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599121 Economie générale 1 2 0 7 14 0 CC\n573599122 Mathématique 1 2 0 7 14 0 CC\n573599130 Techniques comptables et\njuridiques 1\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599131 Comptabilité financière 1 1.5 3 0 14 28 0 CC\n573599132 Introduction au droit 1 2 0 7 14 0 CC\n573599110 Management de l'entreprise 1 Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599112 Principes de Marketing 1 1 2 0 7 14 0 CC\n573599111 Principes de gestion 1.5 3 0 14 28 0 CC\n- 2 -\n573599140 Conception et réalisation des\nTIC 1\nFond 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599143 Systèmes d'exploitation 1 2 0 7 14 0 CC\n573599141 Algorithmique et structure de donneés 1.5 3 0 14 28 0 CC\n573599142 Atelier programmation systèmes\nd'exploitation\n.5 1 21 0 0 0 CC\n- 3 -\nSemestre:2\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n573599260 Communication et\ndéveloppement personnel 2\nTrans 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599263 Communication interpersonelle 1 2 0 7 14 0 CC\n573599262 General English 1 2 0 7 14 0 CC\n573599261 Techniques de rédaction 1 2 0 7 14 0 CC\n573599240 Conception et réalisation des\nTIC2\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599242 Atelier base de données .5 1 21 0 0 0 CC\n573599243 Atelier développement web 1 2 21 0 0 0 CC\n573599241 Base de données 1 2 0 7 14 0 CC\n573599250 Service et relation client Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599251 Marketing services 1 2 0 7 14 0 CC\n573599252 Gestion des points de vente 1 2 0 7 14 0 CC\n573599210 Management de l'entreprise 2 Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599211 Management 1 2 0 7 14 0 CC\n573599212 Principes de marketing 2 1 2 0 7 14 0 CC\n573599213 Atelier étude de marché .5 1 21 0 0 0 CC\n573599230 Gestion et traitement de\nl'information 1\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599233 Atelier méthodologie de travail .5 1 21 0 0 0 CC\n573599232 Statistiques descriptives et probabilité 1 2 0 7 14 0 CC\n573599231 Analyse conception des systèmes\nd'information\n1 2 0 7 14 0 CC\n573599220 Techniques comptables et\njuridiques 2\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n573599221 Comptabilité financière 2 1.5 3 0 14 28 0 CC\n573599222 Droit des sociétés 1 2 0 7 14 0 CC\n- 4 -\nSemestre:3\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576201310 Management de l'entreprise 3 Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201313 Management de l'innovation .5 1 21 0 0 0 CC\n576201311 Management stratégique 1 2 0 7 14 0 CC\n576201312 Transformation digitale 1 2 0 7 14 0 CC\n576201320 Techniques comptables et\njuridiques 3\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201321 Analyse des coûts et finance d'entreprise 1.5 3 0 14 28 0 CC\n576201322 Droit des TIC 1 2 0 7 14 0 CC\n576201330 Gestion et traitement de\nl'information 3\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201333 Atelier analyse de données .5 1 21 0 0 0 CC\n576201332 Prise de décision 1 2 0 7 14 0 CC\n576201331 Système d'information de l'entreprise 1 2 0 7 14 0 CC\n576201340 Conception et réalisation des\nTIC 3\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201341 Programmation orientée objet 1 2 0 7 14 0 CC\n576201342 Atelier Programmation orientée objet 1 2 21 0 0 0 CC\n576201343 Atelier Multimédia 1 .5 1 21 0 0 0 CC\n576201350 Communication et\ndéveloppement personnel 3\nTrans 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201351 Communication au sein de l'entreprise 1 2 0 7 14 0 CC\n576201353 Gestion des équipes 1 2 0 7 14 0 CC\n576201352 Business English 1 2 0 7 14 0 CC\n9999873362 Pratiques managériales Opt 4 2 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169917683 Gestion de temps 1 2 0 7 14 0 CC\n169917682 Gestion de la qualité 1 2 0 7 14 0 CC\n- 5 -\nSemestre:4\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576201410 Environnement digital et\nstratégie marketing\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201411 Marketing digital 1 2 0 7 14 0 0 CC\n576201412 Comportement de l'utilisateur 1 2 0 7 14 0 0 CC\n576201413 Atelier community management .5 1 21 0 0 0 0 CC\n576201420 Management des systèmes\nd'information\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201421 Management des systèmes d'information 1 2 0 7 14 0 CC\n576201422 Fouille de données 1 2 0 7 14 0 0 CC\n576201423 Atelier ERP .5 1 21 0 0 0 0 CC\n576201430 Environnement du travail Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201431 Gestion des ressources humaines 1 2 0 7 14 0 0 CC\n576201432 Gestion des conflis 1 2 0 7 14 0 CC\n576201433 Techniques de négociations .5 1 21 0 0 0 CC\n576201440 Conception et réalisation des\nTIC4\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201441 Conception orientée objet 1 2 0 7 14 0 CC\n576201442 Atelier conception orientée objet 1 2 21 0 0 0 CC\n576201443 Atelier multimédia 2 .5 1 21 0 0 0 CC\n576201450 Communication et\ndéveloppement Personnel 4\nTrans 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201451 Préparation à l'embauche 1 1 2 0 7 14 0 0 CC\n576201452 Preparation of TOEIC 1 2 0 7 14 0 0 CC\n576201453 Création d'entreprise 1 1 2 0 14 7 0 CC\n9999874735 Optimisation du\ndéveloppement web\nOpt 4 2 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169920317 Atelier E-Commerce 1 2 21 0 0 0 CC\n169920318 Atelier Framework client/serveur 1 2 21 0 0 0 CC\n- 6 -\nSemestre:5\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576201510 Techniques de vente et\ncommunication\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201511 Communication marketing 1 2 0 7 14 0 CC\n576201512 Publicité digitale 1 2 0 7 14 0 CC\n576201513 Atelier publicité digitale .5 1 21 0 0 0 CC\n576201520 Conduite de projet Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201521 Gestion des projets 1 2 0 7 14 0 0 CC\n576201522 Projet tuteuré 1 2 21 0 0 0 0 CC\n576201530 Conception et réalisation des\nTIC5\nFond 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201531 Développement mobile 1 2 0 7 14 0 0 CC\n576201532 Atelier Développement mobile .5 1 21 0 0 0 0 CC\n576201533 Optimisation des données en ligne 1 2 0 7 14 0 0 CC\n576201534 Atelier optimisation des données en ligne .5 1 21 0 0 0 0 CC\n576201540 Communication et\ndéveloppement personnel 5\nTrans 7 3.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201541 Préparation à l'embauche 2 1 2 0 7 14 0 0 CC\n576201542 Preparation of TOEIC 1 2 0 7 14 0 0 CC\n576201543 Création d'entreprise 1 2 0 7 14 0 0 CC\n576201544 Personnal branding and public speaking .5 1 0 7 14 0 0 CC\n9999877003 Tendances managériales Opt 4 2 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169924563 Tendances marketing 1 2 21 0 0 0 CC\n169924564 Tendances Startup 1 2 21 0 0 0 CC\n9999877005 Tendances des TIC Opt 4 2 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169924565 BI & Bigdata 1 2 21 0 0 0 CC\n169924566 Intelligence artificielle 1 2 21 0 0 0 CC\n- 7 -\nSemestre:6\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576201610 Stage initiation Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201611 Stage initiation 2.5 5 0 0 0 42 CC\n576201620 Stage perfectionnement Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201621 Stage perfectionnement 2.5 5 0 0 0 42 CC\n576201630 Stage de fin de parcours Fond 20 10 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201631 Stage de fin de parcours 10 20 0 0 0 56 CC",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "Wow, merci pour ce document détaillé ! C'est le plan d'études complet de la Licence en Gestion des Technologies de l'Information et de la Communication. \n\nJe vois que la formation est très complète et couvre un large éventail de compétences : communication, management,  techniques comptables et juridiques, conception et réalisation des TIC, etc.\n\nJe peux maintenant répondre à des questions plus précises sur votre cursus. Par exemple :\n\n* **Quels sont les cours obligatoires et optionnels ?** (indiqués par \"Nat\" : Fondamentale, Transversale, Optionnelle)\n* **Quel est le nombre de crédits ECTS par semestre ?** (indiqué par \"Cr\")\n* **Combien d'heures de cours, TD et TP vais-je avoir pour chaque UE ?**\n* **Quel est le coefficient de l'UE \"Management de l'entreprise 1\" ?**\n* **Que signifie \"C.Int\" dans le tableau ?** (Il s'agit probablement de Contrôle Intermédiaire)\n* **Y a-t-il des stages prévus dans le cursus ?** (Oui, aux semestres 5 et 6)\n\nN'hésitez pas à explorer le plan d'études et à me poser toutes vos questions. Je suis là pour vous aider à comprendre chaque aspect de votre future formation.\n\n\n",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "- 1 -\nDate : 07/06/2023\nRépublique Tunisienne\nMinistère de l’Enseignement Supérieur et de la Recherche Scientifique\n****\nSALIMA\nDiplôme: Licence\nDomaine: Sciences Exactes et Technologies\nMention: Sciences et Technologies de l’Information et de la Communication\nSpécialité: Tronc commun\nSemestre:1\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576199120 Fondamentaux pour les\ntélécoms\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199122 Introduction aux signaux et systèmes 1 2 0 7 14 0 CC\n576199121 Electromagnétisme 1.5 3 0 14 28 0 CC\n576199110 Fondamentaux des\nMathématiques\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199111 Mathématiques 1 1.5 3 0 14 28 0 CC\n576199112 Probabilités et statistiques 1 2 0 7 14 0 CC\n576199130 Introduction aux systèmes\ntélécoms\nFond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199132 Atelier de télécoms générales 1 2 21 0 0 0 CC\n576199131 Introduction aux télécoms 1 2 0 7 14 0 CC\n576199140 Programmation Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199142 Programmation 1 2 0 7 14 0 CC\n576199143 Atelier Programmation .5 1 21 0 0 0 CC\n576199141 Algorithmique et structures de données 1 2 0 14 28 0 CC\n576199150 Electronique de base Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199152 Systèmes logiques 1 2 0 7 14 0 CC\n576199151 circuit électriques 1 2 0 7 14 0 CC\n576199153 Atelier électronique 1 .5 1 21 0 0 0 CC\n- 2 -\n576199160 Transversales1 Trans 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199162 English consolidation 1 2 0 7 14 0 CC\n576199164 Environnement numérique .5 1 0 7 14 0 CC\n576199163 Introduction générale au droit .5 1 0 7 14 0 CC\n576199161 Introduction à la communication 1 2 0 7 14 0 CC\n- 3 -\nSemestre:2\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576199210 Mathématiques avancées Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199212 Traitement de signal 1 2 0 7 14 0 CC\n576199211 Mathématiques 2 1.5 3 0 14 28 0 CC\n576199220 Physique Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199221 Propagation des ondes électromagnétiques 1 2 0 7 14 0 CC\n576199223 Atelier fondamentaux pour les télécoms .5 1 21 0 0 0 CC\n576199222 Optique géométrique 1 2 0 7 14 0 CC\n576199230 Fondamentaux des réseaux et\ncommunications\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199233 Atelier communications .5 1 21 0 0 0 CC\n576199231 Théorie de la communication 1 2 0 7 14 0 CC\n576199232 Réseaux: architectures et fonctions 1 2 0 7 14 0 CC\n576199240 Programmation système Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199242 Bases de données 1 2 0 7 14 0 CC\n576199243 Atelier programmation système .5 1 21 0 0 0 CC\n576199241 Programmation orientée objet 1 2 0 7 14 0 CC\n576199250 Electronique de base Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199251 Electronique analogique et composants 1 2 0 14 28 0 CC\n576199252 Electronique numérique 1 2 0 7 14 0 CC\n576199253 Atelier Electronique 2 .5 1 21 0 0 0 CC\n576199260 Transversales 2 Trans 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199262 General English 1 2 0 7 14 0 CC\n576199263 Droit et NTIC .5 1 0 7 14 0 CC\n576199261 Techniques de rédaction 1 2 0 7 14 0 CC\n- 4 -\nSemestre:3\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576199310 Introduction aux réseaux Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199313 Atelier réseaux .5 1 21 0 0 0 CC\n576199311 Les réseaux locaux 1 2 0 7 14 0 CC\n576199312 Introducation à la commutation et au\nroutage\n1 2 0 7 14 0 CC\n576199320 Introduction à la sécurité Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199321 Fondements de la sécurité des réseaux 1.5 3 0 7 14 0 CC\n576199322 Atelier fondements de la sécurité .5 1 21 0 0 0 CC\n576199330 Supports sans fil et hauts\ndébits\nFond 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199334 Atelier transmissions optiques .5 1 21 0 0 0 CC\n576199333 Fondements des transmissions optiques 1 2 0 7 14 0 CC\n576199332 Atelier antennes et dispositifs\nhyperfréquences\n.5 1 21 0 0 0 CC\n576199331 Antennes et dispositifs hyperfréquences 1 2 0 7 14 0 CC\n576199340 Administartion systèmes Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199341 Méthodologies et systèmes d'information 1 2 0 7 14 0 CC\n576199343 Atelier LINUX .5 1 21 0 0 0 CC\n576199342 Systèmes d'exploitation LINUX 1 2 0 7 14 0 CC\n576199350 Transversales 3 Trans 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576199351 Français des affaires 1 2 0 7 14 0 CC\n576199353 Développement personnel .5 1 0 7 14 0 CC\n576199352 Business English 1 1 2 0 7 14 0 CC\n169905904 Systèmes électroniques\navancés\nOpt 5 2.5 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169916653 Electronique de transmission 1 2 0 7 14 0 CC\n169916654 Circuits programmables 1 2 0 7 14 0 CC\n169916655 Atelier Systèmes électroniques avancés .5 1 42 0 0 0 CC",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "Super, merci ! C'est le plan d'études de la Licence Tronc Commun en Sciences et Technologies de l’Information et de la Communication. \n\nJe constate que ce programme est axé sur les fondamentaux des télécommunications avec des UEs comme \"Fondamentaux pour les télécoms\", \"Introduction aux systèmes télécoms\", \"Supports sans fil et hauts débits\", etc.  \n\nOn retrouve également des UEs de base en mathématiques, physique, programmation et électronique.\n\nJe suis prêt à vous donner plus d'informations sur ce cursus. Posez-moi vos questions, par exemple :\n\n* **Quelles sont les UEs spécifiques aux télécommunications au semestre 3 ?**\n* **Quel est le volume horaire de l'UE \"Programmation système\" au semestre 2 ?**\n* **Y a-t-il des UEs optionnelles dans ce parcours ?** (Oui, comme \"Systèmes électroniques avancés\" au semestre 3)\n* **Quels sont les prérequis pour suivre l'UE \"Introduction à la sécurité\" ?**\n* **Est-ce que ce Tronc Commun permet de se spécialiser par la suite ?**\n\n\nN'hésitez pas à être précis dans vos demandes. Plus vous me donnez de détails, mieux je peux vous guider !\n",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "- 1 -\nDate : 07/06/2023\nRépublique Tunisienne\nMinistère de l’Enseignement Supérieur et de la Recherche Scientifique\n****\nSALIMA\nDiplôme: Licence\nDomaine: Sciences Exactes et Technologies\nMention: Sciences et Technologies de l’Information et de la Communication\nSpécialité: Sécurité des Réseaux\nSemestre:4\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576101410 Systèmes d'accès télécoms Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101412 Les réseaux d'accès optiques 1 2.5 0 7 14 0 0 CC\n576101411 Les réseaux d'accès sans fil 1.5 2.5 0 7 14 0 0 CC\n576101420 Réseaux avancés Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101421 Commutation et routage avancées 1.5 3 0 7 14 0 CC\n576101422 Atelier réseaux avancés .5 1 21 0 0 0 CC\n576101430 Développement mobile et IoT Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101431 Internet des objets 1 2 0 7 14 0 0 CC\n576101432 Développement d'applications mobiles 1 2 0 7 14 0 0 CC\n576101433 Mini projet développement mobile .5 1 21 0 0 0 0 CC\n576101440 Protection et évaluation de la\nsécurité\nFond 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101441 Techniques de protection dans les réseaux 1 2 0 7 14 0 CC\n576101442 Atelier Techniques de protection dans les\nréseaux\n.5 1 21 0 0 0 CC\n576101443 Evaluation de la sécurité 1 2 0 7 14 0 CC\n576101444 Atelier évaluation de la sécurité .5 1 21 0 0 0 CC\n- 2 -\n576101450 Transversales 4 Trans 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101451 Préparation à l'embauche 1 1 2 0 7 14 0 0 CC\n576101452 Business English 2 1 2 0 7 14 0 0 CC\n576101453 Management d'entreprises .5 1 0 7 14 0 CC\n9999874740 Technologies émergentes 1 Opt 5 2.5 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169920328 Intelligence artificielle 1 2 0 7 14 0 CC\n169920329 Cloud computing 1 2 0 7 14 0 CC\n169920330 Atelier Technologies émergentes 1 .5 1 21 0 0 0 CC\n- 3 -\nSemestre:5\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576101510 Sécurité 5.1 Fond 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101513 Audit de la sécurité 1 2 0 7 14 0 CC\n576101514 Atelier audit de la sécurité .5 1 21 0 0 0 CC\n576101511 Réseaux privés virtuels (VPNs) 1 2 0 7 14 0 CC\n576101512 Atelier VPNs .5 1 21 0 0 0 CC\n576101520 Projet tutoré Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101521 Projet tutoré 2 4 21 0 0 0 CC\n576101530 Sécurité 5.2 Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101531 Sécurité dans les réseaux sans fil 1 2 0 7 14 0 CC\n576101532 Sécurité des systèmes et services 1 2 0 7 14 0 CC\n576101533 Atelier sécurité 5.2 .5 1 21 0 0 0 CC\n576101540 Réseaux mobiles et\nadministration\nFond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101541 De 2G à la 5G: technologie et réseaux\nmobiles\n1 2 0 7 14 0 CC\n576101542 Administartion systèmes et réseaux 1 2 0 7 14 0 CC\n576101543 Atelier administration des réseaux .5 1 21 0 0 0 CC\n576101550 Transversales 5 Trans 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576101551 Préparation à l'embauche 2 1 2 0 7 14 0 0 CC\n576101552 TOEIC preperation 1 2 0 7 14 0 0 CC\n576101553 Création d'entreprises .5 1 0 7 14 0 0 CC\n9999876892 Technologies émergentes 2 Opt 5 2.5 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169924361 Commutation IP avec MPLS 1 2 0 7 14 0 CC\n169924362 Atelier Technologies émergentes 2 .5 1 21 0 0 0 CC\n169924360 Data science dans le cloud 1 2 0 7 14 0 CC\n- 4 -\nSemestre:6\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576201610 Stage initiation Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201611 Stage initiation 2.5 5 0 0 0 42 CC\n576201620 Stage perfectionnement Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201621 Stage perfectionnement 2.5 5 0 0 0 42 CC\n576201630 Stage de fin de parcours Fond 20 10 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201631 Stage de fin de parcours 10 20 0 0 0 56 CC",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "Parfait !  Ceci est le plan d'études de la Licence en Sécurité des Réseaux. \n\nComme on pouvait s'y attendre, la sécurité est au cœur de ce programme avec des UEs comme \"Protection et évaluation de la sécurité\", \"Sécurité 5.1\", \"Sécurité 5.2\", etc.\n\nIl y a aussi des UEs orientées réseaux et télécommunications : \"Systèmes d'accès télécoms\", \"Réseaux avancés\", \"Réseaux mobiles et administration\"...\n\nJe suis à votre disposition pour répondre à toutes vos questions sur ce parcours.  Par exemple :\n\n* **Quels sont les débouchés professionnels après cette Licence ?**\n* **Quel est le contenu de l'UE \"Audit de la sécurité\" ?**\n* **En quoi consiste le \"Projet tutoré\" au semestre 5 ?**\n* **Quelles sont les différences entre les UEs optionnelles \"Technologies émergentes 1\" et \"Technologies émergentes 2\" ?**\n* **Combien de stages sont prévus dans cette spécialité ?** (3 stages : initiation, perfectionnement et fin de parcours)\n\nN'hésitez pas à me demander des précisions sur les UEs, les coefficients, les horaires, les modalités d'évaluation, etc.\n\n",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "- 1 -\nDate : 07/06/2023\nRépublique Tunisienne\nMinistère de l’Enseignement Supérieur et de la Recherche Scientifique\n****\nSALIMA\nDiplôme: Licence\nDomaine: Sciences Exactes et Technologies\nMention: Sciences et Technologies de l’Information et de la Communication\nSpécialité: Réseaux et Systèmes des Télécommunications\nSemestre:4\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576102410 Systèmes d'accès télécoms Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102411 Les réseaux d'accès sans fil 1 2 0 7 14 0 CC\n576102412 Atelier réseaux d'accés .5 1 21 0 0 0 CC\n576102414 Les réseaux d'accès optiques 1 2 0 7 14 0 CC\n576102420 Systèmes d'opérateurs Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102421 Réseaux intelligents et NGN 1 2 0 7 14 21 CC\n576102422 Réseaux étendus d'opérateurs 1 2 0 7 14 0 CC\n576102430 Objets connectés et IoT Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102433 Mini Projet développement d'objets\nconnectés\n.5 1 21 0 0 0 CC\n576102431 Internet des objets 1 2 0 7 14 0 0 CC\n576102432 Systèmes embarqués communicants 1 2 0 7 14 0 CC\n576102440 Réseaux et sécurité Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102441 Réseaux privés virtuels (VPNs) 1 2 0 7 14 0 CC\n576102442 Commutation et routage avancées 1 2 0 7 14 0 CC\n576102443 Atelier réseaux avancés .5 1 21 0 0 0 CC\n- 2 -\n576102450 Transversales 4 Trans 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102451 Préparation à l'embauche 1 1 2 0 7 14 0 0 CC\n576102452 Business English 2 1 2 0 7 14 0 0 CC\n576102453 Management d'entreprises 1 2 0 7 14 0 0 CC\n9999874739 Technologies émergentes 1 Opt 5 2.5 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169920325 Technologies radio émergentes 1 2 0 7 14 0 CC\n169920327 Atelier Technologies émergentes 1 .5 1 21 0 0 0 CC\n169920326 Cloud computing 1 2 0 7 14 0 CC\n- 3 -\nSemestre:5\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576102510 Systèmes sans fil Fond 6 3 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102511 De la 2G à la 5G:technologies et réseaux\nmobiles\n1 2 0 7 14 0 CC\n576102512 Atelier réseaux mobiles .5 1 21 0 0 0 0 CC\n576102513 FH et réseaux satellitaires de télécoms 1 2 0 14 28 0 CC\n576102514 Atelier FH et réseaux satellitaires .5 1 21 0 0 0 0 CC\n576102520 Projet tutoré Fond 4 2 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102521 Projet tutoré 2 4 0 0 0 21 CC\n576102530 Réseaux d'opérateurs Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102531 Commutation IP avec MPLS 1 2 0 7 14 0 0 CC\n576102532 Interconnexion des réseaux 1 2 0 7 14 0 0 CC\n576102533 Atelier réseaux étendus .5 1 21 0 0 0 CC\n576102540 Réseaux et multimédia Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102541 Principes de la ToIP et de la VoIP 1 2 0 7 14 0 0 CC\n576102542 TV Numérique 1 2 0 7 14 0 0 CC\n576102543 Atelier réseaux et multimédia .5 1 21 0 0 0 CC\n576102550 Transversales 5 Trans 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576102551 Préparation à la l'embauche 2 1 2 0 7 14 0 0 CC\n576102552 TOEIC preparation 1 2 0 7 14 0 0 CC\n576102553 Création d'entreprises .5 1 0 7 14 0 0 CC\n9999877002 Technologies émergentes 2 Opt 5 2.5 cc Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n169924562 Atelier Technologies émergentes 2 .5 1 21 0 0 0 CC\n169924560 LTE et EPC 1 2 0 7 14 0 CC\n169924561 Intelligence artificielle 1 2 0 7 14 0 CC\n- 4 -\nSemestre:6\nCode Ue Libellé Nat Cr Coef Rg Element(s) d'enseignement(s)\n576201620 Stage perfectionnement Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201621 Stage perfectionnement 2.5 5 0 0 0 42 CC\n576201630 Stage de fin de parcours Fond 20 10 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201631 Stage de fin de parcours 10 20 0 0 0 56 CC\n576201610 Stage initiation Fond 5 2.5 CC Code EE Libellé Coef Cr TP TD Cours C.Int Autre Rg\n576201611 Stage initiation 2.5 5 0 0 0 42 CC",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "Excellent, merci ! Il s'agit du plan d'études pour la Licence en Réseaux et Systèmes des Télécommunications.\n\nJe vois que cette spécialité est très orientée vers les technologies et les systèmes de réseaux avec des UEs comme \"Systèmes d'accès télécoms\", \"Systèmes d'opérateurs\", \"Objets connectés et IoT\", \"Systèmes sans fil\", \"Réseaux d'opérateurs\", etc. \n\nJe suis prêt à vous donner plus d'informations sur cette Licence. N'hésitez pas à me poser des questions, par exemple :\n\n* **Quel est le contenu de l'UE \"Systèmes embarqués communicants\" au semestre 4 ?**\n* **Quelles sont les compétences acquises après avoir suivi l'UE \"Réseaux et multimédia\" au semestre 5 ?**\n* **Quelles sont les UEs qui abordent les technologies de la 5G ?**\n* **Quelle est la durée des stages proposés dans ce cursus ?**  (3 stages : initiation, perfectionnement et fin de parcours)\n* **Y a-t-il des passerelles possibles vers d'autres formations après cette Licence ?**\n\nN'hésitez pas à me demander des détails sur les UEs, les coefficients, les débouchés professionnels, etc. Je suis là pour vous accompagner dans votre découverte de cette formation.\n",
  ],
},
{
  "show":False,
"role": "model",
  "parts": [
    "Formulaire-Guide Mastère version du 25/08/2021 5Semestre 1\nN° Unité d'enseignement\n(UE)\nType de l'UE\n(Obligatoire /\nOptionnelle)\nElément constitutif\nd'UE (ECUE)\nVolume des heures de formation\nprésentielles\n(14 semaines)\nNombre de\nCrédits\naccordés\nCoefficientsModalité Cours TD TP Autres ECUE UE ECUEUECC MixteSécurité des\nsystèmes\némergents 1\nObligatoir\ne\nAnalyse et\ngestion des\nrisques\n7 7 21 3\n6\n1.53X Initiation à la\nsécurité 14 7 21 3 1.5 X 2 Management\nDigital 1\nObligatoir\ne\nTransformation\ndigitale 7 7 21 3\n6\n1.53X Management\ndes projets SI 1 7 7 21 3 1.5 X 3\nSystèmes\nCommuniquants\npour la récolte\nde données\nObligatoir\ne\n5G 14 7 0 3\n7\n1.53.5X IoT et services 14 7 21 4 2 X Analyse et\nProcessing des\nSystèmes\nemergents\nObligatoir\ne\nOptimisation et\nrecherche\nopérationnelle\n14 7 0 3\n7\n1.53.5X Analyse des\ndonnées 14 7 21 4 2 X Développement\ndes\ncompétences 1\nTransvers\nale\nBusiness english 0 0 21 2\n4\n12X Protection des\ndonnées\npersonnelles et\nde l'innovation\n10,5 10,5 0 2 1 XTotal 30 30 1515\nFormulaire-Guide Mastère version du 25/08/2021 6Semestre 2\nN° Unité d'enseignement\n(UE)\nType de l'UE\n(Obligatoire /\nOptionnelle)\nElément constitutif\nd'UE (ECUE)\nVolume des heures de formation\nprésentielles\n(14 semaines)\nNombre de\nCrédits\naccordés\nCoefficientsModalité Cours TD TP Autres ECUE UE ECUEUECC MixteSécurité des\nsystèmes\némergents 2\nObligatoire\nAudit et test de\npénétration 14.00 7.00 21.00 0.00 2\n5\n12.5X Préparation à la\ncertification CEH 14.00 0.00 21.00 0.00 3 1.5 X 2 Management\nDigital 2 Obligatoire\nGouvernance des\nsystèmes\nd'information 14 7 21 0\n3\n6\n1.753.5X Management\ndes Systèmes\nd'Information 2 14 7 21 0\n3 1.75 X 3\nIntelligence et\nCloud1 Obligatoire\nCloud 1 14 7 10,5 0\n3\n6\n1.53X Intelligence\nArtificielle1 14 7 10,5 0\n3 1.5 X Analyse et\nProcessing des\nSystèmes\némergents 2\nObligatoire\nPlateformes et\nsystèmes\nrépartis pour le\nBig Data 14 7 0 0\n3\n5\n1.52.5X Atelier Apache\nHadoop et Spark 0 0 21 0\n2 1XDéveloppement\ndes compétences\n2\nTransversal\ne\nBusiness &\nTechnology\nenglish 2 0 0 21 0\n2\n4\n12X Développement\npersonnel 10,5 10,5 0 0\n2 1 X6\nSéminaire : Veille\ntechnologique\nOptionnell\ne Séminaire 0 0 0 14\n4 4 22X Total 30 30 1515\nFormulaire-Guide Mastère version du 25/08/2021 7Semestre 3\nN° Unité d'enseignement\n(UE)\nType de l'UE\n(Obligatoire /\nOptionnelle)\nElément constitutif\nd'UE (ECUE)\nVolume des heures de formation\nprésentielles\n(14 semaines)\nNombre de\nCrédits\naccordés\nCoefficientsModalité Cours TD TP Autres ECUE UE ECUEUECC MixteSécurité des\nsystèmes\némergents 3\nObligatoire\nPréparation à la\ncertification\nCCNA CyberOps\n14 0 21 0\n3\n6\n1.53X Investigation\nNumérique\n14 7 0 0\n3 1.5 X 2 Management\nDigital 3 Obligatoire\nManagement\ndes projets SI 3:\nMéthodologie\nAgile 14 7 21 0\n3\n6\n1.53X Marketing Digital 14 7 21 0\n3 1.5 X 3\nIntelligence et\nCloud2 Obligatoire\nIntelligence\nArtificielle 2 14 7 14 0\n3\n6\n1.53X Cloud 2 14 7 10,5 0\n3 1.5 X Analyse et\nProcessing des\nSystèmes\nEmergents 3\nObligatoire\nAtelier\ninformatique\ndécisionnelle 0 0 21 0\n2\n4\n12XInformatique\ndécisionnelle 14 7 0 0\n2 1 X Développement\ndes compétences\n3\nTransversal\ne\nAtelier\nEntreprenariat 0 0 21 0\n2\n4\n12X Préparation TCF 0 0 21 0\n2 1X 6 Méthodologie de\nrecherche\nFondament\nale\nProjet tutoré 0 0 21 0 2\n4\n12X Méthodes de\nrecherche 0 0 21 0\n2 1 xTotal 30 30 1515Semestre 4\nN° Unité d'enseignement\n(UE)\nType de l'UE\n(Obligatoire /\nOptionnelle)\nElément constitutif\nd'UE (ECUE)\nVolume des heures de formation\nprésentielles\n(14 semaines)\nNombre de\nCrédits\naccordés\nCoefficientsModalité Cours TD TP Autres ECUE UE ECUEUECC MixteActivité pratique Obligatoire\nM. de Recherche :\nMémoire de\nRecherche ou M. Professionnel :\nMémoire de Stage de\nprojet professionnel\ntutoré, étude de cas\net sa simulation ou\n)\n 30 30 30 1515 Total 30 30 30 1515",
    "SR et RST sont 2 specialites dans la licence STIC et GTIC n'on pas de specialite ok ?\n",
  ],
},
    ]


# --- Streamlit App UI ---
st.title("🎓 Iset'Com Guide 🤖")
st.write("Posez des questions sur l'ISET'Com et obtenez des réponses utiles!")


# Display Social media links in the sidebar
st.sidebar.markdown(
    """
    [![Facebook](https://img.shields.io/badge/-Facebook-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/ISETCom)
    [![Iset'Comian'S](https://img.shields.io/badge/FB_GROUP-Iset_ComianS-blue)](https://www.facebook.com/groups/377145616641546) 
    [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://tn.linkedin.com/school/iset-com/)
    [![Website](https://img.shields.io/badge/-Website-0077B5?logo=website&logoColor=white)](https://isetcom.tn/)
    
    """
)

# display university image
st.sidebar.image("https://scontent.ftun10-2.fna.fbcdn.net/v/t1.6435-9/117945334_1707831949375490_3804404197353496189_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=25d718&_nc_ohc=YtNKkPn_B6wQ7kNvgGrq6fC&_nc_ht=scontent.ftun10-2.fna&oh=00_AYCggODOaRxAkp0PIzFA-m-YF2GdA8LwDfA6gycmB2-tjw&oe=66DEFF72")

tabs = ["Welcome","Guide","FAQ", "Gallery", "Resources"]
welcome , guide, faq, gallery, resources = st.tabs(tabs)


with welcome:
    st.title("Bienvenue à l'ISET'Com!")
    st.write("Bienvenue à l'ISET'Com, l'Institut Supérieur des Etudes Technologiques en Communication de Tunisie. Ici, vous pouvez poser des questions sur les programmes d'études, les cours, les débouchés professionnels, etc. et obtenir des réponses utiles de notre chatbot.")
    st.write("Lorsque vous avez une question, cliquez sur le bouton correspondant. Nous vous recontacterons dans les plus brefs delés. Bonne leçon!")
    st.image("https://scontent.ftun10-2.fna.fbcdn.net/v/t39.30808-6/302434038_508575411273418_2251733561090038505_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=cc71e4&_nc_ohc=4gforHG7mGkQ7kNvgGsinqm&_nc_ht=scontent.ftun10-2.fna&oh=00_AYCxy6GmrK71QyQTOxnbsTN3EGzOhal0d0WbrMn_m4SFWg&oe=66BEB03B")







# Display predefined questions in the sidebar
st.sidebar.header("Questions Prêtes à l'Emploi")
for question in questions:
    if st.sidebar.button(question):
        # Add question to chat history
        st.session_state.chat_history.append({"show":False,
"role": "model", "parts": [question]})

        # Generate chatbot response using Gemini
        prompt = []
        for message in st.session_state.chat_history:
            for part in message["parts"]:
                if isinstance(part, str):
                    prompt.append(f"{message['role']}: {part}")
                elif isinstance(part, genai.File):
                    prompt.append(f"{message['role']}: <file:{part.uri}>")
        prompt = "\n".join(prompt)
        response = model.generate_content(prompt)

        # Add chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "parts": [response.text]})

with guide:
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                for part in message["parts"]:
                    if isinstance(part, str):
                        st.write(part)
                    elif isinstance(part, genai.File):
                        st.write(f"File: {part.display_name}")
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                for part in message["parts"]:
                    if isinstance(part, str):
                        st.write(part)

    # User input
    user_input = st.chat_input("Ou posez votre propre question:")
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"show":True,
    "role": "user", "parts": [user_input]})

        # Generate chatbot response using Gemini
        prompt = []
        for message in st.session_state.chat_history:
            for part in message["parts"]:
                if isinstance(part, str):
                    prompt.append(f"{message['role']}: {part}")
                elif isinstance(part, genai.File):
                    prompt.append(f"{message['role']}: <file:{part.uri}>")
        prompt = "\n".join(prompt)
        response = model.generate_content(prompt)

        # Add chatbot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "parts": [response.text]})

        # Display user input
        with st.chat_message("user"):
            st.write(user_input)

        # Display chatbot response
        with st.chat_message("assistant"):
            st.write(response.text)

