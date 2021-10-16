from os import path
import yaml
import time
import os
from kubernetes import client, config
from kubernetes.client.api import core_v1_api

#Name of the deployment needs to be lowercase!!
def DeploymentName():
    DeploymentName = input("Deployment name: ").strip()
    f = open('%s.yaml' %(DeploymentName), "x")

    data = {'apiVersion': 'apps/v1', 'kind': 'Deployment', 'metadata': {'name': DeploymentName,'labels': {'app': 'nginx'}}, 'spec':
            {'replicas': 1, 'selector': {'matchLabels': {'app': 'nginx'}}, 'template': {'metadata': {'labels': {'app': 'nginx'}},
             'spec': {'containers': [{'name': 'nginx', 'image': 'nginx:1.15.4', 'ports': [{'containerPort': 80}]}]}}}}
    with open('%s.yaml' %(DeploymentName), "w") as file:
        documents = yaml.dump(data, file)
    return DeploymentName

def PodName(DeployName):
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        if ( i.metadata.name.startswith(DeployName)):
             return i.metadata.name

def create_service(Deployname):
    core_v1_api = client.CoreV1Api()
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="%s-service" % Deployname
        ),
        spec=client.V1ServiceSpec(
            selector={"app": 'nginx'},
            ports=[client.V1ServicePort(
                port=8080,
                target_port=8080
            )]
        )
    )
    #Creation of the deployment on namespace default
    core_v1_api.create_namespaced_service(namespace="default", body=body)
    print("Service created ! Name : %s-service" % Deployname)

def getClusterIP(Deployname):
    config.load_kube_config()
    core_v1_api = client.CoreV1Api()
    service = core_v1_api.read_namespaced_service(name="%s-service" % Deployname, namespace="default")
    print("Cluster_IP :" ,service.spec.cluster_ip)
    return service.spec.cluster_ip

def VerifyStatus(pod_name):
    config.load_kube_config()
    core_v1 = core_v1_api.CoreV1Api()
    api_response = core_v1.read_namespaced_pod(name=pod_name,namespace="default")
    print("Pod Status : " , api_response.status.phase)
    return api_response.status.phase

def createDeployment(name):

    config.load_kube_config()
    api_instance = core_v1_api.CoreV1Api()
    with open(path.join(path.dirname(__file__),'%s.yaml' %name)) as f:
            dep = yaml.safe_load(f)
            k8s_apps_v1 = client.AppsV1Api()
            resp = k8s_apps_v1.create_namespaced_deployment(
                body=dep,namespace="default")
            print("Deployment created. Deployment Name = '%s'" % resp.metadata.name)
    os.remove('%s.yaml' %name)
    #create_service(name)

def main():

    name = DeploymentName()                                          # Create yaml file with given name
    print("1 - Create deployment \n2 - Create Service \n3 - Verify status of POD \n4 - Show Cluster IP\n5 - exit\n")
    while True:
        var = input("Input : ").strip()
        if ( var == "1" ):  createDeployment(name)                  # Create a deployment given a name
        elif (var == "2" ): create_service(name)                    # Create a Service and expose to type ClusterIP
        #PodName(name)                                              # Given the Deploy name , returns the Pod name
        elif (var == "3" ): VerifyStatus(PodName(name))             # Requires the name of the Pod to verify
        elif (var == "4" ): getClusterIP(name)                      # Return the Cluster_IP of the exposed service
        elif (var == "5" ): exit()
        else : print("Invalid input")

if __name__ == '__main__':
    main()
