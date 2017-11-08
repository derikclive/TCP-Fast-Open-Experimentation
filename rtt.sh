for site in google.com youtube.com facebook.com baidu.com wikipedia.org yahoo.com google.co.in qq.com reddit.com taobao.com twitter.com amazon.com sohu.com google.co.jp tmall.com live.com vk.com instagram.com sina.com.cn jd.com weibo.com 360.cn google.de google.co.uk linkedin.com list.tmall.com google.fr google.ru google.com.br yandex.ru google.com.hk yahoo.co.jp netflix.com google.it t.co imgur.com google.es ebay.com onclkds.com ntd.tv bing.com pornhub.com msn.com microsoft.com hao123.com google.ca livejasmin.com alipay.com wordpress.com google.com.mx tumblr.com aliexpress.com twitch.tv mail.ru xvideos.com ok.ru stackoverflow.com imdb.com blogspot.com office.com amazon.co.jp pinterest.com github.com microsoftonline.com popads.net csdn.net google.com.tr wikia.com google.com.au diply.com whatsapp.com apple.com google.com.tw paypal.com xhamster.com youth.cn google.co.id detail.tmall.com gmw.cn google.pl tianya.cn adobe.com soso.com coccoc.com so.com bongacams.com txxx.com amazon.de porn555.com dropbox.com googleusercontent.com pixnet.net google.co.th amazon.in google.com.pk clicksgear.com google.com.eg bbc.co.uk craigslist.org google.com.sa thepiratebay.org google.com.ar china.com cnn.com bbc.com fc2.com soundcloud.com quora.com amazon.co.uk uptodown.com google.nl booking.com nytimes.com uptrend.com ask.com ettoday.net dailymotion.com naver.com rakuten.co.jp xnxx.com blastingnews.com savefrom.net adf.ly ebay.de nicovideo.jp detik.com amazonaws.com google.co.za google.co.ve espn.com vice.com blogger.com daikynguyenvn.com onlinesbi.com fbcdn.net stackexchange.com vimeo.com theguardian.com flipkart.com tribunnews.com gomovies.to google.com.ua salesforce.com chaturbate.com mozilla.org ebay.co.uk bet365.com buzzfeed.com spotify.com steamcommunity.com slideshare.net google.gr google.com.vn xinhuanet.com upornia.com popcash.net google.com.co google.com.sg globo.com chase.com google.co.kr avito.ru google.be google.se dailymail.co.uk mediafire.com douyu.com cnet.com uol.com.br google.com.ph indeed.com deviantart.com thewhizmarketing.com openload.co github.io wikihow.com google.az nih.gov 9gag.com rambler.ru washingtonpost.com google.cn zhihu.com twimg.com w3schools.com pinimg.com hclips.com google.at google.ro iwanttodeliver.com varzesh3.com huaban.com softonic.com steampowered.com etsy.com sogou.com google.com.ng babytree.com redtube.com lifebuzz.com force.com; do
  echo $site >> rtts.txt
  # -c count // stops sending after count ECHO_REQUEST packets
  # -W timeout // time to wait for a response in seconds
  # -i interval //wait interval seconds before sending each packet
  ping -c 4 -W 1 -i 0.2 'www.'$site | tail -1| awk '{print $4}' | cut -d '/' -f 2 >> rtts.txt  
  # { time -f%e wget --quiet $site -O /dev/null ; } 2>> rtts.txt

done
# https://stackoverflow.com/questions/9634915/extract-average-time-from-ping-c
# ping -c 4 www.stackoverflow.com | tail -1| awk '{print $4}' | cut -d '/' -f 2





