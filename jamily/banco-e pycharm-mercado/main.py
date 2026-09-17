from flask import Flask, render_template, redirect, url_for, flash, request
import fdb

app = Flask(__name__)


app.config['SECRET_KEY'] = 'Aqui_e_a_chave_do_grupo'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO\BANCO.FDB'
user = 'SYSDBA'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/')
def criarconta():
    return render_template('criarconta.html')


@app.route('/endereco')
def endereco():
    return render_template('endereco.html')

@app.route('/adicionar_endereco', methods=['POST'])
def adicionar_endereco():
    cep = request.form['cep']
    rua = request.form['rua_avenida']
    numero = request.form['numero']
    complemento = request.form['complemento']
    nome = request.form['nome']
    telefone = request.form['telefone']

    cursor = con.cursor()

    try:
        cursor.execute("""SELECT 1 FROM endereco e WHERE nome = ?,rua = ?,numero = ?""", (nome,rua_avenida,numero))
        if cursor.fetchone():
            flash('Erro: Endereço já cadastrado')
            return redirect(url_for('endereco'))

        cursor.execute( """ INSERT INTO endereco (cep,rua_avenida,numero,complemento,nome,telefone)
                            VALUES (?, ? ,?,?, ? ,?)""", (cep,rua,numero,complemento,nome,telefone))

        con.commit()
        return redirect(url_for('pagamento'))

    except Exception as e:
        flash(f"Ocorreu um error -> {e}")
        con.rollback()
        return redirect(url_for('endereco'))

    finally:
        cursor.close()

@app.route('/pagamento')
def pagamento():
    cursor = con.cursor() #abrindo o cursor

    cursor.execute("""SELECT e.rua, e.numero, e.cep 
                            FROM endereco e""")

    enderecos = cursor.fetchall()

    cursor.close()
    return render_template('pagamento.html', enderecos=enderecos)

@app.route('/editar_endereco/<int:id>', methods=['GET','POST'])
def editar_endereco(id):
    cursor = con.cursor()
    try:
        cursor.execute("""SELECT e.id_endereco, e.rua, e.numero, e.cep
                          FROM endereco e  WHERE ID_usuario = ?""", (id,))

        enderecos = cursor.fetchall()


        if not endereco:
            flash('Endereço não encontrado')
            return redirect(url_for('pagamento'))

        if request.method == 'POST':
            cep = request.form['cep']
            rua = request.form['rua_avenida']
            numero = request.form['numero']
            complemento = request.form['complemento']
            nome = request.form['nome']
            telefone = request.form['telefone']

            cursor.execute(""" UPDATE endereco SET cep = ?, rua = ?, numero = ?, complemento = ?, nome = ?, nome = ?, telefone = ?
                               where id_endereco = ?""", (cep,rua,numero,complemento,nome,telefone,id))
            con.commit()
            flash("Endereço editado com sucesso")
            return redirect(url_for('pagamento'))

        return render_template('pagamento.html', enderecos=enderecos)

    except Exception as e:
            con.rollback()
            flash(f"Ocorreu um error -> {e}")
            return redirect(url_for('pagamento'))


    finally:
        cursor.close()
@app.route('/finalizar')
def finalizar():
    return render_template('pagamento-banco.html')


@app.route('/cadastrar_cartao', methods=['POST'])
def cadastrar_cartao():
    numero_cartao = request.form['numero']
    nome = request.form['nome']
    vencimento = request.form['vencimento']
    codigo = request.form['codigo']
    cpf = request.form['cpf']

    cursor = con.cursor()

    try:
        cursor.execute("""SELECT 1 FROM pagamento p WHERE numero_cartao = ?,nome = ?,vencimento = ?, codigo = ?,cpf = ?""", (numero_cartao,nome,vencimento,codigo,cpf))
        if cursor.fetchone():
            flash('Erro: Cartão já cadastrado')
            return redirect(url_for('finalizar'))

        cursor.execute( """ INSERT INTO pagamento (numero_cartao, nome, vencimento, codigo, cpf)
                            VALUES (?, ? ,?,?, ?)""", (numero_cartao, nome, vencimento, codigo, cpf))

        con.commit()
        return redirect(url_for('mensagem'))

    except Exception as e:
        flash(f"Ocorreu um error -> {e}")
        con.rollback()
        return redirect(url_for('finalizar'))

    finally:
        cursor.close()

@app.route('/mensagem')
def mensagem():
    return render_template('mensagem.html')

if __name__ == '__main__':
    app.run(debug=True)
