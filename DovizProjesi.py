from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow , QMessageBox ,QLCDNumber
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QSize, QRect, QPropertyAnimation , QTime , Qt
import sys
import requests
from bs4 import BeautifulSoup
from UsersData import UserData

# TODO Mail Gonder

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ud = UserData()
        self.time = QTime.currentTime()
        self.time = self.time.toString(Qt.DefaultLocaleLongDate)
        self.__fading_button = None
        self.doviz = Doviz()

        self.ui = Ui_MainWindow()
        self.a = self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/MainLogo/Logo.png')) # QIcon(':/pefix/<file>...</file>') !!! Window Icon

        self.ui.Button_Exit.hide()
        self.ui.Frame_NewAccount.hide()
        self.ui.Text_NewAccount.clicked.connect(lambda : self.clicked(self.sender()))
        self.ui.Button_CreateAccount.clicked.connect(lambda : self.sorgula2(self.ui.Frame_NewAccount_User.text(),self.ui.Frame_NewAccount_Gmail.text(),self.ui.Frame_NewAccount_Pass.text(),self.ui.Frame_NewAccount_PassConfirm.text(), self.ui.checkBox.isChecked()))

        self.ui.LCD_clock.setSegmentStyle(QLCDNumber.Filled)
        self.ui.LCD_clock.setDigitCount(8)
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)

        self.ChangeBackground(self.time.split())
        self.ui.Text_NewAccount.hide()
        self.ui.Text_Login.hide()
        self.ui.Frame_Login.hide()

        self.ui.Button_Update.clicked.connect(self.animation) #animasyona baglan
        self.ui.Text_Login_2.clicked.connect(self.animation)
        self.ui.Button_CreateAccount.clicked.connect(self.animation)
        self.ui.Button_Exit.clicked.connect(self.animation)
        self.ui.Button_Login.clicked.connect(self.animation)
        self.ui.Button_NewAccount.clicked.connect(self.animation)

        self.ui.Text_Login_2.clicked.connect(lambda : self.sorgula(self.ui.Frame_Login_User.text(), self.ui.Frame_Login_Pass.text()))

        self.setGeometry(550,150,840,405)
        self.setMinimumHeight(405)
        self.setMaximumHeight(405)
        self.ui.Text_Login.clicked.connect(lambda : self.clicked(self.sender()))
    def displayTime(self):
        currentTime = QTime.currentTime()
        displayText = currentTime.toString('hh:mm:ss')
        self.ui.LCD_clock.display(displayText)
    def sorgula2(self,UserName,UserMail,UserPass,ConfirmPass,Check):
        if UserName == '' or UserMail == '' or UserPass == '' :
           self.message(7)
        else:
            if UserPass != ConfirmPass :
                self.message(3)
            else:
                if self.ud.NewUser(UserName, UserPass, UserMail, Check) == 'mevcut':
                    self.message(4)
                elif self.ud.NewUser(UserName, UserPass, UserMail, Check) == 'isim':
                    self.message(5)
                elif self.ud.NewUser(UserName, UserPass, UserMail, Check) == 'mail':
                    self.message(6)
                else :
                    self.ui.Frame_NewAccount_Gmail.clear()
                    self.ui.Frame_NewAccount_Pass.clear()
                    self.ui.Frame_NewAccount_PassConfirm.clear()
                    self.ui.Frame_NewAccount_User.clear()
    def sorgula(self,userName, userPass):
        if self.ud.query(userName, userPass) == 2:
            self.size_animation('go')
            self.UserName = userName.capitalize()
            self.ui.Frame_Login_User.clear()
            self.ui.Frame_Login_Pass.clear()
            self.ui.Button_Exit.show()
            self.ui.Button_Login.hide()
            self.ui.Button_NewAccount.hide()
            self.ui.selamla.setText("Hosgeldin "+self.UserName)
        elif self.ud.query(userName, userPass) == 1:
            self.message(1)
        elif self.ud.query(userName, userPass) == 0:
            self.message(0)
        else:
            self.message()
    def message(self, i):
        detail = None
        if i == 1:
            icon = QMessageBox.Warning
            text = 'Sifrenizi Yanlis!'
            info = 'Sifrenizi Tekrar Kontrol Ediniz.'
            title = 'Ooops..'
            detail = 'Eger sifrenizi unuttuysaniz  sifremi unuttum\'a basiniz'
        elif i == 0 :
            icon = QMessageBox.Warning
            text = 'Kullanici Bilgileri Yanlis!'
            info = 'Boyle Bir Hesap Mevcut Degil.'
            title = 'Hmm...'
        elif i == 2 :
            icon = QMessageBox.Critical
            text = 'Bir Hata Olustu!'
            info = 'Beklenmedik Bir Hata olustu.'
            title = 'Hata!!'
        elif i == 3: #sifreler uyusmuyorsa
            icon = QMessageBox.Warning
            text = 'Sifreler Uyusmadi'
            info = 'Sifreniz Birbiriyle Uyusmadi Lutfen Daha Dikkatli Giriiniz'
            title = 'Sifre Uyusmadi!'
        elif i == 4 : #Kullanici mevcutsa
            icon = QMessageBox.Information
            text = 'Kullanici Zaten Mevcut'
            info = 'Boyle Bir Kullanici Zaten Mevcut!'
            title = 'Kullanici Mevcut'
            detail = 'Eger sifrenizi unuttuysaniz login sekmesindeki sifremi unuttum\'a basabilirsiniz.'
        elif i == 5 : #isim kullaniliyorsa
            icon = QMessageBox.Information
            text = 'Kullanici Adi Zaten Alinmis'
            info = None
            title = 'Kullanici Adi'
        elif i == 6 : #mail kullaniliyorsa
            icon = QMessageBox.Information
            text = 'Mail Adresi Zaten Mevcut'
            info = None
            title = 'Mail Adresi'
        elif i == 7 : #bos kutucuk varsa
            icon = QMessageBox.Warning
            text = 'Isetenen bilgilerin hepsini girmeye ozen gosteriniz!'
            info = None
            title = 'Uyari!'

        msg = QMessageBox()
        msg.setDetailedText(detail)
        msg.setObjectName('haydar')
        msg.setIcon(icon)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setWindowTitle(title)
        msg.setWindowIcon(QIcon(":/Message/message.png"))
        msg.exec_()

    def ChangeBackground(self,list):
        list = list[0]
        if int(list[0]) > 7 or int(list[0]) <= 2 :
            self.ui.centralwidget.setStyleSheet("#centralwidget{\n"
                                                "border-image: url(:/Background/NightBackground.jpg);\n"
                                                "}")
        else:
            self.ui.centralwidget.setStyleSheet("#centralwidget{\n"
                                             "border-image: url(:/Background/DayBackground.jpg);\n"
                                             "}")

    def guncel_doviz(self):
        self.doviz.veri_cek()
        self.ui.label_GramAltin.setText(self.doviz.Altin_deger+' tl')
        self.ui.label_Dolar.setText(self.doviz.Dolar_deger+' tl')
        self.ui.label_Sterlin.setText(self.doviz.Sterlin_deger+' tl')
        self.ui.label_Euro.setText(self.doviz.Euro_deger+' tl')
        self.ui.Altin_Degisim.setText(self.doviz.Altin_degisim)
        self.ui.Dolar_Degisim.setText(self.doviz.Dolar_degisim)
        self.ui.Sterlin_Degisim.setText(self.doviz.Sterlin_degisim)
        self.ui.Euro_Degisim.setText(self.doviz.Euro_degisim)
        self.degisim_icon(self.doviz.dolar_change, self.doviz.Dolar_isim)
        self.degisim_icon(self.doviz.altin_change, self.doviz.Altin_isim)
        self.degisim_icon(self.doviz.euro_change, self.doviz.Euro_isim)
        self.degisim_icon(self.doviz.sterlin_change, self.doviz.Sterlin_isim)
    def degisim_icon(self, changes, name):
        if name == 'DOLAR':
            if changes > 0:
                self.ui.Dolar_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsUp.png);")
                self.ui.Dolar_Degisim.setStyleSheet("color: green")
            else:
                self.ui.Dolar_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsDown.png);")
                self.ui.Dolar_Degisim.setStyleSheet("color: red")
        elif name == 'GRAM ALTIN':
            if changes > 0:
                self.ui.Altin_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsUp.png);")
                self.ui.Altin_Degisim.setStyleSheet('color: green')
            else:
                self.ui.Altin_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsDown.png);")
                self.ui.Altin_Degisim.setStyleSheet('color: red')
        elif name == 'EURO':
            if changes > 0:
                self.ui.Euro_Degisim.setStyleSheet('color: green')
                self.ui.Euro_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsUp.png);")
            else:
                self.ui.Euro_Degisim.setStyleSheet('color: red')
                self.ui.Euro_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsDown.png);")
        elif name == 'STERLİN':
            if changes > 0:
                self.ui.Sterlin_Degisim.setStyleSheet('color: green')
                self.ui.Sterlin_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsUp.png);")
            else:
                self.ui.Sterlin_Degisim.setStyleSheet('color: red')
                self.ui.Sterlin_Degisim_Icon.setStyleSheet("image: url(:/icons/ArrowsDown.png);")

    def animation(self):#animasyon baslangici
        self.__fading_button = self.sender()  # enter the "fading button" state
        if self.__fading_button.objectName() == 'Button_Login':
            if self.ui.Text_Login.isHidden():
                self.ui.Text_Login.show()
            else:
                self.ui.LCD_clock.move(260, 140)
                self.ui.LCD_clock.resize(341, 91)
                self.ui.Text_Login.hide()
                self.ui.Frame_Login.hide()
        elif self.__fading_button.objectName() == 'Button_NewAccount':
            if self.ui.Text_NewAccount.isHidden():
                self.ui.Text_NewAccount.show()
            else:
                self.ui.LCD_clock.move(260, 140)
                self.ui.LCD_clock.resize(341, 91)
                self.ui.Frame_NewAccount.hide()
                self.ui.Text_NewAccount.hide()
        elif self.__fading_button.objectName() == 'Button_Exit': # ---->>>> cikis butonunun fonskiyonu !! <<<<-------
            self.ui.Button_Exit.hide()
            self.ui.Button_Login.show()
            self.ui.Button_NewAccount.show()
            self.setMinimumHeight(405)
            self.setMaximumHeight(405)


        self.__fading_button.setIconSize(QSize(65, 65))
        QTimer.singleShot(100, self.BackNormal)
        self.clicked(self.__fading_button)
    def BackNormal(self):#animasyon bitsi
        self.__fading_button.setIconSize(QSize(50, 50))
        self.__fading_button = None  # exit the "fading button" state

    def clicked(self, sender):
        if sender.objectName() == "Button_Update":
            self.guncel_doviz()
        elif sender.text() == 'LOGIN':
            self.ui.LCD_clock.move(580,330)
            self.ui.LCD_clock.resize(251,61)
            self.ui.Text_NewAccount.hide()
            self.ui.Frame_NewAccount.hide()
            self.size_animation('LOGIN')
        elif sender.objectName() == 'Text_NewAccount' :
            self.ui.Frame_NewAccount.show()
            self.ui.LCD_clock.move(10,330)
            self.ui.LCD_clock.resize(251, 61)
            self.ui.Text_Login.hide()
            self.ui.Frame_Login.hide()
            self.size_animation('NewAccount')
    def size_animation(self, inf):
        if inf == 'LOGIN':
            self.ui.Frame_Login.show()
        elif inf == 'go' :
            self.anim = QPropertyAnimation(self , b'geometry')
            self.anim.setDuration(9000)
            self.anim.setStartValue(QRect(550,150,840,406))
            self.anim.setEndValue(QRect(550,150,840,801))
            self.anim.start()
            self.setMaximumHeight(808)
            self.setMinimumHeight(808)
            self.ui.Frame_Login.hide()
            self.ui.Text_Login.hide()
            self.ui.LCD_clock.move(260, 140)
            self.ui.LCD_clock.resize(341, 91)
