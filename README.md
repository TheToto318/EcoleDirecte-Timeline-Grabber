# EcoleDirecte-Timeline-Grabber
An ical timeline grabber for the EcoleDirecte platform written in python

Need a student account !!

- Usage (CLI): 

              To use directly the script take the "main.py" file.

              Variables : User and password for logging and start, end date desired for your timeline (Y-M-D).

              A calendar.ical will be generated in the script folder.



- Usage (Docker, ubuntu based image):

          Use the docker file and the "timeline.py" file (same folder) and run a docker build command.
          Or load the image from the release section directly with "docker load -i <path to image tar file>".

          Environnement variables : - MY_USER
                                    - MY_PASS
                                    - startDate (Y-M-D)
                                    - endDate (Y-M-D)
                                    - interval (in min)
          
          
          Volume : calendar.ical file is created in the "/calendar" directory in the container.
                   In consequence : "-v yourlocalpath:/calendar"
                   
          Docker run command exemple : docker run -t -d \
                                      --name=timelinegrabber \
                                      -e MY_USER=id \
                                      -e MY_PASS=pass \
                                      -e startDate=2020-11-02 \
                                      -e endDate=2021-08-01 \
                                      -e interval=45 \
                                      -v /volume1/Thomas/calendar:/calendar \
                                      "tag used during build"
                                      
          A calendar.ical file will be generated or update ech 45 minutes.
                                      
                                      
