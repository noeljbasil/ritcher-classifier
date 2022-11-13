# Building damage classifier
Note: This project was implemented as mid term project of ml-zoomcamp

## Problem Description
This project is one of the starter problems mentioned on Drivendata.org. Based on aspects of building location and construction, the goal of the project is to predict the level of damage to buildings caused by the 2015 Gorkha earthquake in Nepal. We're trying to predict the ordinal variable damage_grade, which represents a level of damage to the building that was hit by the earthquake. Hence this will be a multi-class classification problem. 

Detailed EDA and experiments can be referenced via `notebook.ipynb`

## Steps tp reproducing the app for yourself
You can use the follwing commandas to use the model developed on your local system after cloning the repository to your system:
```
bentoml build
bentoml contaierize <bento tag>
docker run -it --rm -p 3000:3000 <docker image tag>
```
The model will now be availabel at `https://localhost:3000/classify` for testing and usage

You can also deploy the docker container which was generated to a cloud service so that it is available on a public IP. I have deployed containerized using Mogenius and Streamlit. 

The swagger UI is available at: 
https://njbasil-ritche-prod-ritcher-classifier-cf5h5e.mo4.mogenius.io/

I have further developed a front end UI using streamlit which can be access at: 
https://noeljbasil-ritcher-classifier-ui-q59q1m.streamlit.app/

#### Demo of the app is shown below
![](https://github.com/noeljbasil/ritcher-classifier/blob/main/Recording%202022-11-13%20at%2003.28.39.gif)

Inorder to similarly deploy to Mogenius, you need to first upload the docker image to DockerHub via the following steps:
* Create and account
* Create a repository under free tier and name it . e.g. ritcher-classifer
* Go to `username(top righ of the DockerHub tab)>Account Setting>security>generate a new access token`
* From your local terminal, with docker running, run the following to login to DockerHub, retag your local docker image and push it to Dockerhub:
```
docker login -u username
docker tag <existing-image-tag> <hub-user>/<repo-name>:<tag>
docker push <hub-user>/<repo-name>:<tag>
```
  Note: 
- The password for loggin in will be the access token you generated in earlier step        
- `docker images` command will give you the list of docker images and their tags

Once you have you image in DockerHub, you can deploy the app using the following steps:
- Create an account on Mobegenius: https://studio.mogenius.com/user/registration
- Verfiy your account and select the free plan
- Create a cloud space with a reflective name, e.g. RitcherClassifier
- Choose Create from docker image from any registry
- Give the service a name, and enter the address of your image on DockerHub
- Select Stage as "production", increase all the resources to maximum and leave everything else on default setting
- Add 3000 to HTTPS port at the very end and hit "Create Service"

You now have successfully deployed your app and the external IP address can be accessed under 'Hostname>External hostname' and the API endpoint can be accessed at `external IP address/classify`

Once you have the API endpoint, you can create a user interface around it using streamlit. I have create a simple UI using `ui.py` script

Now inorder to share the streamlit app, we need to upload the `ui.py` file along with any dependent files to GitHub. Once you have pushed them to GitHub, you can follow the below steps to deploy it:
- Create an account at https://share.streamlit.io/
- Once you are logged in, click "New app" from the upper right corner of your workspace, then fill in your repo, branch, and file path, and click "Deploy"
