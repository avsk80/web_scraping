from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.error import URLError
from urllib.error import HTTPError

from flask import render_template, request, Flask, jsonify
from flask_cors import cross_origin, CORS

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    global html_page, review_page
    if request.method == 'POST':
        try:
            string = request.form['content'].replace(" ","")
            url = "https://www.flipkart.com/search?q=" + string
            print(url)

            try:
                html_page = urlopen(url)
            except HTTPError as e:
                print("getting HTTP error")
            except URLError  as e:
                print("error in generating url")

            flipkart_html = BeautifulSoup(html_page, 'html.parser')
            # print(flipkart_html)
            # print(flipkart_html.findAll("div",attrs={"class":"bhgxx2 col-12-12"}))
            box = flipkart_html.findAll("div", attrs={"class": "bhgxx2 col-12-12"})
            # print(len(box))
            # print(box)
            # print(box[0])
            item_link = box[0].a['href']
            print("link =", box[0].a['href'])
            item_review_link = "https://www.flipkart.com" + item_link
            print(item_review_link)
            try:
                review_page = urlopen(item_review_link)
            except HTTPError as e:
                print("getting HTTP error")
            except URLError  as e:
                print("error in generating url")

            review_html = BeautifulSoup(review_page, 'html.parser')
            # print(review_html)
            # print(review_html.findAll("div",attrs={"class":"_3nrCtb"}))
            review_box = review_html.findAll("div", attrs={"class": "_3nrCtb"})
            # print(len(review_box))
            fileName = string + ".csv"
            fw = open(fileName, "w")
            headers = "Product, Name, Rating, Header, Comment \n"
            fw.write(headers)
            #print(review_box)
            reviews = []
            for i in review_box:
                try:
                    commentHead = i.div.div.div.p.text
                    # print(commentHead)
                    # print(i.findAll("p", {"class": "_2xg6Ul"})[0].text)
                except Exception:
                    commentHead = 'no head'
                    # print(i.p.text)
                    # print(len(i.findAll("p", {"class": "_2xg6Ul"})))
                #
                try:
                    rating = i.div.div.div.div.text
                    # print(rating)
                    # print(i.div.div.div.div.text)
                except Exception:
                    rating = 'no rating'

                try:
                    comments = i.div.div.findAll("div", {"class": ""})[1].text
                # print(comments)
                # print(i.div.div.findAll("div", {"class":""})[0].div.text)
                # print(i.div.div.findAll("div", {"class":""})[1].text)
                # print(i.div.div.findAll("div", {"class":""}))
                except Exception:
                    comments = 'no comments'

                try:
                    name = i.div.div.findAll("p", {"class": "_3LYOAd _3sxSiS"})[0].text
                # print(name)
                # print(i)
                # print(i.div.div.findAll("p",{"class":"_3LYOAd _3sxSiS"})[0].text)
                except Exception:
                    name = 'no name'

                dict_reviews = {"Product": string, "Name": name, "Rating": rating, "Header": commentHead,
                                "Comments": comments}
                reviews.append(dict_reviews)
            #print(reviews)
            #print(reviews[0:(len(reviews) - 1)])
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
            #return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)
