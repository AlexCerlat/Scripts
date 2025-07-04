import paramiko
import time 
from concurrent.futures import ThreadPoolExecutor

# Definiți lista de adrese IP la care doriți să vă conectați
ip_list = []

# Funcție pentru adăugarea unei adrese IP în listă
def adauga_ip_list():
    try:
        ip = input("Introduceți o adresă IP: ")  # Citim adresa IP de la utilizator
        ip_list.append(ip)  # Adăugăm adresa IP în listă
        print(f"Adresa IP {ip} a fost adăugată în listă.")
    except ValueError:
        print("Introduceți o adresă IP validă.")
# Folosiți funcția pentru a adăuga adrese IP în listă
while True:
    adauga_ip_list()
    continua = input("Doriți să adăugați altă adresă IP? (Da/Nu): ")
    if continua.lower() == "nu":
        break

# Definiți numele de utilizator și parola SSH
username = "admin"
password = "Jupiterus()"

# Definiți comenzile pe care doriți să le executați
comenzi = [
    "copy running-config tftp:",
    "192.168.211.67",
    " "
    ]
# Funcție pentru înlocuirea VLAN-ului în lista de comenzi
#def inlocuieste_vlan(vlan):
    #for i in range(len(comenzi)):
        #comenzi[i] = comenzi[i].replace("none", str(vlan))

# Solicită utilizatorului să introducă un număr de VLAN
#try:
    #vlan = int(input("Introduceți un număr de VLAN pentru adaugare: "))
    #inlocuieste_vlan(vlan)
    #print(f"VLAN-ul {vlan} a fost adăugat în lista de comenzi.")
#except ValueError:
    #print("Introduceți un număr de VLAN valid.")

def connect_to_switch(ip, username, password):
    try:
        # Creează o conexiune SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, username=username, password=password)

        # Deschide un canal SSH
        ssh_channel = ssh_client.invoke_shell()

        print(f"Conectat la {ip} prin SSH.")

        # Execută comenzile pe dispozitiv
        for x in comenzi:
            ssh_channel.send(x + "\n")
            time.sleep(1)
            
            
            
            
            
              # Adăugați o pauză de 1 secundă între comenzi
            output = " "
            print(x)
            while not output.endswith(" "):
                output += ssh_channel.recv(1024).decode('utf-8')
            print(output)

        # Închideți conexiunea SSH
        ssh_client.close()
        print(f"Deconectat de la {ip}")

    except Exception as e:
        print(f"Eroare la conectarea la {ip}: {str(e)}")

def execute_ssh_connections():
    # Folosirea ThreadPoolExecutor pentru a executa mai multe conexiuni în mod concomitent
    with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
        results = [executor.submit(connect_to_switch, ip, username, password) for ip in ip_list]

execute_ssh_connections()