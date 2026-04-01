# prerequisites
- minikube
- docker
- kubectl

# commands to run in order
```bash
# start minikube cluster and update context
minikube start --driver=docker
minikube update-context
```

```bash
# verify
kubectl get nodes
```

```bash
# build images localy
docker build -t api-a:1.0 ./api-a
docker build -t api-b:1.0 ./api-b
```

```bash
# load images
minikube image load api-a:1.0
minikube image load api-b:1.0
```

```bash
# verify
minikube image ls   
```

```bash
# apply deployments and services
kubectl apply -f api-a.yaml
kubectl apply -f api-b.yaml
```

```bash
# verify rollout
kubectl get deployments
kubectl get pods
kubectl get rs
kubectl get svc
```

```bash
# (optional) verify logs for both api-a and api-b pods
kubectl logs <pod-name> 
# look for : Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

```bash
# test api a
kubectl port-forward svc/api-a 8080:80
```

```bash
# in another terminal
curl http://localhost:8080/
# {
#     "service":"A",
#     "message":"hello from A"
# }

curl http://localhost:8080/health
# {
#     "status":"ok"
# }
```

```bash
# test api b 
kubectl port-forward svc/api-b 8081:80
```

```bash
# in another terminal
curl http://localhost:8081/
# {
#     "service":"B",
#     "calls":"http://api-a",
#     "response_from_a":
#     {
#         "service":"A",
#         "message":"hello from A"
#     }
# }
```

# Add centralised logging to this setup

```bash
# add grafana helm repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

```bash
# create namespace
kubectl create namespace logging
```

```bash
# install loki stack
helm install loki grafana/loki-stack \
  -n logging \
  --set promtail.enabled=true \
  --set grafana.enabled=true
```

```bash
# verify stack
kubectl get pods -n logging
kubectl get svc -n logging
```

```bash
# access grafana
kubectl port-forward -n logging svc/loki-grafana 3000:80
go to localhost:3000
```

```bash
# get admin password
username: admin
kubectl get secret -n logging loki-grafana -o jsonpath="{.data.admin-password}" | base64 -d
```

```bash
# if loki is not configured in grafana
add new datasource, http://loki.logging.svc.cluster.local:3100
```

```bash
# validate
in Explore, use "code" query, {app=~".+"}, {app=~"app-a"}, {app=~"app-b"}
```