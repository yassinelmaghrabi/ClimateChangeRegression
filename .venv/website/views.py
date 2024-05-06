from flask import Blueprint ,render_template,request,redirect,url_for,flash,session
views = Blueprint('views' , __name__)
from regression import globaltempsembed, globaltempsdata, globalpredict
@views.route('/')
def home():
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

@views.route('/process_form_predict', methods=['POST'])
def process_form_predict():

    if 'year' in request.form:
        year = float(request.form['year'])
    else:
        year = 1750




    session['year'] = year



    return redirect(url_for('views.global_predict'))

@views.route('/global')
def global_temp():

    test_size = session.get('test_size', DEFAULT_TEST_SIZE)
    degree = session.get('degree', DEFAULT_DEGREE)


    plot = globaltempsembed(deg=degree, test_size=test_size)
    data = globaltempsdata(deg=degree, test_size=test_size)

    print(plot)


    return render_template('global.html', plot=plot, data=data)

@views.route('/globalpredict')
def global_predict():
    val = session.get('year', 1750)


    val = globalpredict(val)


    return render_template('predict.html', val=val)


DEFAULT_TEST_SIZE = 0.2
DEFAULT_DEGREE = 1