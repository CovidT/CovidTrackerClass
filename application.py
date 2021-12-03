from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from controller.covidcontroller import CovidTrackerController
from models.testresult import CovidTestResult
import re
from numpy import random

application = Flask(__name__)

application.secret_key = 'your secret key'
host = 'covidtest.crra19lrcu6t.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'covidtest'
db ='covidlogin'
application = application
application.config['MYSQL_HOST'] = host
application.config['MYSQL_USER'] = user
application.config['MYSQL_PASSWORD'] = password
application.config['MYSQL_DB'] = db
mysql = MySQL(application)



def getApp():
    return application

@application.route('/')
def homepage():
    return render_template('homepage.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        covidtrackercontroller = CovidTrackerController()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if covidtrackercontroller.checkGovernment(username,password,cursor):
            session['loggedin'] = True
            return render_template('register.html')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@application.route('/vaccine', methods=['GET', 'POST'])
def vaccine():
    msg = ''
    if request.method == 'POST' and 'uniqueId' in request.form:
        uniqueId = request.form['uniqueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        covidtrackercontroller = CovidTrackerController()
        vaccine=covidtrackercontroller.getVaccinationDetails(uniqueId,cursor)
        if vaccine is not None:
            msg = 'UniqueId is validated'
            session['name'] = vaccine.getname()
            session['email'] = vaccine.getemail()
            session['dateofbirth'] = vaccine.getdateofbirth()
            session['firstdose'] = vaccine.getfirstdose()
            session['firstdosename'] = vaccine.getfirstname()
            session['firstdate'] = vaccine.getdate()
            session['seconddose'] = vaccine.getseconddose()
            session['seconddate'] = vaccine.getseconddate()
            session['seconddosename'] = vaccine.getsecondname()
            return render_template('vaccinedetails.html', msg=msg)
        else:
            msg = 'Incorrect UniqueId'
    return render_template('vaccine.html', msg=msg)

@application.route('/testresult', methods=['GET', 'POST'])
def testresults():
    msg = ''
    if request.method == 'POST' and 'uniqueId' in request.form:
        uniqueId = request.form['uniqueId']
        covidtrackercontroller = CovidTrackerController()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        covidresult = covidtrackercontroller.getCovidResult(uniqueId,cursor)
        if covidresult is not None:
            msg = 'UniqueId is validated'
            session['name'] = covidresult.getname()
            session['email'] = covidresult.getemail()
            session['dateofbirth'] = covidresult.getdateofbirth()
            session['date'] = covidresult.getdate()
            session['result'] = covidresult.getresult()
            session['location'] = covidresult.getlocation()
            return render_template('testdetails.html', msg=msg)
        else:
            msg = 'Incorrect UniqueId'
    return render_template('testresults.html', msg=msg)

@application.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('homepage'))

@application.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'dob' in request.form and 'location' in request.form:
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        location = request.form['location']
        uniqueid = name[:4] + dob[len(dob) - 2:len(dob)]
        selected_field = (request.form["coviddata"])
        if selected_field == 'vaccine':
            vaccine_dose = request.form['dosenumber']
            vaccine_date = request.form['vaccinedate']
            vaccine_name = request.form['vaccinename']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cmd = 'SELECT * FROM vaccine WHERE uniqueid = "%s"' % uniqueid
            cursor.execute(cmd)
            account = cursor.fetchone()
            if account:
                cmd = "UPDATE vaccine SET seconddose='%s', seconddate='%s', seconddosename='%s' WHERE (UniqueId = '%s');" % (
                    vaccine_dose, vaccine_date, vaccine_name, uniqueid)
                cursor.execute(cmd)
                mysql.connection.commit()
                msg = 'You have successfully registered !'
            else:
                if vaccine_dose == '1':
                    cmd = "INSERT INTO vaccine (name, dateofbirth, email, firstdose, date, firstdosename, UniqueId, location) VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s', '%s')" % (
                    name, dob, email,
                    vaccine_dose, vaccine_date, vaccine_name, uniqueid, location)
                elif vaccine_dose == '2':
                    cmd = "INSERT INTO vaccine (name, dateofbirth, email, seconddose, seconddate, seconddosename, UniqueId, location) VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s', '%s')" % (
                    name, dob, email,
                    vaccine_dose, vaccine_date, vaccine_name, uniqueid, location)
                cursor.execute(cmd)
                mysql.connection.commit()
                msg = 'You have successfully registered !'
        elif selected_field == 'test':
            test_date = request.form['testdate']
            test_result = request.form['testresult']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cmd = 'SELECT * FROM test WHERE uniqueid = "%s"' % uniqueid
            cursor.execute(cmd)
            account = cursor.fetchone()
            if account:
                cmd = "UPDATE test SET date='%s', Result='%s' WHERE (UniqueId = '%s');" % (
                    test_date, test_result, uniqueid)
                cursor.execute(cmd)
                mysql.connection.commit()
                msg = 'You have successfully registered !'
            else:
                result = CovidTestResult()
                result.setname(name)
                result.setdateofbirth(dob)
                result.setemail(email)
                result.setdate(test_date)
                result.setresult(test_result)
                result.setuniqueid(uniqueid)
                result.setlocation(location)
                covidtrackercontroller = CovidTrackerController()
                covidtrackercontroller.enterCovidResult(mysql,result,cursor)
                msg = 'You have successfully registered !'
        else:
            msg = "Please select vaccine details or test results to register"

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@application.route('/map')
def CovidMap():
    return render_template("covidmap.html")


@application.route('/mapdata')
def Mapdata():
    province_relation = {
        "Manitoba": "MB",
        "Saskatchewan": "SK",
        "Alberta": "AB",
        "British Columbia": "BC",
        "Nunavut": "NU",
        "New Brunswick": "NB",
        "Newfoundland and Labrador": "NF",
        "Nova Scotia": "NS",
        "Ontario": "ON",
        "Prince Edward Island": "PE",
        "Québec": "QC",
        "Yukon": "YT",
        "Northwest Territories": "NT"
    }
    fills = {
        "MB": "NORMAL",
        "SK": "NORMAL",
        "AB": "NORMAL",
        "BC": "NORMAL",
        "NU": "NORMAL",
        "NB": "NORMAL",
        "NF": "NORMAL",
        "NS": "NORMAL",
        "ON": "NORMAL",
        "PE": "NORMAL",
        "QC": "NORMAL",
        "YT": "NORMAL",
        "NT": "NORMAL"
    }
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    for key, value in province_relation.items():
        cmd = 'SELECT COUNT(*) FROM test WHERE Location = "% s" and Result = "Positive"' % (key)
        cursor.execute(cmd)
        count = cursor.fetchone()
        if count['COUNT(*)'] > 1 and count['COUNT(*)'] <= 3 :
            fills[value] = "CAUTION"
        elif count['COUNT(*)'] > 3:
            fills[value] = "RISK"
        else:
            fills[value] = "NORMAL"
    return fills


if __name__ == '__main__':
   application.run()
