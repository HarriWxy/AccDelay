




import socket
import json



if __name__ == "__main__":





    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("127.0.0.1", 5555)


    client_socket.connect(server_address)

    while True:
        try:
            # send results
            msg_to_server = input("-> send to snk server:")

            # cmd1: set time
            if msg_to_server =='set time 1':
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
            else:
                print('-> rcvd msg failed')

            # compute




        finally:
            pass

    print('-> client close')
    client_socket.close()






