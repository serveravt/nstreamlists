# coding=UTF-8
import sys
import codecs
import xml.etree.cElementTree as ET
import urllib. string


class track():
    def __init__(self,  title, path):
        self.title = title
        self.path = path

"""
    format
    EXTINF:bla bla bla ,Alice In Chains - Rotten Apple
    http://192.168.1.203:8000/pid/a200b433ed7efbf3073c18a4a84bc2c0cadc3425/stream.mp4
"""

def parsem3u(infile):
    try:
        assert(type(infile) == '_io.TextIOWrapper')
    except AssertionError:
        infile = codecs.open(infile,'r', "utf-8")

    """
        All M3U files start with #EXTM3U.
        If the first line doesn't start with this, we're either
        not working with an M3U or the file we got is corrupted.
    """

    line = infile.readline()
    if not line.startswith('#EXTM3U'):
       return

    # initialize playlist variables before reading file
    playlist=[]
    song=track(None,None)

    for line in infile:
        line=line.strip()
        if line.startswith('#EXTINF:'):
            # pull length and title from #EXTINF line
            title=line.split('#EXTINF:')[1].split(',',1)[1];
            song=track(title,None)
        elif (len(line) != 0):
            # pull song path from all other, non-blank lines
            song.path=line
            playlist.append(song)
            # reset the song variable so it doesn't use the same EXTINF more than once
            song=track(None,None)

    infile.close()

    return playlist




"""
    <channel>
    <title><![CDATA[ирония]]></title>
    <stream_url>http://www.ex.ua/load/217109298</stream_url>
    <description><![CDATA[Home Media Online]]></description>
    <category_id>1</category_id>
    </channel>
"""

def saveAsXML(playlist):
    items = ET.Element("items")
    playlist_name = ET.SubElement(items, "playlist_name").text = "Playlist name"

    for track in playlist:
        channel = ET.SubElement(items, "channel")
        ET.SubElement(channel, "title").text = track.title
        ET.SubElement(channel, "stream_url").text = track.path
        ET.SubElement(channel, "description").text = track.title
        ET.SubElement(channel, "category_id").text = "1"

    tree = ET.ElementTree(items)
    tree.write("output.xml", encoding="UTF-8", xml_declaration=True)

def downloadNewList():
    urllib.urlretrieve("http://192.168.1.203:8000/torrent-telik", "list.m3u")

def convert():
    # m3ufile=sys.argv[1]
    downloadNewList()
    m3ufile = "list.m3u"
    playlist = parsem3u(m3ufile)
    saveAsXML(playlist)

# for now, just pull the track info and print it onscreen
# get the M3U file path from the first command line argument
def main():
   convert()


if __name__ == '__main__':
    main()