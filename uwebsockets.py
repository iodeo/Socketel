"""
Websockets client for micropython

Based very heavily off
https://github.com/aaugustin/websockets/blob/master/websockets/client.py
"""

#import libraries
import ussl
import ure as re
import urandom as random
import ustruct as struct
import usocket as socket
import ubinascii as binascii
from ucollections import namedtuple

# Opcodes
OP_CONT = const(0x0)
OP_TEXT = const(0x1)
OP_BYTES = const(0x2)
OP_CLOSE = const(0x8)
OP_PING = const(0x9)
OP_PONG = const(0xa)

# Close codes
CLOSE_OK = const(1000)
CLOSE_GOING_AWAY = const(1001)
CLOSE_PROTOCOL_ERROR = const(1002)
CLOSE_DATA_NOT_SUPPORTED = const(1003)
CLOSE_BAD_DATA = const(1007)
CLOSE_POLICY_VIOLATION = const(1008)
CLOSE_TOO_BIG = const(1009)
CLOSE_MISSING_EXTN = const(1010)
CLOSE_BAD_CONDITION = const(1011)

URL_RE = re.compile(r'(wss|ws)://([A-Za-z0-9-\.]+)(?:\:([0-9]+))?(/.+)?')
URI = namedtuple('URI', ('protocol', 'hostname', 'port', 'path'))

class NoDataException(Exception):
    pass

def urlparse(uri):
    """Parse ws:// URLs"""
    match = URL_RE.match(uri)
    if match:
        protocol = match.group(1)
        host = match.group(2)
        port = match.group(3)
        path = match.group(4)

        if protocol == 'wss':
            if port is None:
                port = 443
        elif protocol == 'ws':
            if port is None:
                port = 80
        else:
            raise ValueError('Scheme {} is invalid'.format(protocol))

        return URI(protocol, host, int(port), path)


