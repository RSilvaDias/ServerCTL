cd distributor
dnc . -sp "../dc;../repository" -v
cd ..
kubectl delete deploy distributor serverctl mrr0 mrr1 hd0 hd1 hdr0 hdr1 mr0 mr1
kubectl delete svc mrr0 mrr1 hd0 hd1 hdr0 hdr1 mr0 mr1
docker build . -t rsdias/fapesp:distributor
docker push rsdias/fapesp:distributor
kubectl apply -f distributor.yaml
kubectl apply -f fapespctl.yaml