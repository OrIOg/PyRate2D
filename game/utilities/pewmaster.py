#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
from threading import Thread
import time
import base64
import json


def sanitize(url):
    return base64.b64encode(urllib.parse.quote(url).encode("utf-8")).decode()


def desanitize(url):
    return urllib.parse.unquote(base64.b64decode(url).decode("utf-8"))


def querylize(_dict: dict):
    query = ""
    for key, value in _dict.items():
        query += "&{}={}".format(key, sanitize(value))
    return query


class Lobby:
    PEWMASTER_QUERY = "http://www.pixelsiege.net/master/query.php?game="
    PEWMASTER_UPDATE = "http://www.pixelsiege.net/master/update.php?action="

    @staticmethod
    def list(game):
        lobbies = []
        url = "{}{}".format(Lobby.PEWMASTER_QUERY, sanitize(game))
        status = 404
        try:
            response = urllib.request.urlopen(url)
            status = respons.status
            if status == 200:
                raw_lobbies = response.read().decode("utf-8").splitlines()[1:]
                for raw_lobby in raw_lobbies:
                    lobby = Lobby.parse(game, raw_lobby)
                    lobbies.append(lobby)
        except:
            pass

        return (lobbies, status)

    @staticmethod
    def parse(game, raw_data):
        data = raw_data.split('|')
        hostname, private_ip, public_ip, info = [""] * 4
        try:
            hostname, private_ip, public_ip, info = desanitize(
                data[0]), desanitize(data[1]), data[2], desanitize(data[3])
            info = json.loads(base64.b64decode(info).decode("utf-8"))
        except:
            hostname, private_ip, public_ip = desanitize(
                data[0]), desanitize(data[1]), data[2]
        return Lobby(game, hostname, private_ip, public_ip, info, isData=True)

    def __init__(self, game, hostname, private_ip=None, public_ip=None, info=None, isData=False):
        self.game = game
        self.hostname = hostname
        self.private_ip = private_ip if private_ip else "127.0.0.1"
        self.public_ip = public_ip
        self.id = None
        if not public_ip:
            ip_request = urllib.request.urlopen('http://ip.42.pl/raw')
            if ip_request.status == 200:
                self.public_ip = ip_request.read().decode("utf-8")

        self.info = info
        self.__created = False

        if not isData:
            self.__created = True
            self.__update_thread = Thread(target=self.__update)
            self.__update_thread.daemon = True

            query = {"game": self.game, "hostname": self.hostname}
            if self.private_ip:
                query["ip"] = self.private_ip
            if self.info:
                dump = json.dumps(self.info, indent=None,
                                  ensure_ascii=False, separators=(',', ':'))
                query["info"] = base64.b64encode(dump.encode("utf-8"))

            queryString = querylize(query)
            url = self.PEWMASTER_UPDATE + "create&" + queryString
            response = urllib.request.urlopen(url)
            self.id = int(response.read().decode("utf-8"))
            self.__update_thread.start()

    def close(self):
        if not self.__created:
            return
        self.__update_thread.join(0)
        url = self.PEWMASTER_UPDATE + "close&id=" + str(self.id)
        urllib.request.urlopen(url)
        self.__created = False

    def update(self, hostname=None, info=None):
        if not self.__created:
            return
        query = {}
        if hostname:
            query["hostname"] = hostname
            self.hostname = hostname
        if info:
            query["info"] = info
            self.info = info
        queryString = querylize(query)
        url = self.PEWMASTER_UPDATE + "update&id=" + str(self.id) + queryString
        urllib.request.urlopen(url)

    def __update(self):
        while True:
            time.sleep(60)
            url = self.PEWMASTER_UPDATE + "update&id=" + str(self.id)
            urllib.request.urlopen(url)

    def __repr__(self):
        return "{} - {}({}) {}".format(self.game, self.hostname, self.public_ip, self.info)


if __name__ == "__main__":
    name = "111" + str(time.time())
    info_data = [1, 2, 3, {'k': True, 'n': False, "Ö": "éè&î@ͿΏ"}]
    lobby = Lobby(name, "lobby_test", info=info_data)
    print(lobby)
    print(Lobby.list(name))
    time.sleep(5)
    lobby.update(hostname="UpdatedLobby")
    print(lobby)
    print(Lobby.list(name))
    lobby.close()
