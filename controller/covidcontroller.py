from models.testresult import CovidTestResult
from models.vaccine import VaccinationDetails

class CovidTrackerController:
    Government = 'null'
    vaccine = VaccinationDetails()
    covidresult = CovidTestResult()

    def checkGovernment(self,username,password,cursor):
        tablename = "government_login"
        cmd = 'SELECT * FROM %s WHERE username = "%s" AND password = "%s"' % (tablename, username, password)
        cursor.execute(cmd)
        account = cursor.fetchone()
        if account:
            return True
        return False

    def getCovidResult(self,uniqueId,cursor):
        cmd = 'SELECT * FROM test WHERE uniqueId = "% s"' % (uniqueId)
        cursor.execute(cmd)
        account = cursor.fetchone()
        if account:
            self.covidresult.setname(account['Name'])
            self.covidresult.setemail(account['email'])
            self.covidresult.setdateofbirth(account['dateofbirth'])
            self.covidresult.setdate(account['date'])
            self.covidresult.setresult(account['Result'])
            self.covidresult.setlocation(account['location'])
            return self.covidresult
        return None

    def getVaccinationDetails(self,uniqueId,cursor):
        cmd = 'SELECT * FROM vaccine WHERE uniqueId = "% s"' % (uniqueId)
        cursor.execute(cmd)
        account = cursor.fetchone()
        if account:
            self.vaccine.setname(account['name'])
            self.vaccine.setemail(account['email'])
            self.vaccine.setdateofbirth(account['dateofbirth'])
            self.vaccine.setfirstdose(account['firstdose'])
            self.vaccine.setfirstname(account['firstdosename'])
            self.vaccine.setdate(account['date'])
            self.vaccine.setseconddose(account['seconddose'])
            self.vaccine.setseconddate(account['seconddate'])
            self.vaccine.setsecondname(account['seconddosename'])
            return self.vaccine
        return None

    def enterCovidResult(self,mysql,result,cursor):
        cmd = "INSERT INTO test (name, dateofbirth, email, date, result, UniqueId, location) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            result.getname(), result.getdateofbirth(), result.getemail(), result.getdate(), result.getresult(), result.getuniqueid(), result.getlocation())
        cursor.execute(cmd)
        mysql.connection.commit()
