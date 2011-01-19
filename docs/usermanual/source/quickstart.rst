Quickstart
==========

Once you have :doc:`installed </installation>` ProjectName, you are ready to
start streaming music as soon as you set a few things.

First lets start ProjectName. On Windows go to the :menuselection:`Start -->
Programs --> ProjectName --> Start ProjectName`.

.. note::

    On windows, the installer will launch the browser itself. Windows
    users may
    skip to :ref:`the next section <set-admin-password>` if they have just
    installed ProjectName.

On Linux you may invoke ProjectName from your desktop environment's menu
or run :command:`ProjectName` from the terminal.

Now point your web browser to http://localhost:4000/admin. You should see the
ProjectName first run wizard.

.. todo:: Insert screenshot

.. _set-admin-password:

Setting the Administrator Password
----------------------------------

Enter a password which will be used to change any server settings

.. IMPORTANT::

   The Administrator Password allows you to change any settings of your server.
   You should keep it safe and ensure that no one else knows it.

Adding the list of music directories
------------------------------------

ProjectName will scan a list of directories for all your music.
In this stage you should mark which directories should be scanned.
Note that ProjectName is intelligent enough to scan directories below the
specified directory. For example if you specify :file:`D:\\My Music` then
ProjectName will also look for music in :file:`D:\\My Music\\Arcade Fire` and
:file:`D:\\My Music\\Jazz`, so you only need to specify top level directories.

.. todo:: Insert screenshot

ProjectName will show you a directory tree as shown in the screenshot. To add
a directory, simply tick the checkbox next to it.

.. todo:: tick screenshot

Once you are done, ProjectName is ready to go.
You may edit these and other settings any time later
by visiting the :doc:`Administration </administration>` area.

Click on the :guilabel:`Finish` button to start ProjectName.
ProjectName is now ready to go.

Play a song
-----------

Once the setup is done, you should not be at the ProjectName home screen. You
can see the artists, albums and tracks. To play a track,
simply click the arrow next to it.

To create playlists or listen to songs in your favourite music player, :doc:`read on </using>`.
