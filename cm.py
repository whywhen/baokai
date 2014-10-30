#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import imaplib, string, email
reload(sys)
#importre
sys.setdefaultencoding("utf8")

def savefile( filename, data, path ):
   print filename 
   try:
       filepath = path + filename
       
       print filepath
       f = open( filepath, 'wb' )
   except:
       #sys.stdout.write( chr(filepath).encode('utf8') )
       print( 'filename error' )
       f.close()
   f.write( data )
   f.close()

#字符编码转换方法
def my_unicode(s, encoding):
   if encoding:
       return unicode(s, encoding)
   else:
       return unicode(s)

#获得字符编码方法
def get_charset(message, default="utf8"):
   #Get the message charset
   return message.get_charset()
   return default

#解析邮件方法（区分出正文与附件）
def parseEmail(msg, mypath):
   mailContent = None
   contenttype = None
   suffix =None
   for part in msg.walk():
       if not part.is_multipart():
           contenttype = part.get_content_type()   
#           print "NOW!"
           filename = part.get_filename()
#           sys.stdout.write( len(filename) )
#
#should write something here, because when this python script is called by shell script , the returned varible "filename" might be NULL
#
#           sys.stdout.write( chr( filename ).encode( 'utf8' ) )
           charset = get_charset(part)
           #是否有附件
           if filename:
               h = email.Header.Header(filename)
               dh = email.Header.decode_header(h)
               fname = dh[0][0]
               encodeStr = dh[0][1]
               if encodeStr != None:
                   if charset == None:
                       fname = fname.decode(encodeStr, 'gbk')
                   else:
                       fname = fname.decode(encodeStr, charset)
               data = part.get_payload(decode=True)
               #print('Attachment : ' + fname)
               #保存附件
#               re_xls = re.compile('.*xls')
               if "xls" in fname :
                  is_xls = True 
               else:
                  is_xls = False
               if ( fname != None or fname != '' ) and ( is_xls == True ) :
                   savefile(fname, data, mypath)            
           else:
               if contenttype in ['text/plain']:
                   suffix = '.txt'
               if contenttype in ['text/html']:
                   suffix = '.htm'
               if charset == None:
                   mailContent = part.get_payload(decode=True)
               else:
                   mailContent = part.get_payload(decode=True).decode(charset)         
   return  (mailContent, suffix)

#获取邮件方法
def getMail(mailhost, account, password, diskroot, port = 993, ssl = 1):
   mypath = diskroot + '/'
   #是否采用ssl
   if ssl == 1:
       imapServer = imaplib.IMAP4_SSL(mailhost, port)
   else:
       imapServer = imaplib.IMAP4(mailhost, port)
   imapServer.login(account, password)
   imapServer.select()
   #邮件状态设置，新邮件为Unseen
   #Message statues = 'All,Unseen,Seen,Recent,Answered, Flagged'
   resp, items = imapServer.search(None, "ALL")
   number = 1
   for i in items[0].split():
      #get information of email
      resp, mailData = imapServer.fetch(i, "(RFC822)")   
      mailText = mailData[0][1]
      msg = email.message_from_string(mailText)
      mailContent, suffix = parseEmail(msg, mypath)
          
   imapServer.close()
   imapServer.logout()


if __name__ =="__main__" :
   #邮件保存在e盘
   mypath ='./importing'
   #print 'begin to get email...'
   muser = ''
   mpass = ''
   getMail('outlook.office365.com', muser, mpass, mypath, 993, 1)
   #print 'the end of get email.'

