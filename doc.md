# Spuštění serveru
Potřebná verze pythonu: alespoň Python 3.9
Potřebné moduly pro python: mysql-connector-python
Konfigurační soubor serveru se nachází ve složce config s názvem server.ini
    - server/ip: ip adresa, na které bude server naslouchat
    - server/port: port, na kterém bude server naslochat
    - server/timeout: timeout pro přijímání klientů
    - database/ip: ip adresa databáze
    - database/user: uživatel, pod kterým bude server přistupovat do databáze
    - database/password: heslo pro připojení do databáze
    - database/db_name: název databáze kterou server používá
Server lze spustit příkazem: python server.py

# Spuštění klienta
Potřebná verze pythonu: alespoň Python 3.9
Potřebné moduly pro python: PyQt6
Konfigurační soubor serveru se nachází ve složce config s názvem client.ini
    - server/ip: ip adresa serveru, na který se klient připojí
    - server/port: port, na kterém je spuštěn server 
Server lze spustit příkazem: python client.py