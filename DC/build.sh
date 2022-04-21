docker build . -t rsdias/fapesp:distributor
docker push rsdias/fapesp:distributor
kubectl apply -f distributor.yaml
kubectl apply -f fapespctl.yaml