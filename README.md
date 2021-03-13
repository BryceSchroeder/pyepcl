# pyepcl

Experimental control of the Zebra P430i card printer on GNU/Linux or 
other similar UNIX-like OSes.
This just sends raster data to the printer; it doesn't use the 
printer's own built in barcode, text, vector graphics features.
Assumes a five-panel YMCKO ribbon, though it should be easily 
adaptable to monochrome or other ribbons, and it may work with other 
printers that also use the EPCL printer language. Note that Zebra 
printers have like four different languages so good luck figuring 
out which yours is, but this should include the following:
P205, P210, P310, P320, P420, P520, P720, the corresponding /i or /s 
models and the corresponding +10 models e.g. P430i which is what I used
to test it.

This might ruin your printer, ribbon, and cards, especially if it is 
used on a printer other than the P430i, because that is the only one
I have. It working on others is a theoretical possibility. I don't
promise that it will work.

It also does not use compression, so it is relatively slow. It still
takes under a minute to print a card, though, so for most purposes
it should be sufficient.

Your printing system (CUPS or whatever) should just be configured 
as if the card printer were a plain text printer, and turn off any
preprocessing that the printing system might do.

Usage: 
  epcl color.png resin-black.png varnish.png outputfile.txt
Note: resin and varnish images must be greyscale, not RGB or indexed
Black is the presence of resin black / varnish.
All images must be 1030 wide (X) and 646 pixels tall (Y).
Print in raw mode, e.g:
  lp -d P430i -o raw outputfile.txt
This doesn't use the card flipper, laminator, or any of the card
programming features.
