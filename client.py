#! /usr/bin/env python


import socket
import sys
import time
import re
from status_codes import *

size = 1024

class Client:

  def __init__(self, host='0.0.0.0', port='9999'):
    self.user = '' 
    self.port = port
    self.host = host
    self.fqdn = socket.gethostbyname(socket.gethostname())
    self.prompt = "[{0}@{1}] {2}>"
    self.current_channel = ''
    self.channels = []
    self.done = False
    self.registered = False
    self.authenticated = False
    
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect((self.host, self.port))
      print "Connected to minChat server: {0}:{1}".format(self.host, self.port)

    except:
      print "failed to connect to server"

  self.commandTranslate(self, data):
    # like dispatch on server side. takes in user command and figures out what
    # to send to the server

    if(len(data) < 1):
      # if just hit enter
      return None

    #/msg #channel some message
    msg_regex = '^/msg\ #(\w+)\ (\w.*)'
    #/join #channel
    join_regex = '^/join\ #(\w+)'
    #/leave #channel
    leave_regex = '^/leave\ #(\w+)'
    #/quit
    quit_regex  = '^/quit'
    #/auth username password
    auth_regex = '^/auth\ (\w+)\ (\w+)'
    #/reg username password
    reg_regex =  '^/reg\ (\w+)\ (\w+)'


    regex_list = []
    regex_list.append(msg_regex)
    regex_list.append(join_regex)
    regex_list.append(leave_regex)
    regex_list.append(quit_regex)
    regex_list.append(auth_regex)
    regex_list.append(reg_regex)
    
    for regex in regex_list:
      r = re.match(regex, data)
        if(r is not None):
          # there was a match

          if regex == msg_regex:
            channel = r.groups()[0]
            message = r.groups()[1]
            return 'MSG {0} #{1}\r'.format(channel, message)

          else:
            # could not parse. send error to client.
            return None



  def cmdloop(self):
    while not done:
      try:
        # write prompt
        sys.stdout.write(self.prompt.format(self.user, self.fqdn, self.current_channel)
        sys.stdout.flush()
        
        # get input from stdin, server socket
        inputready, outputready, exceptready = select.select([0, self.sock], [],[])

        for socket in inputready:

          if socket == 0:
            # stdin
            data = sys.stdin.readline().strip()
            server_command = self.commandTranslate(data)
            if not server_command:
              # error parsing
              print "Could not parse command."
              continue
            else:
              # valid command to send to server
              self.socket.send(server_command)
              server_response = self.socket.recv(size)
              self.serverTranslate(server_response)  # figure out what to do based on response


          elif socket == self.socket:
            # message from server
            # ping or new message has arrived.

          else:
            print "other socket?!!"

      except KeyboardInterrupt:
        print 'Exiting!'
        self.socket.close()
        break




  def reg():

  def auth():

  def msg():

  def disconnect():



