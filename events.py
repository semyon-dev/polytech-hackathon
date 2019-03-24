import requests
import bs4

news = []

newstitles = [{}]
newsabout = []
newsdate = [{}]
newsimg = []
def ParseCode(fnews):
    for i in range(len(fnews)-1):
        if (fnews[i] != "" and fnews[i] != ", "):
            a = fnews[i].replace("'", "")
            a = a.replace("\'", "")
            a = a.replace(", ", "")
            a = a.replace(" ,", "")
            a = a.replace("\'", "")
            a = a.strip('\" ')

            newstitles.append(a)

    newstitles.pop(0)

def GetTitles(bs):
    bs2 = str(bs.findAll("a", "event-header"))
    ParseCode(clean(bs2))


def clean(string_line):
    result = ""
    p = 0
    res = []
    not_skip = True
    for i in list(string_line):
        p += 1
        if not_skip:
            if i == "<":
                not_skip = False
                if (i + list(string_line)[p + 1]) != '< ':
                    next = i + list(string_line)[p + 1]
                    res.append(result)
                    result = ""
            else:
                if (i != "[" and i != {}):
                    if (i != string_line[len(string_line)-2] and i != string_line[len(string_line)-1]):
                        next = list(string_line)[p + 1]
                        result += i
        else:
            if i == ">":
                not_skip = True

    return res


def GetAbout(bs):
    bs2 = str(bs.findAll("span", "event-snap"))
    ParseCodeAbout(cleanabout(bs2))


def cleanabout(string_line):
    result = ""
    p = 0
    res = []
    not_skip = True
    for i in list(string_line):
        p += 1
        if not_skip:
            if i == "<":
                res.append(result)
                result = ""
                not_skip = False
            else:
                if (i != "[" and i != {}):
                    if (i != string_line[len(string_line)-2] and i != string_line[len(string_line)-1]):
                        if (i != "\n"):
                                if ((i + str(next)) == ".<"):
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

def ParseCodeAbout(fnews):
    for i in range(len(fnews)-1):
        if (fnews[i] != "" and fnews[i] != ", "):
            a = fnews[i].replace(",", "")
            a = a.replace("'", "")
            print(a)
            newsabout.append(a)


def GetDates(bs):
    bs2 = str(bs.findAll("span", "e-edge-start"))
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
            fnews[i] = fnews[i].replace("\t", "")
            fnews[i] = fnews[i].replace("\n", "")
            newsdate.append(fnews[i])

    newsdate.pop(0)


def GetImgUri(bs):
    bs2 = bs.findAll("a", "event-fig")
    b = []
    for i in range(len(bs2)):
        temp = bs2[i]
        b.append(temp.findAll("img")[0])
    ParseCodeImg(cleanimg(b))

def cleanimg(line):
    result = ""
    p = 0
    res = []
    not_skip = True
    for i in list(line):
        p += 1
        res.append(i.attrs['src'])

    res.append(result)
    return res


def ParseCodeImg(fnews):
    for i in range(len(fnews)-1):
            newsimg.append("https://www.spbstu.ru" + fnews[i])


def GetAnnouncements():
    uri = "https://www.spbstu.ru/media/announcements"
    request = requests.get(uri)
    request.encoding = 'utf-8'
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    bs.decode('utf-8')
    GetTitles(bs)
    GetAbout(bs)
    GetDates(bs)
    GetImgUri(bs)

    for i in range(len(newstitles)):
        a = {}
        a["title"] = newstitles[i]
        a["about"] = newsabout[i]
        a["date"] = newsdate[i]
        a["picture"] = newsimg[i]
        news.append(a)

    return news