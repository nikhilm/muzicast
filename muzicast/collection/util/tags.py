# Important constants for tag handling.

# Every tag should be listed here, as the canonical translation copy.
# If machine is true, then the tag will not appear in some contexts,
# as it is not intended to be human-readable.  If internal is true,
# the tag will not show up for editing, as it is generated internally
# by Quod Libet.

def T(name, translation, machine=False, internal=False):
    return (name, (translation, machine, internal))

def MT(name, translation, internal=False):
    return T(name, translation, machine=True, internal=internal)

def IT(name, translation, machine=False):
    return T(name, translation, machine=machine, internal=True)

# Fake out gettext for some convenience.
def N_(name):
    return T(name, name)

TAGS = dict([
    N_("album"),
    N_("arranger"),
    N_("artist"),
    N_("author"),
    N_("composer"),
    N_("conductor"),
    N_("contact"),
    N_("copyright"),
    N_("date"),
    N_("description"),
    N_("genre"),
    N_("grouping"),
    N_("language"),
    N_("license"),
    N_("location"),
    N_("lyricist"),
    # Translators: Also e.g. "record label", "publisher"
    N_("organization"),
    N_("performer"),
    N_("title"),
    N_("version"),
    N_("website"),

    T("albumartist", ("album artist")),
    T("bpm", ("BPM")),
    T("isrc", "ISRC"),
    # Translators: This used to be called "part".
    T("discsubtitle", ("disc subtitle")),
    T("part", ("disc subtitle")),
    T("discnumber", ("disc")),
    T("tracknumber", ("track")),
    T("labelid", ("label ID")),
    T("originaldate", ("original release date")),
    T("originalalbum", ("original album")),
    T("originalartist", ("original artist")),
    T("recordingdate", ("recording date")),
    T("releasecountry", ("release country")),
    T("albumartistsort", ("album artist (sort)")),
    T("artistsort", ("artist (sort)")),
    T("albumsort", ("album (sort)")),
    T("performersort", ("performer (sort)")),
    T("performerssort", ("performers (sort)")),

    # http://musicbrainz.org/doc/MusicBrainzTag

    MT("musicbrainz_trackid", ("MusicBrainz track ID")),
    MT("musicbrainz_albumid", ("MusicBrainz release ID")),
    MT("musicbrainz_artistid", ("Musicbrainz artist ID")),
    MT("musicbrainz_albumartistid", ("MusicBrainz album artist ID")),
    MT("musicbrainz_trmid", ("MusicBrainz TRM ID")),
    MT("musicip_puid", ("MusicIP PUID")),
    MT("musicbrainz_albumstatus", ("MusicBrainz album status")),
    MT("musicbrainz_albumtype", ("MusicBrainz album type")),

    # Translators: "gain" means a volume adjustment, not "to acquire".
    MT("replaygain_track_gain", ("track gain")),
    MT("replaygain_track_peak", ("track peak")),
    # Translators: "gain" means a volume adjustment, not "to acquire".
    MT("replaygain_album_gain", ("album gain")),
    MT("replaygain_album_peak", ("album peak")),
    MT("replaygain_reference_loudness", ("reference loudness")),

    IT("added", ("added")),
    IT("lastplayed", ("last played")),
    IT("disc", ("disc")),
    IT("discs", ("discs")),
    IT("track", ("track")),
    IT("tracks", ("tracks")),
    IT("laststarted", ("last started")),
    IT("filename", ("full name")),
    IT("basename", ("filename")),
    IT("dirname", ("directory")),
    IT("mtime", ("modified")),
    IT("playcount", ("plays")),
    IT("skipcount", ("skips")),
    IT("uri", "URI"),
    IT("mountpoint", ("mount point")),
    IT("errors", ("errors")),
    IT("length", ("length")),
    IT("people", ("people")),
    IT("performers", ("performers")),
    IT("rating", ("rating")),
    IT("year", ("year")),
    IT("bookmark", ("bookmark")),
    ])

def add(tag, translation):
    TAGS[tag] = (translation, False, False)

def readable(tag):
    try:
        if tag[0] == "~":
            if tag[1] == "#": tag = tag[2:]
            else: tag = tag[1:]
    except IndexError: return ("Invalid tag")
    else: return TAGS.get(tag, (tag,))[0]

STANDARD_TAGS = [key for key in TAGS if not (TAGS[key][1] or TAGS[key][2])]
MACHINE_TAGS = [key for key in TAGS if TAGS[key][1]]
del(key)

