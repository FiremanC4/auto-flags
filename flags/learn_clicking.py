from pyrogram import Client, filters, idle
from pyrogram.types import Message, Chat
from pyrogram.errors.exceptions.bad_request_400 import DataInvalid
import pretify_flags
import time
import random 
import re

import os

path = os.path.realpath(__file__)
path = os.path.dirname(path)
os.chdir(path)


class Flags:
    def __init__(self, *, log):
        self.log = log
        self.num = 0
        self.time = 600
        self.flags = {'🇳🇴': 'Норвегія',
         '🇳🇿': 'Нова Зеландія',
         '🇸🇦': 'Саудівська Аравія',
         '🇲🇽': 'Мексика',
         '🇳🇮': 'Нікарагуа',
         '🇸🇨': 'Сейшельські Острови',
         '🇨🇦': 'Канада',
         '🇰🇼': 'Кувейт',
         '🇲🇨': 'Монако',
         '🇰🇷': 'Південна Корея',}
        self.pr_fl = ''
        self.pr_tx = ''
        self.pr_kb = None
     
    def load(self):
        fls = pretify_flags.load()
        self.flags = fls

    def save(self):
        pretify_flags.save(self.flags)

    def get(self, fl, fi):
        self.pr_fl = fl
        self.pr_tx = fi
        if fl in self.flags:
            self.pr_tx = self.flags[fl]
            if self.log:
                print('Знаю: ', self.pr_fl, self.pr_tx)
            
        elif self.log:
            print('Незнаю: ', fl)
        return self.pr_tx

    def remove(self, flag):
        try:
            if self.log:
                print(f'Видаляю: {flag}')
            del self.flags[flag]
        except ValueError:
            print(f'Не знайдено: {flag}')
        
    def comfirm(self):
        self.flags[self.pr_fl] = self.pr_tx
        if self.log:
            print('Успіх: ', self.pr_fl, self.pr_tx)

    def total(self):
        print('\nТест завершено.\n всього було запитань: ', self.num)
        self.num = 0

    def parse_countries(self, msg):
        kb = msg.reply_markup.inline_keyboard
        result = ''
        for row in kb:
            for el in row:
                result += el.text + '\n'
    
        return result

FLAGS = Flags(log=False)
FLAGS.load()

app = Client()

quiz = filters.create(
    lambda _, __, m: bool(m.chat.id == 5810123083 and 'Залишилось часу' in m.text
    ))
    
success = filters.create(
    lambda _, __, m: bool(m.chat.id == 5810123083 and 'Вірно!' in m.text
    ))

unsuccess = filters.create(
    lambda _, __, m: bool(m.chat.id == 5810123083 and 'Помилка!' in m.text
    ))
    
end = filters.create(
    lambda _, __, m: bool(m.chat.id == 5810123083 and 'Quiz finished!' in m.text
    ))


@app.on_message(quiz)
async def profile_info_cmd(client: Client, msg: Message):
    FLAGS.num +=1
    print(f'{FLAGS.num} / 191 - ({100*FLAGS.num/191:.1f}%) ---------------')
    time.sleep(random.random()*3.14)
    flag = re.findall(r"""Прапор: (.*)""", str(msg.text))[0]
    fir = msg.reply_markup.inline_keyboard[0][0].callback_data
    FLAGS.pr_kb = f'{flag}\n' + FLAGS.parse_countries(msg)
    
    err = True
    while err:
        try:
            ans = FLAGS.get(flag, fir)

            await client.request_callback_answer(
            chat_id=msg.chat.id,
            message_id=msg.id,
            callback_data=ans 
            )
            err = False
        except DataInvalid:
            FLAGS.remove(flag)


@app.on_message(success)
async def profile_info_cmd(client: Client, msg: Message):
    FLAGS.comfirm()

@app.on_message(unsuccess)
async def profile_info_cmd(client: Client, msg: Message):
    print(FLAGS.pr_kb)
    FLAGS.remove(FLAGS.pr_fl)
    
@app.on_message(filters.command('save') & filters.me)
async def profile_info_cmd(client: Client, msg: Message):
    FLAGS.save()
    await msg.delete()

@app.on_message(end)
async def profile_info_cmd(client: Client, msg: Message):
    FLAGS.save()
    FLAGS.total()
    


if __name__ == "__main__":
    app1.start()
    app2.start()
    print('<<<RUN>>>')
    idle()
    app1.stop()
    app2.stop()
