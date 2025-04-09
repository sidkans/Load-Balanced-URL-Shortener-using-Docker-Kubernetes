# Commands to execute ->

(All the commands have been tested in powershell)

# week 1->

(make sure redis is running)

docker-compose up --build

docker build -t flask-redis-app .

docker run -p 5000:5000 --name flask-app flask-redis-app

Invoke-RestMethod -Uri "http://localhost:5000/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

# week 2->

(make sure minikube is running): minikube start

kubectl apply -f deployments.yaml

kubectl get pods

minikube service url-shortener-service --url

## Now we have to take the URL given in terminal and change the BASE_URL in deployments.yaml to use that URL.

## followed by this in a new terminal while keeping the tunnel open on the previous terminal:

kubectl apply -f deployments.yaml

kubectl rollout restart deployment url-shortener

Invoke-RestMethod -Uri "<BASE_URL>" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

## Note: In the Invoke-RestMethod command, we have to manually put the BASE_URL which we have set in the yaml file as well.

# week 3->

minikube addons enable metrics-server

kubectl apply -f hpa.yaml

kubectl get hpa

kubectl describe hpa url-shortener-hpa

minikube addons enable ingress

kubectl apply -f ingress.yaml

kubectl get ingress

## For monitoring:

kubectl logs -f -l app=url-shortener

kubectl top pods
