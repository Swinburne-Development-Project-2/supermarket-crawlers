from facade import facade

myFacade = facade()
resourceList = myFacade.returnListLink()
for link in resourceList:
    myFacade.scrawler(link)
    