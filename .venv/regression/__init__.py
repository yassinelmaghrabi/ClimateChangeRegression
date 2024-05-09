from .globaltemps import globaltemps
from .temperatureByCountry import countrytemps

def globaltempsembed( deg=2,test_size=0.2):
    gt = globaltemps(degree=deg,test_size=test_size)
    return gt.plotembed()
def globaltempsdata( deg=2,test_size=0.2):
    gt = globaltemps(degree=deg,test_size=test_size)
    data = {
        "r2": gt.r2_,
        "msr": gt.msr_,
        "coef": gt.coef_
    }
    return data
def globalpredict(val):
    gt = globaltemps()
    return gt.predict(val)

def countrytempsembed( country="Dominica",deg=2,test_size=0.2):
    ct = countrytemps(country=country,degree=deg,test_size=test_size)
    return ct.plotembed()
def countrytempsdata(country="Dominica",deg=2,test_size=0.2):
    ct = countrytemps(country=country,degree=deg,test_size=test_size)
    data = {
        "r2": ct.r2_,
        "msr": ct.msr_,
        "coef": ct.coef_
    }
    return data
def countrypredict(val,country="Dominica"):
    ct = countrytemps(country=country)
    return ct.predict(val)
def getcountrylist():
    return countrytemps.get_available_countries()