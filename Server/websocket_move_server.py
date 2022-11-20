from websocket_server import WebsocketServer
import logging
import base64
import threading
import configparser
import logging

class Websocket_Server():

    def __init__(self, host, port):
        self.server = WebsocketServer(port, host=host)

        self.connection_server_to_raspberrypi = {

            "TEST":None, # Global Server IP スマホとかで見たときに格納
            "SAMP":None
        }
        

    # クライアント接続時に呼ばれる関数
    def new_client(self, client, server):
        print("OK")


    # クライアント切断時に呼ばれる関数
    def client_left(self, client, server):

        # 辞書型のKeyのみを取り出す
        def get_keys_from_value(d, val):
            key = [k for k, v in d.items() if v == val][0]
            return str(key)

        # Client情報に送られてきたデータの送信先があれば実行
        if client in self.connection_server_to_raspberrypi.values():
            key = get_keys_from_value(self.connection_server_to_raspberrypi,client)
            with open(f"/Library/WebServer/Documents/Web2/{key}.txt","w") as f:
                f.write("STOP")

            with open(f"{path}Data/{key}_move.txt", "w") as f:
                    f.write("")


    # クライアントからメッセージを受信したときに呼ばれる関数
    def message_received(self, client, server, message):

        # print("client({}) said: {}".format(client['id'], message))

                # 辞書型のKeyのみを取り出す
        def get_keys_from_value(d, val):
            key = [k for k, v in d.items() if v == val][0]
            return str(key)

        if message in self.connection_server_to_raspberrypi.keys():
            self.connection_server_to_raspberrypi[message] = client
            with open(f"/Library/WebServer/Documents/Web2/{message}.txt","w") as f:
                f.write("START")

        else:
            
            data = base64.b64decode(message).decode()
            print(data)

            if data == "wake_up_move":
                # Client情報に送られてきたデータの送信先があれば、そこへ送信
                if client in self.connection_server_to_raspberrypi.values():
                    key = get_keys_from_value(self.connection_server_to_raspberrypi,client)
                    # 各ユーザーのデバイスへ移動データを選別
                    need_data = key[0:4]
                    with open(f"/Library/WebServer/Documents/Web2/{need_data}.txt","w") as f:
                        f.write("RESTART")
                        

            else:             
                # Client情報に送られてきたデータの送信先があれば、そこへ送信
                if client in self.connection_server_to_raspberrypi.values():
                    key = get_keys_from_value(self.connection_server_to_raspberrypi,client)
                    # 各ユーザーのデバイスへ移動データを選別
                    need_data = key[0:4]
                    with open(f"{path}Data/{need_data}_move.txt", "w") as f:
                        f.write(data)
                        # print(data)

                
    
    # サーバーを起動する
    def run(self):
        # クライアント接続時のコールバック関数にself.new_client関数をセット
        self.server.set_fn_new_client(self.new_client)
        # クライアント切断時のコールバック関数にself.client_left関数をセット
        self.server.set_fn_client_left(self.client_left)
    # メッセージ受信時のコールバック関数にself.message_received関数をセット
        self.server.set_fn_message_received(self.message_received) 
        self.server.run_forever()


if __name__ == "__main__":

    path = "./"

    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read(f'{path}connection.ini', 'UTF-8')

    SERVER_IP = config.get('server', 'ip')
    SERVER_PORT = int(config.get('server', 'move_port'))

    ws_server = Websocket_Server(SERVER_IP, SERVER_PORT)
    ws_server.run()