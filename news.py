import requests
import bs4

news = []

newstitles = [{}]
newsdate = [{}]
newsimg = [{}]
def ParseCode(fnews):
    for i in range(len(fnews)-1):
        if (fnews[i] != "" and fnews[i] != ", "):
            newstitles.append(fnews[i])

    newstitles.pop(0)


def GetTitles(bs):
    bs2 = str(bs.findAll("h4", "article-title"))
    ParseCode(_clean_all_tag_from_str(bs2, 1))


def _clean_all_tag_from_str(string_line, flag):
    result = ""
    p = 0
    res = []
    not_skip = True
    for i in list(string_line):
        p += 1
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                if (i != "[" and i != {}):
                    if (i != string_line[len(string_line)-2] and i != string_line[len(string_line)-1]):
                        next = list(string_line)[p + 1]
                        if (i != "\n"):
                                if ((i + next) == ", "):
                                    res.append(result)
                                    result = ""
                                result += i
                        else:
                            res.append(result)
                            result = ""
        else:
            if i == ">":
                not_skip = True

    return res


def GetDates(bs):
    bs2 = str(bs.findAll("div", "article-date"))
    ParseCodeDate(clean2(bs2))

def clean2(string_line):
    result = ""
    p = 0
    res = []
    not_skip = True
    for i in list(string_line):
        p += 1
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                if (i != "[" and i != {}):
                    if (i != string_line[len(string_line)-2] and i != string_line[len(string_line)-1]):
                        next = list(string_line)[p + 1]
                        abc = i + next + list(string_line)[p + 2]

                        result += i
        else:
            if i == ">":
                not_skip = True
                res.append(result)
                result = ""

    res.append(result)
    return res

def ParseCodeDate(fnews):
    for i in range(len(fnews)-1):
        if (fnews[i] != "" and fnews[i] != ", "):
            newsdate.append(fnews[i])
    newsdate.pop(0)


def GetImgUri(bs):
    bs2 = str(bs.findAll("img", "img-responsive"))
    ParseCodeImg(cleanimg(bs2))

def cleanimg(string_line):
    result = ""
    p = 0
    res = []
    not_skip = True
    for i in list(string_line):
        p += 1
        if not_skip:
            if (i != string_line[len(string_line) - 2] and i != string_line[len(string_line) - 1]):
                abc = i + list(string_line)[p + 1] + list(string_line)[p + 2]
                if ((i + list(string_line)[p + 1] + list(string_line)[p + 2]) == 'r="'):
                    not_skip = False
        else:
            if (i != string_line[len(string_line) - 3] and i != string_line[len(string_line) - 2] and i != string_line[len(string_line) - 1]):
                abc = i + list(string_line)[p + 1] + list(string_line)[p + 2]
                result += i
                if abc == '">,': #g/>
                    not_skip = True
                    res.append(result)
                    result = ""
                if list(string_line)[p] == "/":
                    result += "/"

    res.append(result)
    return res


def ParseCodeImg(fnews):
    for i in range(len(fnews)-1):
        if (fnews[i] != "" and fnews[i] != ", "):
            b = fnews[i]
            b = b[0:-1]
            for i in range(4):
                b = b[1:]
            b = 'https://www.spbstu.ru/' + str(b)
            newsimg.append(b)
    newsimg.pop(0)


def GetNews(page):
    uri = "https://www.spbstu.ru/media/news" + "/?PAGEN_2=" + str(page)
    request = requests.get(uri)
    request.encoding = 'utf-8'
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    bs.decode('utf-8')
    GetTitles(bs)
    GetDates(bs)
    GetImgUri(bs)

    for i in range(len(newstitles)):
        a = {}
        a["title"] = newstitles[i]
        a["date"] = newsdate[i]
        a["img"] = newsimg[i]
        news.append(a)
    print(news)