# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pymysql, os, json
from dateutil import parser

# do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val

# do validation and checks before insert
def validate_date(val):
   if val != None:
        res = True
        try:
            res = bool(parser.parse(val))
        except ValueError:
            res = False

def parse_file(json_data):
    json_obj = json.loads(json_data)

    # connect to MySQL
    con = pymysql.connect(host = 'localhost',user = 'root',passwd = 'punter89',db = 'spreadthejam')
    cursor = con.cursor()

    # parse json data to SQL insert
    for i, item in enumerate(json_obj):
        #band_id = 46
        article_body = validate_string(item.get("articleBody", None))
        article_body_html = validate_string(item.get("articleBodyHtml", None))

        canonical_url = validate_string(item.get("canonicalUrl", None))

        date_published = validate_string(item.get("datePublished", None))

        if not validate_date(date_published):
            date_published = None

        date_published_raw = validate_string(item.get("datePublishedRaw", None))
        if not validate_date(date_published_raw):
            date_published_raw = None

        description = validate_string(item.get("description", None))

        headline = validate_string(item.get("headline", None))
        if headline != None:
            if(len(headline) >= 1024):
                headline = headline[0:1023]

        in_language = validate_string(item.get("inLanguage", None))

        url = validate_string(item.get("url", None))

        main_image = validate_string(item.get("mainImage", None))
        if main_image != None:
            if(len(main_image) >= 1024):
                main_image = None
        cursor.execute("INSERT INTO article (article_body, article_body_html, canonical_url, date_published, date_published_raw, description, headline, in_language, url, main_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (article_body, article_body_html, canonical_url, date_published, date_published_raw, description, headline, in_language, url, main_image))
        con.commit()

    con.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    directory = os.path.abspath('.') + "/articles"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            json_data = open(f).read()
            parse_file(json_data)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
