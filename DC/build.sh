docker build . -t rsdias/fapesp:dist10k
docker push rsdias/fapesp:dist10k
kubectl apply -f distributor.yaml
#kubectl apply -f fapespctl.yaml