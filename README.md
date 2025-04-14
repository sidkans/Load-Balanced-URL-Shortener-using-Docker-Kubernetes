# Commands to execute ->

(All the commands have been tested in powershell)

# week 1->

(make sure redis is running)

docker-compose up --build

docker build -t flask-redis-app .

docker run -p 5000:5000 --name flask-app flask-redis-app

Invoke-RestMethod -Uri "http://localhost:5000/" -Method Get

Invoke-RestMethod -Uri "http://localhost:5000/health" -Method Get

Invoke-WebRequest -Uri ("http://localhost:5000/" + (Invoke-RestMethod -Uri "http://localhost:5000/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"long_url": "https://example.com"}').short_code) -Method Get -MaximumRedirection 0 -ErrorAction Ignore

Invoke-RestMethod -Uri "http://localhost:5000/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

# week 2->

(make sure minikube is running): minikube start

kubectl apply -f deployments.yaml

kubectl get pods
kubectl get svc

minikube tunnel

Invoke-RestMethod -Uri "http://127.0.0.1:5000/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

# week 3->

minikube addons enable metrics-server

kubectl apply -f hpa.yaml

kubectl get hpa

kubectl describe hpa url-shortener-hpa

minikube addons enable ingress

kubectl apply -f ingress.yaml

kubectl get ingress

## For monitoring:

kubectl logs -f <podname>

kubectl logs -f -l app=url-shortener

kubectl top pods
