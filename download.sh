dir=`pwd`

rm -rf webpages
mkdir webpages
#chmod 0777 webpages
cd webpages


function PageDownload() {
  #Remove any existing pages
  rm -rf $1
  mkdir $1
  #chmod 0777 $1
  cd $1
  #-H - for recursive reteival across multiple hosts, -p - to download all the requisites to display the pages
  # --user-agent - It is used since some pages like amazon give Service Unavailable Error while using wget as the user agent,so we use web brosers like mozilla or chorime as the agent
  wget -Hp --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36" -e robots=off -v  $2

  #find all the files in the current directory and comress it to the maxminum extent possible and encode it using openssl to have a SSL
  for i in `find . -type f`; do gzip -9 <$i >/tmp/tmp; y=`stat -c %s /tmp/tmp`; openssl rand $y -out $i; done

  cd ..
}

PageDownload amazon http://www.amazon.com
PageDownload nytimes http://www.nytimes.com
PageDownload wsj http://www.wsj.com
PageDownload wikipedia http://en.wikipedia.org/wiki/Transmission_Control_Protocol

cd $dir
