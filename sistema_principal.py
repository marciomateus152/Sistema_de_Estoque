from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import mysql.connector
import csv
import io
from werkzeug.security import generate_password_hash, check_password_hash

aplicacao = Flask(__name__, template_folder='modelos', static_folder='estaticos')
aplicacao.secret_key = 'chave_seguranca_estoque_pro'

def conectar_banco_dados():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_estoque_avancado"
    )

@aplicacao.route('/')
def rota_inicial():
    if 'usuario_autenticado' in session:
        return redirect(url_for('exibir_painel'))
    return redirect(url_for('fazer_login'))

@aplicacao.route('/entrar', methods=['GET', 'POST'])
def fazer_login():
    if request.method == 'POST':
        usuario = request.form.get('nome_acesso')
        senha = request.form.get('senha')
        if usuario == "admin" and senha == "admin123":
            session['usuario_autenticado'] = "Administrador"
            return redirect(url_for('exibir_painel'))
        else:
            flash("Usuário ou senha incorretos!", "erro")
            return redirect(url_for('fazer_login'))
    return render_template('entrar.html')

@aplicacao.route('/painel')
def exibir_painel():
    if 'usuario_autenticado' not in session:
        return redirect(url_for('fazer_login'))
    conexao_banco = conectar_banco_dados()
    cursor_banco = conexao_banco.cursor(dictionary=True)
    consulta_produtos = """
        SELECT p.identificador, p.codigo_produto, p.nome_produto, c.nome_categoria, 
               p.quantidade_atual, p.estoque_minimo, p.preco_custo, p.preco_venda,
               (p.quantidade_atual * p.preco_custo) AS custo_total,
               (p.quantidade_atual * p.preco_venda) AS valor_venda_total,
               ((p.preco_venda - p.preco_custo) * p.quantidade_atual) AS lucro_projetado
        FROM produtos p
        LEFT JOIN categorias c ON p.identificador_categoria = c.identificador
        ORDER BY p.identificador DESC
    """
    cursor_banco.execute(consulta_produtos)
    lista_produtos = cursor_banco.fetchall()
    cursor_banco.execute("SELECT * FROM categorias")
    lista_categorias = cursor_banco.fetchall()
    conexao_banco.close()
    total_itens = sum(item['quantidade_atual'] for item in lista_produtos)
    investimento = sum(item['custo_total'] for item in lista_produtos)
    lucro = sum(item['lucro_projetado'] for item in lista_produtos)
    alertas = sum(1 for item in lista_produtos if item['quantidade_atual'] <= item['estoque_minimo'])
    return render_template(
        'painel.html', 
        produtos=lista_produtos, 
        categorias=lista_categorias,
        usuario=session['usuario_autenticado'],
        metricas={'total_itens': total_itens, 'investimento': investimento, 'lucro': lucro, 'alertas': alertas}
    )

@aplicacao.route('/registrar', methods=['POST'])
def registrar_produto():
    if 'usuario_autenticado' not in session:
        return redirect(url_for('fazer_login'))
    dados = (
        request.form['codigo_produto'],
        request.form['nome_produto'],
        request.form['identificador_categoria'],
        request.form['quantidade_atual'],
        request.form['estoque_minimo'],
        request.form['preco_custo'],
        request.form['preco_venda']
    )
    conexao_banco = conectar_banco_dados()
    cursor_banco = conexao_banco.cursor()
    try:
        cursor_banco.execute(
            "INSERT INTO produtos (codigo_produto, nome_produto, identificador_categoria, quantidade_atual, estoque_minimo, preco_custo, preco_venda) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            dados
        )
        conexao_banco.commit()
    except:
        flash('Erro ao registrar produto.', 'erro')
    finally:
        conexao_banco.close()
    return redirect(url_for('exibir_painel'))

@aplicacao.route('/excluir/<int:id>')
def excluir_produto(id):
    if 'usuario_autenticado' in session:
        conexao = conectar_banco_dados()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE identificador = %s", (id,))
        conexao.commit()
        conexao.close()
    return redirect(url_for('exibir_painel'))

@aplicacao.route('/exportar_csv')
def exportar_csv():
    if 'usuario_autenticado' not in session:
        return redirect(url_for('fazer_login'))
    conexao = conectar_banco_dados()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT codigo_produto, nome_produto, quantidade_atual, preco_venda FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    saida = io.StringIO()
    escritor = csv.writer(saida)
    escritor.writerow(['Codigo', 'Produto', 'Quantidade', 'Preco Venda'])
    for p in produtos:
        escritor.writerow([p['codigo_produto'], p['nome_produto'], p['quantidade_atual'], p['preco_venda']])
    resposta = make_response(saida.getvalue())
    resposta.headers["Content-Disposition"] = "attachment; filename=estoque_pro.csv"
    resposta.headers["Content-type"] = "text/csv"
    return resposta

@aplicacao.route('/sair')
def sair():
    session.clear()
    return redirect(url_for('fazer_login'))

if __name__ == '__main__':
    aplicacao.run(debug=True)