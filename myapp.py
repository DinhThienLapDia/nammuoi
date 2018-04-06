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

from telethon.tl.functions.channels import InviteToChannelRequest

from flask import Flask, render_template, request, send_from_directory
template_dir = '/root/nammuoi'
app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def index():
   return render_template("index.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      try:
          apikey = request.form.get('apikey')
          accesshash = request.form.get('accesshash')
          phonenumber = request.form.get('phonenumber')
          channelname = request.form.get('channelname')

          client = TelegramClient(phonenumber, apikey, accesshash)



      

          client.session.report_errors = False
          client.connect()

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
          return render_template("result.html",members = members)
      except Exception as e:
          return render_template("error.html")
@app.route('/codeinputresult',methods = ['POST', 'GET'])
def codeinputresult():
   if request.method == 'POST':
      try:
          apikey = request.form.get('apikey')
          accesshash = request.form.get('accesshash')
          phonenumber = request.form.get('phonenumber')
          channelname = request.form.get('channelname')
          code = request.form.get('code')

          client = TelegramClient(phonenumber, apikey, accesshash)



      

          client.session.report_errors = False
          client.connect()
          
          client.send_code_request(phonenumber)
            
          client.sign_in(phone=phonenumber, code=code)
         
          channel_entity = client.get_entity(channelname)
          members = client.get_participants(channel_entity)
      
          return render_template("result.html",members = members)
      except Exception as e:
          return render_template("error.html")

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

def printmemberattr(members):
  result = []
  for member in members:
      result  = dir(member)
  print(result)

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = False  )
