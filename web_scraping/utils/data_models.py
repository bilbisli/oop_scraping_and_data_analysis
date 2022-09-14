
import os
import csv


class Article(object):
    def __init__(self, title, link, content, date_time, author=None, source=None):
        self.title = title
        self.link = link
        self.content = content
        self.date_time = date_time
        self.author = author
        self.source = source
    
    def get_save_fields(self):
        # uncomment next line and comment line after for dynamic field retrieval
        # fields = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        fields = ['date_time', 'title', 'content', 'author', 'source' , 'link']
        return fields


    @staticmethod
    def save_articles(articles, save_path='bbc_articles.csv', encoding='UTF8'):
        if not articles:
            print('No articles to save.')
            return

        if os.path.exists(save_path):
            with open(save_path, "r", newline='', encoding=encoding) as csv_file:
                csv_reader = csv.reader(csv_file)
                fields = next(csv_reader)
            with open(save_path, "a", newline='', encoding=encoding) as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                for article in articles:
                    line = [getattr(article, field) for field in fields]
                    writer.writerow(line)
        else:
            fields = articles[0].get_save_fields()
            with open(save_path, "w", newline='', encoding=encoding) as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(fields)
                for article in articles:
                    line = [getattr(article, field) for field in fields]
                    writer.writerow(line)
