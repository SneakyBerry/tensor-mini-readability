import configparser


class Config:
	def __init__(self, url='DEFAULT', filename='conf.ini'):
		if url.rsplit('://')[0] == url:
			self.url = 'http://' + url
		elif url == 'DEFAULT':
			self.url = 'DEFAULT'
		else:
			self.url = url
		self.site = self.url.split('://')[-1].split('/')[0]
		self.config = configparser.ConfigParser()
		# Default static settings
		self.title_tag = 'h1'
		self.article_tag = 'p'
		self.is_set = False

		self.config.read(filename)
		if self.config.sections() == []:
			self.config_error = True
			print('Config file not found or empty, using default tags.')
		else:
			self.config_error = False

	def get_config(self, preset='DEFAULT',enumeration=False):
		if self.config_error is True:
			title_tag = self.title_tag
			article_tag = self.article_tag

		else:
			if self.site in self.config and enumeration is False:
				self.is_set = True
				preset = self.site

			try:
				conf = self.config[preset]
				title_tag = conf['TITLE_TAG']
				article_tag = conf['ARTICLE_TAG']

			except KeyError:
				conf = self.config[preset]
				title_tag = conf['TITLE_TAG']
				article_tag = conf['ARTICLE_TAG']

		conf_data = {
			'title_tag': title_tag.replace(' ', '').split(','),
			'article_tag': article_tag.replace(' ', '').split(','),
			'is_set': self.is_set}

		return conf_data

	# def write_config(self, url, title_tag, article_tag):


if __name__ == '__main__':
	pass
