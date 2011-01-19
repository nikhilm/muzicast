Linux
=====

.. todo:: Put download URL

First download ProjectName for Linux from

Installation on Linux depends on your distribution.
ProjectName requires the following additional packages to
be installed.

* Python 2.6 or later
* setuptools
* gevent 0.13.0 or later
* gunicorn 0.11.0 or later

Installing ProjectName on Debian
--------------------------------

#. Install the required packages

.. parsed-literal::

    sudo apt-get install python python-setuptools python-gevent gunicorn

#. Install ProjectName

.. parsed-literal::

    tar zxvf ProjectName-|release|.tar.gz
    cd ProjectName-|release|
    sudo python setup.py install

To run ProjectName, see the :doc:`/quickstart`.

Installing ProjectName on Fedora/Redhat
---------------------------------------

.. todo:: check package names

#. Install the required packages

.. parsed-literal::

    sudo yum install python python-setuptools python-gevent gunicorn

#. Install ProjectName

.. parsed-literal::

    tar zxvf ProjectName-|release|.tar.gz
    cd ProjectName-|release|
    sudo python setup.py install

You may now proceed to the :doc:`/quickstart`.

Installing ProjectName on Archlinux
-----------------------------------

.. todo:: Provide AUR package

Archlinux has a `AUR <http://aur.archlinux.org>`_ PKGBUILD available which will create a package.

`Download <http://aur.archlinux.org>`_ the PKGBUILD and save it to
`/tmp/ProjectName/` then run

.. parsed-literal::
    
    cd /tmp/ProjectName
    makepkg
    pacman -U ProjectName-|release|.pkg.tar.xz

See the :doc:`/quickstart` for setting up ProjectName.
