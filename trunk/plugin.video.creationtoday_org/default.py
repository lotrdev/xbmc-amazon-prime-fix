import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
import os
import re
import string
import sys
from addon import Addon
from net import Net
import urlresolver


addon = Addon('plugin.video.creationtoday_org', sys.argv)
net = Net()

base_url = 'http://www.creationtoday.org'

play = addon.queries.get('play', None)


def MAIN():
	addDir('Creation Today Show', 'http://feeds.drdino.com/csepodcast?format=xml',4,'')	
	addDir('Creation Minute', 'https://www.youtube.com/playlist?list=PLvFrrGonrTSOO8_ZtChPQrBxx4MSla9Qb',2,'')
	addDir('Creation Bytes', 'https://www.youtube.com/playlist?list=PLA2805B73D20F70D3',2,'')
	addDir('Creation Seminars', 'https://www.youtube.com/playlist?list=PL6-cVj-ZRivqKeqAklhYfFFmmAdvwcnCT',2,'')	
	addDir('Debates', 'https://www.youtube.com/playlist?list=PL6-cVj-ZRivpHQhRLUXmLV3nxZ_kWtND-',2,'')	

##################################################################################################################################

def ADDLINKS(url):
	link = getUrl(url)
	match=re.compile('<span class="title"><a href="(.+?)"').findall(link)
	title=re.compile('<span class="title"><a href=".+?" rel="bookmark" title=".+?">(.+?)</a></span>').findall(link)
	thumb=re.compile('<img src="(.+?)" width="150" height="94" alt="" />').findall(link)
	mylist=zip((match),(title),(thumb))
	for url,title,thumb in mylist:
		title=title.replace("&#8211;","-")
		title=title.replace("&#8217;","\'")
		addDir(title, url, 10, thumb)

##################################################################################################################################

def ADDLINKS_Youtube_Playlist(url):
	link = getUrl(url)
	match=re.compile('<a href=.+?watch\?v=(.+?)&amp.+?class="yt-uix-sessionlink"').findall(link)
	title=re.compile('<a href=.+?watch.+?title="(.+?)" class="yt-uix-sessionlink"').findall(link)
	mylist=zip((match),(title))
	for match,title in mylist:
		thumb = "http://img.youtube.com/vi/"+match+"/0.jpg"
		title=title.replace("&#8211;","-")
		title=title.replace("&#8217;","\'")
		addon.add_video_item({'url': 'http://www.youtube.com/watch?v=' + match},{'title': title},img=thumb)

##################################################################################################################################

