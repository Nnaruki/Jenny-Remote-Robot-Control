import socket
import configparser
import logging



# 辞書型のKeyのみを取り出す
def get_keys_from_value(d, val):
    key = [k for k, v in d.items() if v == val][0]
    return str(key)

if __name__ == '__main__':

    path = "./"

    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read(f'{path}connection.ini', 'UTF-8')

    # Connection Settings
    SERVER_IP = config.get('server', 'ip')
    SERVER_PORT = int(config.get('server', 'udp_picture_port'))

    # Image Settings
    IMAGE_WIDTH = int(config.get('packet', 'image_width'))
    IMAGE_HEIGHT = int(config.get('packet', 'image_height'))
    IMAGE_SIZE = IMAGE_WIDTH * IMAGE_HEIGHT // 2
    logging.info(" IMAGE SIZE: " + str(IMAGE_SIZE))


    member_list = {

        "TEST":None,
        "SAMP":None
        
        }

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        logging.info(" Binding port on: " + SERVER_IP + ":" + str(SERVER_PORT))

        judge_data = None

        while True:
            data, addr = s.recvfrom(IMAGE_SIZE)
            if len(data)<100:
                judge_data = data.decode()[1:5]
                print(judge_data)

            if judge_data in member_list.keys():
                member_list[judge_data] = addr
                # print(member_list)
            else:
                pass

            if addr in member_list.values():
                judge = get_keys_from_value(member_list, addr)
                with open(f"{path}Data/{judge}.jpeg", mode="wb") as f:
                    f.write(data)
        
        
            # print(addr, data)