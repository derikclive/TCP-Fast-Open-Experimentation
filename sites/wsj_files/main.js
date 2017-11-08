window.onload = function() {
  if (Enabler.isInitialized()) {
    adVisible();
  } else {
    Enabler.addEventListener(studio.events.StudioEvent.INIT, adVisible);
  }
};

function adVisible() {
  var json, title, article, ord;
  // CIU - WP API CALL
  // json = '//wsjcsbucket.s3.amazonaws.com/feeds/json/86407_ups/86407-ups-ciu-migrated-feed.js';
  json = '//d885pvmm0z6oe.cloudfront.net/feeds/json/86407_ups/86407-ups-ciu-migrated-feed.js?ord=';
  ord = Math.random() * 10000000000000000;
  // DO NOT TOUCH ANY CODE BELOW
  json = json + ord;

  $.getJSON(json, function(data) {
    initCIU(data);
  });
}

function initCIU(data) {
  var articleLength = 5;
  // RUN OF SITE TRACKING INFO
  var mod = "hpto_1";
  var utm_source = mod;
  var utm_medium = "WSJ";
  var utm_content = "300x1050";
  var utm_campaign = "86407";
  var trackingInfo = "/?mod=" + mod + "&utm_source=" + utm_source + "&utm_medium=" + utm_medium + "&utm_content=" + utm_content + "&utm_campaign=" + utm_campaign;
  var html = '';
  var obj = shuffle(data.posts);

  for (var i = 0; i < articleLength; i++) {
    var title = obj[i].title;
    var wpUrl = obj[i].url;
    var slug = obj[i].slug;
    var hero = obj[i].article_thumbnail;
    hero = hero.replace('http', 'https');
    var snippet = obj[i].snippet.substring(0, 101); // takes first 100 characters.
    snippet = respectFullWords(snippet);
    //===========================================
    var url = slug + trackingInfo;
    //===========================================
    // first article-slot (i = 0)
    if (i === 0) {
      html += '<div data-href="' + url + '" data-slot="slot' + (i + 1) + '" class="article-slot">';
      html += '<img class="first-image-slot" src="' + hero + '" height="200">';
      html += '<div class="first-article-title article-title">' + title + '</div>';
      html += '<div class="first-snippet snippet">' + snippet + '...<div class="read-more-block"><span class="read-more"> More </span><span class="arrows">>></span></div></div></div>';
      html += '<div class="border"></div>';
      continue;
    } else if (i > 0) {
      html += '<div data-href="' + url + '" data-slot="slot' + i + '" class="article-slot">';
      html += '<img class="image-slot" src="' + hero + '" height="75">';
      html += '<div class="article-title">' + title + '</div>';
      html += '<div class="snippet">' + snippet + '...<span class="read-more"> More </span><span class="arrows">>></span></div></div>';
      html += '<div class="border"></div>';
    }

  }
  html += '<img id="see-more" src="img/see-more-articles.png">';
  $('#article-zone').hide().html(html).fadeIn(500);
  $('#loader').fadeOut(200);
  $('.border').last().remove();

  centerArticles();
  // titles underline on over
  $('.article-slot').on('hover', function() {
    $(this).find($('.article-title')).toggleClass('underline');
  });
  // link on click event
  $('.article-slot').on('click', function() {
    var slot = $(this).data("slot");
    var permalink = $(this).data("href");
    Enabler.counter(slot, true);
    top.location.href = permalink;
  });
  // logo exit
  $('.main-container').on('click', '#logo', function() {
    Enabler.exit('logo');
  });

  // 'see more articles' event handler fxn
  $("#see-more").on('click', function() {
    $("#article-zone").empty();
    adVisible();
    Enabler.counter("see-more", true);
  });

  //Sets Native CIU events in DFP
  var set_enabler_events = function() {
    Enabler.exit("logo");
    Enabler.counter("slot1", true);
    Enabler.counter("slot2", true);
    Enabler.counter("slot3", true);
    Enabler.counter("slot4", true);
    Enabler.counter("slot5", true);
    Enabler.counter("see-more", true);
  };
}

// fisher yates
function shuffle(array) {
  var m = array.length,
    t, i;

  // While there remain elements to shuffle…
  while (m) {

    // Pick a remaining element…
    i = Math.floor(Math.random() * m--);

    // And swap it with the current element.
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }

  return array;
}

function centerArticles() {
  var totalAvailableHeight = $('.main-container').height() - $('#logo').height() - $("#see-more").height() - $('.wsjcs-bottom-disclaimer').height();
  var articleHeight = $('#article-zone').height();
  var leftoverHeight = totalAvailableHeight - articleHeight;
  var margin = (leftoverHeight / 10); // excludes first article slot margin-top
  if (margin > 0) {
    $.each($('.article-slot'), function() {
      $(this).css('padding-top', margin);
      $(this).css('padding-bottom', margin);
    });
  }
  $(".article-slot").first().css('padding-top', 6);
}

function respectFullWords(snippet) {
  return snippet.substr(0, Math.min(snippet.length, snippet.lastIndexOf(" ")));
}
