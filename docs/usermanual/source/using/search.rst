Search for music
================

You can search the entire server music collection by using the search
box located on all pages in the :doc:`web interface </using/interface>`.

Type in a couple of characters and press :kbd:`Enter` to get a page with
search results. Tracks which match your queries can be played directly
from the search results page. Artist and album information can be
viewed by clicking on the links.

Advanced usage
--------------

You can search on specific criteria to search for by using
special operators. For example, to search for an artist called **Stars**
rather than artists and albums, type in::

    artist:Stars

To view songs by **Arcade Fire** which contain the word **car**::

    artist:"Arcade Fire" title:car

Notice how **Arcade Fire** was surrounded by quotes. You should surround
a query in quotes when it is more than one word. The query::

    artist:Arcade Fire

would instead search for artists having **Arcade** in their name, and filtering
that by any tracks or albums having the term **Fire**.

The following operators are supported:

* `artist:`
* `album:`
* `title:`
* `genre:`
* `year:`

Note that the default search (without any operator) will only search in artist,
album and track names, not genres or other criteria. Also, search results match
*all* search terms, and not each one individually. Search is also
*case-insensitive* which means that "RADIOHEAD" and "radiohead" mean the same
thing.
