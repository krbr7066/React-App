from flask import Flask, request, send_from_directory, render_template, flash, redirect, url_for, session, logging
import flask
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = flask.Flask("__main__")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'ThreatDetectorDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MySQL
mysql = MySQL(app)

@app.route("/")
def my_index():
    return flask.render_template("index.html",token="Hello Flask+React")

class RegisterForm(Form):
    username = StringField('Username', validators=[validators.Length(min=4, max=25)])
    email  = StringField(u'Email', validators=[validators.Length(min=4, max=25)])
    password  = PasswordField(u'Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmedPassword',message=u'Passwords do not match')
        ])
    confirmedPassword = PasswordField(u'Confirm Password')


# go to register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    # if the form sunmitted
    if request.method == 'POST' and form.validate():

        # create cursor
        cur = mysql.connection.cursor()
        #         if cur.execute("select * from INFORMATION_SCHEMA.TABLES where 'TABLE_SCHEMA'='sql3333055' and 'TABLE_NAME'='tdusers'") is False:
        #             cur.execute("CREATE TABLE tdusers (id INT(11) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30), email VARCHAR(100), password VARCHAR(100), confirmedPassword VARCHAR(100))")

        if cur.execute(
                "select * from INFORMATION_SCHEMA.TABLES where 'TABLE_SCHEMA'='ThreatDetectorDB' and 'TABLE_NAME'='tdusers'") is False:
            cur.execute(
                "CREATE TABLE tdusers (id INT(11) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30), email VARCHAR(100), password VARCHAR(100), confirmedPassword VARCHAR(100))")

        #         # create table if not exists
        #         cur.execute("CREATE TABLE if not exists tdusers (id INT(11) AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30), email VARCHAR(100), password VARCHAR(100), confirmedPassword VARCHAR(100))")

        username = form.username.data
        cur.execute("select username from tdusers where username =(%s)", (username,))

        username_result = cur.fetchall()
        # if username already existed
        if username_result:
            flash(u"Username already exist. Please choose another one!", "danger")
        else:
            email = form.email.data
            cur.execute("select email from tdusers where email =(%s)", (email,))
            email_result = cur.fetchall()
            # if email already existed
            if email_result:
                flash(u"Email already exist. Please log in!", 'danger')
            else:
                password = sha256_crypt.hash(str(form.password.data))
                confirmedPassword = form.confirmedPassword.data

                # execute query
                cur.execute("insert into tdusers(username, email, password, confirmedPassword) values(%s, %s, %s, %s)",
                            (username, email, password, confirmedPassword))

                # commit to DB
                mysql.connection.commit()

                flash('You are now registered and can log in', 'success')

                # close connection
                cur.close()

            return redirect(url_for('login'))

    return render_template('register.html', form=form)

app.run(debug=True)