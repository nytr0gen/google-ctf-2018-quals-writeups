const express = require('express')
const cookieParser = require('cookie-parser')
const bwt = require('../lib/bwt')('testkey');
const crypto = require('crypto');

const router = express.Router();
router.use(cookieParser());

function h(s) {
    const hash = crypto.createHash('sha256');
    hash.update(s+'');
    return hash.digest('hex');
}

function authRequired(req, res, next) {
  if (!req.user) {
    return res.redirect('/user/login');
  } else if (!req.cookies.auth) {
      res.cookie('auth', bwt.encode(req.user));
  }
  next();
}

function addTemplateVariables(req, res, next) {
  res.locals.profile = req.user;
  next();
}

function logout(req, res, next) {
    res.clearCookie('auth');
    next();
}

router.use((req, res, next) => {
    if (req.cookies.auth) {
        let user = bwt.decode(req.cookies.auth);
        if (user)
            req.user = user;
    }
    next();
});


module.exports = {
    required: authRequired,
    router,
    template: addTemplateVariables,
    logout
}
