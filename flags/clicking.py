from pyrogram import Client, filters, idle
from pyrogram.types import Message
import pretify_flags
import time
import random 
import re
import os

path = os.path.realpath(__file__)
path = os.path.dirname(path)
os.chdir(path)

class Flags:
    def __init__(self):
        self.num = 0
        self.time = 600
        self.load()
     
    def load(self):
        fls = pretify_flags.load()
        self.flags = fls
            
    def get(self, text):
        print(f'{self.num} / 191 - ({100*self.num/191:.1f}%) ---------------')
        self.num +=1

        flag = re.findall(r"""Прапор: (.*)""", str(text))[0]
        return self.flags[flag]

    def total(self):
        print('\nТест завершено.\n всього було запитань: ', self.num)
        self.num = 0

FLAGS = Flags()

app = Client()

quiz = filters.create(
    lambda _, __, m: bool(
        m.chat.id == 5810123083 
        and 'Залишилось часу' in m.text
    ))  
end = filters.create(lambda _, __, m: bool(
        m.chat.id == 5810123083 
        and ('Quiz finished!' in m.text or 'Час закінчився! Ви набрали' in m.text)
    ))


@app.on_message(quiz)
async def answer_to_quiz(client: Client, msg: Message):
    time.sleep(random.random() + 1.14)
    ans = FLAGS.get(msg.text)

    try:
        await client.request_callback_answer(
        chat_id=msg.chat.id,
        message_id=msg.id,
        callback_data=ans 
        )
    except TimeoutError:
        pass

@app.on_message(end)
async def show_total(client: Client, msg: Message):
    FLAGS.total()
    


if __name__ == "__main__":
    app1.start()
    app2.start()
    print('<<<RUN>>>')
    idle()
    app1.stop()
    app2.stop()