def ADDLINKS_Creation_Today(url):
	link = getUrl(url)
	match=re.compile('<media:content url="http://player.vimeo.com/external/(.+?).sd').findall(link)
	title=re.compile('<title>(.+?)</title>').findall(link)
	del title[0]
	del title[0]
	del title[len(title)-1]
	del match[len(match)-1]
	mylist=zip((match),(title))
	for url,title in mylist:
		title=title.replace("&#8211;","-")
		title=title.replace("&#8217;","\'")
		addon.add_video_item({'url': 'http://www.vimeo.com/' + url},{'title': title})
	url='https://www.youtube.com/playlist?list=PLvFrrGonrTSNru0E3AEhBTTAsOvPxK5Q8'
	link = getUrl(url)
	match=re.compile('<a href=.+?watch\?v=(.+?)&amp.+?class="yt-uix-sessionlink"').findall(link)
	title=re.compile('<a href=.+?watch.+?title="(.+?)" class="yt-uix-sessionlink"').findall(link)
	mylist=zip((match),(title))
	for match,title in reversed(mylist):
		thumb = "http://img.youtube.com/vi/"+match+"/0.jpg"
		title=title.replace("&#8211;","-")
		title=title.replace("&#8217;","\'")
		addon.add_video_item({'url': 'http://www.youtube.com/watch?v=' + match},{'title': title},img=thumb)
	url='https://www.youtube.com/playlist?list=PLvFrrGonrTSORF70pT4NyrLNVDfWZE4hu'
	link = getUrl(url)
	match=re.compile('<a href=.+?watch\?v=(.+?)&amp.+?class="yt-uix-sessionlink"').findall(link)
	title=re.compile('<a href=.+?watch.+?title="(.+?)" class="yt-uix-sessionlink"').findall(link)
	mylist=zip((match),(title))
	for match,title in reversed(mylist):
		thumb = "http://img.youtube.com/vi/"+match+"/0.jpg"
		title=title.replace("&#8211;","-")
		title=title.replace("&#8217;","\'")
		addon.add_video_item({'url': 'http://www.youtube.com/watch?v=' + match},{'title': title},img=thumb)
	url='https://www.youtube.com/playlist?list=PLA5F3E0C0A891053E'
	link = getUrl(url)
	match=re.compile('<a href=.+?watch\?v=(.+?)&amp.+?class="yt-uix-sessionlink"').findall(link)
	title=re.compile('<a href=.+?watch.+?title="(.+?)" class="yt-uix-sessionlink"').findall(link)
	mylist=zip((match),(title))
	for match,title in reversed(mylist):
		thumb = "http://img.youtube.com/vi/"+match+"/0.jpg"
		title=title.replace("&#8211;","-")
		title=title.replace("&#8217;","\'")
		addon.add_video_item({'url': 'http://www.youtube.com/watch?v=' + match},{'title': title},img=thumb)



if play:
	url = addon.queries.get('url', '')
	host = addon.queries.get('host', '')
	media_id = addon.queries.get('media_id', '')
	#stream_url = urlresolver.resolve(play)
	stream_url = urlresolver.HostedMediaFile(url=url, host=host, media_id=media_id).resolve()
	addon.resolve_url(stream_url)

##################################################################################################################################

def getUrl(url):
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link

##################################################################################################################################

def GETSOURCE(url,name,iconimage):
	link = getUrl(url)
	match=re.compile('<iframe src="http://player.vimeo.com/video/(.+?)title').findall(link)
	site=0
	if len(match)==0:
		match=re.compile('src=".+?www.youtube.+?embed/(.+?)\?rel').findall(link)
		site=1
	if len(match)==0:
		match=re.compile('src=".+?www.youtube.+?embed/(.+?)"').findall(link)
		site=1
	match=match[0]
	if site==0:
		match=addon.resolve_item({'url': 'http://www.vimeo.com/' + match})
	if site==1:
		match=addon.resolve_item({'url': 'http://www.youtube.com/watch?v=' + match})
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "title": name} )
	xbmc.Player().play(match,liz)
	xbmc.sleep(2500)
	while xbmc.Player().isPlaying():
		xbmc.sleep(250)
	xbmc.Player().stop()
	sys.exit()
  
##################################################################################################################################

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
##################################################################################################################################
	

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

##################################################################################################################################

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

##################################################################################################################################
        
              
params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        MAIN()
       
elif mode==1:
        print ""+url
        ADDLINKS(url)
        
elif mode==2:
        print ""+url
        ADDLINKS_Youtube_Playlist(url)

elif mode==3:
        print ""+url
        ADDLINKS_Youtube_Playlist(url)

elif mode==4:
        print ""+url
        ADDLINKS_Creation_Today(url)

elif mode==5:
        print ""+url
        PROGRAMS(url)

elif mode==6:
        print ""+url
        RECENT(url)

elif mode==7:
        print ""+url
        LIVE(url)

elif mode==8:
        print ""+url
        SEARCH(url)

elif mode==9:
        print ""+url
        AIRDATE(url)

elif mode==10:
        print ""+url
        GETSOURCE(url,name,iconimage)
elif mode==11:
        print ""+url
        PREVIOUS()

xbmcplugin.endOfDirectory(int(sys.argv[1]))




