

1. `/report` calls out the admin. admin may be a phantomjs, or any headless browser, because it executes css.

I first tried an xss. I imagined `catchat.js` is a clue because of the `cleanupRoomFullOfBadPeople` function. but everything is filtered with `esc`. everything?! not really

```
ban(data) {
  if (data.name == localStorage.name) {
    document.cookie = 'banned=1; Path=/';
    sse.close();
    display(`You have been banned and from now on won't be able to receive and send messages.`);
  } else {
    display(`${esc(data.name)} was banned.<style>span[data-name^=${esc(data.name)}] { color: red; }</style>`);
  }
},
```

that means that when someone is banned, everyone will execute his name in css.

but how is that helpful with `esc`? well i tried everything on xss cheatsheets. then i tried if the admin really executes my code with a `background: url`

```
/name ]{}body{background:url(send?name=admin&msg=caca)}div[
```

Surprise. he does. but how do i get the cookie?

I tried
```
]{}span[data-secret]{background:url(send?name=admin&msg=yas)}div[
```

but he does not have it.

in `catchat.js` there's a clue

```
// Admin helper function. Invoke this to automate banning people in a misbehaving room.
// Note: the admin will already have their secret set in the cookie (it's a cookie with long expiration),
// so no need to deal with /secret and such when joining a room.
```

so he does have it in cookie. and if i run `/secret flag` i will get it in dom. but `new-flag` will override it.

2.
```
res.setHeader('Set-Cookie', 'flag=' + arg[1] + '; Path=/; Max-Age=31536000');
```
in server.js. it has no filter. so I can send `/secret plm;domain=google.com` and it wont set the flag to cookie. it will not rewrite the flag. but it will trigger `secret` message in frontend.

3.
i had to keep reporting `/report` so i could see my payload. I automated this step in `gen.js`
