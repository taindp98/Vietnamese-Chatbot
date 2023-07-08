## Developing the UI of chatbot application by using Flask and Docker

### Install Docker

- Ubuntu: https://docs.docker.com/engine/install/ubuntu/
- Window: https://docs.docker.com/desktop/install/windows-install/

Dive into Docker: https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/

  Note: fixbug "docker-permission-denied" in the Ubuntu
  ```
  $ chmod 777 /var/run/docker.sock
  ```
### Structure of a project with Docker and Flask:

- An application file with Flask framework: app.py
- The requirements.txt file indicates the needed dependencies to run the application.
- Dockerfile:
  + Indicate the Python's version: FROM python:3.x-slim-buster.
  + Copy the dependencies: COPY requirements.txt requirements.txt.
  + Install the dependencies: RUN pip3 install -r requirements.txt.
  + Finally, the execution: CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"] to run the app.py file. We need to replace the local IP consistency in the Windows and Linux.

  ```
  FROM python:3.6-slim-buster

  WORKDIR /deploy

  COPY requirements.txt requirements.txt
  RUN pip3 install -r requirements.txt

  COPY . .

  CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
  ```

### Dockerize a Flask application
  1. Modify the Dockerfile.
  2. ``` $ docker build --tag <folder-docker-name> . ```

      Don’t forget the . character at the end, which sets the build context to the current directory. The {folder-docker-name} is named the docker image name.

  3. ``` $ docker images ```
    
      To list the existing docker images in this machine.

  4. ``` $ docker run -d -p 5000:5000 <image-name> ```

      Note: the correct port ID is important because the localhost of the local device and docker container are different each other.

  5. Another way to build and run the app using docker-compose with the docker-compose.yaml file.

### Kubenetes

Minikube is a utility that can be used to run Kubernetes on our local machine. It creates a single node cluster contained in a Virtual Machine(VM).

Start running minikube by following.


```$ minikube start ```

and then check the status of minikube.

```$ minikube status ```

**Important**: Need to define a Deployment (deployment.yaml) that maps the container to a set of pods along with a Service that establishes networking and the Service is specified in a service.yaml file is like so.

  1. Create the deployment within minikube.

  ```$ kubectl create --filename deployment.yaml ```

  **Note**: the "spec" field must match with the dockerized app name.

  2. Create a Service using the service.yaml file. 

  ```$ kubectl create --filename service.yaml ```

  **Note**: the "spec" field must match with the dockerized app name.

  3. When both "deployment.yaml" and "service.yaml" configuration files are correct, check the status: RUNNING.

  ```$ kubectl get all```


  4. Loading the Docker Image into Minikube.

  In order to get the locally built image of my dockerized app into my minikube Kubernetes cluster I can use the minikube cli as follows.

  ```$ minikube image load <image-name> ```

  5. Run service tunnel

  ```$ minikube service <service-name> --url ```

  or

  ```$ minikube tunnel ```

  6. Cleanup

  Clean up the unneeded resources in the minikube cluster.

  ```$ kubectl delete deployment flask-ui-chatbot-deploy ```

  ```$ kubectl delete service flask-svc```

  7. Stop the dockerized minikube

  ```$ minikube stop ```

### Reference

https://thecodinginterface.com/blog/flask-rest-api-minikube/
https://www.analyticsvidhya.com/blog/2022/01/deploying-ml-models-using-kubernetes/