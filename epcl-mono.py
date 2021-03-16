#!/usr/bin/env python3
# PyEPCL - Partial Python3 implementation of the EPCL 
# This file may be used under the terms of the GNU Lesser
# General Public License version 3 as published by the Free Software
# Foundation and appearing in the file LICENSE.LGPLv3 included in the
# packaging of this file.  Please review the following information to
# ensure the GNU Lesser General Public License version 3 requirements
# will be met: https://www.gnu.org/licenses/lgpl.html.
#
# This version is for use with a mono ribbon, e.g. just resin black, 
# or one of the third-party UV only ribbons you can get from China.
# Use: epcl mono.png outputfile.txt
# Note: the mono.png image must be greyscale, not RGB or indexed
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
    black = Image.open(sys.argv[1])
    of = open(sys.argv[2], 'wb')
    K = _mono(black)
    print (K.shape, np.min(K), np.max(K), K.dtype)

    of.write(b"\x1BF\r\x1BvF\r")
    of.write(b"\x1B$LD 0 0\r")
    of.write(b"\x1B$LD 0 1\r")
    of.write(b"\x1B$LD 0 2\r")

    # Write resin black
    of.write(b'\x1BG 0 0 0 81 1030 1\r')

    for n in range(1030):
        data = bytes(np.flip(np.packbits(K[1029-n], None, 'little').flatten()))
        data = data.replace(b'[', b'[[')
        data = data.replace(b'\r', b'[\r')
        data = data.replace(b'\x1b', b'[\x1b')
        of.write(b'\x1BO'+data+b'\r')


   


    
    of.write(b'\x1BI 10\r')
    of.write(b'\x1BMO\r')
