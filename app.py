from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ccb0ce4501150d103e1dae7b8431d6ab70c026903df97cbd'

result_params = {}


@app.route('/', methods=('GET', 'POST'))
def book_input():  # put application's code here
    if request.method == 'POST':
        title = request.form['title'] or 'Untitled'
        text = request.form['text']

        if not text:
            flash('Text is required!')
        else:
            result_params['title'] = title
            result_params['text'] = text
            return redirect(url_for('result'))

    return render_template('book_input.html')


@app.route('/result/')
def result():
    return render_template('result.html', result=result_params)


if __name__ == '__main__':
    app.run()
