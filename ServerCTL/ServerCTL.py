from flask import Flask, jsonify,request
from os import path
import yaml, time, os
from kubernetes import client, config, utils
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException

#### Kubernetes Functions ####
def deploymentName(DeploymentName):

    deploy = ["apiVersion: apps/v1\n","kind: Deployment\n","metadata:\n","  name: ",DeploymentName,"\n","  labels:\n","    app: ",DeploymentName,"\n","spec:\n",
    "  replicas: 1\n","  selector:\n","    matchLabels:\n","      app: ",DeploymentName,"\n","  template:\n","    metadata:\n","      labels:\n","        app: ",DeploymentName,"\n",
    "    spec:\n","      containers:\n","      - name: ",DeploymentName,"\n","        image: docker.io/rsdias/fapesp:remotedist\n","        imagePullPolicy: Always\n",
    "        ports:\n","        - containerPort: 8081\n","        - containerPort: 2010\n",
    ]

    service = ["apiVersion: v1\n","kind: Service\n","metadata:\n","  name: ",DeploymentName,"\n","spec:\n","  ports:\n","  - port: 8081\n","    name: tcp1\n",
    "    targetPort: 8081\n","  - port : 2010\n","    name: tcp2\n","    targetPort: 2010\n","  selector:\n","    app: ",DeploymentName,"\n","  type: ClusterIP\n"
    ]
    
    file1 = open('%s.yaml' %(DeploymentName), "x")
    file1.writelines(deploy)
    file1.close()
    file2 = open('%s-service.yaml' %(DeploymentName), "x")
    file2.writelines(service)
    file2.close()

def podName(DeployName):
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if ( i.metadata.name.startswith(DeployName)):
             return i.metadata.name

def deletePod(pod):
    configuration = client.Configuration()

    with client.ApiClient(configuration) as api_client:
        api_instance = client.CoreV1Api(api_client)
    
        namespace = 'default' 
        name = pod # str | Pod name, e.g. via api_instance.list_namespaced_pod(namespace)
        
        try:
            api_response = api_instance.delete_namespaced_pod(name, namespace)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

def create_service(Deployname):
    core_v1_api = client.CoreV1Api()
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="%s-service" % Deployname
        ),
        spec=client.V1ServiceSpec(
            selector={"app": Deployname},
            ports=[client.V1ServicePort(
                name='tcp1',
                port=8081,
                target_port=8081),
            
            client.V1ServicePort( 
                name='tcp2',
                port=2010,
                target_port=2010
            )]
        )
    )
    #Creation of the deployment on namespace default
    core_v1_api.create_namespaced_service(namespace="default", body=body)
    

def getClusterIP(Deployname):    
    core_v1_api = client.CoreV1Api()
    service = core_v1_api.read_namespaced_service(name="%s-service" % Deployname, namespace="default")
    return service.spec.cluster_ip

def verifyStatus(pod_name):
    core_v1 = core_v1_api.CoreV1Api()
    api_response = core_v1.read_namespaced_pod(name=pod_name,namespace="default")
    return api_response.status.phase

def createDeployment(name):
    deploymentName(name)
    api_instance = core_v1_api.CoreV1Api()
    with open(path.join(path.dirname(__file__),'%s.yaml' %name)) as f:
            dep = yaml.safe_load(f)
            k8s_apps_v1 = client.AppsV1Api()
            resp = k8s_apps_v1.create_namespaced_deployment(body=dep,namespace="default")
            print("Deployment created. Deployment Name = '%s'" % resp.metadata.name)
    os.remove('%s.yaml' %name)
    k8sClient = client.ApiClient()
    utils.create_from_yaml(k8sClient, "%s-service.yaml" %name)
    os.remove('%s-service.yaml' %name)
    pod_name = podName(name)
    Status = verifyStatus(pod_name)
    while Status != "Running":
        Status = verifyStatus(pod_name)
        if ( Status == "Running"):
            print("Pod Created and Running")

    print("Podname : ",pod_name, "Status : ",Status)




app = Flask(__name__)
names = [
    {
        'id': 1,
        'name': u'serverctl-service',
        'creator' : u'serverctl'
    }
]
inicio = 0
total = 0
deployquantity = 0

@app.route('/names/mr', methods=['GET'])
def get_amount_mr():
    count = 0
    for x in names:
        print(x)
        if ( x['creator'] == "MR" or x['creator'] == "mr"):
            count = count + 1 
    return str(count)

@app.route('/names/mrr', methods=['GET'])
def get_amount_mrr():
    count = 0
    for y in names:
        print(y)
        if (y['creator'] == "MRR" or y['creator'] == "mrr"):
            count = count + 1
    return str(count)

@app.route('/names/hd', methods=['GET'])
def get_amount_hd():
    count = 0
    for y in names:
        print(y)
        if (y['creator'] == "HD" or y['creator'] == "hd"):
            count = count + 1
    return str(count)

@app.route('/names/hdr', methods=['GET'])
def get_amount_hdr():
    count = 0
    for y in names:
        print(y)
        if (y['creator'] == "HDR" or y['creator'] == "hdr"):
            count = count + 1
    return str(count)



@app.route('/names', methods=['POST'])
def createService():
    if not request.json or not 'name' in request.json:
        abort(400)
    name = {
        'id': names[-1]['id'] + 1,
        'name': request.json['name'],
    }
    names.append(name)
    servicename = request.json['name']
    finalname = servicename.lower()
    createDeployment(finalname)
    return jsonify({'name': name}), 201

@app.route('/names/many' , methods=['POST'])
def createPods():
    if not request.json or not 'name' in request.json:
        abort(400)
    
    quantity = request.json['quantity']
    name = request.json['name']
    global inicio
    global total
    global deployquantity
    for x in range(quantity):
        deployname = name+str(x)
        finalname = deployname.lower()
        createDeployment(finalname)
        #print(finalname)
        newname = {
        'id': names[-1]['id'] + 1,
        'name': finalname,
        'creator' : name
        }
        names.append(newname)
        total = total + 1
    inicio = inicio + quantity
    deployquantity = quantity  
    return jsonify({'name' : name}),201


if __name__ == '__main__':
    #config.load_kube_config()           #Local
    config.load_incluster_config()       #Inside CLuster
    app.run(host="0.0.0.0",port=5000)
