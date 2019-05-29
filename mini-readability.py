from bs4 import BeautifulSoup
from conf import Config
import requests
import os
import sys


class Article:
	def __init__(self, url):
		if url.rsplit('://')[0] == url:
			self.url = 'http://' + url
		else:
			self.url = url
		self.protocol = ''
		self.domain = ''
		self.response = None
		self.protocol = self.url.rsplit('://')[0]
		self.domain = self.url.split('://')[-1].split('/')[0]

		try:
			self.response = requests.get(self.url)
		except Exception as e:
			print("Get page error: " + str(e))
			exit(1)

		self.title_tag = 'h1'
		self.article_tag = 'p'
		self.is_set = False
		self.title = []
		self.title_text = ''
		self.dom = None
		self.soup = None
		self.html = None
		self.encoding = None
		self.error_log = ''

	def set_config(self, config):
		self.title_tag = config['title_tag']
		self.article_tag = config['article_tag']
		self.is_set = config['is_set']

	def get_response(self):
		try:
			self.encoding = self.response.encoding
			self.html = self.response.content.decode(self.encoding)
		except:
			print('Decoding error: ' + str(Exception))

	def get_title(self):
		if self.html is None:
			self.get_response()
		soup = BeautifulSoup(''.join(self.html), 'lxml')

		if type(self.title_tag) is list:
			for tag in self.title_tag:
				if soup(tag) != []:
					self.title_tag = tag
					self.title = soup(self.title_tag)
					break
				else:
					pass

			if self.is_set is True and self.title == []:
				print('Title not found with tags configured for this site. Try default? (Y/n) ')
				choice = str(input())
				if choice == 'Y':
					conf = Config(self.url).get_config(enumeration=True)
					self.set_config(conf)
					self.get_title()


		else:
			if soup(self.title_tag) != []:
				self.title = soup(self.title_tag)

			else:
				print('Config file not found and default tags content is empty. Create conf.ini and try again.')
				exit(1)

		if self.title == []:
			print('Tags not found. Check configuration.')
			exit(1)

		self.title_text = self.title[0].text + '\r\n' * 2
		return self.title_text

	def find_dom(self):
		if self.title == []:
			self.get_title()
		self.dom = self.title[0]

		if type(self.article_tag) is list:
			for tag in self.article_tag:
				dom = self.dom
				try:
					while dom.findAll(tag) == []:
						dom = dom.parent
					self.dom = dom
					self.article_tag = tag
					break

				except AttributeError:
					pass

		else:
			try:
				while self.dom.findAll(self.article_tag) == []:
					self.dom = self.dom.parent

			except AttributeError:
				print('Dom not found with default tags.')
				exit(1)

	def get_text(self):
		if self.html is None:
			self.get_response()
		if self.dom is None:
			self.find_dom()
		text_tags = []
		try:
			text_tags = self.dom.findAll(self.article_tag)

		except AttributeError:
			print('Error: ' + str(AttributeError))
			exit(1)

		article_text = ''
		for article in text_tags:
			if len(article) < 5:
				pass

			if article.a is not None:
				link = str(article.a.get('href'))
				if link.find('http') == -1:
					link = self.protocol + '://' + self.domain + link
				address = (article.a.text + ' ' + '[' + link + ']')
				art = str(article).replace(str(article.a), str(address))
				paragraph = BeautifulSoup(art, 'lxml').text
			else:
				paragraph = article.text
			words = paragraph.split(' ')
			row = ''
			text = ''

			for word in words:
				if len(row + word + ' ') < 80:
					row = row + word + ' '
				else:
					text = text + row + '\r\n'
					row = word + ' '
			text = text.replace('&nbsp', ' ')
			if len(text) > 2:
				article_text = article_text + text + row + '\r\n' * 2

		return article_text[:-4]

	def get_path(self):
		save_tree = self.url.split('://')[-1].split('/')
		filename = 'article.txt'
		path = os.getcwd()

		for folder in save_tree:
			if folder == '':
				pass
			elif folder.find('htm') != -1:
				filename = folder.split('.')[0] + '.txt'
			elif self.title == []:
				break
			else:
				try:
					os.mkdir(path + '/' + folder)
				except FileExistsError:
					pass
				finally:
					path = path + '/' + folder

		path = path + '/' + filename
		return path

	def get_all(self):
		return self.get_title() + self.get_text()

	def write_to_file(self):
		self.get_title()
		text = self.get_text()
		path = self.get_path()
		file = open(path, 'w')
		file.write(self.title_text + text)
		file.close()
		print('Success!')


if __name__ == '__main__':
	url = ''

	try:
		url = sys.argv[1]

	except IndexError:
		print('Syntax: ' + sys.argv[0] + ' url')
		exit(1)

	finally:
		try:
			config = Config(url).get_config()
			article = Article(url)
			article.set_config(config)
			article.write_to_file()

		except KeyboardInterrupt:
			print('Bye!')
			exit(0)
