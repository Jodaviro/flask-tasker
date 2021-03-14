from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.forms import LoginForm

app = create_app()

todos = ['Comprar café', 'Buscar cita de asilo', 'Preparar documentos']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)



@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', error=error)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.htm', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['POST', 'GET'])
def hello():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username
    }

    flash('Nombre de usuario registrado con éxito!')

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('hello.html', **context)


# if __name__ == '__main__':
#     pass
