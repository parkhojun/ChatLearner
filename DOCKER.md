Docker Build Steps:
```
cd Data
docker build -f Dockerfile.data -t chatlearner-hugedata .
cd ..
docker build -t mara8534/chatlearner .
```