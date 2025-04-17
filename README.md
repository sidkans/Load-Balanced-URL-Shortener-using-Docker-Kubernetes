# Commands to execute ->

(All the commands have been tested in powershell)

# week 1->

(make sure redis is running)

docker-compose up --build



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

Invoke-RestMethod -Uri "http://url-shortener.local/shorten" -Method Post -Headers @{"Content-Type"="application/json"} -Body ('{"long_url": "https://example.com"}')

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


## Load Testing:

# 1. Install Apache Benchmark
choco install apache-httpd

# 2. Create test payload file
@{
    "long_url" = "https://www.example.com/very/long/url"
} | ConvertTo-Json | Out-File -FilePath payload.json

# 3. Open separate terminals for monitoring during load test
# Terminal 1 - Watch pod scaling:
kubectl get pods -w

# Terminal 2 - Monitor HPA:
kubectl get hpa -w

# Terminal 3 - Watch resource usage:
kubectl top pods

# 4. Run load tests
# Test GET endpoint (1000 requests, 100 concurrent)
ab -n 1000 -c 100 http://url-shortener.local/

# Test POST endpoint for URL shortening
ab -n 1000 -c 100 -p payload.json -T application/json http://url-shortener.local/shorten

# 5. Check results
kubectl describe hpa url-shortener-hpa
kubectl get pods
kubectl top pods
