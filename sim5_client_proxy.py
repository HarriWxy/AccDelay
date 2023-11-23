import socket
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import numpy as np
from collections import deque

def init_figure():
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 80)

def update_figure(step):
    global time_count
    if len(x) < num:
        x.append(step)
    y.append(time_count)
    if time_count > 0:
        time_count -= 1
    mean.append(lat_sum/lat_count)
    line.set_data(x, list(y))
    line2.set_data(x,list(mean))
    return line

def com_with_server():
    """
    This function establishes communication with a server and sends/receives messages.
    Multi-Thread for communication with server, then main thread for plotting.
    """
    global lat_sum,lat_count,time_count
    while True:
        try:
            # send results
            msg_to_server = input("-> send to snk server:")
            if msg_to_server == '': 
                'send test for latency'
                # tmp_cmd2 = {
                #     "do":"get",
                #     "arg":"access",
                #     "value":["SAT-00001","SAT-00002"]
                # }
                # msg = json.dumps(tmp_cmd2)
                # client_socket.sendall(msg.encode())
                # time.sleep(0.02) # wait for server
                tmp_cmd2 = {
                    "do":"get",
                    "arg":"access",
                    "value":"*"
                }
                msg = json.dumps(tmp_cmd2)
                client_socket.sendall(msg.encode())
                print("-> msg to server: {} ".format('my send message'))

            # cmd1: set time
            elif msg_to_server =='set time 1':
                time_stamp="2000-01-01T00:10:00Z"
                tmp_cmd2 = {
                    "id": 0,
                    "do": "set",
                    "arg": "time",
                }
                tmp_cmd2['value'] = time_stamp
                msg = json.dumps(tmp_cmd2)

                client_socket.sendall(msg.encode())

                print("-> msg to server: {} ".format(time_stamp))
            elif msg_to_server =='set time 2':
                time_stamp = "2000-01-01T00:04:23Z"
                tmp_cmd2 = {
                    "id": 0,
                    "do": "set",
                    "arg": "time",
                }
                tmp_cmd2['value'] = time_stamp
                msg = json.dumps(tmp_cmd2)

                client_socket.sendall(msg.encode())

                print("-> msg to server: {} ".format(time_stamp))
            # cmd2: get route
            elif msg_to_server=='get route 1':
                tmp_cmd2 = {
                    "id": 0,
                    "do": "get",
                    "arg": "route",
                }
                tmp_cmd2['value'] = ("SAT-00000","SAT-00007")
                msg = json.dumps(tmp_cmd2)
                client_socket.sendall(msg.encode())

                print("-> msg to server: get route")
            elif msg_to_server == 'get route 2':
                tmp_cmd2 = {
                    "id": 0,
                    "do": "get",
                    "arg": "route",
                }
                tmp_cmd2['value'] = ("SAT-00003", "SAT-00107")
                msg = json.dumps(tmp_cmd2)
                client_socket.sendall(msg.encode())

                print("-> msg to server: get route")
            # cmd3: stop connection
            elif msg_to_server == 'set procedure stop':
                tmp_cmd2 = {
                    "id": 0,
                    "do": "set",
                    "arg": "procedure",
                    "value":"stop"

                }
                msg = json.dumps(tmp_cmd2)
                client_socket.sendall(msg.encode())

                print("-> msg to server: {} ".format('set stop'))
                break
            else:
                print('wrong cmd, retype')
                continue


            # rcv msg
            print("-> waiting msg from server...")
            msg_from_server = client_socket.recv(1024)
            msg_from_server = json.loads(msg_from_server.decode())
            if isinstance(msg_from_server,dict):
                print('-> client rcvd: {} '.format(msg_from_server))
                data = msg_from_server['data']
                acc_latency = int(data['access_latency'])
                print('-> access latency: {} '.format(acc_latency))
                lat_sum += acc_latency
                lat_count += 1
                time_count = acc_latency
                # plt.show()
            else:
                print('-> rcvd msg failed')

            # compute

        finally:
            pass
    print('-> client close')
    client_socket.close()



if __name__ == "__main__":
    # connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1", 5555)
    client_socket.connect(server_address)

    t1 = Thread(target=com_with_server)
    # counter
    lat_sum = 0
    lat_count = 1e-6
    # plt figure
    fig = plt.figure()
    ax = plt.subplot()
    
    num = 1000
    time_count = 0
    x, y, mean = [], deque(maxlen=num), deque(maxlen=num)
    line, = plt.plot([], [], 'b-') 
    line2, = plt.plot([], [], 'r-') 
    t1.start()
    ani = FuncAnimation(fig,update_figure,init_func=init_figure,frames=num,interval=1)
    plt.show()
    t1.join()
    
   






