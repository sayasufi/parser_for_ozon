<a href="https://wakatime.com/badge/user/018c3f04-b140-41f9-a489-5b0143d153f5/project/018d9262-850a-4e11-9201-35a8cf99e71e"><img src="https://wakatime.com/badge/user/018c3f04-b140-41f9-a489-5b0143d153f5/project/018d9262-850a-4e11-9201-35a8cf99e71e.svg" alt="wakatime"></a>

# Парсер для сайта ozon.ru

---

## Используемые фреймворки и библиотеки

<ul>
<li><strong>Python</strong></li>
<li><strong>Beautifulsoup4</strong></li>
<li><strong>Selenium</strong></li>
<li><strong>Pandas</strong></li>
<li><strong>Numpy</strong></li>
</ul>

---

## Запуск программы

1. Создайте `venv` виртуальное окружение:

```bash
pip install venv virtual_env_name
```

2. Активируйте `venv` виртуальное окружение:

```bash
source virtual_env_name/Scripts/activate
```

3. Загрузите файлы с репозитория

```bash
git remote add origin https://github.com/sayasufi/parser_for_ozon.git
git pull https://github.com/sayasufi/parser_for_ozon.git master
```

4. Установите все необходимые зависимости:

```bash
pip install -r requirements.txt
```

5. Запустите парсер:

```bash
python source/main.py --name Видеокарта --pages 5 --threshold 20

# Либо изменить файл utils/.env и запустить так
python source/main.py
```

---

## Файл .env
```bash
NAME=3070 # Поисковый запрос
NUMBER_OF_PAGES=1 # Кол-во страниц для парсинга
FILTER=20 # Пороговое значения отсеивания свойств товара в процентах
```

---