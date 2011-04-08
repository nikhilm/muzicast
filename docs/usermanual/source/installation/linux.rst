Linux
=====

First download Muzicast for Linux from
`the Muzicast homepage <https://github.com/nikhilm/muzicast/downloads>`_.

Installation on Linux depends on your distribution.
Muzicast requires the following additional packages to
be installed.

* Python 2.6 or later
* setuptools
* watchdog
* flask
* pylast
* sqlobject
* blinker
* jinja2

and their related dependencies. All of them should be easy installable using
the package manager.

Installing Muzicast on Debian
--------------------------------

#. Install the required packages

.. parsed-literal::

    sudo apt-get install python python-pip
    sudo pip install watchdog flask pylast sqlobject blinker jinja2

#. Install Muzicast

.. parsed-literal::

    tar zxvf muzicast-|release|.tar.gz
    cd muzicast-|release|
    sudo python setup.py install

To run Muzicast, see the :doc:`/quickstart`.

Installing Muzicast on Fedora/Redhat
---------------------------------------

#. Install the required packages

.. parsed-literal::

    sudo yum install python python-pip
    sudo pip install watchdog flask pylast sqlobject blinker jinja2

#. Install Muzicast

.. parsed-literal::

    tar zxvf muzicast-|release|.tar.gz
    cd muzicast-|release|
    sudo python setup.py install

You may now proceed to the :doc:`/quickstart`.

Installing Muzicast on Archlinux
-----------------------------------

.. parsed-literal::

    su
    (As root)
    # pacman -S python-pip
    # pip install watchdog flask pylast sqlobject blinker jinja2

.. parsed-literal::
    
    tar zxvf muzicast-|release|.tar.gz
    cd muzicast-|release|
    sudo python setup.py install

See the :doc:`/quickstart` for setting up Muzicast.
