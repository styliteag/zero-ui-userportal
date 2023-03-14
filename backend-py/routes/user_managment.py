from flask import jsonify, request, Blueprint
from untils.response import Response
from threading import Timer
import sys, os
sys.path.append(os.getcwd())
from constants.constants import *
from services.user_managment import USER_MANAGMENT
from services.member import MEMBER
import datetime

services_member = MEMBER()
services_user_managment = USER_MANAGMENT()


from vars import DARWIN, LINUX
sys_vars = DARWIN() if os.uname().sysname == "Darwin" else LINUX()

route_user_managment = Blueprint('user_managment', __name__)


@route_user_managment.route('/api/user-managment', methods=['GET', 'POST'])
def api_user_managment():

    if request.method == 'POST':
        user = services_user_managment.createUserData(request.json["username"], request.json["password"], request.json["role"])
        
        response_object = Response(200, "ok")
        
    elif request.method == 'GET':
        users = []
        data = services_user_managment.getUsersData()
        for user in data:
            users.append(user.get("username"))
        
        response_object = Response(200, "ok", users)
        
    return jsonify(response_object)


@route_user_managment.route('/api/user-managment/user/<string:user>', methods=['GET', 'POST'])
def api_user_managment_userinfo(user : str):
        
    userdata = services_user_managment.getUserInfo(user)
        
    response_object = Response(200, "ok", {"username" : userdata.get("username"), "role" : userdata.get("role"), "usericon" : userdata.get("usericon")})
        
    return jsonify(response_object)

@route_user_managment.route('/api/user-managment/add/<string:user>', methods=['GET', 'POST'])
def api_user_managment_add(user : str):

        user = services_user_managment.createUserData(user, request.json["password"], request.json["role"], request.json["usericon"])
        
        response_object = Response(200, "ok")

        return jsonify(response_object)

@route_user_managment.route('/api/user-managment/modify/<string:user>', methods=['GET', 'POST'])
def api_user_managment_modify(user : str):

        userdata = db.read_user_credentials(request.json["username"])
        if user == "admin":
            user = services_user_managment.updateUserData(request.json["username"], request.json["password"], request.json["role"], request.json["usericon"])
            response_object = Response(200, "ok", user)
        elif userdata != []:
            if hash.is_correct_password(userdata[0].get("salted_passwort"), request.json["old_password"]):
                user = services_user_managment.updateUserData(request.json["username"], request.json["password"], request.json["role"], request.json["usericon"])

                response_object = Response(200, "ok", request.json["username"])
            else:
                response_object = Response(403, "Unauth")
        else:
            response_object = Response(404, "Unauth")


        return jsonify(response_object)



       

@route_user_managment.route('/api/user-managment/del/<string:user>', methods=['GET', 'POST'])
def api_user_managment_del(user : str):

    if request.method == 'POST':

        user = services_user_managment.delUserData(user)
        
        if user:
            response_object = Response(200, "ok")


        
    return jsonify(response_object)

@route_user_managment.route('/api/user-managment/member/<string:user>', methods=['GET', 'POST'])
def api_user_managment_member(user : str):

    if request.method == 'GET':
        member = services_user_managment.getUserMember(user)
        
        try:
            for network in member:
                for idx, user_member in enumerate(member[network]):
                    try:
                        auth = services_user_managment.isUserMemberAuth(network, user_member["address"])
                        member[network][idx]["timetolive"] = services_member.getMembersData(network, [user_member["address"]])[0].get("timetolive")
                    except:
                        auth = False
                        member[network][idx]["timetolive"] = ""
                    
                    member[network][idx]["authorized"] = auth
                    print(member)
            response_object = Response(200, "ok", member)
        except Exception as e:
            response_object = Response(200, "ok", "Fehler bei der Abfrage " + str(e))
            

    elif request.method == 'POST':
        services_user_managment.updateUserMember(user, request.json["right"])
        
        response_object = Response(200, "ok", )

    return jsonify(response_object)


@route_user_managment.route('/api/user-managment/member/<string:user>/reason', methods=['POST'])
def api_user_managment_log_reason(user : str):

    if request.method == 'POST':
        if request.json.get("duration"):
            try:
                services_member.updateMemberAdditionalData(request.json["nwid"], request.json["mid"], {"timetolive" : services_user_managment.datetimeadd(int(request.json["duration"]))})
            except:
                services_member.updateMemberAdditionalData(request.json["nwid"], request.json["mid"], {"timetolive" : datetime.datetime.now(sys_vars.tz).strftime(f'%Y-%m-%d {request.json["duration"]}:00')})
        else:
            services_member.updateMemberAdditionalData(request.json["nwid"], request.json["mid"], {"timetolive" : "\u221e"})
        
        logger.info(f'Reason : {request.json["reason"]}  |  Duration : {request.json["duration"]}', ip=request.remote_addr, username=user)
    
    response_object = Response(200, "ok")
    return jsonify(response_object)


    
    def datetimeadd(self, hour : int):
        timetolive =  + timedelta(hours=hour)
        return timetolive.strftime('%Y-%m-%d %H:%M:%S')