from transformers import pipeline


class SentimentAnalysis(object):

    MAX_INPUT_LENGTH = 512
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    @classmethod
    def analyse_sentiment(cls, article, model=None):
        if model is None:
            classifier = cls.get_model()
        else:
            classifier = model
        return classifier(article, truncation=True)[0]

    @classmethod
    def get_model(cls, model_name=None):
        if model_name is None:
            model_name = cls.model_name
        return pipeline("sentiment-analysis", 
            model=model_name, 
            tokenizer=model_name, 
            max_length=cls.MAX_INPUT_LENGTH
        )


class ArticleSummarization(object):

    MAX_INPUT_LENGTH = 1024

    @classmethod
    def summarize(cls, article, model=None, max_length=100, min_length=50):
        if model is None:
            summarizer = cls.get_model()
        else:
            summarizer = model
        if max_length > cls.MAX_INPUT_LENGTH:
            max_length = cls.MAX_INPUT_LENGTH
        res = summarizer(article, 
            max_length=max_length, 
            min_length=min_length, 
            truncation=True,
        )
        return res[0]

    @classmethod
    def get_model(cls):
        return pipeline("summarization", model="facebook/bart-large-cnn")


if __name__ == '__main__':
    article = """In a moment of symbolic unity, Prince William and Prince Harry walked side by side behind the Queen's coffin as it left Buckingham Palace.
    Along with King Charles and other members of the Royal Family, they processed to Westminster Hall where the Queen will lie in state.
    The sight of the brothers together, walking behind the coffin, will evoke poignant memories of their mother Diana's funeral 25 years ago.
    Crowds applauded the solemn procession.
    The Queen's coffin, carried on a gun carriage, passed below the Buckingham Palace balcony where only three months ago she appeared for the final moments of the Platinum Jubilee celebrations.
    Bandsmen played sombre music to accompany this careful choreography of mourning, Beethoven and Mendelssohn alongside the drumbeat of marching feet - exactly 75 steps per minute - and the sound of horses' hooves in the autumn sunshine.
    The same gun carriage had carried the coffins of the Queen's father and mother - and as it went past there were ripples of applause and some tears from people crowding along the route.
    Walking on foot behind the coffin were the Queen's four children, King Charles, Princess Anne and Prince Edward, in military uniform, with Prince Andrew, no longer a working royal, in a morning suit and wearing medals.
    And behind them were William, now the Prince of Wales, and Prince Harry, the Duke of Sussex, also as a non-working royal not wearing military uniform.
    This time the brothers were side by side, unlike Prince Philip's funeral last year when they had someone walking between them, in what was seen at the time as a sign of separation.
    The brothers appearing together sends a strong visual message of family unity, after so much speculation about tensions and disagreements between them.
    Their wives, Catherine and Meghan, Duchess of Sussex and Camilla, the Queen Consort, travelled in cars behind.
    William, Harry, Catherine and Meghan had appeared together at the weekend to greet well-wishers in Windsor, tuning into a public mood wanting reconciliation, and bringing back memories of the "fab four" of young royals.
    A thundercloud of media interest has hung over claims of a strained brotherly relationship, now conducted from different sides of the Atlantic.
    But it's not clear what the feelings might really be for a family whose private grief comes with so much public scrutiny.
    Catherine is now the new Princess of Wales and the images of the coffin procession will bring back thoughts of another September funeral, when Diana in 1997 was buried from Westminster Abbey.
    William and Harry, as young schoolboys, walked in that funeral procession, with their father King Charles and grandfather Prince Philip. In step at a time when their worlds had been turned upside down.
    Today's procession was another national moment. Crowds held up mobile phones to capture a glimpse of history taking place before them. Big Ben rang out around the streets, tolling each minute. Queen Elizabeth had left Buckingham Palace for the very final time.
    Her connections with the palace went back across the eras. She'd been Christened there 96 years ago and there were guests in that family photo who had been alive at the same time as the Duke of Wellington, victor of Waterloo.
    The coffin has been covered with the emblems of the monarchy, the Royal Standard and the Imperial State Crown. But there are also personal connections in the flowers in the wreath. Along with white roses and white dahlias there was pine from Balmoral and lavender and rosemary, a symbol of remembrance, from the gardens at Windsor.
    Marie Jackson, BBC News, at the Mall
    Among those on the Mall was Nicola Dainton, a 56-year-old grandmother from Chorley Wood, Hertfordshire, who was joined by her daughter Emily, and her grandchildren, Freddie, two, and baby Millie, for what she described as a "very emotional" moment.
    She said Princes William and Harry appeared "deep in their thoughts of the Queen" but said the moment felt very different to their mother's funeral.
    "They were two young boys then. This felt more they were there to support the family," she added.
    Dawn Livingstone, who was with six of her family all from County Tyrone, said the moment had been sad, sombre and fitting."She has left a legacy that will never be paralleled by anyone else," she said.Matthew Ferguson, her son-in-law, said: "It's the closest I have ever been to the Queen. It's been a privilege and an overwhelming experience."The family, who left home at 02:00, are now heading to Westminster Hall to take in more of the atmosphere before a 22:00 flight home.
    Royal aides have described this procession as a significant symbolic turning point in the funeral journey. The Queen was head of her family, but she was also head of state - and here her family were putting her back into the public realm.
    The procession was taking her to the heart of political life, through Whitehall, past Downing Street and to the Houses of Parliament.
    At Westminster Hall, the oldest part of the Palace of Westminster, there was a short service of prayers and readings conducted by the Archbishop of Canterbury, Justin Welby.
    Soldiers from the Grenadier Guards had lifted the coffin into place on a "catafalque", a raised platform inside the medieval hall.
    With the Royal Family standing in the historic hall, a psalm was sung - "O Lord, thou hast searched me out and known me" - and a reading which began "Let not your heart be troubled".
    Prince Harry and Meghan appeared to be holding hands as they left.
    From 17:00 BST on Wednesday, the Queen's lying-in-state will begin, when the public will have their chance to pay respect, until the morning of the funeral on Monday.
    The queues have already started and everyone, like the Queen's family in the procession, will have arrived with, and will leave with, their own memories.
    What next? A day-by-day guide from now to the funeral
    How titles and the line of succession have changed
    What's a state funeral? Will shops close? And other questions"""
    print(SentimentAnalysis.analyse_sentiment(article))
    print('\n----\n')
    print(ArticleSummarization.summarize(article))
