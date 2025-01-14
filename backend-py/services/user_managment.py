import sys, os, time
from typing import Hashable
sys.path.append(os.getcwd())
from constants.constants import *
from services.member import MEMBER
import datetime
from datetime import timedelta

from vars import DARWIN, LINUX
sys_vars = DARWIN() if os.uname().sysname == "Darwin" else LINUX()


class USER_MANAGMENT():
    """Classe um die Anfragen rund ums UserManagment zu handeln"""
        

    def _hash_passwort(self, passwort : str) -> Hashable:
        
        return hash.hash_password(passwort)

    def createUserData(self, username : str, passwort : str, role : str):
        if db.read_user_credentials(username) == []:
            db.write_user_credentials(**{"username" : username, "salted_passwort" : self._hash_passwort(passwort), "role" : role})

            return True

    def delUserData(self, username : str) -> bool:
        if db.read_user_credentials(username) != []:
            db.delete_user(username)

            return True
        
    def getUsersData(self) -> list:
        return db.read_users()

    def getUserMember(self, user : str) -> dict:
        members = db.read_user_member(user)[0].get("members")
        if members:
            return members

    def updateUserMember(self, user : str, data : dict) -> None:
        db.clean_user_member(user)
        if data[0].get("config") != None:
            for member in data:
                memberData = {"name" : self.fix_none_username(member.get("name")), "address" : member.get("config")["address"]}
                time.sleep(0.5)
                db.update_user_member(user, member["networkId"], memberData) 
        else:
            db.clean_user_member(user)

    def isUserMemberAuth(self, nwid : str, mid : str) -> bool:
        data = MEMBER().getMembersData(nwid, [mid])
        return data[0]["config"]["authorized"]


    def fix_none_username(self, name : str) -> str:
        if name == None:
            name = "Dummy Name"
        return name
    
    def deauth(self, nwid, mid):
       zerotier_api.make_request("POST", f"/controller/network/{nwid}/member/{mid}", json = {"authorized" : False})
       
    def convert(self, hours : int): 
        minuts  = hours  * 60
        seconds = minuts * 60
        return seconds
        
    def datetimecheck(self, timestamp : datetime):
        timetolive       = timestamp
        aktuelles_datum = datetime.datetime.now(sys_vars.tz).strftime('%Y-%m-%d %H:%M:%S')
        isover = aktuelles_datum > timetolive
        return isover

    def datetimeadd(self, hour : int):
        timetolive = datetime.datetime.now(sys_vars.tz) + timedelta(hours=hour)
        return timetolive.strftime('%Y-%m-%d %H:%M:%S')

    def watcher(self):
        for network in db.read_networks():
            for member in network.get("members"):
                try:
                    TTL = member.get("additionalConfig").get("timetolive")
                    if self.datetimecheck(TTL) == True and TTL != "\u221e":
                        self.deauth(network["id"], member["id"])
                        try:
                            additionalConfig = db.read_networks_member_value(network["id"], member["id"])["additionalConfig"]
                        except:
                            additionalConfig = {}
                        db.update_network_members(network["id"], member["id"], {"additionalConfig" : db.merge_two_dicts(additionalConfig, {"authorized" : False})})
                except:
                    pass

