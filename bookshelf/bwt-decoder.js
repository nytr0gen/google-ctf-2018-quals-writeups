'strict';

const crypto = require('crypto');

function pint(n) {
    let b = new Buffer(4)
    b.writeInt32LE(n)
    return b
}

function encode(o) {
    let b = new Buffer(0)

    for (let k in o) {
        let v = o[k]

        b = Buffer.concat([b, pint(k.length), Buffer.from(k)])

        switch(typeof v) {
        case "string":
            b = Buffer.concat([b, Buffer.from([1]), pint(Buffer.byteLength(v)), Buffer.from(v.toLowerCase())])
            break
        case 'number':
            b = Buffer.concat([b, Buffer.from([2]), pint(v)])
            break
        default:
            b = Buffer.concat([b, Buffer.from([0])])
            break
        }
    }

    b = b.toString('base64')

    return b
}

function decode(b) {
    let o = {}
    let i = 0
    b = new Buffer(b, 'base64')

    while (i < b.length) {
        n = b.readUInt32LE(i), i += 4
        k = b.toString('utf8', i, i+n), i += n
        t = b.readUInt8(i), i += 1

        console.log(k, n);

        switch(t) {
        case 1:
            n = b.readUInt32LE(i), i += 4
            v = b.toString('utf8', i, i+n), i += n
            o[k] = v
            break
        case 2:
            n = b.readUInt32LE(i), i += 4
            o[k] = n
            break
        default:
            break
        }
    }
    return o
}

var encodeNP = function(s){
    var hex, c;
    var result = '';
    for (var i = 0; i < s.length; i++) {
        c = s[i];
        if (c >= 32 && c <= 126) {
            result += String.fromCharCode(c);
        } else {
            hex = c.toString(16);
            result += '\\u' + ('000'+hex).slice(-4);
        }
    }

    return result;
}

const plm = process.argv[2];
console.log(encodeNP(new Buffer(plm, 'base64')));
console.log(decode(plm));
