# -*- coding:utf-8 -*-
import re

import leancloud
from django.http import HttpResponse
from django.shortcuts import render
# from django.http import HttpRequest as request
import LCD.RSAsign as rsasign

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from leancloud import Query, LeanCloudError
from wechatpy import create_reply, parse_message
from wechatpy.events import SubscribeEvent, UnsubscribeEvent, MassSendJobFinishEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, \
    LocationMessage
from wechatpy.events import BaseEvent
from wechatpy.utils import check_signature

from LCD.froms import NameForm, SaltForm
from LCD.models import Todo

TRASHED, PLANNED, COMPLETED = -1, 0, 1

WECHAT_TOKEN = 'sayhello'
AppID = 'wxad25526b9589c4c9'
AppSecret = '27b5ffa5802f8664ff0c38eefe6983c5'


def ping(request):
    salt = ''
    if request.method == 'POST':
        sf = SaltForm(request.POST)
        if sf.is_valid():
            salt = sf.cleaned_data['salt']
    if request.method == 'GET':
        salt = request.GET['salt']
    if salt is None or salt == '':
        return render(request, 'body.html', {'string': 'error!'})
    else:
        xmlContent = '<PingResponse><message></message><responseCode>OK</responseCode><salt>' + salt + '</salt></PingResponse>'
        xmlSignature = rsasign.sign(xmlContent)
        body = '<!-- ' + xmlSignature + ' -->\n' + xmlContent
        return render(request, 'body.html', {'string': body})
    return render(request, 'body.html', {'string': 'Ping!'})


def releaseTicket(request):
    salt = ''
    if request.method == 'POST':
        sf = SaltForm(request.POST)
        if sf.is_valid():
            salt = sf.cleaned_data['salt']
    if request.method == 'GET':
        salt = request.GET['salt']

    if salt is None or salt == '':
        return render(request, 'body.html', {'string': 'error!'})
    else:
        xmlContent = '<ReleaseTicketResponse><message></message><responseCode>OK</responseCode><salt>' + salt + '</salt></ReleaseTicketResponse>'
        xmlSignature = rsasign.sign(xmlContent)
        body = '<!-- ' + xmlSignature + ' -->\n' + xmlContent
        return render(request, 'body.html', {'string': body})
    return render(request, 'body.html', {'string': 'releaseTicket!'})


def obtainTicket(request):
    salt = ''
    username = ''
    if request.method == 'POST':
        nf = NameForm(request.POST)
        if nf.is_valid():
            salt = nf.cleaned_data['salt']
            username = nf.cleaned_data['userName']
    if request.method == 'GET':
        salt = request.GET['salt']
        username = request.GET('userName')
    prolongationPeriod = "607875500"
    if salt is None or salt == '' or username is None or username == '':
        return render(request, 'body.html', {'string': 'error!'})
    else:
        xmlContent = '<ObtainTicketResponse><message></message><prolongationPeriod>' + prolongationPeriod + '</prolongationPeriod><responseCode>OK</responseCode><salt>' + salt + '</salt><ticketId>1</ticketId><ticketProperties>licensee=' + username + '\tlicenseType=0\t</ticketProperties></ObtainTicketResponse>'
        xmlSignature = rsasign.sign(xmlContent)
        body = '<!-- ' + xmlSignature + ' -->\n' + xmlContent
        return render(request, 'body.html', {'string': body})
    return render(request, 'body.html', {'string': 'obtainTicket!'})


def home(request):
    string = u"我在自强学堂学习Django，用它来建网站"
    return render(request, 'home.html', {'string': string})


def index1(request):
    return render(request, 'home.html', {'string': 'Hello,This is a JetBrains License Server!'})


def show(request):
    try:
        todo = Query(Todo).descending('createdAt').find()
        todo = [x.get('content') for x in todo]
    except LeanCloudError as e:
        todo = []
        raise e
    return render(request, 'todos.html', {'todos': todo})


@csrf_exempt
def index(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        # logger.info('echo_str: %s' % echo_str)
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response

    # POST
    message = parse_message(request.body)

    # logger.info(type(message))

    if isinstance(message, TextMessage):
        # content = message.content.strip()  # 当前会话内容

        # reply_text = robot_reply(message.source, content)
        # logger.info('target: %s, source: %s, id: %s' % (message.target, message.source, message.id))
        reply = create_reply('reply_text', message=message)
        # logger.info(reply)
        return HttpResponse(reply, content_type="application/xml")

    elif isinstance(message, VoiceMessage):

        # rgx = re.compile("<!\[CDATA\[(.*?)\]\]>")
        # m = rgx.search(VoiceMessage.format)
        reply_text = str(VoiceMessage.recognition)
    elif isinstance(message, ImageMessage):
        reply_text = '图片信息我也看不懂/:P-(/:P-(/:P-('
    elif isinstance(message, VideoMessage):
        reply_text = '视频我不会看/:P-('
    elif isinstance(message, LinkMessage):
        reply_text = '链接信息'
    elif isinstance(message, LocationMessage):
        label = message.label
        # logger.info(label)
        reply_text = label
    elif isinstance(message, BaseEvent):  # 事件信息
        # logger.info(message.type)
        if isinstance(message, SubscribeEvent):  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
            reply_text = '事件信息'
            # logger.info('关注')
            # logger.info(message.target)
            # register_user(message.source)
        if isinstance(message, UnsubscribeEvent):  # 取消关注
            # logger.info('取消关注')
            reply_text = ''

        if isinstance(message, MassSendJobFinishEvent):
            # logger.info('群发消息事件')
            reply_text = ''

    reply = create_reply(reply_text, message=message)
    return HttpResponse(reply, content_type="application/xml")
