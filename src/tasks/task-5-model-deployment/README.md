
# Streamlit Project with Machine Learning Models and AWS Docker Deployment

Step 1- Open the project in Pycham or VS code

source venv/bin/activate

Step 2- Open Terminal and run the following commands 

pip install -r requirements.txt

streamlit run app/Home.py

## Optional - Alternative way to run the application
Docker commands -

docker build -t appimage .

docker run -d --name appcontainer -p 8501:8501 appimage


# AWS Deployment Steps

   sudo yum update -y

   sudo yum install -y docker

   sudo service docker start

   sudo usermod -a -G docker ec2-user

   exit    (logout)

   Log back in to ec2 instance

   docker info
   
   copy the streamlit folder
   
   cd streamlit (navigate to streamlit folder)
   
   sudo systemctl start docker

   docker build -t appimage .

   docker run -d --name appcontainer -p 8501:8501 appimage


## How to check the app is running or not

   ps -ef | grep python


## How to check docker container status

   docker ps -a


## How to restart the docker

   sudo systemctl restart docker

## How to restart the docker container

   docker restart appcontainer

## How to rebuild new image
   docker ps -a 
   
   docker container stop "container name"

   check the status
   
   docker ps -a

   docker container rm "container name"

   docker image ls
   
   docker image rm "image name"

   docker image rm "python image"

   docker build -t appimage .

   docker run -d --name appcontainer -p 8501:8501 appimage
