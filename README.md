# Mini readability
# Установка
	pip install -r requirements.txt

# Запуск
В директории скрипта:

	python3 mini-readability.py URL

# Описание
  Для решения этой задачи я использовал 2 класса. 

1.  Класс конфигурации, который находится в файле conf.py и который использует conf.ini в качестве файла конфигурации 
стандартно, но при инициализации класса можно передать другой файл. При создании экземпляра класса Conf можно передать URL и/
или путь до файла конфигурации, далее при обращении к методу get_config мы получим json настроек из conf.ini. Если задан URL, 
извлекаем домен, если он есть в файле конфигурации, возвращаем настройки для него, если нет, то возвращаем стандартные.


2.  Класс Article, который непосредственно взаимодействует со страницей.

__Методы класса Article:__

__Приватные:__

`get_path` - Усложнение 1, получение пути по URL

`find_dom` - Поиск по древу html тегов контента

`get_respones` - Получение ответа от веб-сервера и его декодирование

__Публичные:__

`set_config` - Принимает и устанавливает настройки (json)

`get_title` - Возвращает заголовок статьи

`get_text` - Возвращает форматированный текст статьи

`get_all` - Возвращает текст статьи с заголовком

`write_to_file` - По пути записывает текст и заголовок новости с заданным в усложнении 1 форматированием

__Конфигурация__ `conf.ini`

`[sitename]` - Имя сайта в формате домена, например: `[sbis.ru]`

`TITLE_TAG=h1` - теги заголовка, можно указать через запятую.

`ARTICLE_TAG=p` - теги текста, также можно указать через запятую.

# Алгоритм
1. При общащении к файлу скрипта исполняется main, который общащается к классу Config и получает конфигурацию

2. Задаётся конфигурация и запускается метод `write_to_file` из класса Article

3. Происходит проверка и форматирование url

4. Получаем и декодируем html

5. С помощью `BeautifulSoup` пытаемся найти заголовок статьи, заданный в файле конфигурации, либо, если он не задан, `<h1>`. Если заголовок задан в настройках для сайта, используем его, если не нашли, предлагаем попробовать со стандартными настройками. Настройки выполнены в виде списка, в цикле проходим по списку и проверяем, будет возвращён первый найденный тег, полученный из настроек. Если полученные настройки не список, то ищем по заданному в переменной `self.title_tag`, в случае неудачи - выход из программы и предложение поправить конфиги. Если тег найден, записываем в переменную `self.title_text` значение найденного тега, а в переменную `self.title` DOM.

6. Ищем dom, который содержит тег(и) заданные в переменной `self.article_tag`. Если получаем список тегов, возвращаем первое вхождение. Для этого пробуем получить список найденных тегов в цикле while, переходя к родителю, считая начальным положением dom тега заголовка, если получили в ответ `AttributeError` в процессе выполнения цикла, пропускаем текущий тег, переходим к следующему. Если получили не пустой список, записываем в переменную `self.dom` текущее положение в древе, в переменную `self.article_tag` текущий тег

7. Извлекаем текст. Для этого ищем все вхождения тега `self.article_tag` в `self.dom`, получаем список. В цикле проходим по каждому элементу списка, вытаскиваем из него текст, форматируем его согласно правилам, если в тексте встречается тег `a`, вытаскиваем из него ссылку, дописываем в переменную `article_text` текст параграфа. В конце возвращаем текст статьи

8. Получаем текущий путь из URL, если есть, что записать, создаём папки.

9. Записываем заголовок и текст статьи в файл, прощаемся.


# Страницы, на которых было проверено

См. - `test pages.txt`, результаты представлены в папке `test`.

# Дальнейшее улучшение 

Можно извлекать содержимое не одного тега, а сразу нескольких. Искать по аттрибутам, чтобы улучшить точность извлечения текста.
