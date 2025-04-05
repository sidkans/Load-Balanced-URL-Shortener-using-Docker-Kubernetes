# Commands to execute ->
(All the commands have been tested in powershell)
# week 1->
(make sure redis is running) 

docker-compose up --build

docker build -t flask-redis-app .

docker run -p 5000:5000 --name flask-app flask-redis-app

Invoke-RestMethod -Uri "http://localhost:5000/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

# week 2->
(make sure minikube is running) 

kubectl apply -f deployments.yaml

kubectl get pods

# week 3->
(only task 1 done so far)
minikube addons enable metrics-server

kubectl apply -f hpa.yaml

kubectl get hpa

kubectl describe hpa url-shortener-hpa




