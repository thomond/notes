# Blueprint for notes app main screen
# flask imports
from flask import Blueprint, render_template, url_for, request, session, redirect, flash
import sqlite3
# project imports
from .db import get_db
from datetime import datetime
bp = Blueprint('notes', __name__, url_prefix='/notes' )


@bp.route('/', methods=['GET', 'POST'])
def notes_index():
      notes = []
      # static resources
      url_for('static',filename='style.css')
      #do_login('test')
      if 'username' not in session: 
         flash("%s"%session)
         flash("Not logged in")
         return redirect("/notes/auth")

      username = session['username']
      userid   = session['userid']
     
      # Process form data / commands
      try: 
        cmd =  request.form['c'] 
        if cmd == 'new': 
            if 'draft' not in session: session['draft'] =  new_note(userid)
            notes.append(session['draft'])
        if cmd == 'save':# save draft  
            # Check if note id is present in DB or new
            postid = form['postid']
            textbody =  form['textbody']
            texttitle =  form['texttitle']
            if 'draft' in session: save_note(postid, textbody,texttitle) 
            else: update_note(postid, textbody,texttitle)
        if cmd == 'delete': 
            postid = form['postid']
            if postid != -1: delete_note(userid,postid)
      except KeyError as e: 
        pass
      # retrive notes from db
      notes = notes + get_notes(userid)
      return render_template('notes_tmpl.html',notes=notes,username=username)

def new_note(userid):
    return [ -1, userid ,datetime.now() , 'Title', 'Text' ] # Create new draft note

def save_note(postid, textbody,texttitle):
    try:
        draft = session['draft']
        draft[3] = texttitle
        draft[4] = textbody
        get_db().execute("insert into note (author_id, created, title, body)  values (?,?,?,?)", (draft[1],draft[2],draft[3],draft[4]))
        get_db().commit()
        flash("Note Saved")
        return True
    except sqlite3.Error as err:
        flash("%s"%err)
        return False

def delete_note(userid, postid):
    # verify postid
    # delete note from DB
    get_db().execute('delete from note where id = ?', postid)
    get_db().commit()
    flash("Deleted Note")
    return True

def get_notes(userid):
    # retrive notes from db
    return get_db().execute('select * from note where author_id = ?',(userid,)).fetchall()

def update_note(postid, textbody,texttitle):
    # Verify note id
    try:
        get_db().execute('update note set body = ? , title = ? where id = ? ',(textbody, texttitle, postid))
        get_db().commit()
        flash("Note Updated")
        return True
    except sqlite3.Error as err:
        flash("%s"%err)
        return False

def do_login(username='test'):
     # Check login / test login
     if 'username' or 'userid' not in session:
         session['username'] = username
         if username == 'test': session['userid'] = 0

def chk_login(username,pw): pass
