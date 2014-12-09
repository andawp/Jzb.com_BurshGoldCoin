__author__ = 'andawp'
# -*- coding: utf-8 -*-
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib, cookielib, re, time, json, random
class Robot:
    def __init__(self, forumUrl, userName, password, proxy = None):
        ''' 初始化论坛url、用户名、密码和代理服务器 '''
        self.forumUrl = forumUrl
        self.userName = userName
        self.password = password
        self.formhash = ''
        self.isLogon = False
        self.isSign = False
        self.xq = ''
        self.jar = cookielib.CookieJar()
        if not proxy:
            openner = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(self.jar))
        else:
            openner = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(self.jar),
        urllib2.ProxyHandler({'http' : proxy}))
        urllib2.install_opener(openner)

    def login(self):
            ''' 登录论坛 '''
            url = "http://reg.jzb.com" + "/login/loginpost?uname=andawp&passwd=123456&logintype=0&islogin=0&callback=&_=1418023569425"
            postData = urllib.urlencode({'username': self.userName,
            'password': self.password, 'answer': '',
            'cookietime': '2592000', 'handlekey': 'ls',
            'questionid': '0', 'quickforward': 'yes',
            'fastloginfield': 'username'})
            req = urllib2.Request(url,postData)
            content = urllib2.urlopen(req).read()
            jsonstr = json.loads(content[2:len(content)-3])
            if jsonstr['status'] == 1:
                self.isLogon = True
                print 'logon success!'
                self.initFormhashXq()
            else:
                print 'logon faild!'

    def initFormhashXq(self):
        ''' 获取formhash和心情 '''
        content = urllib2.urlopen('http://jzb.com' + '/bbs/plugin.php?id=dsu_paulsign:sign').read().decode('utf-8')
        rows = re.findall(r'formhash=([^&]+)', content)
        if len(rows)!=0:
            self.formhash = rows[1]
            print 'formhash is: ' + self.formhash
        else:
            print 'none formhash!'
        #rows = re.findall(r'<input id=.* type=\"radio\" name=\"qdxq\"value=\"(.*?)\" style=\"display:none\">', content)
        #if len(rows)!=0:
        #    self.xq = rows[0]
        #    print 'xq is: ' + self.xq
        #elif u'已经签到' in content:
        #    self.isSign = True
        #    print 'signed before!'
        #else:
        #    print 'none xq!'

    def reply(self, tid, subject = u'',msg = u'支持~~~顶一下下~~嘻嘻'):
        ''' 回帖 '''
        url = 'http://jzb.com' + '/bbs/forum.php?mod=post&action=reply&fid=2979&tid={}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'.format(tid)
        postData = urllib.urlencode({'formhash': self.formhash,
        'message': msg.encode('utf-8'),
        'subject': subject.encode('utf-8'),
        'posttime':int(time.time()) })
        headers = {'Referer': 'http://jzb.com/bbs/thread-' + str(tid) +  '-1-2.html',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.28 Safari/537.36'}
        req = urllib2.Request(url, postData, headers=headers)
        content = urllib2.urlopen(req).read().decode('utf-8')
        #print content
        if u'发布成功' in content:
            print 'reply success!'
        else:
            print 'reply faild!'

    def publish(self, fid, typeid, subject = u'发个帖子测试一下下，嘻嘻~~~',msg = u'发个帖子测试一下下，嘻嘻~~~'):
        ''' 发帖 '''
        url = self.forumUrl + '/forum.php?mod=post&action=newthread&fid={}&extra=&topicsubmit=yes'.format(fid)
        postData = urllib.urlencode({'formhash': self.formhash,
        'message': msg.encode('gbk'), 'subject': subject.encode('utf-8'),
        'posttime':int(time.time()), 'addfeed':'1',
        'allownoticeauthor':'1', 'checkbox':'0', 'newalbum':'',
        'readperm':'', 'rewardfloor':'', 'rushreplyfrom':'',
        'rushreplyto':'', 'save':'', 'stopfloor':'',
        'typeid':typeid, 'uploadalbum':'', 'usesig':'1',
        'wysiwyg':'0' })
        req = urllib2.Request(url,postData)
        content = urllib2.urlopen(req).read().decode('utf-8')
        #print content
        if subject in content:
            print 'publish success!'
        else:
            print 'publish faild!'

    def sign(self,msg = u'哈哈，我来签到了！'):
        ''' 签到 '''
        if self.isSign:
            return
        if self.isLogon and self.xq:
            url = self.forumUrl + '/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
            postData = urllib.urlencode({'fastreply': '1',
        'formhash': self.formhash, 'qdmode': '1',
        'qdxq': self.xq, 'todaysay':msg.encode('utf-8') })
            req = urllib2.Request(url,postData)
            content = urllib2.urlopen(req).read().decode('utf-8')
            #print content
            if u'签到成功' in content:
                self.isSign = True
                print 'sign success!'
                return
        print 'sign faild!'

    def speak(self,msg = u'hah,哈哈，测试一下！'):
        ''' 发表心情 '''
        url = self.forumUrl + '/home.php?mod=spacecp&ac=doing&handlekey=doing&inajax=1'
        postData = urllib.urlencode({'addsubmit': '1',
        'formhash': self.formhash, 'referer': 'home.php',
        'spacenote': 'true', 'message':msg.encode('utf-8') })
        req = urllib2.Request(url,postData)
        content = urllib2.urlopen(req).read().decode('utf-8')
        #print content
        if u'操作成功' in content:
            print 'speak success!'
        else:
            print 'speak faild!'

if __name__ == '__main__':
    replayContent = [u'谢谢分享，辛苦了...', u'逢贴必顶，占坑为王.',u'很好的东西，谢谢分享', u'谢谢整理!!!!!!!!!!!', u'一定要切合实际!!!!!', u'写得好  赞一个!!!!!', u'不看还不知道呢，还好今天看到，要不都不知道。', u'都不容易，努力尽力就好。', u'很好的心得，谢谢！', u'按时浇水，静等花开']
    robot = Robot('http://reg.jzb.com', 'andawp', '123456')
    robot.login()
    for i in range(3000000, 3154650):#填入开始和结束的帖子的tid号，一般查看页面的url就能找到
        time.sleep(random.randrange(5, 10)) #随机休眠10~30秒
        robot.reply(str(i), msg=replayContent[random.randrange(1, 10)]) #随机选取replayContent中的回复语句进行回复
    #robot.sign()
    #robot.speak()
    #robot.publish(92,51, u'头 痛 ', u""" 一位女士对医生说她头痛，医生建议她出嫁。过了一年，医生偶然遇见了这位女士：“喂，怎么？你出嫁了吗？”“谢谢，出嫁了。”“头还痛吗？”“不痛了，可我丈夫的头开始痛了。”""")
    #robot.reply(107137)
