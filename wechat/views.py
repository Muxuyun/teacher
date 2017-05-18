# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError 
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)
# 传入基本信息
conf = WechatConf(
    token='yuzhipeng', 
    appid='wx45eb06660e8df23e', 
    appsecret='97d0954b9e8779a23485b1d2ba3b1fc1', 
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
)
@csrf_exempt
def WeChat(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    # 实例化 WechatBasic 类
    wechat_instance = WechatBasic(conf=conf)
    # 验证微信公众平台的消息
    if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
       return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
           response = request.GET.get('echostr', 'error')
        else:
            try:
                print request.body
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                # 判断消息类型
                if isinstance(message, TextMessage):
                    reply_text = '文本回复'
                elif isinstance(message, VoiceMessage):
                    reply_text = 'voice'
                elif isinstance(message, ImageMessage):
                    reply_text = 'image'
                elif isinstance(message, LinkMessage):
                    reply_text = 'link'
                elif isinstance(message, LocationMessage):
                    reply_text = 'location'
                elif isinstance(message, VideoMessage):
                    reply_text = 'video'
                elif isinstance(message, ShortVideoMessage):
                    reply_text = 'shortvideo'
                else:
                    reply_text = 'other'
                response = wechat_instance.response_text(content=reply_text)
                if isinstance(message,ImageMessage):
                    response = wechat_instance.response_news([

                {
	         'title':u'第一条新闻',
                 'description':u'新闻描述',
                 'picurl':u'https://github.com/yuzp1996/myblog/blob/master/blog/static/blog/img/lovegirl.jpg',
                 'url':u'https://yuzp1996.github.io/',
                }
                ])            



            except ParseError: 
                print ParseError   
                return HttpResponseBadRequest('Invalid XML Data')
        return HttpResponse(response, content_type="application/xml")
