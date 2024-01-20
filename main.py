"LINUX"
import re
import subprocess
import optparse

def recherche_adresse_mac(chaine):
    correspondance = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', str(chaine))
    if correspondance:
        return correspondance.group(0)
    else:
        print("[-] Aucune adresse MAC trouvée.")
        return None

def obtenir_arguments():
    parseur = optparse.OptionParser()
    parseur.add_option("-i", "--interface", dest="interface", help="Interface à laquelle changer son adresse MAC")
    parseur.add_option("-m", "--mac", dest="nouvelle_adresse_mac", help="Nouvelle adresse MAC")
    (options, arguments) = parseur.parse_args()
    if not options.interface:
        parseur.error("[-] Veuillez spécifier une interface, utilisez --help pour plus d'informations")
    elif not options.nouvelle_adresse_mac:
        parseur.error("[-] Veuillez spécifier une adresse MAC, utilisez --help pour plus d'informations")
    return options

def definir_nouvelle_adresse_mac(interface, nouvelle_adresse_mac):
    print(f"[+] Changement d'adresse MAC de {interface} à {nouvelle_adresse_mac}")
    subprocess.call(f"ifconfig {interface} down", shell=True)
    subprocess.call(f"ifconfig {interface} hw ether {nouvelle_adresse_mac}", shell=True)
    subprocess.call(f"ifconfig {interface} up", shell=True)

def obtenir_adresse_mac_depuis_interface(interface):
    resultat_ifconfig = subprocess.check_output(["ifconfig", interface])
    resultat_recherche_adresse_mac = recherche_adresse_mac(resultat_ifconfig)
    if resultat_recherche_adresse_mac:
        return resultat_recherche_adresse_mac
    else:
        print("[-] Impossible de lire l'adresse MAC.")

options = obtenir_arguments()
adresse_mac_actuelle = obtenir_adresse_mac_depuis_interface(options.interface)
print("L'adresse MAC actuelle pour l'interface "+options.interface + " est : "+adresse_mac_actuelle)

definir_nouvelle_adresse_mac(options.interface, options.nouvelle_adresse_mac)
nouvelle_adresse_mac = obtenir_adresse_mac_depuis_interface(options.interface)
