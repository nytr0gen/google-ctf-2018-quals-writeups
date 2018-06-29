import os
import zipfile
import zlib
import hashlib
from struct import pack, unpack
import sys

POLY_SZ = 20


class BitStream:
  def __init__(self, data, sz=None):
    if sz is None:
      sz = len(data) * 8

    self.sz = sz
    self.data = bytearray(data)
    self.idx = 0

  def get_bit(self):
    if self.idx >= self.sz:
      raise Exception('All bits used. Go away.')

    i_byte = self.idx / 8
    i_bit = self.idx % 8

    bit = (self.data[i_byte] >> i_bit) & 1
    self.idx += 1

    return bit

  def get_bits(self, sz):
    v = 0
    for i in xrange(sz):
      b = self.get_bit()
      v |= b << i

    return v


class LFSR:
  def __init__(self, poly, iv, sz):
    self.sz = sz
    self.poly = poly
    self.r = iv
    self.mask = (1 << sz) - 1

  def get_bit(self, show):
    # leftmost bit
    bit = (self.r >> (self.sz - 1)) & 1

    new_bit = 1
    masked = self.r & self.poly
    for i in xrange(self.sz):
      new_bit ^= (masked >> i) & 1

    if show: print(self.r, bit, new_bit)

    # rightmost bit
    self.r = ((self.r << 1) | new_bit) & self.mask

    return bit


class LFSRCipher:
  def __init__(self, key, poly_sz=8, key_iv=None, cipher_iv=None):
    if len(key) < poly_sz:
      raise Exception('LFSRCipher key length must be at least %i' % poly_sz)
    key = BitStream(key)

    if key_iv is None:
      # key_iv = os.urandom(poly_sz)
      key_iv = '\x1aMA\x13\xdd\xd2?\xcb@\x89uhD\x01Qo\xcb\xd5\nT'
    self.key_iv = key_iv
    key_iv_stream = BitStream(key_iv)

    if cipher_iv is None:
      # cipher_iv = os.urandom(poly_sz)
      cipher_iv = "'Z\xb2\xff)\x9bG\x01\x8au\xae\x17b{\xdd\x16g\xb0\xa1\x94"
    self.cipher_iv = cipher_iv
    cipher_iv_stream = BitStream(cipher_iv)

    self.lfsr = []
    for i in xrange(8):
      caca = key.get_bits(poly_sz)
      l = LFSR(
        caca ^ key_iv_stream.get_bits(poly_sz),
        cipher_iv_stream.get_bits(poly_sz),
        poly_sz
      )
      self.lfsr.append(l)

  def get_keystream_byte(self):
    b = 0
    for i, l in enumerate(self.lfsr):
      gb = l.get_bit(i == 0) << i
      b |= gb
    return b

  def get_headers(self):
    return self.key_iv + self.cipher_iv

  def crypt(self, s):
    s = bytearray(s)
    for i in xrange(len(s)):
      b = self.get_keystream_byte()
      # print(b)
      s[i] ^= b
    return str(s)


# A super short ZIP implementation.
SETBIT = lambda n: 1 << n

db = lambda v: pack("<B", v)
dw = lambda v: pack("<H", v)
dd = lambda v: pack("<I", v)

ub = lambda v: unpack("<B", v)[0]
uw = lambda v: unpack("<H", v)[0]
ud = lambda v: unpack("<I", v)[0]


