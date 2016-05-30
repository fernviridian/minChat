#! /usr/bin/env python

# minchat server

# references
# https://www.reddit.com/r/learnpython/comments/2ny3kw/i_created_a_multithreaded_chat_script_how_can_i/

import socket
import time
import re
import sys
import select
from status_codes import *
############################################################################
# user class
############################################################################

class User:
  def __init__(name, password, connection):
    self.name = name
    self.password = password
    ip, port = connection.getsockname()
    self.ip = ip
    self.port = port
    self.channels = []
    self.time = time.time()

  def getName():
    return self.name

  def updateConnection(connection):
    ip, port = connection.getsockname()
    self.ip = ip
    self.port = port

  def checkTimeout():
    now = time.time()
    # send client message PING

  def inChannel(channel):
    return channel in channels

  def getChannels():
    return self.channels

  def join(channel):
    if channel in channels:
      # user already in channel
      return ERR_ALREADYINCHAN
    else:
      # user not in channel, join channel
      self.channels.append(channel)
      return OK_JOIN

  def leave(channel):
    if channel in channels:
      self.channels.remove(channel) 
      return OK_LEAVE
    else:
      return ERR_NOCHAN

  def sendMessage(message):
    # find connection for this user
    for connection in connections:
      ip, port = connection.getsockname()
      if ip = self.ip and port = self.port:
        # send message
        connection.send(message)

  def getPassword():
    return self.password

############################################################################
# user manager class
############################################################################

class UserManager:
  def __init__():
    self.users = []

  def register(name, password, connection):

    # check to see if user already exists
    for user in self.users:
      if name == user.getName():
        return ERR_USERNAME_TAKEN
      else:
        if(re.match('^[a-zA-Z0-9_]+$', name) and re.match('^[a-zA-Z0-9_]+$', password)):
          user = User(name, password, connection)
          users.append(user)
          return OK_REG
        else:
          return ERR_INVALID

  def authenticate(name, password, connection):
    # check to see if user exists
    for user in self.users:
      if name == user.getName():
        # found user, try to authenticate
        if password == user.getPassword():
          user.updateConnection(connection)
          return OK_AUTH
        else:
          return ERR_DENIED

  def sendMessage(name, message):
    '''
    just relays along message formatted elsewhere
    '''
    for user in self.users:
      if name == user.getName():
        user.sendMessage(message)

  def channelList():
    '''
    return list of channels on the server
    '''
    # does this in a hacky way by querying each user's channel list, and returning that
    channels = []
    for user in self.users:
      t = user.getChannels()
      for chan in t:
        if chan not in channels:
          # if not in list already, add it. this way no duplicates
          channels.append(chan)
    if not channels:
      # no channels to list, return error code to client
      return ERR_NOCHAN
    else:
      # return list object of channels
      return channels

  def channelUsers(channel):
    channel_users = []
    for user in self.users:
      if user.inChannel():
        channel_users.append(user.getName())
    return channel_users

############################################################################
# dispatch regex matching
############################################################################

def dispatch(message, connection):
  pong_regex = '^PONG\ ([0-9]+)'
  quit_regex = '^QUIT'
  reg_regex = '^REG\ (\w+)\ (\w+)'
  auth_regex = '^AUTH\ (\w+)\ (\w+)'
  msg_regex = '^MSG\ #(\w+)\ (\w.*)'
  join_regex = '^JOIN\ #(\w+)'
  leave_regex = '^LEAVE\ #(\w+)'
  list_regex = '^LIST'

  regex_list = []
  regex_list.append(pong_regex)
  regex_list.append(quit_regex)
  regex_list.append(reg_regex)
  regex_list.append(auth_regex)
  regex_list.append(msg_regex)
  regex_list.append(join_regex)
  regex_list.append(leave_regex)
  regex_list.append(list_regex)

  for regex in regex_list:
    r = re.match(regex, message)
    if(r is not None):
      # there was a match with this regex

      if regex == pong_regex:
        timestamp = r.groups()[0]
        return pong(timestamp)

      elif regex == quit_regex:
        return quit()

      elif regex == reg_regex:
        username = r.groups()[0]
        password = r.groups()[1]
        return register(username, password, connection)

      elif regex == auth_regex:
        username = r.groups()[0]
        password = r.groups()[1]
        return authenticate(username, password, connection)

      elif regex == msg_regex:
        channel = r.groups()[0]
        message = r.groups()[1]
        return msg(channel, message)

      elif regex == join_regex:
        channel = r.groups()[0]
        return join(channel)

      elif regex == leave_regex:
        channel = r.groups()[0]
        return leave(channel)

      elif regex == list_regex:
        # list channels
        return listChannels()

      else:
        # invalid input
        return invalid()

############################################################################
# dispatch functions
############################################################################

def pong(timestamp):
  
  pass

def quit():
  # server got quit message from client, let client know
  # they can disconnect now. this is a nicety, and not required.
  return "%{0} {1}\r".format(fqdn, OK_QUIT)

def register(username, password, connection):
  # called when client wants to register a nickname
  return "%{0} {1}\r".format(fqdn, user_manager.register(username, password, connection))

def authenticate(username, password, connection):
  return "%{0} {1}\r".format(fqdn, user_manager.authenticate(username, password, connection))

def msg(channel, message):
  pass

def join(channel)
  pass

def leave(channel):
  pass

def listChannels():
  ret = user_manager.channelList()
  if type(ret) is not list:
    # something went wrong
    return "%{0} {1}\r".format(fqdn, ret)
  else:
    channels = ",".join(ret)
    return "%{0} {1} {2}".format(fwdn, OK_LIST, channels)

def invalid():
  return "%{0} {1}\r".format(fqdn, ERR_INVALID)

############################################################################
# globals
############################################################################

user_manager = userManager()
host = ''
port = 9999
keepalive = 20  # ping every 20 seconds to see if client is connected
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
running = True
server.listen(1)
input = [server, sys.stdin]
fqdn = socket.gethostbyname(socket.gethostname())
connections = []
channels = []

############################################################################
# main server loop
############################################################################

while running:
 
  readable, writable, errored = select.select([server] + connections, [], [])
  for connection in readable:

    if connection == server:
      # socket is server socket
      # new connection to server socket
      conn, client = connection.accept()
      connections.append(conn)

    else:
      # all other sockets, data to be read from socket
      print "all other sockets"

      data = connection.recv(size)
      if not data:
        print "conn closed"
        connections.remove(connection)
      else:
        # do something with incoming data message
        dispatch(data, connection)

server.close()
