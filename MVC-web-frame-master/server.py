import socket
import _thread

from models.base_model import SQLModel
from request import Request
from utils import log

from routes import error

from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_public import route_dict as public_routes


def response_for_path(request):

    r = {}
    r.update(weibo_routes())
    r.update(user_routes())
    r.update(public_routes())
    response = r.get(request.path, error)
    log('路由分发 <{}> -> <{}>'.format(request.path, response))
    return response(request)


def request_from_connection(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            request = request.decode()
            log('HTTP 请求: <{}>'.format(request.encode()))
            return request


def process_request(connection):
    with connection:
        r = request_from_connection(connection)
        request = Request(r)
        response = response_for_path(request)
        log("HTTP 响应:\n <{}>".format(response))
        connection.sendall(response)


def run(host, port):
    """
    启动服务器
    """
    SQLModel.init_db()
    log('数据库链接初始化 <{}>'.format(SQLModel.connection.host_info))
    log('开始运行于 http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()

        while True:
            connection, address = s.accept()
            log('请求地址 {}'.format(address))
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    run(**config)
