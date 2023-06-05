import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
}


def getPtopid():
    userData = {
        "uid": "202022202014033",
        "upw": "Zss199619972003!"
    }
    loginUrl = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login"
    resp = requests.post(url=loginUrl, data=userData, headers=headers)
    resp.encoding = resp.apparent_encoding
    respText = resp.text
    if (respText.find("验证码") != -1):
        sendMsg("出现验证码，请稍后再试！")
        exit()
    indexStartPtopid = respText.find("ptopid")
    indexEndSid = respText.find("\"}}")
    respTextSub = respText[indexStartPtopid:indexEndSid]
    print(respTextSub)
    with open("ptopid.txt", "w") as f:
        f.write(respTextSub)
        f.close()

def sendMsg(codeSrc):
    data = {
        "token": "8906471ad908426db7f4e17d229bf46a",
        "title": "通行码",
        "content": codeSrc,
    }
    requests.post(url="http://www.pushplus.plus/send/", data=data)

if __name__ == '__main__':
    if(os.path.exists("ptopid.txt")):
        getPtopid()
    with open("ptopid.txt", "r") as f:
        respTextSub = f.read()
        if (respTextSub == ""):
            getPtopid()
        else:
            url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/" +\
                "gettongxing?"+respTextSub
            resp = requests.get(url, headers=headers)
            resp.encoding = resp.apparent_encoding
            if (resp.text.find("重新登录") != -1):
                getPtopid()
                with open("ptopid.txt", "r") as f:
                    respTextSub = f.read()
                    url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/" +\
                        "gettongxing?"+respTextSub
                    resp = requests.get(url, headers=headers)
                    resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, 'lxml')
            id = 0
            for child in soup.find(id="bak_0").children:
                if (id == 1):
                    backgroundUrl = child['style'].split("/")
                id = id+1
            print(backgroundUrl[2].split(")")[0])
            sendMsg(backgroundUrl[2].split(")")[0])
