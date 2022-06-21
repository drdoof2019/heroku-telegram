
import configparser
import os, sys
import platform
re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
def banner():
	print(f"""
	{re}╔═╗{cy}┌─┐┌┬┐┬ ┬┌─┐
	{re}╚═╗{cy}├┤  │ │ │├─┘
	{re}╚═╝{cy}└─┘ ┴ └─┘┴

	Version : 1.00
        Developed with <3
	""")

print(platform.system())
if platform.system() == 'Windows':
    os.system('cls')
    banner()
    print(gr+"[+] Installing requierments ...")
    os.system('python -m pip install -r requirements.txt')
    #os.system('pip3 install telethon')
    os.system('cls')
    banner()
    os.system("type nul >> config.data")
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    fiyat_oran = input(gr+"[+] Fiyat Oranı Girin (Örneğin %0.5 için: 0.5) : "+re)
    cpass.set('cred', 'fiyat_oran', fiyat_oran)
    volume_oran = input(gr+"[+] Volume Oranı Girin (Örneğin %1 için: 1) : "+re)
    cpass.set('cred', 'volume_oran', volume_oran)
    bekleme_suresi = input(gr+"[+] Bekleme Süresi Girin (Örneğin 4 saniye için: 4) : "+re)
    cpass.set('cred', 'bekleme_suresi', bekleme_suresi)
    silme_suresi = input(gr+"[+] Tespitinin üzerinden kaç dakika geçince hafızadan silsin? (Örneğin 15 dakika için: 15) : "+re)
    cpass.set('cred', 'silme_suresi', silme_suresi)
    tespit_sayisi = input(gr+"[+] Kaç kere tespit edilirse paylaşılacağını girin (Örneğin 3 kere ard arda tespit için: 3) : "+re)
    cpass.set('cred', 'tespit_sayisi', tespit_sayisi)
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    os.system('cls')
    print(gr+"[+] setup complete !")
elif platform.system() == 'Linux':
    os.system('clear')
    banner()
    print(gr+"[+] Installing requierments ...")
    os.system('python3 -m pip install -r requirements.txt')
    os.system('clear')
    banner()
    os.system("touch config.data")
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    fiyat_oran = input(gr+"[+] Fiyat Oranı Girin (Örneğin %0.5 için: 0.5) : "+re)
    cpass.set('cred', 'fiyat_oran', fiyat_oran)
    volume_oran = input(gr+"[+] Volume Oranı Girin (Örneğin %1 için: 1) : "+re)
    cpass.set('cred', 'volume_oran', volume_oran)
    bekleme_suresi = input(gr+"[+] Bekleme Süresi Girin (Örneğin 4 saniye için: 4) : "+re)
    cpass.set('cred', 'bekleme_suresi', bekleme_suresi)
    silme_suresi = input(gr+"[+] Tespitinin üzerinden kaç dakika geçince hafızadan silsin? (Örneğin 15 dakika için: 15) : "+re)
    cpass.set('cred', 'silme_suresi', silme_suresi)
    tespit_sayisi = input(gr+"[+] Kaç kere tespit edilirse paylaşılacağını girin (Örneğin 3 kere ard arda tespit için: 3) : "+re)
    cpass.set('cred', 'tespit_sayisi', tespit_sayisi)
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    os.system('clear')
    print(gr+"[+] setup complete !")
