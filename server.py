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

  def getChannels():
    return self.channels

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

  def channelUsers

    return True

    return False


def sendAll(msg):
  '''
  broadcast to all connections
  '''
  for connection in connections:
    connection.send(msg)
    import pdb; pdb.set_trace()

def parseCommand(data):
  '''
  deciphers the command sent to server, and returns appropriate message
  '''

  try:
    command = str(data)

  except:
    # return ERR_INVALID
    msg = "%{0} {1} %{2}".format(host, ERR_INVALID, "String not parsable.")
    return msg

  # msg is a valid string, so parse from there.
  #regex = "(.*)\ (.*)\ 
  # write pythex

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
        print "msg all"
        sendAll(data)

server.close()
