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

host = ''
port = 9999
keepalive = 20  # ping every 20 seconds to see if client is connected
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
running = True
server.listen(1)
input = [server, sys.stdin]

connections = []
channels = []

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


class UserManager:
  def __init__():
    self.users = []

  def createUser(name, password, connection):

    # check to see if user already exists
    for user in self.users:
      if name == user.getName():
        return ERR_USERNAME_TAKEN
      else:
        if(re.match('^[a-zA-Z0-9_]+$', name) and re.match('^[a-zA-Z0-9_]+$', password)):
          user = User(name, password, connection)
          users.append(user)
        else:
        return ERR_INVALID

  def authenticate(name, password, connection):
    # check to see if user exists
    for user in self.users:
      if name == user.getName():
        # found user, try to authenticate
        if password == user.getPassword():
          user.updateConnection(connection)
          return True
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
    return channels

  def channelUsers(channel):
    channel_users = []
    for user in self.users:
      if user.inChannel():
        channel_users.append(user.getName())
    return channel_users


# main loop

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

server.close()
