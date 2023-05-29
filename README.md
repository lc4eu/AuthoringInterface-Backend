# AuthoringInterface

\*Note - Open a terminal to perform steps 1 to 3.

1. Python is a pre-requisite for the installation.

   - To check if you have python, run the following command - <br/>
     For windows - "python –version"<br/>
     For Ubuntu - "python -V"<br/>

   If you do not have it follow given instructions for the installation of python -

   - Upgrade and update Ubuntu to the latest version <br/>
     "sudo apt update && sudo apt upgrade"
   - Install the required packages<br/>
     "sudo apt install wget build-essential libncursesw5-dev libssl-dev \
     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev"
   - Download python 3.11<br/>
     "sudo add-apt-repository ppa:deadsnakes/ppa"
   - Install it<br/>
     "sudo apt install python3.11"

2. After the installation of python, we need to install pip.

   - To check if you have pip, run the following command -<br/>
     "pip -V"

   If you do not have it follow given instructions for the installation of pip -

   - Start by updating the package list using the following command:<br/>
     "sudo apt update"
   - Use the following command to install pip for Python 3:<br/>
     "sudo apt install python3-pip"
   - Once the installation is complete, verify the installation by checking the pip version:<br/>
     "pip3 --version"

3. The installation of MySQL server and workbench is also a requirement.

   3.1 Open a terminal and go to the root directory by typing the following command - "cd"

   3.2 Run the following command -
   "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential"

   3.3 Now run following commands to install mySQL server -<br/>

   "sudo apt update"<br/>
   "sudo apt install mysql-server"<br/>
   "sudo mysql"<br/>
  
    Now you have entered the mysql environment. Type the following command in it to change the password.<br/>
   "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';"<br/>
    \*Note - put your desired password in place of 'new_password'<br/>
   You can exit mysql by pressing Ctrl + Z

   \*Note - If you get error run the following commands to uninstall mysql-server and then try the above steps of step 3.3 again from starting-<br/>

   "sudo apt-get purge mysql-server mysql-client mysql-common mysql-server-core-\* mysql-client-core-\*"<br/>
   "sudo rm -rf /etc/mysql /var/lib/mysql"<br/>
   "sudo apt autoremove"<br/>
   "sudo apt autoclean"<br/>

4. Creation of database -<br/>
   Open a terminal and type the following command -<br/>
     "mysql -u root -p"<br/>
   Type in the following command to create the database -<br/>
     "CREATE DATABASE IF NOT EXISTS db2;"

# Setup for backend -

4. Make a folder named AuthoringInterface.

5. Inside the AuthoringInterface make a new folder named backend.

6. Open a terminal in VS code.

7. Move inside the backend folder with the following command-<br/>
     "cd backend"

8. Run the following command to get the backend code -<br/>

   "git clone https://github.com/v-a-r-s-h-a/backend_AI ."<br/>
    \*Note - Do not forget to add the dot

9. Setup Virtual Environment, run the following command in terminal -

   - "python3 -m venv env"<br/>
     \*Note - If you get the following error -<br/>
     bash: /home/name/AuthoringInterface/backend/env/bin/python3: No such file or directory<br/>
     Try the following command -<br/>
      "python -m venv env"<br/>
      If you still get this error. Do the following -<br/>
      "sudo ln -s /usr/bin/python3 /usr/bin/python"<br/>
      "python -m venv env"

10. Enable the virtual environment using the following command -<br/>
    For ubuntu - "source env/bin/activate"<br/>
    For windows - "env/bin/activate"

11. Run the following commands in the terminal to install dependencies<br/>
    "sudo apt-get install python3-dev default-libmysqlclient-dev build-essential"<br/>
    "python3 -m ensurepip"<br/>
    "pip install -r requirements.txt"

12. Inside the env\lib\python3.10\site-packages\flask_navigation\item.py, change line 131 and 132 with below code - <br/>
    class ItemCollection(collections.abc.MutableSequence,
    collections.abc.Iterable):

13. Inside the env\lib\python3.10\site-packages\flask_navigation\navbar.py, change line 7 below code -<br/>
    class NavigationBar(collections.abc.Iterable):

14. Now the config.py file needs to modified, you can find this file in the backend folder. The variable needs to updated with the values that you created while setting up your mySQL workbench environment.<br/>
    The variable that need to be changed is -<br/>
      app.config['MYSQL_PASSWORD'] = '?'<br/>

    The value for 'MYSQL_PASSWORD' is the password that you set while setting mysql-server. Instead of ? type your password.

15. Run the backend using the following command -<br/>
    "python3 main.py"

16. Type "http://127.0.0.1:9999/create_database" on your browser to enable the creation of databases. Please load it only once.

# Setup for frontend -

18. Open a new terminal in VS Code. Make sure you are in the AuthoringInterface folder.

19. Install nodejs if you do not have it by running the following commands-<br/>
      "sudo apt update"<br/>
      "sudo apt install nodejs"<br/>
      "node -v"<br/>
      "sudo apt-get install npm"<br/>
        
    \*Note - If you get the following error - <br/>
        "dpkg: error processing package mysql-server (--configure):dependency problems - leaving          unconfigured No apport report written because the error message indicates its a followup error from a previous failure.
        Errors were encountered while processing:
          mysql-server-8.0
          mysql-server
        E: Sub-process /usr/bin/dpkg returned an error code (1)"
        
      - Try the following solution -<br/>
        "sudo apt-get remove --purge nodejs"<br/>
        "sudo apt autoremove"<br/>
      Repeat the commands of step 19 from beginning to setup node properly.

20. Update the node to latest verison -<br/>
    "sudo snap install curl"<br/>
    "curl -fsSL https://deb.nodesource.com/setup_current.x | sudo -E bash -"<br/>
    "sudo apt-get install -y nodejs"<br/>
      \*Note - If you get error in this step, run the following command -<br/>
      "sudo apt remove nodejs"<br/>
      After you have have run the above command restart from step 19.

23. Make sure you are in the AuthoringInderface directory. Now run the following command to get the frontend code.<br/>
    "git clone https://github.com/v-a-r-s-h-a/client"<br/>

24. A folder named client can be seen in the AuthoringInterface folder.

29. Move inside the client folder with the following command -<br/>
    "cd client"

30. Make sure you are in the client folder. Install all the following dependencies -<br/>
    - "npm i"

    \*Note - If you cannot install a dependecy add --legacy-peer-deps or "-force" to it as shown below - <br/>
    "npm i -force"

32. Now you are in the client folder. Start the frontend with the following command -<br/>
    "npm start"


# To start the app use the following commands -
  - To start the backend run the following commands on one terminal- <br/>
    "cd backend"<br/>
    "source env/bin/activate"<br/>
    "python3 main.py"<br/>

  - To start the frontend run the following commands on another terminal - <br/>
    "cd client" <br/>
    "npm start"




