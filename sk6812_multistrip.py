#!/usr/bin/env python3

# Copyright (c) 2019-2022 Thomas Kolb
# This file is licensed under the terms of the MIT license. See COPYING for
# details.

import struct
import socket
import time

from random import random

class SK6812Command:
  # command definitions
  SET_COLOR    = 0
  FADE_COLOR   = 1
  ADD_COLOR    = 2
  SET_FADESTEP = 3
  ACK_REQUEST  = 255

  def __init__(self, action = SET_COLOR, strip = 0, module = 0, d0 = 0, d1 = 0, d2 = 0, d3 = 0):
    self.action = int(action)
    self.strip  = int(strip)
    self.module = int(module)
    self.d0 = int(d0)
    self.d1 = int(d1)
    self.d2 = int(d2)
    self.d3 = int(d3)

  def serialize(self):
    return struct.pack(">BBBBBBB", self.action, self.strip, self.module, self.d0, self.d1, self.d2, self.d3)

class SK6812:
  def __init__(self, host, port):
    self.__commands = []

    # create the UDP socket
    family, socktype, proto, canonname, sockaddr = socket.getaddrinfo(host, port, 0, socket.SOCK_DGRAM)[0]

    self.__socket = socket.socket(family, socktype, proto)
    self.__socket.settimeout(0.0) # nonblocking mode
    self.__socket.connect(sockaddr)

  def commit(self):
    # send the data
    packet = b''
    for command in self.__commands:
      packet = packet + command.serialize()

    if packet:
      self.__socket.send(packet)

    self.__commands = []

  def set_fadestep(self, fadestep):
    # add a "set fadestep" command
    self.__commands.append(SK6812Command(SK6812Command.SET_FADESTEP, d0 = fadestep))

  def set_color(self, strip, module, r, g, b, w):
    # add a "set color" command
    self.__commands.append(SK6812Command(SK6812Command.SET_COLOR, strip, module, r, g, b, w))

  def fade_color(self, strip, module, r, g, b, w):
    # add a "fade to color" command
    self.__commands.append(SK6812Command(SK6812Command.FADE_COLOR, strip, module, r, g, b, w))

  def add_color(self, strip, module, r, g, b, w):
    # add a "add to color" command
    self.__commands.append(SK6812Command(SK6812Command.ADD_COLOR, strip, module, r, g, b, w))

  def ack_request(self, seq):
    # add a "request for acknowledgement" command
    self.__commands.append(SK6812Command(SK6812Command.ACK_REQUEST, 0, 0, (seq >> 8) & 0xFF, seq & 0xFF, 0, 0))

  def try_read_seq(self):
    try:
      data = self.__socket.recv(2)
    except socket.error:
      return -1

    if not data or len(data) != 2:
      return -1
    else:
      return struct.unpack(">H", data)[0]

if __name__ == "__main__":
  w = SK6812("192.168.2.222", 2703)
  w.set_fadestep(1);

  while True:
    w.set_color(10, 255, 255, 255, 255)
    for i in range(20):
      w.fade_color(i, 0, 0, 0)
    w.commit()
    time.sleep(0.2)
