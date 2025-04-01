Commands to execute

docker-compose up --build

docker build -t flask-redis-app .

docker run -p 5000:5000 --name flask-app flask-redis-app
