# # Twisted - управляемая событиями(event) структура
# # Событиями управляют функции – event handler
# # Цикл обработки событий отслеживает события и запускает соответствующие event handler
# # Работа цикла лежит на объекте reactor из модуля twisted.internet
#
# # Модуль socketserver для сетевого программирования
# from twisted.internet import protocol, reactor
#
#
# class Twist(protocol.Protocol):
#     # Событие connectionMade срабатывает при соединении
#     def connectionMade(self):
#         print('connection success!')
#
#     # Событие dataReceived - получение и отправление данных
#     def dataReceived(self, data):
#         print(data)
#         # transport.write - отправка сообщения
#         self.transport.write('Hello from server!'.encode())
#
#     # Событие connectionLost срабатывает при разрыве соединения с клиентом
#     def connectionLost(self, reason):
#         print('Connection lost!')
#
#
# # Конфигурация поведения протокола описывается в – классе Factory из twisted.internet.protocol.Factory
# factory = protocol.Factory()
# factory.protocol = Twist
# print('wait...')
#
# reactor.listenTCP(8007, factory)
# reactor.run()
#
#
# # from twisted.internet.protocol import Factory, Protocol
# # from twisted.internet import reactor
# #
# #
# # class Server(Protocol):
# #     def connectionMade(self):
# #         self.transport.write(str(self.factory.quote + '\r\n').encode())
# #
# #     def connectionLost(self, reason):
# #         print('connection lost ...')
# #
# #     def dataReceived(self, data):
# #         print(data)
# #         self.transport.write()
# #
# #
# # class ServerFactory(Factory):
# #     protocol = Server
# #
# #     def __init__(self, quote=None):
# #         self.quote = quote
# #
# #
# # reactor.listenTCP(8007, ServerFactory("quote"))
# # reactor.run()