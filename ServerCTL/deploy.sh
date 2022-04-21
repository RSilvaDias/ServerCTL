docker build . -t rsdias/fapesp:serverctl
docker push rsdias/fapesp:serverctl
kubectl apply -f fapespctl.yaml