class BetterZipCreator:
  def __init__(self, arcname, key):
    self.key = key
    self.arcname = arcname

  # def write_eocdh(self, arc, ent_no, cdh_start, cdh_end):
  #   header_to_write = [
  #     "PK\x05\x06",
  #     dw(0),  # Disk no.
  #     dw(0),  # Disk with CDH.
  #     dw(ent_no),
  #     dw(ent_no),
  #     dd(cdh_end - cdh_start),
  #     dd(cdh_start),
  #     dw(0),  # Comment length.
  #   ]

  #   arc.write(''.join(header_to_write))

  def close(self):
    with open(self.arcname, "rb") as arc:
      data = arc.read()
      i = 0

      # def write_lfh(self, arc, f):
      #   fname, data = f
      #   crc = zlib.crc32(data) & 0xffffffff

      #   crypto_headers = c.get_headers()
      #   encrypted_data = c.crypt(data)

      #   sha256 = hashlib.sha256(data)
      #   encrypted_hash = c.crypt(sha256.digest())

      #######
      # read_lfh
      #######
      assert(data[i:i+4] == "PK\x03\x04"); i += 4 # "PK\x03\x04",
      assert(data[i:i+2] == dw(90)); i += 2 # dw(90),  # The encryption is so good it's version 9.0 at least!
      i += 2 # dw(SETBIT(0) | SETBIT(15)),  # Super strong encryption enabled!!!
      i += 2 # dw(0),  # No compression.
      assert(data[i:i+4] == dd(0)); i += 4 # dw(0), dw(0),  # Time/date, we don't care.
      crc = ud(data[i:i+4]); i += 4 # dd(crc),
      actual_sz = ud(data[i:i+4]); i += 4 # dd(actual_sz),
      len_data = ud(data[i:i+4]); i += 4 # dd(len(data)),
      len_fname = uw(data[i:i+2]); i += 2 # dw(len(fname)),
      assert(data[i:i+2] == dw(0)); i += 2 # dw(0),  # Extra field length.
      fname = data[i:i+len_fname]; i += len_fname # fname

      # actual_sz = len(crypto_headers) + len(data) + sha256.digest_size
      len_crypto_headers = actual_sz - len_data - 32

      crypto_headers = data[i:i+len_crypto_headers];
      i += len_crypto_headers # arc.write(crypto_headers)

      # crypto_headers = self.key_iv + self.cipher_iv
      key_iv = crypto_headers[:20]
      cipher_iv = crypto_headers[20:]

      encrypted_data = data[i:i+len_data];
      i += len_data # arc.write(encrypted_data)

      encrypted_hash = data[i:i+32];
      i += 32 # arc.write(encrypted_hash)

      #######
      # read_cdh
      #######
      assert(data[i:i+4] == "PK\x01\x02"); i += 4 # "PK\x01\x02",
      i += 2 # dw(90),  # The encryption is so good it's version 9.0 at least!
      i += 2 # dw(90),  # The encryption is so good it needs version 9.0 at least!
      i += 2 # dw(SETBIT(0) | SETBIT(15)),  # Super strong encryption enabled!!!
      i += 2 # dw(0),  # No compression.
      assert(data[i:i+4] == dd(0)); i += 4 # dw(0), dw(0),  # Time/date, we don't care.
      assert(ud(data[i:i+4]) == crc); i += 4 # dd(crc),
      assert(ud(data[i:i+4]) == actual_sz); i += 4 # dd(actual_sz),
      i += 4 # dd(len(data)),
      i += 2 # dw(len(fname)),
      assert(data[i:i+2] == dw(0)); i += 2 # dw(0),  # Extra field length.
      i += 2 # dw(0),  # Comment field length.
      i += 2 # dw(0),  # Disk number start.
      i += 2 # dw(0),  # File attributes.
      i += 4 # dd(0),  # External file attributes.
      offset = ud(data[i:i+4]); i += 4 # dd(offset),
      assert(fname == data[i:i+len_fname]); i += len_fname# fname
      # eocdh is irrelevant
      # self.write_eocdh(arc, len(self.files), cdh_start, cdh_end)

      print([key_iv, cipher_iv])

      print([crc, actual_sz, len_data, len_crypto_headers, len_fname, fname])

      c = LFSRCipher(self.key, POLY_SZ, key_iv, cipher_iv)
      v = c.crypt(encrypted_data[:40])
      # print(v)



if __name__ == '__main__':
  if len(sys.argv) != 3:
    sys.exit("usage: getter_zip.py <arcname.zip> <key_as_hex_string>")

  z = BetterZipCreator(sys.argv[1], sys.argv[2].decode('hex'))
  z.close()
