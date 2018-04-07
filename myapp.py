from telethon import TelegramClient

from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from telethon.tl.types import ChannelParticipantsRecent
from telethon.tl.types import InputChannel
from telethon.tl.types import ChannelAdminLogEventsFilter
from telethon.tl.types import InputUserSelf
from telethon.tl.types import InputUser

from telethon import utils
from telethon.utils import get_input_peer

from io import StringIO
import csv
import _thread
import time
import os

from flask import make_response

from telethon.tl.functions.channels import InviteToChannelRequest

from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename

template_dir = '/root/nammuoi'
app = Flask(__name__, template_folder=template_dir)

resultlist = []
inputdict = {'apikey':'','accesshash':'','phonenumber':'','channelname':'','channeltoadd':''}
file_content = []
listtoexportcsv = []

api_id = 268912
api_hash = '61d882470fd08f66ea5ea10db7d9723b'

phone_number = '+84902231633'

client = TelegramClient(phone_number, api_id, api_hash)


@app.route('/')
def index():
   return render_template("index.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      try:
          apikey = request.form.get('apikey')
          inputdict['apikey'] = apikey
          accesshash = request.form.get('accesshash')
          inputdict['accesshash'] = accesshash
          phonenumber = request.form.get('phonenumber')
          inputdict['phonenumber']=phonenumber
          channelname = request.form.get('channelname')

          client = TelegramClient(phonenumber, apikey, accesshash)



      

          client.session.report_errors = False
          client.connect()
          
          if 'file' not in request.files:
            print("No file to upload")
            if not client.is_user_authorized():
         #client.send_code_request(phonenumber)
         #client.sign_in(phonenumber, input('Enter the code: '))
                 client.send_code_request(phonenumber)
                 print("sent code")
                 return render_template("codeinput.html")
            channel_entity = client.get_entity(channelname)
            members = client.get_participants(channel_entity)
            printmemberattr(members)
            print(members)
            for member in members:
              listtoexportcsv.append([member.id,member.username,member.phone])
            return render_template("result.html",members = members)
          else:
            print("upload file users and add to telegram channel")
            channeltoadd = request.form.get('channeltoadd')
            inputdict['channeltoadd'] = channeltoadd
            if channeltoadd == "":
              print("không nhập thông tin channel")
              return render_template("error.html")
            else:
              print("start to get file name")
              file = request.files['file']
              filename = secure_filename(file.filename) 
              print(filename)

              # os.path.join is used so that paths work in every operating system
              file.save(os.path.join("/root/nammuoi",filename))
              with open("/root/nammuoi/" + filename) as f:
                  for line in f:
                    file_content.append(line)

              if not client.is_user_authorized():
                client.send_code_request(phonenumber)
                print("sent code to phone")
                return render_template("adduserscodeinput.html")

        # You should use os.path.join here too.
              
              try:
                  _thread.start_new_thread( addUserFromFileToChannel, (file_content,client,channeltoadd) )
              except:
                  print ("Error: unable to start thread")
              return render_template("success.html")

      except Exception as e:
          print(e)
          return render_template("error.html")
@app.route('/codeinputresult',methods = ['POST', 'GET'])
def codeinputresult():
   if request.method == 'POST':
      try:
            
          client.sign_in(phone=inputdict['phonenumber'], code=code)
         
          channel_entity = client.get_entity(inputdict['channelname'])
          members = client.get_participants(channel_entity)

          for member in members:
            resultlist.append(dir(member))
          
          return render_template("result.html",members = members)
      except Exception as e:
          return render_template("error.html")



@app.route('/exportcsv')
def post(self):
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(listtoexportcsv)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

def getUserNames(client,channel):
    print('2:')
    channel_entity = client.get_entity(channel)
    #channel_to_invite = utils.get_input_peer(client.get_entity('crynet'))
    #r = client(GetFullChannelRequest(client.get_entity('namnguyenvn')))
    #print(r.users)
    #print(r)
    #print(r.full_chat)
    #print('channel to invite:' + str(channel_to_invite.channel_id))
    #print('\n')
    #input_channel = utils.get_input_peer(channel_entity)
    #print(input_channel)
    #print('\n')
    #print(input_channel.channel_id)
    members = client.get_participants(channel_entity)
    #client(InviteToChannelRequest(channel_entity,members))
    return members
@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('',path)

@app.route('/adduserscodeinputresult')
def adduserscodeinputresult():
   if request.method == 'POST':
      try:
          
          code = request.form.get('code')
            
          client.sign_in(phone=inputdict['phonenumber'], code=code)
         
          try:
            _thread.start_new_thread( addUserFromFileToChannel, (file_content,client,inputdict['channeltoadd']) )
          except Exception as e:
            raise e
          
          return render_template("success.html")
      except Exception as e:
          return render_template("error.html")

def addUserFromFileToChannel(input_file_content,client, channeltoinvite):
  channeltoinvite = client.get_entity(channeltoinvite)
  print("get channel to invite success")
  print(input_file_content)
  for x in input_file_content:
    print(x)
    client.get_entity(x)
    print("get username to invite success")
    client.invoke(InviteToChannelRequest(get_input_peer(channeltoinvite),[get_input_peer(client.get_entity(x))]))
    time.sleep(5)


def printmemberattr(members):
  result = []
  for member in members:
      result  = dir(member)
  print(result)

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = False  )
