# ServerCTL

First draft of the ServerCTL script to integrate the middleware Distributor.
Basic funcionalities include:
  - Create a deployment on Kubernetes
  - Verify status of pod
  - Expose service to generate a cluster_IP

For the program to run on a Pod inside a Cluster, certain authorization is required by k8s.
The file naive.yaml gives us the RABC authorization so our serverCTL can perform the desired tasks within our cluster.

As for now, to give this authorizations , simple run Kubectl apply -f naive.yaml

A aditional version of the script is inside the POD folder. It's a very early draft of communication between a Python client and our ServerCTL using the ZMQ library,
for the purpose of testing pod to pod comunication.
