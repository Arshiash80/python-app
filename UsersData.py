import sqlite3



class UserData:
    def __init__(self):
        self.conn = sqlite3.connect("UsersData.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS datas(UserName TEXT, UserPassword TEXT, UserMail TEXT, Checking bool)')
    def NewUser(self,UserName, UserPassword, UserMail, Check):
        isim = self.cursor.execute("SELECT* FROM datas WHERE UserName = ?", (UserName, ))
        liste_isim = isim.fetchall()
        mail = self.cursor.execute("SELECT* FROM datas WHERE UserMail = ?", (UserMail, ))
        liste_mail = mail.fetchall()
        mevcut = self.cursor.execute("SELECT* FROM datas WHERE UserName = ? and UserMail= ?",(UserName, UserMail))
        mevcut_mu = mevcut.fetchall()
        if len(liste_isim) == 0 and len(liste_mail) == 0:
            self.cursor.execute("INSERT INTO datas VALUES(?,?,?,?)",(UserName, UserPassword, UserMail, Check))
            self.conn.commit()
        else:
            if len(mevcut_mu) != 0 :
                return 'mevcut'
            elif len(liste_isim) != 0 :

                return 'isim'
            elif len(liste_mail) != 0 :
                return 'mail'
    def query(self,UserName, UserPassword):
        query = self.cursor.execute("SELECT UserPassword = ? FROM datas WHERE UserName = ?",(UserPassword, UserName))
        query_list = query.fetchall()
        if len(query_list) == 0:
            return 0 #kullanici hoc yok
        elif len(query_list) == 1 :
            if query_list[0][0] == 1:
                return 2 #kullanici var
            elif query_list[0][0] == 0:
                return 1 #isim dogru sifre yanlis
if __name__ == "__main__":
    user = UserData()
    print(user.NewUser('name','pass','gmail',True))
