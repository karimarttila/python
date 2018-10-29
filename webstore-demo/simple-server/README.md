# Python Simple Server  <!-- omit in toc -->


# Table of Contents  <!-- omit in toc -->
- [Introduction](#introduction)
- [Python](#python)
- [Flask](#flask)


# Introduction


# Python

I was using Python 3.6.6 on Ubuntu18 when implementing this Simple Server. I used Python virtual environment to keep my Ubuntu installation clean:

```bash
python3 --version                    => Check your Python version (mine was 3.6.6).
virtualenv --version                 => Check your virtual env version (mine was 16.0.0).
which python3                        => Where is python3? (mine is in /usr/bin/python3).
virtualenv -p /usr/bin/python3 venv  => Create the virtual env.
source venv/bin/activate             => Activate your virtual env
python3 --version?                   => Python 3.6.6 (in this virtual envinronment).
pipenv install flask                 => Use pipenv to install packages.
ls -l Pipfile*                       => List the generated Pipfile(s).
deactivate                           => Leave the virtual environment.
```

And so we finalized our short tour to "Python virtual environment and package management.

# Flask

I decided to use [Flask](http://flask.pocoo.org/) since it is widely-used Python microframework. 

First source the setenv.sh file:

```bash
source ./setenv.sh
```

This sets some environment variables that Flask needs. 

Then run the app:

```bash
./flask-run.sh
```

Open browser in http://localhost:4046 and you should see the index.html file.

