import json
import socket
import random

def ex_instruction(ip,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip, port)
    server_socket.bind(server_address)

    server_socket.listen(1)
    print('-> snk_server-exInstruction is waiting proxy access...')

    client_socket, client_address = server_socket.accept()

    while True:
        try:
            # rcv msg from client
            print("-> waiting for client...")
            msg_from_client = client_socket.recv(1024).decode()
            cmd = json.loads(msg_from_client)
            # assert
            if not isinstance(cmd,dict):
                print("-> wrong cmd")
                msg_to_client = {
                    "do":"nack"
                }
                msg_to_client = json.dumps(msg_to_client)
                client_socket.send(msg_to_client.encode())
                continue
            # rcvd cmd1 set time
            if cmd['do'] =='set' and cmd['arg'] =='time':
                print("-> rcvd set time")
                time_stamp= cmd['value']
                set_time(time_stamp)


                #response ack
                msg_to_client = {
                    "do":"ack",
                    "value":"set time"
                }
                msg_to_client = json.dumps(msg_to_client)
                client_socket.sendall(msg_to_client.encode())

            #rcvd cmd2 get route
            elif cmd['do'] =='get' and cmd['arg']== 'access':
                print("-> rcvd get access")
                latency = get_access_latency(cmd['value'])


                # response ack get route
                msg_to_client = {
                    "do": "post",
                }
                data={}
                data['access_latency'] = latency
                msg_to_client['data'] = data
                msg_to_client = json.dumps(msg_to_client)
                client_socket.sendall(msg_to_client.encode())

                # rcvd cmd2 get route
            elif cmd['do'] == 'get' and cmd['arg'] == 'route':
                print("-> rcvd get routes")
                src = cmd['value'][0]
                dst = cmd['value'][1]
                path, latency = get_route_latency(src, dst)

                # response ack get route
                msg_to_client = {
                    "do": "post",
                }
                data = {}
                data['path'] = path
                data['latency'] = latency
                msg_to_client['data'] = data
                msg_to_client = json.dumps(msg_to_client)
                client_socket.sendall(msg_to_client.encode())

            #rcvd cmd3 set procedure stop
            elif cmd['do'] =='set' and cmd['arg']== 'procedure' and  cmd['value']== 'stop':
                #response stop
                msg_to_client = {
                    "do": "ack",
                    "value": "set procedure stop"
                }
                msg_to_client = json.dumps(msg_to_client)
                client_socket.sendall(msg_to_client.encode())
                client_socket.close()
                print("-> proxy socket disconnected")
                break

            else:
                print("-> wrong cmd")
                msg_to_client = {
                    "do":"nack"
                }
                msg_to_client = json.dumps(msg_to_client)
                client_socket.sendall(msg_to_client.encode())
                continue
        except:
            # clinet disconnected
            # wait for new connection
            client_socket, client_address = server_socket.accept()
        finally:
            pass
    return


def set_time(time_stamp):
    print("-> set time as {}".format(time_stamp))
    # TODO set time
    return

def get_route_latency(src,dst):
    # TODO get route latency
    ret_path = ["SAT-00001","SAT-00002","SAT-00003","SAT-00004","SAT-00005","SAT-00006","SAT-00007"]
    ret_latency=45.67
    return ret_path,ret_latency

def get_access_latency(src_dst):
    if isinstance(src_dst,tuple):
        return 16.78  # ms
    elif src_dst=="*":
        # return random latency
        return random.choice([20,30,40,50,60,70,80,10,33,20,10,20,40,50,60,70,10,20,30])

if __name__ == "__main__":
    ex_instruction("127.0.0.1",5555)


