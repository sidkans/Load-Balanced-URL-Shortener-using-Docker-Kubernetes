# Commands to execute ->

# week 1->
(make sure redis is running) 

docker-compose up --build

docker build -t flask-redis-app .

docker run -p 5000:5000 --name flask-app flask-redis-app

Invoke-RestMethod -Uri "http://localhost:5000/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

# week 2->
(make sure minikube is running) 

kubectl apply -f deployments.yaml

