Ok this is it only i need to change the model for this project and its done 
->what i want you to do is add css to the react app 
STEPS TO CLONE DIRECTORY! 
1 -> Go to your C or D drive which must have good space, its gonna occupy over 3GB 
2 -> create a file in the selected drive a "Mini_Project" 
3 -> cd into the "Mini_Project" file and open cmd 
4 -> in cmd type this "git clone https://github.com/Sandeepkandula2004/Mini_Project/tree/main "
5 -> now after cloning type code. to open vs code. You dont need to install dependencies as they are included in .conda env

STEPS TO OPEN REACT APP 
1 -> opening react files is hard but there is easy way to do it i.e in vs code you can see files to your left and there you can go to frontend folder, then my react app, then again my react app and there you can see src folder which consists of all the react files.
2 -> first open cmd teminal in the vs code then type cd then drag the src folder into the terminal then press enter and there you are into the src folder.
3 -> Components consist of most of the code and need severe attention of css. Components are the heart.

STEPS TO RUN REACT APP
1 -> open terminal and you should be in the src folder and type "npm run dev" which provides you with a local host link hold ctrl and press that link.
2 -> you can see four links but three are important (webcam, upload file and student details)
3 -> these three links need server to run but to open the webcam and upload file doesn't need server.
4 -> for student details you need server to see the contents.

STEPS TO RUN FLASK APP(SERVER)
1 -> first split the terminal into two one for react app and one for flask app.
2 -> make sure that both the terminals are cmd and it should not be powershell.
3 -> in the new terminal cd into backend and run "python app.py".
4 -> the server starts running now get back to chrome as you are running the react app on the front end go to student details you can see the fetched student details.
5 -> sever is needed to fetch the details from the database via api.