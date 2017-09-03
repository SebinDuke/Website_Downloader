import requests,bs4
urllist=[] #list all urls visited so that you don't visit any of them again.
"""
TO-DO LIST:
1.Download all JS files on each page
2.Download all CSS files on each page
3.Get weblink,title and depth as command line parameters
4.Apply regEx to stop the code from getting swayed to other websites who's links may be present on some web page.
"""


def genricWebsiteDownloader(weblink,title,n): #n is the depth
    if n==0 or weblink in urllist:
        return
    new=n-1
    res=requests.get(weblink)
    urllist.append(weblink)
    bsobj=bs4.BeautifulSoup(res.text,'html.parser')
    html=bsobj.prettify()

    f=open(title+'.html','w')
    f.write(html)
    f.close()

    #Download all pics on the page
    itr=0
    for link in bsobj.findAll('img'):
        if 'src' in link.attrs:
            try:
                res=requests.get(link['src'],stream=True)
                print("Downloading "+link['src'])
            except:
                try:
                    res=requests.get(weblink + link['src'],stream=True)
                    urllist.append(weblink + link['src'])
                except:
                    pass
                pass
            try:
                ext=link['src']
                ext=ext[len(ext)-4:]
                itr+=1
                FileName=title+str(itr)+ext

                with open(FileName, 'wb') as f:
                    for i in res:
                        f.write(i)

                link['src']=title
            except:
                pass

    #go to all links in website and run the function recursively
    for link in bsobj.findAll('a'):
        if 'href' in link.attrs:
            try:
                genricWebsiteDownloader(link['href'],link.string,new)
                print("Downloading "+link['href'])
            except:
                try:
                    genricWebsiteDownloader(weblink + link['href'],link.string,new)
                    print("Downloading " +weblink + link['href'])
                except:
                    pass
                pass



weblink='http://meter-down.com'
title="meter-down"
depth=10
genricWebsiteDownloader(weblink,title,depth)