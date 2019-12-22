import dash
import dash_ace
import dash_html_components as html
import flask
from dash.dependencies import Input, Output
from flask import request, jsonify
from flask_cors import CORS

server = flask.Flask(__name__)
CORS(server)

app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/dash/'
                )

app.layout = html.Div([
    dash_ace.DashAceEditor(
        id='input',
        value='test(a: integer) -> string := \n'
              '    return f"value is {a}"',
        theme='tomorrow',
        mode='norm',
        enableBasicAutocompletion=True,
        enableLiveAutocompletion=True,
        placeholder='Norm code ...'
    ),
    html.Div(id='output')
])


@server.route('/autocompleter', methods=['GET'])
def autocompleter():
    prefix = request.args.get('prefix')
    return jsonify([{"name": prefix + "_completed", "value": prefix + "_completed", "score": 300, "meta": "test"}])


@app.callback(Output('output', 'children'), [Input('input', 'value')])
def display_output(value):
    return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
