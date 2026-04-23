from flask import Blueprint, render_template, redirect, url_for

bp_tela_principal = Blueprint('inicio', __name__)

@bp_tela_principal.route('/')
def ini_tela_principal():
    return redirect(url_for('inicio.ini_menu_links'))

@bp_tela_principal.route('/lauany_minervino')
def ini_menu_links():
    return render_template('pasta_menu_links/menu_links.html')