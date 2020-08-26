# ECSS_Work
7.31.2020 
This repo is setup to host code supporting text and image processing, data fusion, and knowledgebase representation. After creating this REPO I invited Darren and John to it.

8.9.2020 
I setup a new project board in GIT called XSEDE Research Project which will enable viewing of the high level schedule for the project that this REPO is supporting. It will also enable capture of notes which will enable asynchronous collaboration between me, John, and Darren. I will use KanBan style project tracking to support promotion of high level tasks through three phases: 'to do', 'in progress', and 'completed'. This will enable flexibility in defining tasks necessary to complete the schedule milestones. I still need to invite Darren and John to the project board.

8.25.2020
I completed a python script in python 3.5 (required for me to use pyquery to pull articles in AJAX and JavaScript). I was able to get about 30 articles for Donald Trump and Vladimir Putin along with images for each article when they had images. The article text are stored in JSON files and the images could not be loaded because they were too large. I will need to ftp these directly to Bridges.

8.26.2020
I re-ran the script to get more articles to see how that would go. I was able to get 175 articles for Donald Trump. My error handling is still not that good in that sometimes the URL kick's back an undefined schema, so I just modify the range of the for loop to the next article after the failed pull and keep going. The articles are more representative of this calendar year quarter (100 articles) while previous two quarters have 75 articles and 25 articles respectively. I did pickle the images file, which is now at 600 MB and I will need to move that to Bridges with help. 
