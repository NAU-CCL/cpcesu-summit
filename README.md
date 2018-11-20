# Env-Testing

Just a pre-prototype repo to figure out repo init and environment testing.

## Dev instructions

After starting up the VM, follow these instructions:

### Checking installed programs

There should be the following programs already installed when you start the VM:

System programs:

* Git 2.17.2
    * git --version
* Java 8 - Oracle JDK/JRE
    * java -version
* PostgreSQL 8.4.22
    * psql --version
* Python 3.6.6
    * python3 --version
* Python pip3 9.0.1
    * pip3 --version
* Virtual Environment 15.1.0
    * virtualenv --version

Dev tools:

* Atom 1.32.2
    * atom --version
* pg Admin III - 1.22.2
    * pgadmin3 --version
* Prepros 6.2.3
    * Open Prepros -> 'i' icon at the bottom-left corner -> "About Prepros"
* PyCharm Community Edition 2018.2.5
    * Open Pycharm -> Help -> About

If any of these are missing, please report it to Joseph Remy - remy@nau.edu .

### Creating PostgreSQL user and DB and adding permissions

```
sudo su postgres
psql
```

If psql errors out for Postgres not running, run the following:

```
sudo service postgresql start
```

Now, create the user and database and add permissions:

```
CREATE DATABASE summit_db;
CREATE USER summit_db_user WITH PASSWORD '$umM1T_DB)';
GRANT ALL PRIVILEGES ON DATABASE summit_db TO summit_db_user;
```

To exit psql and the 'postgres' user:

```
\q
exit
```

### Download repo and update Git config

#### SSH key
Each user needs to have an SSH key for auth. Instead of the classic username and password combo, we use SSH auth. Please talk to Joseph Remy - remy@nau.edu if you do not have an SSH key.

First, download the SSH key from the email Joseph sent you and unlock the id_rsa file with the password he has provided (probably over Discord). I suggest you extract it to the Desktop or Home directory.

Next, after extracting your private key (id_rsa), you will need to move it into the hidden .ssh directory under ~/ (Home directory on Ubuntu for summit, should be /home/summit/.ssh/). Open a Terminal window to do this and navigate to where you extracted your private key. For this example, I've extracted it to the Desktop.

```
cd ~/Desktop
ls # To confirm you extracted it here
mv id_rsa ~/.ssh/
```

Lastly, you will need to change the file permissions for your private key. Otherwise, the BitBucket server/Git will reject your SSH requests. Go to Terminal and type the following:

```
sudo chmod 0700 ~/.ssh/id_rsa
```

If you have multiple private keys, for other things, just copy the contents of the extracted id_rsa into the existing one with an append.

#### Cloning the repo

First, go to the Bitbucket server and get the Clone URL for SSH. Note the dropdown for HTTPS and SSH. The SSH url should start with "ssh://git@...".

Next, open up Terminal and navigate to somewhere to store the repo. I suggest following these instructions.

```
cd ~/Desktop
git clone <URL> ./<REPO-NAME>
```

Lastly, after cloning the repo, go ahead and make sure everything works with a git status.

```
cd <REPO-NAME>/
git status
```

#### Updating the repo config

To make your commits unique to you and have the same template as the rest of the team, please run the following commands inside the repo:

```
git config commit.template _repo/commitTemplate
git config user.email "<YOUR EMAIL>"
git config user.name "<YOUR NAME>"
```

### Starting development environment

First, before you begin coding, you must ALWAYS be in dev virtual environment. This is required so that there are two different views to this application: development and production.

Check if the folder "venv-dev" exists. If it does, skip to the next heading. If it does not, follow these instructions below:

First, make sure you are in the repo root directory. Next, follow this command to make a dev virtual environment.

```
virtualenv ./venv-dev -p /usr/bin/python3
```

#### Activating environment

Call the following commands to start the virtual environment and update it with our current packages:

```
source ./venv-dev/bin/activate
pip install -r requirements/local.txt
```


#### Prepros compiler

If you are working on any of the static files, namely the CSS and JavaScript, you will need to run Prepros to compile them. This helps allow us the break down our files in a tiered way that helps with the overall organization and maintainability of the project.

To run Prepros, just click on the icon in the dock. Next, if the project doesn't appear, open the repo in Files and navigate to the project root (where manage.py exists). Next, open "summit" and you should see the "static" folder. Drag and drop this into Prepros and it'll automatically start running and compiling files.

*Presently, this system is only for global CSS and JS. We are working on a way to do per-app that overrides the global files.*


#### Init project (if not done prior)

Do these commands to init the project after cloning. Not required if done previously.

```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```


#### Deactivating environment

When you are done, just deactivate the environment.

```
deactivate
```



### Starting production environment

When you are ready to try running your repo in a production environment, it is similar to the dev environment: it requires a couple of lines of commands and you will be good to go!

Check if the folder "venv-production" exists. If it does, skip to the next heading. If it does not, follow these instructions below:

First, make sure you are in the repo root directory. Next, follow this command to make a production virtual environment.

```
virtualenv ./venv-production -p /usr/bin/python3
```

#### Activating environment

Call the following commands to start the virtual environment and update it with our current packages:

```
source ./venv-production/bin/activate
pip install -r requirements/production.txt
```


#### Running the server in production mode

Now that are you are ready to try out the production side, go ahead and run Gunicorn, the WSGI software for this Django project:

For local host testing:

```
gunicorn config.wsgi:application
```

For allowing all connections (testing with external devices):

```
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

To connect with an external device, just open Terminal and type:

```
ifconfig
```

Next, grab that IP address and put it into the browser and add ":8000" to the end. Example:

```
http://192.168.0.2:8000
```

This will only work on a local network unless you have done all of the necessary things to make it WAN accessible.

#### Deactivating environment

When you are done, just deactivate the environment.

```
deactivate
```