class Doviz():
    def __init__(self):
        self.url = 'https://www.doviz.com/'
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            self.veri_cek()
    def veri_cek(self):
        self.html_icerigi = self.response.content
        self.soup = BeautifulSoup(self.html_icerigi, 'lxml')
        for alan in self.soup.find_all('div', class_='market-data'):
            for items in alan.find_all('div',class_='item'):
                for altin in items.find_all('a',onclick="trackEvent(this, 'Ana Sayfa', 'Header', 'Gram Altın');"):
                    self.Altin_isim = altin.find('span', class_='name').text.strip()
                    self.Altin_deger = altin.find('span', class_='value').text.strip()
                    self.Altin_degisim = altin.find('div', class_='change').text.strip()
                    self.altin_change = float('.'.join(self.Altin_degisim.strip('%').split(',')))
                for dolar in items.find_all('a', onclick="trackEvent(this, 'Ana Sayfa', 'Header', 'USD'); "):
                    self.Dolar_isim = dolar.find('span', class_='name').text.strip()
                    self.Dolar_deger = dolar.find('span', class_='value').text.strip()
                    self.Dolar_degisim = dolar.find('div', class_='change').text.strip()
                    self.dolar_change = float('.'.join(self.Dolar_degisim.strip('%').split(',')))
                for euro in items.find_all('a',onclick="trackEvent(this, 'Ana Sayfa', 'Header', 'EUR'); "):
                    self.Euro_isim = euro.find('span', class_='name').text.strip()
                    self.Euro_deger = euro.find('span', class_='value').text.strip()
                    self.Euro_degisim = euro.find('div', class_='change').text.strip()
                    self.euro_change = float('.'.join(self.Euro_degisim.strip('%').split(',')))
                for sterlin in items.find_all('a', onclick="trackEvent(this, 'Ana Sayfa', 'Header', 'GBP'); "):
                    self.Sterlin_isim = sterlin.find('span', class_='name').text.strip()
                    self.Sterlin_deger = sterlin.find('span', class_='value').text.strip()
                    self.Sterlin_degisim = sterlin.find('div', class_='change').text.strip()
                    self.sterlin_change = float('.'.join(self.Sterlin_degisim.strip('%').split(',')))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