class Websocket:
    """
    Basis of the Websocket protocol.

    This can probably be replaced with the C-based websocket module, but
    this one currently supports more options.
    """
    is_client = False

    def __init__(self, sock):
        self.sock = sock
        self.open = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def settimeout(self, timeout):
        self.sock.settimeout(timeout)

    def setblocking(self, blocking):
        self.sock.setblocking(blocking)

    def read_frame(self, max_size=None):
        """
        Read a frame from the socket.
        See https://tools.ietf.org/html/rfc6455#section-5.2 for the details.
        """

        # Frame header
        two_bytes = self.sock.read(2)

        if not two_bytes:
            raise NoDataException

        byte1, byte2 = struct.unpack('!BB', two_bytes)

        # Byte 1: FIN(1) _(1) _(1) _(1) OPCODE(4)
        fin = bool(byte1 & 0x80)
        opcode = byte1 & 0x0f

        # Byte 2: MASK(1) LENGTH(7)
        mask = bool(byte2 & (1 << 7))
        length = byte2 & 0x7f

        if length == 126:  # Magic number, length header is 2 bytes
            length, = struct.unpack('!H', self.sock.read(2))
        elif length == 127:  # Magic number, length header is 8 bytes
            length, = struct.unpack('!Q', self.sock.read(8))

        if mask:  # Mask is 4 bytes
            mask_bits = self.sock.read(4)

        try:
            data = b''
            if max_size:
                if length > max_size:
                    length = max_size
            if length > 0:
                data += self.sock.read(length)
        except MemoryError:
            # We can't receive this many bytes, close the socket
            print('WS_READ: MemError') #DEBUG
            self.close(code=CLOSE_TOO_BIG)
            return True, OP_CLOSE, None

        if mask:
            data = bytes(b ^ mask_bits[i % 4]
                         for i, b in enumerate(data))

        return fin, opcode, data

    def write_frame(self, opcode, data=b''):
        """
        Write a frame to the socket.
        See https://tools.ietf.org/html/rfc6455#section-5.2 for the details.
        """
        fin = True
        mask = self.is_client  # messages sent by client are masked

        length = len(data)

        # Frame header
        # Byte 1: FIN(1) _(1) _(1) _(1) OPCODE(4)
        byte1 = 0x80 if fin else 0
        byte1 |= opcode

        # Byte 2: MASK(1) LENGTH(7)
        byte2 = 0x80 if mask else 0

        if length < 126:  # 126 is magic value to use 2-byte length header
            byte2 |= length
            self.sock.write(struct.pack('!BB', byte1, byte2))

        elif length < (1 << 16):  # Length fits in 2-bytes
            byte2 |= 126  # Magic code
            self.sock.write(struct.pack('!BBH', byte1, byte2, length))

        elif length < (1 << 64):
            byte2 |= 127  # Magic code
            self.sock.write(struct.pack('!BBQ', byte1, byte2, length))

        else:
            raise ValueError()

        if mask:  # Mask is 4 bytes
            mask_bits = struct.pack('!I', random.getrandbits(32))
            self.sock.write(mask_bits)

            data = bytes(b ^ mask_bits[i % 4]
                         for i, b in enumerate(data))

        if length > 0:
            self.sock.write(data)

    def recv(self, max_size = None):
        """
        Receive data from the websocket.

        This is slightly different from 'websockets' in that it doesn't
        fire off a routine to process frames and put the data in a queue.
        If you don't call recv() sufficiently often you won't process control
        frames.
        """
        assert self.open

        while self.open:
            try:
                fin, opcode, data = self.read_frame(max_size = max_size)
            except NoDataException:
                return ''
            except ValueError:
                print('WS_RECV: ValueError') #DEBUG
                self._close()
                return

            if not fin:
                print('WS_RECV: got multiframe fragment') #DEBUG
                raise NotImplementedError()

            if opcode == OP_TEXT:
                return data
            elif opcode == OP_BYTES:
                return data
            elif opcode == OP_CLOSE:
                print('WS_RECV: got OP_CLOSE') #DEBUG
                self._close()
                return
            elif opcode == OP_PONG:
                print('WS_RECV: got OP_PONG') #DEBUG
                # Ignore this frame, keep waiting for a data frame
                continue
            elif opcode == OP_PING:
                print('WS_RECV: got OP_PING') #DEBUG
                # We need to send a pong frame
                self.write_frame(OP_PONG, data)
                # And then wait to receive
                continue
            elif opcode == OP_CONT:
                # This is a continuation of a previous frame
                print('WS_RECV: got OP_CONT') #DEBUG
                raise NotImplementedError(opcode)
            else:
                print('WS_RECV: Unknown OP_CODE') #DEBUG
                raise ValueError(opcode)

    def send(self, buf):
        """Send data to the websocket.

        """
        assert self.open

        if isinstance(buf, str):
            opcode = OP_TEXT
            buf = buf.encode('utf-8')
            print('WS_SEND: send OP_TEXT: ' + buf.decode())
        elif isinstance(buf, bytes):
            opcode = OP_BYTES
            print('WS_SEND: send OP_BYTES: ' + buf.decode())
        else:
            raise TypeError()

        self.write_frame(opcode, buf)

    def close(self, code=CLOSE_OK, reason=''):
        """Close the websocket.

        """
        if not self.open:
            return

        buf = struct.pack('!H', code) + reason.encode('utf-8')

        try:
            self.write_frame(OP_CLOSE, buf)
        except:
            pass
        self._close()

    def _close(self):
        self.open = False
        self.sock.close()

class WebsocketClient(Websocket):
    is_client = True

def connect(uri, subprotocol = ''):
    """
    Connect a websocket.

    """

    uri = urlparse(uri)
    assert uri

    assert isinstance(subprotocol, str)

    sock = socket.socket()
    addr = socket.getaddrinfo(uri.hostname, uri.port)
    sock.connect(addr[0][4])
    if uri.protocol == 'wss':
        sock = ussl.wrap_socket(sock)

    def send_header(header, *args):
        sock.write(header % args + '\r\n')

    # Sec-WebSocket-Key is 16 bytes of random base64 encoded
    key = binascii.b2a_base64(bytes(random.getrandbits(8)
                                    for _ in range(16)))[:-1]

    send_header(b'GET %s HTTP/1.1', uri.path or '/')
    send_header(b'Host: %s:%s', uri.hostname, uri.port)
    send_header(b'Connection: Upgrade')
    send_header(b'Sec-WebSocket-Key: %s', key)
    send_header(b'Sec-WebSocket-Version: 13')
    if subprotocol:
        send_header(b'Sec-WebSocket-Protocol: %s', subprotocol)
    send_header(b'Origin: file://')
    send_header(b'Upgrade: websocket')
    send_header(b'User-Agent: Socketel ESP32 Client')
    send_header(b'')

    header = sock.readline()[:-2]
    assert header.startswith(b'HTTP/1.1 101 '), header

    # We don't (currently) need these headers
    # FIXME: should we check the return key?
    while header:
        print("uwebsockets.py header:", header)
        header = sock.readline()[:-2]

    return WebsocketClient(sock)
