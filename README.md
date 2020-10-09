# ECSS_Work
7.31.2020 
This repo is setup to host code supporting text and image processing, data fusion, and knowledgebase representation. After creating this REPO I invited Darren and John to it.

8.9.2020 
I setup a new project board in GIT called XSEDE Research Project which will enable viewing of the high level schedule for the project that this REPO is supporting. It will also enable capture of notes which will enable asynchronous collaboration between me, John, and Darren. I will use KanBan style project tracking to support promotion of high level tasks through three phases: 'to do', 'in progress', and 'completed'. This will enable flexibility in defining tasks necessary to complete the schedule milestones. I still need to invite Darren and John to the project board.

8.25.2020
I completed a python script in python 3.5 (required for me to use pyquery to pull articles in AJAX and JavaScript). I was able to get about 30 articles for Donald Trump and Vladimir Putin along with images for each article when they had images. The article text are stored in JSON files and the images could not be loaded because they were too large. I will need to ftp these directly to Bridges.

8.26.2020
I re-ran the script to get more articles to see how that would go. I was able to get 175 articles for Donald Trump. My error handling is still not that good in that sometimes the URL kick's back an undefined schema, so I just modify the range of the for loop to the next article after the failed pull and keep going. The articles are more representative of this calendar year quarter (100 articles) while previous two quarters have 75 articles and 25 articles respectively. I did pickle the images file, which is now at 600 MB and I will need to move that to Bridges with help. 

8.28.2020
Held the bi-weekly call with Darren and John and was able to confirm a few things about where my data should be stored (Pylon) and next steps. I was able to login to my Globus online account and figured out how to move the pickle files to my pylon directory. Next I will begin looking into face recognition algorithms in order to chip out the faces from the article images and topic modeling algorithms in order to identify / characterize the text articles. After that I plan to look into nonlinear dimensionality reduction algorithms for embedding the two data types.

9.11.2020
Held the bi-weekly with Darren and John. I spent the last few weeks getting familiar with Tensorflow 2.0 using web resources from the ACM. Ahead of the meeting I sent an email with questions about requesting an extension of resources since I am behind schedule in getting started on the project and the expiration of my allocation is set for the end of the year, using TensorBoard with Bridges, and choosing the appropriate filter set for my neural network facial recognition structure. Through screensharing John was able to show me that I should look for an extension button in my 'actions' options in the actual allocation document when I am about 90 days from expiration, which will likely be near the end of October or early November. Next he pointed me to the Bridges User Guide on PSC.edu and specifically where the guidance on using tensor board is, and he confirmed that I had access to the right GPU resources for tensorflow. I was able to confirm that I did not perform all the correct steps when I tried using it earlier this week. John recommended that I request a supplemental of the Bridges GPU resources in order to troubleshoot my code ahead of submitting batch orders to GPU-AI so that I can confirm the code is working on the more available older processors. Lastly, for my filter selection, he recommended I take a day and research as many possible sources of facial recognition implementations using tensorflow 2.0 or pytorch ahead of actually writing my own CNN in order to better facilitate my startup progress on the projet.

9.12.2020
I spent some time searching and reviewing facial recognition code sources specifically employing tensorflow 2.0 to accelerate and simplify my facial recognition project tasks. Of the ones identified, I chose to experiment with tiny face detection by burnpiro at https://github.com/burnpiro/tiny-face-detection-tensorflow2  I also looked at tensorflow playground and tensorflow zoo based on the references of dev Deejay's github gist article on Medium. Burnpiro uses a pretrained tensorflow image recognition network, mobileNetV2, employing transfer learning to get the facial recognition capability. Training the network on the WIDER FACE dataset available in Tensorflow gives it the target facial recognition capability.

9.21.2020
I used the tiny face detection code to employ transfer learning from the object detection capability on the mobileNetV2 network by removing the last layer and re-training a new last layer with the WIDER FACE dataset. This ran for about 12 hours on my laptop (30 of 150 epochs were completed) and finally I think the training stopped because it plateaued. I attempted to use one of the dataset images as a test to see if this was enough training to identify the face and the network failed to recognize the face. I checked the loss metric and the network had 62.9% loss. 

9.25.2020
I met with Darren and John and relayed my experience over the past few weeks on the facial recognition trained network and John recommended that I go ahead and retry training the network using a GPU-AI batch job with fewer epochs to see if it will work because it will still be faster than my laptop which only has 1 gpu. He is also going to check on my supplemental request to try and get the GPU interactive allotment accelerated for me. 

9.30.2020
After some trial and error, I was able to submit an interact request for GPU-AI resources and get varying numbers of hours allocated. In several of these runs (4 hours, 6 hours, 8 hours, and 16 hours) I was able to train the mobilenetV2 network with the WIDER_FACE dataset. I experimented with small numbers of training epochs first (e.g. 4, 12, 30, 50, 100) to ensure the code would successfully complete. In all of these cases, and moving above 30 epochs still only resulted in model .h5 files (those that include actual model weights) for runs below epoch 30. For all epochs above 30, the results all showed the network experienced learning plateaus and did incrementally reduce learning rate, but never any improvements. Additionally, experimenting with the batch job submission for GPU-AI resources, I always experienced problems and these jobs never even started successfully. The error I get at the end of the slurm file is:

+ python train.py
Traceback (most recent call last):
  File "train.py", line 1, in <module>
    import tensorflow as tf
ImportError: No module named tensorflow

I have also attached the slurm file to the code repo for your review.

The sbatch file is as follows, which does work successfully when starting the interact mode with a GPU-AI resource:
#!/bin/bash
#SBATCH -N 1
#SBATCH -p GPU-AI
#SBATCH --ntasks-per-node 20
#SBATCH --gres=gpu:volta16:8
#SBATCH -t 8:00:00

#echo commands to stdout
set -x
#move to working directory  # this job assumes:
# - all input data is stored in this directory
# - all output should be stored in this directory
cd /pylon5/ci561jp/wham/tiny-face-detection-tensorflow2

#load the singularity container to get tensorflow
module load singularity
singularity shell --nv /pylon5/containers/ngc/tensorflow/tensorflow_20.02-tf2-py3.sif

#run GPU program
python train.py

10.5.2020
I attempted to use the model file that completed with only 30 epochs since I could not get the network to make any progress in learning past that. I have added files that show the source image, meme.jpg, as well as the output image, output.jpg, to show the performance. While the face is partially detected, it is not that good. I am assuming it 'could' get better with more training, but I have not been able to get improvements past 30 epochs and need to figure out which configurations in the config.py file to modify to improve the learning. 

10.9.2020
After the call this week I learned that I really need to check the bridges user guide at https://www.psc.edu/bridges/user-guide/sample-batch-scripts#gpu-ai as it can provide me some sample batch scripts that I can use that corresponds with the correct singularity container. I was using something that was not correct. I also need to check and see what the latest image of tensorflow is so I can reference that in my batch script.
