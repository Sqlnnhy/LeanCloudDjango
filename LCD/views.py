# -*- coding:utf-8 -*-
import leancloud
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from leancloud import Query, LeanCloudError
from wechatpy import create_reply
from wechatpy.events import SubscribeEvent, UnsubscribeEvent, MassSendJobFinishEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, \
    LocationMessage
from wechatpy.events import BaseEvent
from wechatpy.utils import check_signature

from LCD.models import Todo

TRASHED, PLANNED, COMPLETED = -1, 0, 1

WECHAT_TOKEN = 'sayhello'
AppID = 'wxad25526b9589c4c9'
AppSecret = '27b5ffa5802f8664ff0c38eefe6983c5'


def home(request):
    string = u"我在自强学堂学习Django，用它来建网站"
    return render(request, 'home.html', {'string': string})


def show(request):
    try:
        todo = Query(Todo).descending('createdAt').find()
        todo = [x.get('content') for x in todo]
    except LeanCloudError as e:
        todo = []
        raise e
    return render(request, 'todos.html', {'todos': todo})


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
    message = 'message'

    # logger.info(type(message))

    if isinstance(message, TextMessage):
        # content = message.content.strip()  # 当前会话内容

        # reply_text = robot_reply(message.source, content)
        # logger.info('target: %s, source: %s, id: %s' % (message.target, message.source, message.id))
        reply = create_reply('reply_text', message=message)
        # logger.info(reply)
        return HttpResponse(reply, content_type="application/xml")

    elif isinstance(message, VoiceMessage):

        reply_text = '语音信息我听不懂/:P-(/:P-(/:P-('
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
