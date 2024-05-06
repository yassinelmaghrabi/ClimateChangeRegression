from .globaltemps import globaltemps

def globaltempsembed(cleaningthreshold=2.5, deg=2,test_size=0.2):
    gt = globaltemps(cleaningthreshold=cleaningthreshold,degree=deg,test_size=test_size)
    return gt.plotembed()
def globaltempsdata(cleaningthreshold=2.5, deg=2,test_size=0.2):
    gt = globaltemps(cleaningthreshold=cleaningthreshold,degree=deg,test_size=test_size)
    data = {
        "r2": gt.r2_,
        "msr": gt.msr_,
        "coef": gt.coef_
    }
    return data
def globalpredict(val):
    gt = globaltemps()
    return gt.predict(val)