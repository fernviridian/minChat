#! /usr/bin/env python


import socket
import sys
import time
import re
from status_codes import *

size = 1024

class Channel:
  # channel object keeps state between switching channels
  def __init__(self, name):
    self.name = name
    self.buf = []
    # ideally we should limit buffer size, but not in the scope of this project.
    # and also prune old messages so we dont consume too much memory

  def backscroll(self):
    # convert lines in self.buf into string and return
    ret_string = ''
    for line in self.buf:
      ret_string += line

    return ret_string  # this can be printed on screen after a screen.flush() easily

  def addLine(self, line):
    # add a line to the buffer
    # used when we get a new message we want to keep.
    # line = <sender>: <message>
    self.buf.append(line)


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

  self.send(msg):
    # send a command to server
    return self.socket.send(msg)
    

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
    #/list
    list_regex = '^/list'

    #/win
    win_regex = '^/win'

    regex_list = []
    regex_list.append(msg_regex)
    regex_list.append(join_regex)
    regex_list.append(leave_regex)
    regex_list.append(quit_regex)
    regex_list.append(auth_regex)
    regex_list.append(reg_regex)
    regex_list.append(list_regex)
    regex_list.append(win_regex)
    
    for regex in regex_list:
      r = re.match(regex, data)
        if(r is not None):
          # there was a match

          if regex == msg_regex:
            channel = r.groups()[0]
            message = r.groups()[1]
            return 'MSG {0} #{1}\r'.format(channel, message)

          elif regex == join_regex:
            channel = r.groups()[0]
            return 'JOIN #{0}\r'.format(channel)

          elif regex == leave_regex:
            channel = r.groups()[0]
            return 'LEAVE #{0}\r'.format(channel)
          
          elif regex == quit_regex:
            return 'QUIT\r'

          elif regex == auth_regex:
            username = r.groups()[0]
            password = r.groups()[1]
            return 'AUTH {0} {1}\r'.format(username, password)

          elif regex == reg_regex:
            username = r.groups()[0]
            password = r.groups()[1]
            return 'REG {0} {1}\r'.format(username, password)

          elif regex == list_regex:
            return 'LIST\r'

          elif regex == win_regex:
            # TODO

          else:
            # could not parse. send error to client.
            return None

  def serverStatusTranslate(self, msg):
    # translate server return codes
    status_regex = '^%(\d+)'
    status_code = PADPAPFPAFP
    switcher = {
        OK_QUIT: 'OK_QUIT',
        OK_REG: 'OK_REG',
        OK_AUTH: 'OK_AUTH',
        OK_ROOMCREATE: 'OK_ROOMCREATE',
        OK_ROOMEXISTS: 'OK_ROOMEXISTS',
        OK_ROOMLIST: 'OK_ROOMLIST',
        OK_NEWJOIN: 'OK_NEWJOIN',
        OK_LEAVE: 'OK_LEAVE',
        OK_LIST: 'OK_LIST',
        OK_JOIN: 'OK_JOIN',
        OK_MSG: 'OK_MSG',
        OK_SEND: 'OK_SEND',
        ERR_BANNED = 'ERR_BANNED',
        ERR_TIMEOUT = 'ERR_TIMEOUT',
        ERR_INVALID = 'ERR_INVALID',
        ERR_NOUSER = 'ERR_NOUSER',
        ERR_DENIED = 'ERR_DENIED',
        ERR_USERNAME_TAKEN = 'ERR_USERNAME_TAKEN',
        ERR_TOOBIG = 'ERR_TOOBIG',
        ERR_NOCHAN = 'ERR_NOCHAN',
        ERR_ALREADYINCHAN = 'ERR_ALREADYINCHAN',
        ERR_OOM = 'ERR_OOM',
        
    }
    return switcher.get(argument, status_code)


  def serverTranslate(self, data):
    # translate responses from server
    # ping or msg
    
    #%PING 1231231\r
    ping_regex = '^\%PING\ (\d+)\\r'
    #%211 #channel username %some message\r
    msg_regex = '^\%(\d+)\ #(\w+)\ (\w+)\ %(\w.*)\\r'

    regex_list = []
    regex_list.append(ping_regex)
    regex_list.append(msg_regex)
    
    for regex in regex_list:
      r = re.match(regex, data)
        if(r is not None):
          # there was a match

          if regex == msg_regex:
            return_code = r.groups()[0]
            channel = r.groups()[1]
            username = r.groups()[2]
            message = r.groups()[3]
            self.printMessage(channel, username, message)

          elif regex == ping_regex:
            epoch = r.groups()[0]

          else:
            # not matching a regex, invalid
            return None
 
  def printMessage(self, channel, user, message):
    # print message to screen with current channel, etc.
     

  def respondPing(self, epoch):
    # respond to server message right away.
    msg = 'PONG {0}\r'.format(epoch)
    self.send(msg)  # dont care about response, just that it completeconnection.
    return

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
              # parse server response
                       
          elif socket == self.socket:
            # message from server
            # ping or new message has arrived.
            server_translated = self.serverTranslate(server_response)  # figure out what to do based on response
            if not server_translated:
              #error parsing
              print "Could not parse server response."
              continue

          else:
            print "other socket?!!"

      except KeyboardInterrupt:
        print 'Exiting!'
        self.socket.close()
        break


if __name__ == '__main__':
  if len(sys.argv) < 2:
        sys.exit('Usage: {0} host port'.format(sys.argv[0]))
        
  client = Client(sys.argv[1], int(sys.argv[2]))
  client.cmdloop()
