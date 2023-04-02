import aminoli as aminofix
from os import path
import json
from time import sleep
from pyfiglet import figlet_format
from colored import fore, style
import datetime
import pytz

print(
    f"""{fore.CADET_BLUE_1 + style.BOLD}
    Check in
Script by Lucas Day
Github : https://github.com/LucasAlgerDay"""
)
print(figlet_format("Check in", font="fourtops"))

def tzc() -> int:
    tz = dict(zip(("GMT" if i==0 else f'{"+"if i>0 else "-"}{"0"if -10<i<10 else ""}{i*-1 if i<0 else i}' for i in range(-12,12)),(i*60 for i in range(-12,12))))
    zones = ['Etc/GMT-11','Etc/GMT-10','Etc/GMT-9','Etc/GMT-8','Etc/GMT-7','Etc/GMT-6','Etc/GMT-5','Etc/GMT-4','Etc/GMT-3','Etc/GMT-2','Etc/GMT-1','Etc/GMT0','Etc/GMT+1','Etc/GMT+2','Etc/GMT+3','Etc/GMT+4','Etc/GMT+5','Etc/GMT+6','Etc/GMT+7','Etc/GMT+8','Etc/GMT+9','Etc/GMT+10','Etc/GMT+11','Etc/GMT+12']
    for _ in zones:
        H = datetime.datetime.now(pytz.timezone(_)).strftime("%H")
        Z = datetime.datetime.now(pytz.timezone(_)).strftime("%Z")
        if H=="23": break
    timezone = tz.get(Z)
    return timezone

THIS_FOLDER=path.dirname(path.abspath(__file__))
emailfile=path.join(THIS_FOLDER,'accounts.json')
dictlist=[]
chatlink = input("Comunidad (link): ")
cooldown = int(input("Cooldown por cuenta: "))
with open(emailfile)as f:dictlist=json.load(f)


print(f"{len(dictlist)} cuentas cargadas")

for acc in dictlist:
    email = acc['email']
    password =  acc['password']
    device = acc['device']
    client = aminofix.Client(deviceId = device)
    try:
        client.login(email=email, password=password)
        chat_info = client.get_from_code(chatlink)
        chat_id = chat_info.objectId
        community_id = chat_info.path[1:chat_info.path.index('/')]
        client.join_community(community_id)
        sub_client = aminofix.SubClient(comId=community_id, profile=client.profile)
        sub_client.check_in(tzc())
        client.leave_community(community_id)
        print(f"{email} checked, esperando {cooldown} para la siguiente cuenta")
        sleep(cooldown)
    except Exception as e:
        print(f"Error en la siguiente cuenta {email}: {e} \n\n\n Esperando {cooldown} para la siguiente cuenta.")
        sleep(cooldown)
        pass
