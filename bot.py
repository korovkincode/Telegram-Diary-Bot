import telebot, datetime, json

#Инициализируем нашего бота с помощью токена

bot = telebot.TeleBot('1164454988:AAFp16EGtxYPl8yF3fOtH1ZkHl1Bm9PrVC4')

#Обработчик команды start

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет, напиши /help, чтобы увидеть список команд')

#Обработчик команды help

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Список моих комманд:\n/create [текст] - Создать новую запись\n/show [дата вида дд.мм.гггг]- Посмотреть записи')

#Обработчик команды create

@bot.message_handler(commands=['create'])
def create_command(message):
	t = message.text
	#При некорректном вводе выводим ошибку
	if t.split() == ['/create']:
		bot.send_message(message.chat.id, 'Некорректный ввод.Напиши /help,чтобы посмотреть как работают команды')
	else:
		#Вычисляем дату и преобразовываем к виду дд.мм.гггг
		note = message.text[8:]
		now = datetime.datetime.now()
		day = str(now.day)
		if len(day) == 1:
			day = '0' + day
		month = str(now.month)
		if len(month) == 1:
			month = '0' + month
		year = str(now.year)
		date = day + '.' + month + '.' + year
		minute = str(now.minute)
		hour = str(now.hour)
		sec = str(now.second)
		if len(minute) == 1:
			minute = '0' + minute
		if len(hour) == 1:
			hour = '0' + hour
		if len(sec) == 1:
			sec = '0' + sec
		time = hour + ':' + minute + ':' + sec
		bot.send_message(message.chat.id, 'Сохраняю запись.Дата: ' + date)
		date = date + '-' + time
		with open('notes.json', 'r') as fin:
			n = json.loads(fin.read())
			print(n)
		if str(message.from_user.id) not in n.keys():
			n[str(message.from_user.id)] = {date : note}
		else:
			x = n[str(message.from_user.id)]
			x[date] = note
			n[str(message.from_user.id)] = x
		print(n)
		with open('notes.json', 'w') as f:
			n_js = json.dumps(n, indent = 2)
			print(n_js, file = f)
		print(n, type(message.from_user.id))
#Обработчик команды show

@bot.message_handler(commands=['show'])
def show_command(message):
	t = message.text
	#При некорректном вводе возвращаем ошибку
	if t.split() == ['/show'] or len(t.split()[1]) < 10:
		bot.send_message(message.chat.id, 'Некорректный ввод.Напиши /help,чтобы посмотреть как работают команды')
	else:
		#Поиск по БД и вывод записей за дату
		with open('notes.json', 'r') as f:
			data = json.loads(f.read())
		#Преобразовываем дату к формату дд.мм.гггг
		date = str(t.split()[1])
		date = date.replace(date[2], '.')
		date = date.replace(date[5], '.')
		day = date[:2]
		month = date[3:5]
		year = date[6:]
		l = data.keys()
		print(l)
		f = True
		notes = {}
		bot.send_message(message.chat.id, 'Записи за ' + date + ':')
		for i in l:
			if i == str(message.from_user.id):
				f = False
				notes = data[str(message.from_user.id)]
		if f:
			bot.send_message(message.chat.id, 'У вас ещё нет записей!')
		else:
			f = True
			l = notes.keys()
			for i in l:
				d1 = i[:2]
				m1 = i[3:5]
				y1 = i[6:10]
				h1 = i[11:13]
				mi1 = i[14:16]
				if d1 == day and m1 == month and y1 == year:
					bot.send_message(message.chat.id, 'Сохранено в ' + h1 + ':' + mi1 + '\n' + notes[i])
					f = False
			if f:
				bot.send_message(message.chat.id, 'У вас нету записей за эту дату!')

#Обработчик текста

@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, 'Даже незнаю,что ответить')
    

bot.polling(none_stop=True, timeout=123)
