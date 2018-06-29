for i in `seq 1 60`; do
curl 'https://books.web.ctfcompetition.com/user/login' -H 'authority: books.web.ctfcompetition.com' -H 'cache-control: max-age=0' -H 'origin: https://books.web.ctfcompetition.com' -H 'upgrade-insecure-requests: 1' -H 'dnt: 1' -H 'content-type: application/x-www-form-urlencoded' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'referer: https://books.web.ctfcompetition.com/user/login' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,ro;q=0.8' --data 'name=nytr0gen1&password=qwerty' --compressed -vv -s 2>&1 | grep -i cookie
echo
echo '=========='
echo
done
