import flask
from time import time
from input_form import InputForm

app = flask.Flask(__name__)
app.static_folder = 'static'
input_forms = {}

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global input_forms
    input_status = ''
    if flask.request.method == 'POST':
        input_form = InputForm(flask.request.form)
        if input_form.is_valid():
            key = str(time())
            input_forms[key] = input_form
            return flask.redirect(flask.url_for('calculations', key=key))
        input_status = 'Please enter the information above properly'
    return flask.render_template('index.html', input_status=input_status)

@app.route('/calculations/<key>', methods=['GET'])
def calculations(key):
    input_form = input_forms[key]
    data = input_form.data()
    return flask.render_template(
        'calculations.html',
        symbol=input_form.symbol,
        market_sentiment=data[0][0],
        market_sentiment_color=data[0][1],
        cross_point=data[1][0],
        cross_price=data[1][1],
        current_price=data[2],
        avg_volume=data[3],
        price_change=data[4][0],
        price_change_color=data[4][1],
        xlabel=data[5],
        graph_data=data[6]
    )

if __name__ == '__main__':
    app.run()
