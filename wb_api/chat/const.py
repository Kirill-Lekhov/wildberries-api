from wb_api.base.enum_toolkit import allow_unknown

from enum import Enum


@allow_unknown
class EventType(Enum):
	MESSAGE = "message"


@allow_unknown
class MessageSource(Enum):
	SELLER_PORTAL = "seller-portal"		# портал продавцов
	SELLER_PUBLIC_API = "seller-public-api"		# API Чата с покупателями
	RUSITE = "rusite"		# портал покупателей
	GLOBAL = "global"		# портал global.wildberries.ru
	IOS = "ios"		# мобильная операционная система от Apple
	ANDROID = "android"		# операционная система Android от Google


@allow_unknown
class MessageSender(Enum):
	CLIENT = "client"
	SELLER = "seller"
	WILDBERRIES = "wb"
