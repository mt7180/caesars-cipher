# caesars-cipher

command line tool to encode a text by caesars cipher as explained here:
https://en.wikipedia.org/wiki/Caesar_cipher

### Usage: python caesar_cipher.py "text" key
parameters:
- text   : text to be encoded
- key    : cyclical shift of each letter by "key"-number of letters in the alphabet

e.g. python caesar_cipher.py "This is a text" 26-3