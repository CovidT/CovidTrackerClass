
class CovidTestResult:
    name = 'null'
    dateofbirth = 'null'
    email = 'null'
    location = 'null'
    uniqueid = 'null'
    date = 'null'
    result ='null'

    def getname(self):
        return self.name

    def getdateofbirth(self):
        return self.dateofbirth

    def getemail(self):
        return self.email

    def getlocation(self):
        return self.location

    def getuniqueid(self):
        return self.uniqueid

    def getdate(self):
        return self.date

    def getresult(self):
        return self.result

    def setname(self,name):
         self.name = name

    def setdateofbirth(self,dateofbirth):
         self.dateofbirth = dateofbirth

    def setemail(self,email):
         self.email =email

    def setlocation(self,location):
        self.location = location

    def setuniqueid(self,uniqueid):
         self.uniqueid = uniqueid

    def setdate(self,date):
         self.date = date

    def setresult(self,result):
        self.result = result