# Python Simple Server  <!-- omit in toc -->


# Table of Contents  <!-- omit in toc -->
- [Introduction](#introduction)
- [Python](#python)
- [Flask](#flask)
- [PyCharm](#pycharm)
- [Python Linting](#python-linting)
- [Testing](#testing)
- [Python REPL](#python-repl)
- [Logging](#logging)
- [Readability](#readability)
- [Productivity](#productivity)
- [Performance](#performance)


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


# PyCharm

I use [PyCharm](https://www.jetbrains.com/pycharm) for Python programming. PyCharm is really good IDE for Python programming - the editor is great and there are a lot of utilities that make your Python programming more productive (code completion, test runners, automatic linter ([PEP](https://www.python.org/dev/peps/pep-0008/)) etc). 

I use [IntelliJ IDEA](https://www.jetbrains.com/idea/) for Java programming and since PyCharm and IDEA are provided by the same company (JetBrains) they provide very similar look-and-feel. I also use IntelliJ IDEA with [Cursive](https://cursive-ide.com/) plugin for Clojure programming and it also provides very similar look-and-feel. So, there are a lot of synergy benefits to use the same IDE for several programming languages.


# Python Linting

[PEP8](https://www.python.org/dev/peps/pep-0008/) provides a definitive style guide for Python programming. PyCharm provides nice automatic linting of Python code related to this style guide.


# Testing

Run the tests in console:

```bash
./run-pytest.sh
```

The tests are implemented using [pytest](https://docs.pytest.org/en/latest/). Pytest is pretty straightforward to use and PyCharm also provides nice integration to unit tests implemented using pytest (debugger etc.). In PyCharm just create a new pytest configuration and configure it to use your specific pytest file and you are good to go to run that test and the code it calls in your debugger.


# Python REPL

Python REPL is one of the best REPLs I have used outside the Lisp world. In the Lisp world REPLs are real REPLs which allow you to experiment with the live system in ways that no other REPL or debugger lets you do in other languages - it's pretty impossible to explain this, you just have to learn some Lisp and try yourself (e.g. [Clojure](https://clojure.org/)). So, now that we have gone through my mandatory Clojure advertisement let's go back to Python REPL. Compared to JShell Java REPL Python wins the fight hands down. Python REPL came with the first version of Python (we just had to wait some 20 years for Java REPL) and because Python is dynamically typed language the REPL is pretty easy to use (compared to Java JShell which is really awkward to use, even with a good IDE). 

PyCharm provides a nice REPL, an example follows:

```python
 >>> runfile('/mnt/edata/aw/kari/github/python/webstore-demo/simple-server/simpleserver/domaindb/domain.py', wdir='/mnt/edata/aw/kari/github/python/webstore-demo/simple-server')
>>> myD = Domain()
2018-10-30 18:40:11,769 - __main__ - __init_product_db - DEBUG - ENTER
2018-10-30 18:40:11,770 - __main__ - __read_product_groups - DEBUG - ENTER
...
2018-10-30 18:40:11,771 - __main__ - __read_raw_products - DEBUG - EXIT
2018-10-30 18:40:11,771 - __main__ - __init_product_db - DEBUG - EXIT
>>> myD.get_raw_products(1)
[['2001', '1', 'Kalevala', '3.95', 'Elias Lönnrot', '1835', 'Finland', 'Finnish'], ...]
```

So, using the runfile method you are able to reload any module to Python console and then try the methods there in isolation.

# Logging

What a relief Python logging configuration is after Spring hassle. You just create the [logging.conf](TODO) file and that's about it. I created a [SSLogger](TODO) class so that using logging in various python modules would be coherent.

# Readability

Python wins Javascript in readability hands down. It is probably the most readable language there is. I would say that it is even more readable than Clojure which is also very readable language (once you get used to read a functional language). Java also loses to Python in readability just because Java is such a verbose language which really makes readability a major issue.

# Productivity

What a joy it was to program Python after Java. Dynamically typed language! Concise! Clear syntax! Simple! The productivity of Python programming compared to Java is like from another planet - I explored PyCharm new features and Flask the first evening and in the second evening I implemented the domaindb module and most of the userdb module and related unit tests. 

The Python (and especially PyCharm) **REPL** is definitely the best REPL I have used outside Lisp world. 

Using PyCharm debugger is also so stream-lined and fast that if you have even minor issues in your code you tend to add a breakpoint and hit the debugger. This is actually pretty interesting since in the Lisp world you hardly ever use the debugger - you tend to have a live REPL to your system while you add new functionalities to the system. You can't have a live REPL to your Python system in the same sense but PyCharm debugger is a pretty good second option. And when you compare Python debugger to Java debugger - Python is lightning fast to start. Creating Run configurations for your unit tests in PyCharm is also very easy and straightforward. PyCharm debugger is also a great tool to check what's inside various entities (e.g. I just used the debugger to check where the http status code is inside the Flask response entity and what is its name) - if you are lazy to search that information in library API documentation.

In general I think Python must be the most productive language I have ever used. Clojure might win the case in productivity after a couple of years of serious Clojure hacking but Python is unbeatable in the scripting category - you may have months of gaps between your Python hacking sessions but the language is always easy to put in real work regardless how long it was you programmed Python the last time.

If you compare Python to Java Python wins hands down. Java is verbose - Python is concise. Java has long development cycle (edit, compile, build, load to JVM, run) - Python has short development cycle (edit, run). Java has difficult syntax - Python has very easy syntax.

If you compare Python to Javascript/Node, Python wins in clean syntax and overall easyness to create and test code. 

There is nothing inherently bad in Python. I would be cautious to use Python in a big project with tens of developers working in the same code base unless you have some strict rules how to protect collaboration from the typical mistakes using dynamically typed language in a big project (e.g. mandatory use of [type hints](https://docs.python.org/3/library/typing.html)). 


# Performance

The [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) might cause some issues if you try to create a system which should be responsive to a large amount of events / sessions. Node is also single-threaded but Node has a special architecture in which Node runs single thread in an event loop and delegates e.g. I/O work to worker pool threads. This makes Node extremely efficient in handling tasks which are not CPU intensive (on the other side CPU intensive tasks may degrade the Node performance quite a lot). Java system on the contrary typically spins a dedicated thread for each request. This is more expensive (consumes more machine resources) but one thread (for one client) does not block processing of another thread (client). Python has the infamous Global Interpreter Lock which has generated a lot of debate in the Python community during Python's lifetime. In most cases this is not a problem since you usually use Python for small tasks. But if you use Python for CPU intensive work handling a huge set of tasks or requests in parallel you have to find some special solutions for it (and those do exists if you google them, see e.g. ["Efficiently Exploiting Multiple Cores with Python"](http://python-notes.curiousefficiency.org/en/latest/python3/multicore_python.html)).


