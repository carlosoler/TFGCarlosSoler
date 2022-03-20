from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('login.html')

@app.route('/resgistroUsuario')
def registro_usuario():
    return render_template('resgistroUsuario.html')

@app.route('/resgistroEmpresa')
def registro_empresa():
    return render_template('resgistroEmpresa.html')


if __name__ == '__main__':
    app.run()
