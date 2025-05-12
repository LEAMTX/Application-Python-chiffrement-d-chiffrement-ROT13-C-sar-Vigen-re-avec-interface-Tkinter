import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

###############################
# PARTIE 1 : fonctions-outils
###############################

def mettreEnMaj(texte):
# retourne texte en majuscule
# texte: texte à convertir en majuscule
    return(texte.upper())


def convertirListeASCII(texte):
# retourne la liste des codes ASCII des caractères de texte
# texte : le texte dont on veut la liste des codes
    T = []
    for i in range (0,len(texte)):
        c = ord(texte[i])
        T.append(c)
        #la fonction append nous permet d'ajouter nos donnés au tableau
    return T


def rot13(code):
#retourne le code sur une base de code ASCII après un décalage de 13
#code=ord(lettre)
    if (code>=65 and code <=90):
    
#entre 65 et 90, on est dans le domaine de l'alphabet en majuscule selon la liste ASCII
        code=(code-65+13)%26+65
#on fait modulo 26 pour rester dans l'alphabet en chiffrant
    return code


def rotCesar(code,decalage):
#retourne le code ASCII après un décalage que l'on défini
#code=ord(lettre)
    if (code>=65 and code <=90):
        code=(code-65+decalage)%26+65
        #idem que pour ROT13 mais on remplace 13 par le decalage que l'on choisit
    return code
    
    
def genererPhraseClef (motClef,tailleTexte):
#retourne une phrase clef sur la base du mot clef donné et en fonction de la longueur du texte à chiffrer
#mot clef = suite de caractère qu'on entre pour en faire la base de notre codage et le répéter en fonction du nombre de caractères dans notre phrase à chiffrer
#tailleTexte = nombre de caractère dans le texte à chiffrer
    PhraseClef=motClef
    while (len(PhraseClef)<tailleTexte):
        PhraseClef=PhraseClef+motClef
    PhraseClef=PhraseClef[0:tailleTexte]
    return PhraseClef


def genererTabCodesTranslates(texte):
#on génère un nouveau tableau pour chiffrer en Vigenere sur une base ASCII de translation -32
    Tab=[]
    for i in range (0,len(texte)):
        code=ord(texte[i])-32
        Tab.append(code)
    return Tab


###############################
# PARTIE 2 : fonctions de chiffrement/déchiffrement
###############################

def ChiffrerROT13(texteAChiffrer):
#on traduit le message à chiffrer en chiffres pour appliquer ROT13 et fait une chaine de charactères pour creer le message chiffré
    texteAChiffrer=mettreEnMaj(texteAChiffrer)
    messageChiffré=''
    for i in range (0,len(texteAChiffrer)):
        messageChiffré=messageChiffré+chr(rot13(ord(texteAChiffrer[i])))
    return messageChiffré      


def deChiffrerROT13 (texteADechiffrer):
#pour annuler ROT13 on repasse le message chiffré en ROT13
    return ChiffrerROT13(texteADechiffrer)


def ChiffrerCesar (texteAChiffrer,chiffreCesar):
#on traduit le message à chiffrer en chiffres pour appliquer César et fait une chaine de charactères pour creer le message chiffré
    texteAChiffrer=mettreEnMaj(texteAChiffrer)
    messageChiffré=''
    for i in range (0,len(texteAChiffrer)):
        messageChiffré=messageChiffré+chr(rotCesar(ord(texteAChiffrer[i]),chiffreCesar))
    return messageChiffré


def deChiffrerCesar (texteADeChiffrer,chiffreCesar):
#revenir au message à déchiffrer avec césar revient à faire la même chose que pour chiffrer en césar mais avec le même décalage en négatif
    return ChiffrerCesar (texteADeChiffrer,-chiffreCesar)


def ChiffrerVigenere (texteAChiffrer, motClef):
#on fait la somme de la liste ASCII du message à chiffrer et du mot clef répété en phrase clef selon la longueur de la chaine de charactère pour obtenir le message codé en Vigenere
    PhraseClef=genererPhraseClef(motClef,len(texteAChiffrer))
    Tab1=genererTabCodesTranslates(texteAChiffrer)
    Tab2=genererTabCodesTranslates(PhraseClef)
    MessageChiffré=''
    for i in range (0,len(texteAChiffrer)):
        MessageChiffré=MessageChiffré+chr(((Tab1[i]+Tab2[i])%95)+32)
    return MessageChiffré


def deChiffrerVigenere (texteADechiffrer, motClef):
#après avoir obtenu la phrase clef on soustrait la table ASCII du texte à déchiffrer avec celle de la phrase clef pour retomber sur le message d'origine
    PhraseClef=genererPhraseClef (motClef,len(texteADechiffrer))
    Tab1=genererTabCodesTranslates(PhraseClef)
    Tab2=genererTabCodesTranslates(texteADechiffrer)
    Tabdechiffre=[]
    MessagedeChiffré=""
    for i in range (0,len(texteADechiffrer)):
        dechiffrement=Tab2[i]-Tab1[i]
        while dechiffrement<0:
            dechiffrement=dechiffrement+95
        Tabdechiffre.append(dechiffrement)    
        MessagedeChiffré=MessagedeChiffré+chr(Tabdechiffre[i]+32)
    return MessagedeChiffré  
      
###############################
# PARTIE 3 : Lanceurs
###############################

