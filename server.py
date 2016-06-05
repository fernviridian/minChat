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
  def __init__(self, name, password, connection):
    self.name = name
    self.password = password
    ip, port = connection.getsockname()
    self.ip = ip
    self.port = port
    self.channels = []
    self.time = time.time()
    self.connection = connection

  def getName(self):
    return self.name

  def updateConnection(self, connection):
    ip, port = connection.getsockname()
    self.ip = ip
    self.port = port
    self.connection = connection

  def checkTimeout(self):
    now = time.time()
    # send client message PING

  def inChannel(self, channel):
    return channel in self.channels

  def getChannels(self):
    return self.channels

  def join(self, channel):
    if channel in self.channels:
      # user already in channel
      return ERR_ALREADYINCHAN
    else:
      # user not in channel, join channel
      self.channels.append(channel)
      return OK_JOIN

  def leave(self, channel):
    if channel in self.channels:
      self.channels.remove(channel) 
      return OK_LEAVE
    else:
      return ERR_NOCHAN

  def sendMessage(self, message):
    # find connection for this user
    self.connection.send(message)

  def getPassword(self):
    return self.password

  def isConnection(self, conn):
    # check if connection passed is is for this user...
    if conn == self.connection:
      return True
    else:
     return False

############################################################################
# user manager class
############################################################################

class UserManager:
  # class that manages all the users
  def __init__(self):
    self.users = []

  def getUsernames(self):
    usernames = []
    for user in self.users:
      usernames.append(user.getName())
    return usernames

  def register(self, name, password, connection):
    # check to see if user already exists
    if not self.users:
      # no users registered yet:
      user = User(name, password, connection)
      self.users.append(user)
      return OK_REG

    else:
      # users exist already
      if name in self.getUsernames():
        return ERR_USERNAME_TAKEN
      for user in self.users:
          if(re.match('^[a-zA-Z0-9_]+$', name) and re.match('^[a-zA-Z0-9_]+$', password)):
            user = User(name, password, connection)
            self.users.append(user)
            return OK_REG
          else:
            return ERR_INVALID

  def authenticate(self, name, password, connection):
    # check to see if user exists

    if not self.users:
      return ERR_NOUSER

    for user in self.users:
      if name == user.getName():
        # found user, try to authenticate
        if password == user.getPassword():
          user.updateConnection(connection)
          return OK_AUTH
        else:
          return ERR_DENIED

  def sendMessage(self, name, message):
    '''
    just relays along message formatted elsewhere
    '''
    for user in self.users:
      if name == user.getName():
        user.sendMessage(message)

  def channelList(self):
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

  def channelUsers(self, channel):
    channel_users = []
    for user in self.users:
      if user.inChannel(channel):
        channel_users.append(user.getName())
    return channel_users

  def join(self, channel, connection):
    if not self.users:
      return ERR_NOUSER

    for user in self.users:
      if user.isConnection(connection):
        # found the user
        status = user.join(channel)
        return status
    else:
      # no user found?
      return ERR_NOUSER
      

  def leave(self, channel, connection):
    if not self.users:
      return ERR_NOUSER
    
    for user in self.users:
      if user.isConnection(connection):
        # found the user
        status = user.leave(channel)
        return status
      else:
        # no user found?
        return ERR_INVALID

  def message(self, channel, message, connection):
    # confirm user in channel (redundant, but still check)
    # get user name who is sending message
    # get list of users in channel self.channelUsers()
    # get socket connections for each of those users
    # for each user, send message from send_user to recv_user
    # TODO check if user hangs, and skip that user if necessary.
    # messages were sent to all users successfully :)
    # send confirm to send_user when messages sent succesfuuly.
    done = False

    if not self.users:
      return ERR_DENIED

    for user in self.users:
      if user.isConnection(connection):
        # found the sender user
        # get sender user name
        send_user = user.getName()
        # confirm user in channel:
        if user.inChannel(channel):
          # user is in that channel, can send message
          # need to get list of users in that room, and their connections
          users_in_channel = []
          for user in self.users:
            # f*&k efficiency, lets do this!
            if user.inChannel(channel):
              users_in_channel.append(user)
          # got a list of users in the channel, now send them a message
          #%<FQDN> <status code> <channel/priv_msg_user> <username> %<message>\r
          msg_string = "%{0} #{1} {2} %{3}\r".format(OK_MSG, channel, send_user, message)
          for user in users_in_channel:
            # message user
            user.sendMessage(msg_string)
            # what if sendMessage fails? TODO
            done = True
          break
          
        else:
          # user not allowed to message that channel
          return ERR_DENIED

    if(done):
      # outside for loop. let send_user know message was sent successfully.
      return OK_SEND

    else:
      # catch all, something went wrong
      return ERR_INVALID


  def ping(self):
    # ping all users to see if they are alive.
    # TODO
    pass

