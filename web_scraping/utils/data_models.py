import csv
import os


class Article(object):
    """This class represents an article object scheme"""
    def __init__(self,
                 title,
                 link,
                 content,
                 date_time,
                 author=None,
                 source=None,
                 summary=None,
                 sentiment=None
                 ):
        """
        Args:
            title (str): title of article
            link (str): link of article
            content (str): content of article
            date_time (str): date_time of article
            author (str): author of article
            source (str): source of article
            summary (str): summary of article
            sentiment (str): sentiment of article
        """
        self.title = title
        self.link = link
        self.content = content
        self.date_time = date_time
        self.author = author
        self.source = source
        self.summary = summary
        self.sentiment = sentiment

    @staticmethod
    def get_save_fields():
        """
        This method fetches the desired fields of an article to be saved
        Returns:
            list[str]: fields of article to save
        """
        # uncomment next line and comment line after for dynamic field retrieval
        # fields = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        fields = ['date_time', 'title', 'content', 'author', 'source', 'summary', 'sentiment', 'link']
        return fields

    @staticmethod
    def save_articles(articles, save_path='bbc_articles.csv', encoding='UTF8'):
        """
        This method saves a given list of articles to a csv file (if exists - adds to it)
        Args:
            articles (list[Article]): given articles to save
            save_path (str): path in which to save the unified flight data (including file_name.csv)
            encoding (str): encoding to use when saving
        """
        if not articles:
            return

        if os.path.exists(save_path):
            with open(save_path, "r", newline='', encoding=encoding) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
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
