Linux
=====

.. todo:: Put download URL

First download Muzicast for Linux from

Installation on Linux depends on your distribution.
Muzicast requires the following additional packages to
be installed.

* Python 2.6 or later
* setuptools
* gevent 0.13.0 or later
* gunicorn 0.11.0 or later

Installing Muzicast on Debian
--------------------------------

#. Install the required packages

.. parsed-literal::

    sudo apt-get install python python-setuptools python-gevent gunicorn

#. Install Muzicast

.. parsed-literal::

    tar zxvf Muzicast-|release|.tar.gz
    cd Muzicast-|release|
    sudo python setup.py install

To run Muzicast, see the :doc:`/quickstart`.

Installing Muzicast on Fedora/Redhat
---------------------------------------

.. todo:: check package names

#. Install the required packages

.. parsed-literal::

    sudo yum install python python-setuptools python-gevent gunicorn

#. Install Muzicast

.. parsed-literal::

    tar zxvf Muzicast-|release|.tar.gz
    cd Muzicast-|release|
    sudo python setup.py install

You may now proceed to the :doc:`/quickstart`.

Installing Muzicast on Archlinux
-----------------------------------

.. todo:: Provide AUR package

Archlinux has a `AUR <http://aur.archlinux.org>`_ PKGBUILD available which will create a package.

`Download <http://aur.archlinux.org>`_ the PKGBUILD and save it to
`/tmp/Muzicast/` then run

.. parsed-literal::
    
    cd /tmp/Muzicast
    makepkg
    pacman -U Muzicast-|release|.pkg.tar.xz

See the :doc:`/quickstart` for setting up Muzicast.
