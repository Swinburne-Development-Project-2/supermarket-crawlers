from facade import facade
from DiaryandEgg import dairyandEgg
from NappiesandWipes import NappiesWipes
from babyFood import babyFood
from beauty import Beauty
from freezer import Freezer
from health import Health
from laundy import Laundry
from household import Household
from liquor import liquor
from beer import beer
from champagne import champagne
from spirit import spirit
from glutenfree import glutenfree
from oliveoil import oliveoil
from organic import organic
from chocolate import chocolate
from coffee import coffee
from supersaver import supersaver

supersaver = supersaver().returnLink()
dairy = dairyandEgg().returnLink()
nappies = NappiesWipes().returnLink()
bbfood = babyFood().returnLink()
beauty = Beauty().returnLink()
freezer = Freezer().returnLink()
health = Health().returnLink()
laundry = Laundry().returnLink()
household = Household().returnLink()
liquor = liquor().returnLink()
beer = beer().returnLink()
champagne = champagne().returnLink()
spirit = spirit().returnLink()
glutenf = glutenfree().returnLink()
oliveoil = oliveoil().returnLink()
organic = organic().returnLink()
chocolate = chocolate().returnLink()
coffee = coffee().returnLink()

myFacade = facade()
myFacade.scrawler(supersaver)
myFacade.scrawler(dairy)
myFacade.scrawler(nappies)
myFacade.scrawler(bbfood)
myFacade.scrawler(beauty)
myFacade.scrawler(freezer)
myFacade.scrawler(health)
myFacade.scrawler(laundry)
myFacade.scrawler(household)
myFacade.scrawler(liquor)
myFacade.scrawler(beer)
myFacade.scrawler(champagne)
myFacade.scrawler(spirit)
myFacade.scrawler(glutenf)
myFacade.scrawler(oliveoil)
myFacade.scrawler(organic)
myFacade.scrawler(chocolate)
myFacade.scrawler(coffee)