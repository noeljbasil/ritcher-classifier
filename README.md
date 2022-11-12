# Building damage classifier
Note: This project was implemented as mid term project of ml-zoomcamp

## Problem Description
This project is one of the starter problems mentioned on Drivendata.org. Based on aspects of building location and construction, the goal of the project is to predict the level of damage to buildings caused by the 2015 Gorkha earthquake in Nepal. We're trying to predict the ordinal variable damage_grade, which represents a level of damage to the building that was hit by the earthquake. Hence this will be a multi-class classification problem

You can use the follwing commandas to use the model developed on your local system after cloning the repository to your system:
```
bentoml build
bentoml contaierize <bento tag>
docker run -it --rm -p 3000:3000 <docker image tag>
```
The model will now be availabel at `https://localhost:3000/classify`

You can also deploy the docker container which was generated to a cloud service so that it is available on a public IP
