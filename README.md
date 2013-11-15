pysc
====

[Soundcloud](http://www.soundcloud.com/) in your terminal  
**pysc** is a command-line repl interface to Soundcloud.

Installation
------------
To install **pysc**, simply:  

    pip install pysc

Or if you're not hip to the pip:

    easy_install pysc

Remember that you need to be connected to internet, unless you have a playlist of downloaded songs.

Features
--------

* **Music**
  * List of all music genres available
  * Simple navigation using *next* and *prev*
  * Sound player *pause*/*resume* options
  * Download of Soundcloud downloadable tracks


* **Playlists**
  * Playlists management

Usage
-----

Firstly, let you know about the *settings.py* file. Only two constants are setted up there, they are:  

    CLIENT_ID = '43b1906ada38f27c8e864c07de04b7b7'
    TRACKS_PER_PAG = 50

CLIENT\_ID is just the **pysc** app id inside Soundcloud, you can change it to another app id, but it's pointless. And care if you change it, the id *must be* recognized by Sondcloud, or **pysc** won't be able to use its *api*.  

TRACKS\_PER\_PAG is the number of tracks that will be load in each request. You can set whatever you want in there, **pysc** will deal with pagination for you, just don't set it to **0**.  
It just means telling **pysc** *~create a new request to Soundcloud in every X tracks listened~*.

To run the **pysc** repl, just type `pysc`

Basic example
-------------
>**$ pysc**  
>*welcome to pysc! sound cloud in your terminal ~ powered by soundcloud*  
>*type 'genres' to discover, or just 'help' to see available commands*  
>**&gt;&gt;&gt; genres**  
>*80s ~ Abstract ~ Acid Jazz ~ Acoustic ~ Acoustic Rock ~ African ~ Alternative ~ Ambient ~ Americana ~ Arabic ~ Avantgarde ~ Bachata ~ Ballads ~ Bhangra ~ Blues ~ Blues Rock ~ Bossa Nova ~ Breakbeats ~ Chanson ~ Chillout ~ Chiptunes ~ Choir ~ Classic Rock ...*  
>**&gt;&gt;&gt; play chillout**  
>*gettings tracks...*  
>*now playing 'Heso - Between Space and Time'*  
>**&gt;&gt;&gt; next**  
>*now playing 'Slipstream'*  
>**&gt;&gt;&gt; prev**  
>*now playing 'Heso - Between Space and Time'*

Commands
--------
* **Core**
  * **help**  
    *List all available commands*
  * **about**  
    *See about text*
  * **exit**  
    *Exit pysc*
* **Music**
  * **genres**  
    *List all music genres*
  * **play &lt;genre&gt;**  
    *Play genre, for example: play chillout*
  * **pause, resume**  
    *Pause or resume the sound player*
  * **prev, next**  
    *Go prev or next track*
  * **prevpage, nextpage**
    *Go prev or next page of tracks*
  * **loop, unloop**  
    *Loop or unloop current track*
  * **seek &lt;seconds&gt;**
    *Seek for a track time
  * **forwards &lt;seconds&gt;**  
    *Go forwards*
  * **backwards &lt;seconds&gt;**  
    *Go backwards*
  * **volume &lt;number&gt;**  
    *Manage volume level*

*Other commands will be available soon*.

Contribute
----------
Fork it and send your pull request, i'll be happy to add your ideas!

License
-------
**pysc** is licensed under MIT license.  
Check it [here](https://github.com/ramonsaraiva/pysc/blob/master/LICENSE).
