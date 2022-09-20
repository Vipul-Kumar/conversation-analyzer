import speech_recognition as sr
from datetime import datetime
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import logging

logging.basicConfig(level=logging.CRITICAL)


def takeCommandHindi():
    r = sr.Recognizer()
    with sr.Microphone() as source:

        # seconds of non-speaking audio before
        # a phrase is considered complete
        print('Listening', end=" ")
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            logging.info("Recognizing")
            Query = r.recognize_google(audio, language='hi-In')

            # for listening the command in indian english
            print(f"{Query}", end=" ")

        # handling the exception, so that assistant can
        # ask for telling again the command
        except Exception as e:
            # logging.info(e)
            # logging.info("Say that again sir")
            return None
        return Query


if __name__ == "__main__":
    conversation_name = input("Please enter the case reference number : ")
    datetime_now = datetime.now()
    os.makedirs("logs", exist_ok=True)
    conversation_log = os.path.join("logs", f"{conversation_name}_{datetime_now}.log")
    logging.basicConfig(filename=conversation_log, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    analyzer = SentimentIntensityAnalyzer()
    result = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    positive = 0
    negative = 0
    neutral = 0
    neu_iteration_count = 0
    pos_iteration_count = 0
    neg_iteration_count = 0
    while True:
        query = takeCommandHindi()
        if query is not None:

            translator = Translator()
            text_to_translate = translator.translate(query, src="hi", dest="en")
            text = text_to_translate.text
            logging.info(f"English : {text}")
            vs = analyzer.polarity_scores(text)
            logging.info("{:-<30} {}".format(text, str(vs)))
            if vs["pos"] != 0.0 or vs["neg"] != 0.0 or vs["neu"] != 0.0:
                if vs["pos"] != 0.0:
                    pos_iteration_count = pos_iteration_count + 1
                    positive = round((positive + (vs["pos"])) / pos_iteration_count, 2)
                if vs["neg"] != 0.0:
                    neg_iteration_count = neg_iteration_count + 1
                    negative = round((negative + (vs["neg"])) / neg_iteration_count, 2)
                if vs["neu"] != 0.0:
                    neu_iteration_count = neu_iteration_count + 1
                    neutral = round((neutral + (vs["neu"])) / neu_iteration_count, 2)

                print(
                    f"\rPositive : {round(positive * 100, 2)} || Negative : {round(negative * 100, 2)} || Neutral : {round(neutral * 100, 2)}",
                    end=" ")
        else:
            continue
