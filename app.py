from flask import Flask, render_template, request
from quine_mccluskey import quine_mccluskey_simplification  # Assuming you have the Quine-McCluskey implementation in a separate file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def simplify_expression():
    minterms = list(map(int, request.form['minterms'].split(' ')))
    dc = request.form['dc']
    if dc!='':
        dc = list(map(int, dc.split(' ')))
    else:
        dc=[]
    
    # Apply Quine-McCluskey algorithm
    result = quine_mccluskey_simplification(minterms, dc)

    return render_template('index.html', result=' + '.join(''.join(i) for i in result), minterms=request.form['minterms'], dc=request.form['dc'])

if __name__ == '__main__':
    app.run(debug=True)
