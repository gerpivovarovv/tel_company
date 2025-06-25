import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QHeaderView, QTreeWidgetItem
from PyQt5.QtCore import Qt
from main_win import PersCab
from avtor import WinAv
from reg import WinReg
from pop_bal import PopBal
from pop_min import PopMin
from pop_sms import PopSms
from pop_gig import PopGig
from tariph import ChTar
from adm_cab import AdmCab
from statis import Stat
from cr_tar import CrTar
from edit_tr import EditTar
from del_tar import DelTar
from first_win import FirstWin
from random import choice, randint
from connect import ConeBase


class Company:
    def __init__(self, w_first):
        self.obj_bd = ConeBase()
        self.obj = self.obj_bd.con_base()
        self.cur = self.obj.cursor()
        self.w_reg = WinReg()
        self.w_first = w_first
        self.w_av = WinAv()
        self.w_pers_cab = PersCab()
        self.w_pop_bal = PopBal()
        self.w_pop_min = PopMin()
        self.w_pop_sms = PopSms()
        self.w_pop_gig = PopGig()
        self.w_ch_tar = ChTar()
        self.w_adm_cab = AdmCab()
        self.w_stat = Stat()
        self.w_cr_tar = CrTar()
        self.w_edit_tar = EditTar()
        self.w_del_tar = DelTar()
        self.first_win()


    def first_win(self):
        self.w_first.avtor.clicked.connect(self.show_win_auth)
        self.w_first.reg.clicked.connect(self.show_win_reg)

    def show_win_reg(self):
        self.w_first.hide()
        self.w_reg.show()
        self.w_av.hide()
        self.w_reg.reg_bt.clicked.connect(self.registration)

    def show_win_auth(self):
        self.w_first.hide()
        self.w_av.show()
        self.w_av.reg_bt.clicked.connect(self.show_win_reg)
        self.w_av.avt_bt.clicked.connect(self.authorisation)

    def check_paswd(self):
        paswd = self.w_reg.passwd.text().strip()
        simb = ['*', '&', '{', '}', '|', '+']
        numbs = [str(i) for i in range(10)]
        if len(paswd) < 4 or len(paswd) > 16:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка регистрации")
            msg.setText('''Пароль должен:
            - содержать от 4 до 16 символов
            - содержать минимум 1 заглавную букву
            - содержать минимум 1 цифру
            - не содержать символы: *, &, {, }, |, +''')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            if paswd == paswd.lower():
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка регистрации")
                msg.setText('''Пароль должен:
                - содержать от 4 до 16 символов
                - содержать минимум 1 заглавную букву
                - содержать минимум 1 цифру
                - не содержать символы: *, &, {, }, |, +''')
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                paswd = ''
            else:
                for i in simb:
                    if i in paswd:
                        msg = QMessageBox()
                        msg.setWindowTitle("Ошибка регистрации")
                        msg.setText('''Пароль должен:
                        - содержать от 4 до 16 символов
                        - содержать минимум 1 заглавную букву
                        - содержать минимум 1 цифру
                        - не содержать символы: *, &, {, }, |, +''')
                        msg.setIcon(QMessageBox.Warning)
                        msg.exec_()
                        paswd = ''
                        break
                    else:
                        flag = False
                        for j in numbs:
                            if j in paswd:
                                flag = True
                        if flag is False:
                            paswd = ''
                            break
            return paswd

    def registration(self):
        nam = self.w_reg.name.text()
        sur = self.w_reg.surname.text()
        patr = self.w_reg.patron.text()
        log = self.w_reg.log.text()
        paswd = self.check_paswd()
        birth_date = str(self.w_reg.dateEdit.date().toPyDate())
        pasp = str(self.w_reg.pasp.text())
        if paswd is None or paswd == '':
            pass
        else:
            self.cur.execute(f'''INSERT INTO users (pasp, birth, login, passwd, nam, surname, patronymic, type)
            VALUES ('{pasp}', '{birth_date}', '{log}', '{paswd}', '{nam}', '{sur}', '{patr}', "Пользователь");''')
            self.obj.commit()
            self.cur.execute(f'SELECT users_id FROM users WHERE pasp = {pasp}')
            id_cl = int(str(self.cur.fetchone())[1:3])
            numb = choice(['965', '963']) + str(randint(1000000, 9999999))
            self.cur.execute(f"INSERT INTO phone_numb (numb, bal, minut_ost, sms_ost, gig_ost, tariph_tariph_id,"
                             f"users_users_id) VALUES ({numb}, {0.00}, {0}, {0}, {0.0}, {0}, {id_cl});")
            self.obj.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Уведомление")
            msg.setText("Пользователь успешно зарегистрирован")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.w_reg.hide()
            self.w_av.show()
            self.show_win_auth()

    def authorisation(self):
        self.cur.execute('SELECT * FROM users')
        spis = self.cur.fetchall()
        user = (self.w_av.login.text(), self.w_av.parol.text())
        flag = False
        for row in spis:
            if user == row[3:5]:
                if row[-1] == 'Пользователь':
                    flag = True
                    self.user_data = row
                    # print(self.user_data)
                    self.w_av.hide()
                    self.mainwin()
                else:
                    flag = True
                    self.w_av.hide()
                    self.administartion()

        if flag is False:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка авторизации")
            msg.setText("Данного пользователя нет или введён неверный пароль")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def mainwin(self):
        self.w_ch_tar.hide()
        self.w_pop_min.hide()
        self.w_pop_sms.hide()
        self.w_pop_gig.hide()
        self.w_pers_cab.show()
        self.cur.execute(f'SELECT * FROM phone_numb JOIN tariph ON tariph_tariph_id = tariph_id WHERE users_users_id = {self.user_data[0]}')
        # print(self.cur.fetchone())
        self.user_num = self.cur.fetchone()
        # print(self.user_num)
        self.w_pers_cab.nam_text.setText(self.user_data[5])
        self.w_pers_cab.sur_text.setText(self.user_data[6])
        self.w_pers_cab.patr_text.setText(self.user_data[7])
        self.w_pers_cab.number.setText(f'+7({self.user_num[0][0:3]}){self.user_num[0][3:6]}-{self.user_num[0][6:8]}-{self.user_num[0][8:]}')
        self.w_pers_cab.bal.setText(f'{str(float(self.user_num[1]))}₽')
        self.w_pers_cab.tariph.setText(f'Тариф: {self.user_num[8]}')
        self.w_pers_cab.min.setText(f'{str(self.user_num[2])} мин')
        self.w_pers_cab.sms.setText(f'{str(self.user_num[3])} смс')
        self.w_pers_cab.gig.setText(f'{str(float(self.user_num[4]))} гб')
        self.history()
        self.w_pers_cab.bt_pop_bal.clicked.connect(self.pop_bal)
        self.w_pers_cab.bt_pop_min.clicked.connect(self.pop_min)
        self.w_pers_cab.bt_pop_sms.clicked.connect(self.pop_sms)
        self.w_pers_cab.bt_pop_gig.clicked.connect(self.pop_gig)
        self.w_pers_cab.bt_ch_tar.clicked.connect(self.chan_tar)
        self.w_pers_cab.exit.clicked.connect(self.pers_exit)

    def pers_exit(self):
        self.w_av.login.clear()
        self.w_av.parol.clear()
        self.w_pers_cab.hide()
        self.first_win()
        self.w_first.show()


    def pop_bal(self):
        self.w_pers_cab.hide()
        self.w_pop_bal.show()
        try:
            self.w_pop_bal.bt_pop.clicked.disconnect()
        except TypeError:
            pass    # Если не было соединений, просто пропускаем ошибку
        self.w_pop_bal.bt_pop.clicked.connect(self.plus_money)

    def plus_money(self):
        plus_amount = float(self.w_pop_bal.money.text())
        self.cur.execute(f'UPDATE phone_numb SET bal = bal + {plus_amount} WHERE users_users_id = {self.user_data[0]}')
        self.obj.commit()
        self.w_pop_bal.hide()
        self.mainwin()

    def pop_min(self):
        self.w_pers_cab.hide()
        self.w_pop_min.show()
        self.w_pop_min.kol_min.setRange(0, 3000)

        try:
            self.w_pop_min.kol_min.valueChanged.disconnect()
        except TypeError:
            pass
        self.w_pop_min.kol_min.valueChanged.connect(self.upd_min)

        try:
            self.w_pop_min.cancel.clicked.disconnect()
        except TypeError:
            pass
        self.w_pop_min.cancel.clicked.connect(self.mainwin)

        try:
            self.w_pop_min.popol_min.clicked.disconnect()
        except TypeError:
            pass
        self.w_pop_min.popol_min.clicked.connect(self.popol_min)

    def upd_min(self):
        self.mins = self.w_pop_min.kol_min.value()
        self.price = round(self.mins * 1.05, 2)
        self.w_pop_min.itog.setText(f"Итого: {self.price}₽")

    def popol_min(self):
        # print(self.price, self.mins)
        self.cur.execute(f'''SELECT bal FROM phone_numb WHERE numb = {self.user_num[0]}''')
        bal = float(self.cur.fetchone()[0])
        if bal < self.price:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка пополнения")
            msg.setText("На счёте недостаточно средств")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            self.cur.execute(f'UPDATE phone_numb SET bal = bal - {self.price}, minut_ost = minut_ost + {self.mins}'
                             f' WHERE numb = {self.user_num[0]}')
            self.obj.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Операция прошла успешно")
            msg.setText(f"Ваш счёт был пополнен на {self.mins} минут")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.mainwin()


    def pop_sms(self):
        self.w_pers_cab.hide()
        self.w_pop_sms.show()
        self.w_pop_sms.kol_sms.setRange(0, 1000)

        try:
            self.w_pop_sms.kol_sms.valueChanged.disconnect()
        except TypeError:
            pass
        self.w_pop_sms.kol_sms.valueChanged.connect(self.upd_sms)

        try:
            self.w_pop_sms.cancel.clicked.disconnect()
        except TypeError:
            pass
        self.w_pop_sms.cancel.clicked.connect(self.mainwin)

        try:
            self.w_pop_sms.pop_sms.clicked.disconnect()
        except TypeError:
            pass
        self.w_pop_sms.pop_sms.clicked.connect(self.popol_sms)

    def upd_sms(self):
        self.sms = self.w_pop_sms.kol_sms.value()
        self.price = round(self.sms * 1.02, 2)
        self.w_pop_sms.itog.setText(f"Итого: {self.price}₽")

    def popol_sms(self):
        self.cur.execute(f'''SELECT bal FROM phone_numb WHERE numb = {self.user_num[0]}''')
        bal = float(self.cur.fetchone()[0])
        if bal < self.price:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка пополнения")
            msg.setText("На счёте недостаточно средств")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            self.cur.execute(f'UPDATE phone_numb SET bal = bal - {self.price}, sms_ost = sms_ost + {self.sms}'
                             f' WHERE numb = {self.user_num[0]}')
            self.obj.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Операция прошла успешно")
            msg.setText(f"Ваш счёт был пополнен на {self.sms} SMS")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.mainwin()

    def pop_gig(self):
        self.w_pers_cab.hide()
        self.w_pop_gig.show()
        self.w_pop_gig.kol_gig.setRange(0, 50)

        try:
            self.w_pop_gig.kol_gig.valueChanged.disconnect()
        except TypeError:
            pass
        self.w_pop_gig.kol_gig.valueChanged.connect(self.upd_gig)

        try:
            self.w_pop_gig.cancel.clicked.disconnect()
        except TypeError:
            pass
        self.w_pop_gig.cancel.clicked.connect(self.mainwin)

        try:
            self.w_pop_gig.popol_gig.clicked.disconnect()
        except TypeError:
            pass
        self.w_pop_gig.popol_gig.clicked.connect(self.popol_gig)

    def upd_gig(self):
        self.gigs = self.w_pop_gig.kol_gig.value()
        self.price = round(self.gigs * 25.5, 2)
        self.w_pop_gig.itog.setText(f"Итого: {self.price}₽")

    def popol_gig(self):
        print(self.price, self.gigs)
        self.cur.execute(f'''SELECT bal FROM phone_numb WHERE numb = {self.user_num[0]}''')
        bal = float(self.cur.fetchone()[0])
        if bal < self.price:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка пополнения")
            msg.setText("На счёте недостаточно средств")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            self.cur.execute(f'UPDATE phone_numb SET bal = bal - {self.price}, gig_ost = gig_ost + {float(self.gigs)}'
                             f' WHERE numb = {self.user_num[0]}')
            self.obj.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Операция прошла успешно")
            msg.setText(f"Ваш счёт был пополнен на {self.gigs} гигабайт")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.mainwin()

    def chan_tar(self):
        self.w_pers_cab.hide()
        self.w_ch_tar.show()

        try:
            self.w_ch_tar.cancel.clicked.disconnect()
        except TypeError:
            pass
        self.w_ch_tar.cancel.clicked.connect(self.mainwin)

        if self.w_ch_tar.tarbox.currentText() == '':
            self.cur.execute('''SELECT * FROM tariph''')
            spis = self.cur.fetchall()
            # print(spis)
            del spis[0]
            for i in spis:
                self.w_ch_tar.tarbox.addItem(f'{i[1]}: {i[2]}₽, {i[3]} мин, {i[4]} sms, {i[5]} гб')
        else:
            pass

        try:
            self.w_ch_tar.confirm.clicked.disconnect()
        except TypeError:
            pass
        self.w_ch_tar.confirm.clicked.connect(self.buy_tar)

    def buy_tar(self):
        tar = str(self.w_ch_tar.tarbox.currentText()).split(' ')
        nam_tar = tar[0][:-1]
        print(nam_tar)
        self.cur.execute(f"SELECT tariph_id, price, minut_kol, sms_kol, gig_kol "
                         f"FROM tariph WHERE tariph_name LIKE '{nam_tar}'")
        tariph = self.cur.fetchone()
        tarph = {'id': '', 'price': '', 'min_kol': '', 'sms_kol': '', 'gig_kol': ''}
        j = 0
        for i in tarph:
            tarph[i] = tariph[j]
            j += 1
        # print(tarph)
        self.cur.execute(f'''SELECT bal FROM phone_numb WHERE numb = {self.user_num[0]}''')
        bal = float(self.cur.fetchone()[0])
        if tarph['price'] < bal:
            self.cur.execute(f'UPDATE phone_numb SET bal = bal - {tarph['price']}, tariph_tariph_id = {tarph['id']},'
                             f'minut_ost = {tarph['min_kol']}, sms_ost = {tarph['sms_kol']}, gig_ost = {tarph['gig_kol']}'
                             f' WHERE numb = {self.user_num[0]}')
            self.obj.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Операция прошла успешно")
            msg.setText(f"Тариф {nam_tar} успешно приобретён!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.mainwin()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("На счёте недостаточно средств")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def history(self):
        self.w_pers_cab.history.setColumnCount(3)
        self.w_pers_cab.history.setHeaderLabels(['Тип', 'Дата', 'Номер абонента'])
        self.w_pers_cab.history.expandAll()
        self.cur.execute(f'''SELECT * FROM zhurnal_call WHERE phone_phone_numb = {self.user_num[0]}''')
        data_call = self.cur.fetchall()
        self.cur.execute(f'''SELECT * FROM zhurnal_sms WHERE phone_phone_numb = {self.user_num[0]}''')
        data_sms = self.cur.fetchall()
        # print(data_call)
        # print(data_sms)
        for i in data_call:
            row = QTreeWidgetItem(self.w_pers_cab.history, ['Звонок', str(i[2]),
                                                            f'+7({i[1][0:3]}){i[1][3:6]}-{i[1][6:8]}-{i[1][8:]}'])
            row.setTextAlignment(0, Qt.AlignCenter)
        for i in data_sms:
            row = QTreeWidgetItem(self.w_pers_cab.history, ['SMS', str(i[2]),
                                                            f'+7({i[1][0:3]}){i[1][3:6]}-{i[1][6:8]}-{i[1][8:]}'])
            row.setTextAlignment(0, Qt.AlignCenter)
        header = self.w_pers_cab.history.header()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)


    def administartion(self):
        self.w_adm_cab.show()
        self.w_adm_cab.stat.clicked.connect(self.stat)
        self.w_adm_cab.cr_tar.clicked.connect(self.cr_tar)
        self.w_adm_cab.edit_tar.clicked.connect(self.edit_tar)
        self.w_adm_cab.del_tar.clicked.connect(self.del_tar)
        self.w_adm_cab.exit.clicked.connect(self.adm_exit)

    def adm_exit(self):
        self.w_av.login.clear()
        self.w_av.parol.clear()
        self.w_adm_cab.hide()
        self.first_win()
        self.w_first.show()

    def stat(self):
        self.w_stat.show()
        self.w_stat.stat.setAlignment(Qt.AlignCenter)
        self.w_stat.avg_bal.clicked.connect(self.avg_bal)
        self.w_stat.avg_tar.clicked.connect(self.avg_tar)
        self.w_stat.user_list.clicked.connect(self.info_users)
        self.w_stat.use_tar.clicked.connect(self.use_tar)

    def avg_bal(self):
        self.cur.execute('''SELECT AVG(bal) FROM phone_numb''')
        bal = float(self.cur.fetchone()[0])
        self.w_stat.stat.setText(f'Средний баланс: {round(bal, 2)}₽')

    def info_users(self):
        self.cur.execute('''SELECT nam, surname, patronymic, numb, tariph_name 
                        FROM users 
                        JOIN (
                            SELECT numb, tariph_name, users_users_id 
                            FROM phone_numb 
                            JOIN tariph ON tariph_tariph_id = tariph_id
                            ) AS subtable
                        ON users_id = users_users_id ORDER BY nam;''')
        data = self.cur.fetchall()
        stats = 'Список пользователей\n'
        for i in data:
            stats += f'{i[0]} {i[1]} {i[2]}, +7({i[3][0:3]}){i[3][3:6]}-{i[3][6:8]}-{i[3][8:]}, Тариф - {i[4]}\n'
        self.w_stat.stat.setText(stats)


    def avg_tar(self):
        self.cur.execute('''SELECT AVG(price) FROM tariph''')
        price = float(self.cur.fetchone()[0])
        self.w_stat.stat.setText(f'Средняя стоимость тарифа: {round(price, 2)}₽')

    def use_tar(self):
        self.cur.execute('''SELECT t.tariph_name, COUNT(p.numb) AS num_users
                        FROM company.tariph t
                        LEFT JOIN company.phone_numb p ON t.tariph_id = p.tariph_tariph_id
                        GROUP BY t.tariph_name;''')
        data = self.cur.fetchall()
        stats = 'Использование тарифов\n'
        for i in data:
            stats += f'{i[0]} - {i[1]}\n'
        self.w_stat.stat.setText(stats)

    def cr_tar(self):
        self.w_cr_tar.show()
        try:
            self.w_cr_tar.cr_tar.clicked.disconnect()
        except TypeError:
            pass
        self.w_cr_tar.cr_tar.clicked.connect(self.create_tariph)

    def create_tariph(self):
        nam = self.w_cr_tar.nam.text()
        price = self.w_cr_tar.price.text()
        mins = self.w_cr_tar.mins.text()
        sms = self.w_cr_tar.sms.text()
        gigs = self.w_cr_tar.gigs.text()
        self.cur.execute('''SELECT tariph_name FROM tariph''')
        tariph_names = self.cur.fetchall()
        flag = True
        for i in tariph_names:
            if i[0] == nam:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Такой тариф уже существует")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                flag = False
            else:
                pass
        if flag is True:
            self.cur.execute(f'''INSERT INTO tariph(tariph_name, price, minut_kol, sms_kol, gig_kol) VALUES
            ('{nam}', {int(price)}, {int(mins)}, {int(sms)}, {int(gigs)});''')
            self.obj.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Операция прошла успешно")
            msg.setText(f"Тариф создан успешно")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        else:
            pass

    def edit_tar(self):
        self.w_edit_tar.show()
        if self.w_edit_tar.tarbox.currentText() == '':
            self.cur.execute('''SELECT * FROM tariph''')
            spis = self.cur.fetchall()
            del spis[0]
            for i in spis:
                self.w_edit_tar.tarbox.addItem(f'{i[1]}: {i[2]}₽, {i[3]} мин, {i[4]} sms, {i[5]} гб')
        else:
            pass
        self.w_edit_tar.tarbox.currentTextChanged.connect(self.text_changed)
        try:
            self.w_edit_tar.cr_tar.clicked.disconnect()
        except TypeError:
            pass
        self.w_edit_tar.cr_tar.clicked.connect(self.ed_tar)

    def text_changed(self):
        self.tar = str(self.w_edit_tar.tarbox.currentText()).split(' ')
        try:
            self.w_edit_tar.price.setText(self.tar[1][:-2])
            self.w_edit_tar.mins.setText(self.tar[2])
            self.w_edit_tar.sms.setText(self.tar[4])
            self.w_edit_tar.gigs.setText(self.tar[6])
        except IndexError:
            pass

    def ed_tar(self):
        price = self.w_edit_tar.price.text()
        mins = self.w_edit_tar.mins.text()
        sms = self.w_edit_tar.sms.text()
        gigs = self.w_edit_tar.gigs.text()

        # data = [('Базовый', 300, 100, 50, 2),
        #         ('Комфорт', 500, 300, 100, 5),
        #         ('Премиум', 1000, 1000, 500, 15),
        #         ('Стартовый', 200, 50, 20, 1),
        #         ('Оптимум', 500, 400, 150, 7),
        #         ('Семейный', 1200, 1200, 400, 20),
        #         ('Ультра', 1500, 2000, 1000, 50),
        #         ('Молодёжный', 400, 200, 150, 3),
        #         ('Бизнес', 2000, 3000, 2000, 70),
        #         ('Выгодный', 500, 250, 100, 4)]
        # for i in data:
        #     self.cur.execute(f'''UPDATE tariph SET price = {i[1]}, minut_kol = {i[2]}, sms_kol = {i[3]},
        #             gig_kol = {i[4]} WHERE tariph_name = "{i[0]}"''')
        #     self.obj.commit()

        self.cur.execute(f'''UPDATE tariph SET price = {int(price)}, minut_kol = {int(mins)}, sms_kol = {int(sms)},
        gig_kol = {int(gigs)} WHERE tariph_name = "{self.tar[0][:-1]}"''')
        self.obj.commit()
        msg = QMessageBox()
        msg.setWindowTitle("Операция успешна")
        msg.setText(f"Тариф изменён успешно")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.w_edit_tar.hide()
        self.w_adm_cab.hide()
        self.w_edit_tar.tarbox.clear()
        self.administartion()

    def del_tar(self):
        self.w_del_tar.show()
        if self.w_del_tar.tarbox.currentText() == '':
            self.cur.execute('''SELECT * FROM tariph''')
            spis = self.cur.fetchall()
            del spis[0]
            for i in spis:
                self.w_del_tar.tarbox.addItem(f'{i[1]}: {i[2]}₽, {i[3]} мин, {i[4]} sms, {i[5]} гб')
        else:
            pass
        try:
            self.w_del_tar.del_tar.clicked.disconnect()
        except TypeError:
            pass
        self.w_del_tar.del_tar.clicked.connect(self.delete_tariph)

    def delete_tariph(self):
        tar = str(self.w_del_tar.tarbox.currentText()).split(' ')
        print(tar)
        self.cur.execute(f'''DELETE FROM tariph WHERE tariph_name = "{tar[0][:-1]}"''')
        self.obj.commit()
        self.w_del_tar.tarbox.clear()
        msg = QMessageBox()
        msg.setWindowTitle("Операция прошла успешно")
        msg.setText(f"Тариф удалён")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.del_tar()


app = QApplication(sys.argv)
w_first = FirstWin()
w_first.show()
c = Company(w_first)
sys.exit(app.exec_())