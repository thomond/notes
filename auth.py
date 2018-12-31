

# Blueprint for notes login screen
# flask imports
from flask import Blueprint, render_template, url_for, request, session, flash, redirect
import sqlite3
# project imports
from .db import get_db
from datetime import datetime
bp = Blueprint('auth', __name__, url_prefix='/notes/auth' )

@bp.route('/', methods=['GET', 'POST'])
def index():
    # Process get params
    #cmd =  request.args.get('c','')
    try: cmd = request.form['c'] 
    except KeyError as e: return render_template('auth_tmpl.html')

    if cmd == "register":
        #show register screen
        return render_template('auth_tmpl.html',do_register=True) 
    elif cmd == "Create":
        try: 
            username = request.form['username'] 
            password = request.form['password']
        except KeyError as e: return render_template('auth_tmpl.html')

        # TODO: try/catch
        create_user(username, password)
        
    elif cmd == "Login":
        try: 
            username = request.form['username'] 
            password = request.form['password']
        except KeyError as e: return render_template('auth_tmpl.html')
        # TODO: try/catch
        if do_login(username, password): 
            flash("User logged in")
            return redirect("/notes")
        else: flash("Login Failed.")
    elif cmd == "logout":
        do_logout()
        return render_template('auth_tmpl.html')
    return render_template('auth_tmpl.html')

def create_user(username, pw):
    # TODO: verify username/pw
    try:
        get_db().execute('insert into user (username, password)  values (?,?)', (username, pw))
        get_db().commit()
    except sqlite3.Error as err: 
        flash("Database Error: %s" % err)
        return False
    flash("User Created")
    return True

''' 
    Attempt login for user 
    Returns: true if successful
'''
def do_login(un,pw):
    # Check login / test login
    if 'username' or 'userid' not in session:
        #session['username'] = username
        #if username == 'test': session['userid'] = 0
        #return True
        try:
            [[uid,upw]] = get_db().execute("select id,password from user where username = '%s'"%un).fetchall()
            #flash("%s"%row[0][0])
            if upw == pw: 
                session['username'] = un
                session['userid'] = uid
                return True 
            else: 
                flash("Password Incorrect")
                return False
        except sqlite3.Error as err: 
            flash("Database Error: %s"%err)
            return False
        except ValueError as err:
            flash("User not found")
    else: 
        flash("USer alredy logged in.")
        return False

def do_logout():
    if 'username' in session:
        del session['username']
        del session['userid']
        flash("Logged out")
        return True
    else: return False
