# AuthoringInterface

Note - Open a terminal to perform steps 1 to 3.

1. Python is a pre-requisite for the installation.

   - To check if you have python, run the following command -
     - For windows - "python –version"
     - For Ubuntu - "python -V"

   If you do not have it follow given instructions for the installation of python -

   - Upgrade and update Ubuntu to the latest version
     "sudo apt update && sudo apt upgrade"
   - Install the required packages
     "sudo apt install wget build-essential libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev"
   - Download python 3.11
     "sudo add-apt-repository ppa:deadsnakes/ppa"
   - Install it
     "sudo apt install python3.11"

2. After the installation of python, we need to install pip.

   - To check if you have pip, run the following command -
     - "pip -V"

   If you do not have it follow given instructions for the installation of pip -

   - Start by updating the package list using the following command:
     "sudo apt update"
   - Use the following command to install pip for Python 3:
     "sudo apt install python3-pip"
   - Once the installation is complete, verify the installation by checking the pip version:
     "pip3 --version"

3. The installation of MySQL server and workbench is also a requirement.

   3.1 Open a terminal and go to the root directory by typing the following command - "cd"

   3.2 Run the following command -
   "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential"

   3.3 Now run following commands to install mySQL server -

   - "sudo apt update"
   - "sudo apt install mysql-server"
   - "sudo mysql"
     Now you have entered the mysql environment. Type the following command in it to change the password.
   - "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';"
     - Note - put your desired password in place of 'new_password'
   - You can exit mysql by pressing Ctrl + Z

   Note - If you get error run the following commands to uninstall mysql-server and then try the above steps of step 3.3 again from starting-

   - "sudo apt-get purge mysql-server mysql-client mysql-common mysql-server-core-\* mysql-client-core-\*"
   - "sudo rm -rf /etc/mysql /var/lib/mysql"
   - "sudo apt autoremove"
   - "sudo apt autoclean"

4. Creation of database -
   - Open a terminal and type the following command -
     "sudo mysql"
   - Type in the following command to create the database -
     "CREATE DATABASE IF NOT EXISTS db2;"

# Setup for backend -

4. Make a folder named AuthoringInterface.

5. Inside the AuthoringInterface make a new folder named backend.

6. Open a terminal in VS code.

7. Move inside the backend folder with the following command-

   - "cd backend"

8. Run the following command to get the backend code -

   - "git clone https://github.com/v-a-r-s-h-a/backend_AI ."

9. Setup Virtual Environment, run the following command in terminal -

   - "python3 -m venv env"
     Note - If you get the following error -
     - bash: /home/name/AuthoringInterface/backend/env/bin/python3: No such file or directory
       Try the following command -
       - python -m venv env
         If you still get this error. Do the following -
       - sudo ln -s /usr/bin/python3 /usr/bin/python
       - python -m venv env

10. Enable the virtual environment using the following command -

    - For ubuntu - "source env/bin/activate"
    - For windows - "env/bin/activate"

11. Run the following commands in the terminal to install dependencies

    - "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential"
    - "python3 -m ensurepip"
    - "pip install -r requirements.txt"

12. Inside the env\python3.10\site-packages\flask_navigation\item.py, change line 131 and 132 with below code
    class ItemCollection(collections.abc.MutableSequence,
    collections.abc.Iterable):

13. Inside the env\python3.10\site-packages\flask_navigation\navbar.py, change line 7 below code
    class NavigationBar(collections.abc.Iterable):

14. Now the config.py file needs to modified, the variable need to updated with the values that you have created while setting up your mySQL workbench environment.

    - The variable that need to be changed are -
      app.config['MYSQL_PASSWORD'] = '?'

    'MYSQL_PASSWORD' is the password that you set while setting mysql-server. Instead of ? type your password.

15. Run the backend using the following command -

    - "python3 main.py"

16. Type "http://127.0.0.1:9999/" on your browser to enable the creation of databases.

# Setup for frontend -

18. Open a new terminal. Make sure you are in the AuthoringInterface folder.

19. Install nodejs if you do not have it by running the following commands-

    - "sudo apt update"
    - "sudo apt install nodejs"
    - "node -v"
    - "sudo apt-get install npm"

20. Update the node to latest verison -

    - "curl -fsSL https://deb.nodesource.com/setup_current.x | sudo -E bash -"
    - "sudo apt-get install -y nodejs"

21. Install create-react-app to make react apps -

    - "npm install create-react-app"

22. Run the following command to create a react app -

    - "npx create-react-app client"

23. A folder named client can be seen in the AuthoringInterface folder.

24. Expand the folder and you will see a folder named src. Delete the content of the src folder. Now you have an empty src folder.

25. Come back to the terminal. At the moment you will be in the AuthoringInterface folder.

26. Enter the client folder by running the command -
    - "cd client"
27. Move inside the src folder with the command -
    - "cd src"
28. Now you are in the src folder. Run the following command to get the frontend code.

    - "git clone https://github.com/v-a-r-s-h-a/src_AI ."

29. Move out of the src folder with the command -

    - "cd .."

30. Install all the following dependencies -

    - "npm install axios --legacy-peer-deps"
    - "npm install file-saver --legacy-peer-deps"
    - "npm install jszip --save --legacy-peer-deps"
    - "npm install --legacy-peer-deps @material-ui/core"
    - "npm install --legacy-peer-deps @material-ui/icons"
    - "npm install --legacy-peer-deps react-icons"
    - "npm install @emotion/react @emotion/styled --legacy-peer-deps"
    - "npm install @mui/material --legacy-peer-deps"
    - "npm install reactjs-popup --save --legacy-peer-deps"
    - "npm install --save react-modal --legacy-peer-deps"
    - "npm install react-router-dom --legacy-peer-deps"
    - "npm install @mui/icons-material --legacy-peer-deps"

    - Note - If you cannot install a dependecy add --legacy-peer-deps to it

31. Open the file package.json in client. Before the line containing the word dependencies add the following line -

- "proxy": "http://127.0.0.1:9999",

32. Now you are in the client folder. Start the frontend with the following command -
    - "npm start"
