const http = require('http');
const express = require('express');
const cookieParser = require('cookie-parser')

const app = express();
app.set('etag', false);
app.use(cookieParser());

// Check if banned
app.use(function(req, res, next) {
  if (req.cookies.banned) {
    res.sendStatus(403);
    res.end();
  } else {
    next();
  }
});

// let roomPath = '/room/:room([0-9a-f-]{36})';
app.get('/', function(req, res) {
  console.log(req.headers);
  console.log(req.headers.host);
});

app.listen(8080);
