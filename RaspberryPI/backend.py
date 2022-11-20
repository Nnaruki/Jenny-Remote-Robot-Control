import requests
import subprocess
import time

def judge_http():

    judge = None
    judge_past = None

    while True:

        try:
            recv = requests.get(url,timeout=(3.0,3.0)).content.decode("utf-8") #get file from server(HTTP)
            judge = recv
            if judge != judge_past:
                if recv == "START":
                    # print("START") 
                    subprocess.Popen("sudo systemctl start picture.service",shell=True) #wakepu camera

                elif recv == "STOP":
                    # print("STOP")
                    subprocess.Popen("sudo systemctl stop picture.service",shell=True)  #sleep down camera

                elif recv == "RESTART":
                    subprocess.Popen("sudo systemctl restart move.service",shell=True)  #sleep down camera

        except Exception as e:
            print(e)
            time.sleep(10) #interval of scanning(too short time may cause waste of pacckets)
            
        finally:
            judge_past = judge
            time.sleep(10)

if __name__ == '__main__':

    url=f"http://192.168.0.35/Web2/TEST.txt"
    judge_http()
