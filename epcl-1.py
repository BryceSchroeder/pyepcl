#!/usr/bin/env python3
# PyEPCL - Partial Python3 implementation of the EPCL 
# This file may be used under the terms of the GNU Lesser
# General Public License version 3 as published by the Free Software
# Foundation and appearing in the file LICENSE.LGPLv3 included in the
# packaging of this file.  Please review the following information to
# ensure the GNU Lesser General Public License version 3 requirements
# will be met: https://www.gnu.org/licenses/lgpl.html.

# Use: epcl color.png resin-black.png varnish.png outputfile.txt
# Note: resin and varnish images must be greyscale, not RGB or indexed
# Black is the presence of resin black / varnish.
# All images must be 1030 wide (X) and 646 pixels tall (Y).
# Print in raw mode, e.g:
# lp -d P430i -o raw outputfile.txt
# This doesn't use the card flipper, laminator, or any of the card
# programming features.

from PIL import Image
import numpy as np
import sys

def _mono(img):
    img = np.array(np.array(img) < 127,dtype='uint8')
    return np.flip(np.rot90(img))

def _ymc_sep(img):
    img = np.array(img)
    c = 255-img[:,:,0]
    m = 255-img[:,:,1]
    y = 255-img[:,:,2]
    return np.flip(np.rot90(y),0),np.flip(np.rot90(m),0),np.flip(np.rot90(c),0)

def _encode_compressed(buf):
    rawdata = buf.flatten()
    data = []
    #for c in rawdata:
    i = 0
    while i < len(rawdata):

        i += 1

    data = bytes(np.asarray(data, type='uint8'))
    data = data.replace(b'[', b'[[').replace(
          b'\x0d', b'[\x0d').replace(b'\x1b', b'[\x1b')
    return data

def _encode_uncompressed(buf):
    #return bytes(buf.flatten()).replace(b'[', b'[[').replace(
    #      b'\x0d', b'[\x0d').replace(b'\x1b', b'[\x1b')
    # switching to below eleiminated "command error" and now it syncs up
    return bytes(buf.flatten()).replace(b'[', b'Z').replace(
          b'\x0d', b'\x0e').replace(b'\x1b', b'\x1c')

def _encode_mono(buf):
    return bytes((255*buf).flatten())


class EPCL:
    K=3
    C=2
    M=1
    Y=0
    #def G(image, x, y):
    #    pref = b'\x1BG %d %d 10 %d %d 1\r\x1BZ'%(
    #                x, y, image.shape[0], image.shape[1]*image.shape[0])
    #
    #    return pref+_encode_mono(image)+b'\r'
    def G(image, x, y):
        data = [b'\x1BG %d %d 10 %d %d 1\r\x1BZ'%(
                    x, y, image.shape[0], image.shape[1]*image.shape[0])]


    def GS(image, buf, x, y):
        assert 0 <= buf <= 3
        data = b'\x1BGS %d 2 %d %d %d %d %s\r'%(
                buf, x, y, image.shape[0], image.shape[1],
                _encode_uncompressed(image)
                )
        return data
    def PS(image, buf=K):
        assert 0 <= buf <= 3
        assert image.shape == (646, 1030)
        data= b'\x1BPS %d 2 %s\r'%(buf,_encode_uncompressed(image)[:655350])
        #assert len(data) < 655360, len(data)
        return data
    #def G_Z(image, buf=):
    #    return '\x1BG %d %d %d %d %d %d\r\x1BZ%s\r'%()

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    black = Image.open(sys.argv[2])
    varnish = Image.open(sys.argv[3])
    of = open(sys.argv[4], 'wb')
    Y,M,C = _ymc_sep(image)
    K = _mono(black)
    V = _mono(varnish)
    print (Y.shape, M.shape, C.shape)
    print (K.shape, np.min(K), np.max(K), K.dtype)
    print (V.shape, np.min(V), np.max(V), V.dtype)

    of.write(b"\x1BF\r\x1BvF\r")
    of.write(b"\x1B$LD 0 0\r")
    of.write(b"\x1B$LD 0 1\r")
    of.write(b"\x1B$LD 0 2\r")

    # write colors
    SEP = [Y,M,C]
    x = 0
    while x < 1030:
        y = 0
        while y < 646:
            for bi,sepbuf in enumerate(SEP):
                of.write(EPCL.GS(np.flip(sepbuf[x:x+103,y:y+323],0), bi, x,y))
            y += 323
        x += 103


    # Write resin black
    of.write(b'\x1BG 0 0 0 81 1030 1\r')

    for n in range(1030):
        data = bytes(np.flip(np.packbits(K[1029-n], None, 'little').flatten()))
        data = data.replace(b'[', b'[[')
        data = data.replace(b'\r', b'[\r')
        data = data.replace(b'\x1b', b'[\x1b')
        of.write(b'\x1BO'+data+b'\r')


   


    
     # Write varnish
    of.write(b'\x1BvG 0 0 0 81 1030 1\r')

    for n in range(1030):
        data = bytes(np.flip(np.packbits(V[1029-n], None, 'little').flatten()))
        data = data.replace(b'[', b'[[')
        data = data.replace(b'\r', b'[\r')
        data = data.replace(b'\x1b', b'[\x1b')
        of.write(b'\x1BvO'+data+b'\r')
    
    
    of.write(b'\x1BIS 0\r\x1BIS 1\r\x1BIS 2\r\x1BI 10\r')
    of.write(b'\x1BIV 1\r\x1BMO\r')
