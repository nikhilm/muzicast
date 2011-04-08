Quickstart
==========

Once you have :doc:`installed </installation>` Muzicast, you are ready to
start streaming music as soon as you set a few things.

First lets start Muzicast. On Windows go to the :menuselection:`Start -->
Programs --> Muzicast --> Start Muzicast`.

On Linux you should run :command:`muzicast` from the terminal.

Now point your web browser to http://127.0.0.1:7664/. You should see the
Muzicast first run wizard.

.. image:: /_static/screenshots/firstrun.png

Muzicast is all set up. Click continue, you are now at the adminstration
interface.

.. _set-admin-password:

Setting the Administrator Password
----------------------------------

Enter a password which will be used to change any server settings

.. warning::

   The Administrator Password allows you to change any settings of your server.
   You should keep it safe and ensure that no one else knows it.

Enter a password and click 'Change password'.

Adding the list of music directories
------------------------------------

Muzicast will scan a list of directories for all your music.
In this stage you should mark which directories should be scanned.
Note that Muzicast is intelligent enough to scan directories below the
specified directory. For example if you specify :file:`D:\\My Music` then
Muzicast will also look for music in :file:`D:\\My Music\\Arcade Fire` and
:file:`D:\\My Music\\Jazz`, so you only need to specify top level directories.
You can use the little arrows to the left of the checkboxes to open and close
a directory.

.. image:: /_static/screenshots/dirlist.png

Muzicast will show you a directory tree as shown in the screenshot. To add
a directory, simply tick the checkbox next to it.

.. image:: /_static/screenshots/dirlist_checked.png

Once you are done, click :guilabel:`Save` and Muzicast is ready to go.
You may edit this at any time
by visiting the :doc:`Administration </administration>` area.

Play a song
-----------

Once the setup is done, you can click :guilabel:`Back to Music` at the top of
the screen to reach the Muzicast web interface. Here you
can see the artists, albums and tracks. To play a track,
simply click the song title. The embedded flash player on that page will start
playing the song.

.. note::

    Muzicast can take some time to scan all of your music.
    If you can't see any tracks immediately after installation
    please wait for some time then refresh the page.

To create playlists or listen to songs in your favourite music player, :doc:`read on </using>`.