############################################################################
# dispatch regex matching
############################################################################

def dispatch(msg, connection):
  pong_regex = '^PONG\ ([0-9]+)'
  quit_regex = '^QUIT'
  reg_regex = '^REG\ (\w+)\ (\w+)'
  auth_regex = '^AUTH\ (\w+)\ (\w+)'
  msg_regex = '^MSG\ #(\w+)\ %(\w.*)'
  join_regex = '^JOIN\ #(\w+)'
  leave_regex = '^LEAVE\ #(\w+)'
  list_regex = '^LIST'
  memlist_regex = '^MEMLIST\ #(\w+)'

  regex_list = []
  regex_list.append(pong_regex)
  regex_list.append(quit_regex)
  regex_list.append(reg_regex)
  regex_list.append(auth_regex)
  regex_list.append(msg_regex)
  regex_list.append(join_regex)
  regex_list.append(leave_regex)
  regex_list.append(list_regex)
  regex_list.append(memlist_regex)

  for regex in regex_list:
    r = re.match(regex, msg)
    if(r is not None):
      # there was a match with this regex

      if regex == pong_regex:
        timestamp = r.groups()[0]
        return pong(timestamp)

      elif regex == quit_regex:
        return quit()

      elif regex == memlist_regex:
        channel = r.groups()[0]
        return memlist(channel, connection)

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
        msg = r.groups()[1]
        return message(channel, msg, connection)

      elif regex == join_regex:
        channel = r.groups()[0]
        return join(channel, connection)

      elif regex == leave_regex:
        channel = r.groups()[0]
        return leave(channel, connection)

      elif regex == list_regex:
        # list channels
        return listChannels()

  else:
    # invalid input
    # not matching regex
    return invalid()

############################################################################
# dispatch functions
############################################################################

def pong(timestamp):
  
  pass

def quit():
  # server got quit message from client, let client know
  # they can disconnect now. this is a nicety, and not required.
  return "%{0}\r".format(OK_QUIT)

def register(username, password, connection):
  # called when client wants to register a nickname
  return "%{0}\r".format(user_manager.register(username, password, connection))

def authenticate(username, password, connection):
  return "%{0}\r".format(user_manager.authenticate(username, password, connection))

def memlist(channel, connection):
  #Client can list members of a room
  ret = user_manager.channelUsers(channel)
  if type(ret) is not list:
    # something wrong
    return "%{0}\r".format(reg)
  else:
    channels = ",".join(ret)
    return "%{0} {1}\r".format(OK_LIST, channels)

def message(channel, message, connection):
  # called when a user messages a channel. 
  # looks up user that sent message by connection object, and then sends
  # message to other users in the same specified channel
  user_manager.message(channel, message, connection)
  return None

def join(channel, connection):
  # based on connection user_manager looks up the user object with that connection
  # and then has that user join the channel.
  return "%{0}\r".format(user_manager.join(channel, connection))

def leave(channel, connection):
  # based on connection look up user object and leave channel
  return "%{0}\r".format(user_manager.leave(channel, connection))

def listChannels():
  ret = user_manager.channelList()
  if type(ret) is not list:
    # something went wrong
    return "%{0}\r".format(ret)
  else:
    channels = ",".join(ret)
    return "%{0} {1}".format(OK_LIST, channels)

def invalid():
  return "%{0}\r".format(ERR_INVALID)

############################################################################
# globals
############################################################################

user_manager = UserManager()
host = ''
port = 9999
keepalive = 20  # ping every 20 seconds to see if client is connected
keepalive_response_time = 5  # the client gets 5 seconds to respond
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
running = True
server.listen(1)
input = [server, sys.stdin]
connections = []
channels = []

############################################################################
# main server loop
############################################################################

while running:

  # shitty keepalive here......
  previous_time = time.time()

  now = time.time()
  if(now - previous_time > keepalive):
    # run keepalive bulsshit
    # hacky timeout without threads is nasty?
    user_manager.ping()
    current_time = now
 
  readable, writable, errored = select.select([server] + connections, [], [])
  for connection in readable:

    if connection == server:
      # socket is server socket
      # new connection to server socket
      conn, client = connection.accept()
      connections.append(conn)

    else:
      # all other sockets, data to be read from socket
      print "all other sockets, returning client connection data"

      data = connection.recv(size)
      if not data:
        print "conn closed"
        connections.remove(connection)
      else:
        # do something with incoming data message
        server_response = dispatch(data, connection)
        if not server_response:
          # HACKy stuff for message
          continue
        connection.send(server_response)

server.close()
