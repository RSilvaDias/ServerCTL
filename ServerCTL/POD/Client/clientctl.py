
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to CTL server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://ctl:5555")  # CTL pod ClusterIP

print("Name of deploy : ")
name = input()
print("Sending request…")
socket.send(name.encode())


message = socket.recv()
print(f"Received reply [ {message} ]")
