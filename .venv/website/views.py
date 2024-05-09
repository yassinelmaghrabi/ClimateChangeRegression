import regression
from flask import Blueprint ,render_template,request,redirect,url_for,flash,session
views = Blueprint('views' , __name__)
from regression import globaltempsembed, globaltempsdata, globalpredict, getcountrylist, countrytempsembed ,countrytempsdata,countrypredict
@views.route('/')
def home():
    session.clear()
    return render_template('index.html')



@views.route('/process_form', methods=['POST'])
def process_form():

    if 'test_size' in request.form:
        test_size = float(request.form['test_size'])
    else:
        test_size = DEFAULT_TEST_SIZE

    if 'degree' in request.form:
        degree = int(request.form['degree'])
    else:
        degree = DEFAULT_DEGREE


    session['test_size'] = test_size
    session['degree'] = degree


    return redirect(url_for('views.global_temp'))
@views.route('/process_country_form', methods=['POST'])
def process_country_form():

    if 'test_size' in request.form:
        test_size = float(request.form['test_size']) if request.form['test_size'] != '' else DEFAULT_TEST_SIZE
    else:
        test_size = DEFAULT_TEST_SIZE

    if 'degree' in request.form:
        degree = int(request.form['degree']) if request.form['degree'] != '' else DEFAULT_DEGREE
    else:
        degree = DEFAULT_DEGREE

    if 'select_option' in request.form:
        country = request.form['select_option']
    else:
        country = DEFAULT_COUNTRY

    session['test_size'] = test_size
    session['degree'] = degree
    session['country'] = country

    return redirect(url_for('views.country_temp'))

@views.route('/process_form_predict', methods=['POST'])
def process_form_predict():

    if 'year' in request.form:
        year = float(request.form['year']) if request.form['year'] != '' else 1750
    else:
        year = 1750




    session['year'] = year

    return redirect(url_for('views.global_predict'))
@views.route('/process_form_predict_country', methods=['POST'])
def process_form_predict_country():

    if 'year' in request.form:
        year = float(request.form['year']) if request.form['year'] != '' else 1750
    else:
        year = 1750

    if 'select_option' in request.form:
        country = request.form['select_option']
    else:
        country = DEFAULT_COUNTRY


    session['year'] = year
    session['country'] = country

    return redirect(url_for('views.country_predict'))

@views.route('/global')
def global_temp():

    test_size = session.get('test_size', DEFAULT_TEST_SIZE)
    degree = session.get('degree', DEFAULT_DEGREE)


    plot = globaltempsembed(deg=degree, test_size=test_size)
    data = globaltempsdata(deg=degree, test_size=test_size)

    return render_template('global.html', plot=plot, data=data)
@views.route('/country')
def country_temp():

    test_size = session.get('test_size', DEFAULT_TEST_SIZE)
    degree = session.get('degree', DEFAULT_DEGREE)
    country = session.get('country', DEFAULT_COUNTRY)
    print(country)


    plot = countrytempsembed(deg=degree, test_size=test_size, country=country)
    data = countrytempsdata(deg=degree, test_size=test_size, country=country)

    return render_template('country.html', plot=plot, data=data,list=regression.getcountrylist())

@views.route('/globalpredict')
def global_predict():
    year = session.get('year', 1750)


    val = globalpredict(year)


    return render_template('predict.html', val=val,year=year)

@views.route('/countrypredict')
def country_predict():
    year = session.get('year', 1750)
    country = session.get('country',DEFAULT_COUNTRY)

    val = countrypredict(year,country=country)


    return render_template('countrypredict.html', val=val,list=regression.getcountrylist(),country = country,year=year)
@views.route('/report')
def report():
    return render_template('report.html')

DEFAULT_TEST_SIZE = 0.2
DEFAULT_DEGREE = 2
DEFAULT_COUNTRY = "Dominica"