def boutonAction():
    #verlan=''
    texte= entryTexteSaisi.get()
    #fait appel à texte saisi défini à la ligne 158
    decalage=entryDecalageSaisie.get()
    clef=entryClefSaisie.get()
    if len(texte)>=300:
        strTexteResultat.set("Le texte ne doit pas contenir plus de 300 caractères")
    elif selectedAction.get() == "Chiffrer ROT13":
            strTexteResultat.set(ChiffrerROT13(texte))
    elif selectedAction.get() == "Déchiffrer ROT13":
        strTexteResultat.set(deChiffrerROT13(texte))
    elif selectedAction.get() == "Chiffrer César":
        strTexteResultat.set(ChiffrerCesar(texte,int(decalage)))
    elif selectedAction.get() == "Déchiffrer César":
        strTexteResultat.set(deChiffrerCesar(texte,int(decalage)))
    if len(clef)>=50:
        strTexteResultat.set("La clef ne doit pas contenir plus de 50 caractères")
    elif selectedAction.get() == "Chiffrer Vigenere":
        strTexteResultat.set(ChiffrerVigenere(texte,clef))
    elif selectedAction.get() == "Déchiffrer Vigenere":
        strTexteResultat.set(deChiffrerVigenere(texte,clef))
    return
     

###############################
# PARTIE 3 : Construction de l'interface
###############################

#définition des dimensions de notre interface
fenetre = tk.Tk()
fenetre.title("Clé de chiffrement/déchiffrement")
fenetre.geometry('600x200+600+200')

#etiquette de la zone de saisie (label)
lblTexteSaisi=tk.Label(text="Message à chiffrer ou déchiffrer")
lblTexteSaisi.grid(row=3, column=0)
#Nom de la variable contenant le texte de la zone de saisie
strTexteSaisi=tk.StringVar()
entryTexteSaisi = tk.Entry(fenetre,width = 40,textvariable=strTexteSaisi)
entryTexteSaisi.grid(row=3, column=1)


#etiquette de la zone de saisie decalage(label)
lblTexteSaisi=tk.Label(text="decalage")
lblTexteSaisi.grid(row=5, column=0)
#définition variable decalage
strDecalageSaisie=tk.StringVar()
entryDecalageSaisie = tk.Entry(fenetre,width = 20,textvariable=strDecalageSaisie)
entryDecalageSaisie.grid(row=5, column=1)


#etiquette de la zone de saisie clef(label)
lblTexteSaisi=tk.Label(text="clef")
lblTexteSaisi.grid(row=7, column=0)
#définition variable clefSaisie
strClefSaisie=tk.StringVar()
entryClefSaisie = tk.Entry(fenetre,width = 20,textvariable=strClefSaisie)
entryClefSaisie.grid(row=7, column=1)


#étiquette et nom de la variable message chiffré ou déchiffré
lblTexteResultat=tk.Label(text="Message chiffré ou déchiffré")
lblTexteResultat.grid(row=10, column=0)
strTexteResultat=tk.StringVar()
entryTexteResultat = tk.Entry(fenetre,width = 40,textvariable=strTexteResultat)
entryTexteResultat.grid(row=10, column=1)    


#--combobox, liste déroulante des différents codages
selectedAction = tk.StringVar()
ActionList = ttk.Combobox(fenetre, textvariable=selectedAction)
ActionList['values']=["Chiffrer ROT13","Déchiffrer ROT13","Chiffrer César","Déchiffrer César","Chiffrer Vigenere","Déchiffrer Vigenere"] 
ActionList.grid(row=1,column=1)
ActionList.current(0)   


#--Boutton Action
bouton=tk.Button(fenetre, text="Action!",command=boutonAction)
#command est le lanceur de la fonction boutonAction
bouton.config(height = 1, width = 10)
bouton.grid(row=8, column=1)    

fenetre.mainloop()


###############################
# PARTIE 4 : Tests
###############################

#test de mettreEnMaj
print("mettreEnMaj, doit retourner BONJOUR : ",mettreEnMaj("bonjour"))
print("mettreEnMaj, doit retourner BONJOUR : ",mettreEnMaj("bonJoUr"))
print("mettreEnMaj, doit retourner BON.JOUR : ",mettreEnMaj("bon.JoUr"))

#Test de convertirlistASCII
print("doit retourner [65, 65, 65] : ",convertirListeASCII("AAA"))
print("doit retourner [65, 97, 65] : ",convertirListeASCII("AaA"))

#Test de rot13
print("rot13, doit retourner 78 : ",rot13(65))

#Test rotCesar
print("rotCesar, doit retourner 78: ",rotCesar(65,13))

#Test genererTabCodesTranslates
print("genererTabCodesTranslates, doit retourner [33, 34, 35]: ",genererTabCodesTranslates("ABC"))        
print("genererTabCodesTranslates, doit retourner [45, 79, 73, 0, 74, 69, 0, 70, 65, 73, 83, 0, 68, 69, 0, 76, 7, 73, 78, 70, 79, 0, 1]: ",genererTabCodesTranslates("Moi je fais de l'info !"))
print("genererTabCodesTranslates, doit retourner [18, 33, 0, 53, 37, 63, 41, 46, 38, 47, 18, 33, 0, 53, 37, 63, 41, 46, 38, 47, 18, 33, 0]: ",genererTabCodesTranslates(genererPhraseClef("2A UE_INFO",len("Moi je fais de l'info !"))))

#Test chiffrement ROT13
print("deChiffrerROT13: ",deChiffrerROT13("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

#Test chiffrement Cesar
print("ChiffrerCesar: ",ChiffrerCesar("ABCDEFGHIJKLMNOPQRSTUVWXYZ",13))
print("deChiffrerCesar: ",deChiffrerCesar("NOPQRSTUVWXYZABCDEFGHIJKLM",13))

#Test chiffrement Vigenere
print("ChiffrerVigenere: ",ChiffrerVigenere("Moi, je fais de l'info !","2A UE_INFO"))

#tests deChiffrement Vigenere:
print("Déchiffrer Vigenere: ",deChiffrerVigenere("_1iaEJ/N-1{5 :+_6U0>x1 V","2A UE_INFO"))