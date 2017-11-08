(function() {
  var creativeDefinition = {
    customScriptUrl: '',
    isDynamic: false,
    delayedImpression: false,
    standardEventIds: {
      DISPLAY_TIMER: '72',
      INTERACTION_TIMER: '73',
      INTERACTIVE_IMPRESSION: '74',
      MANUAL_CLOSE: '75',
      BACKUP_IMAGE_IMPRESSION: '76',
      EXPAND_TIMER: '77',
      FULL_SCREEN: '78',
      VIDEO_PLAY: '79',
      VIDEO_VIEW_TIMER: '80',
      VIDEO_COMPLETE: '81',
      VIDEO_INTERACTION: '82',
      VIDEO_PAUSE: '83',
      VIDEO_MUTE: '84',
      VIDEO_REPLAY: '85',
      VIDEO_MIDPOINT: '86',
      VIDEO_STOP: '87',
      VIDEO_UNMUTE: '88',
      DYNAMIC_CREATIVE_IMPRESSION: '',
      HTML5_CREATIVE_IMPRESSION: ''
    },
    exitEvents: [
      {
        name: 'logo',
        reportingId: '22763306',
        url: 'https://bs.serving-sys.com/serving/adServer.bs?cn\x3dtrd\x26mc\x3dclick\x26pli\x3d21397318\x26PluID\x3d0\x26ord\x3d%%CACHEBUSTER%%',
        targetWindow: '_top',
        windowProperties: ''
      }
    ],
    timerEvents: [
    ],
    counterEvents: [
      {
        name: 'see-more',
        reportingId: '22963946',
        videoData: null
      },
      {
        name: 'slot1',
        reportingId: '22762106',
        videoData: null
      },
      {
        name: 'slot2',
        reportingId: '22762346',
        videoData: null
      },
      {
        name: 'slot3',
        reportingId: '22763066',
        videoData: null
      },
      {
        name: 'slot4',
        reportingId: '22929386',
        videoData: null
      },
      {
        name: 'slot5',
        reportingId: '22972106',
        videoData: null
      }
    ],
    childFiles: [
      {
        name: 'ajax-loader.gif',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/img/ajax-loader.gif',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'see-more-articles.png',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/img/see-more-articles.png',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'ups-module-header.png',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/img/ups-module-header.png',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'main.css',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/css/main.css',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'normalize.min.css',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/css/normalize.min.css',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'jquery-ajaxtransport-xdomainrequest.js',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/js/jquery-ajaxtransport-xdomainrequest.js',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'main.js',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/js/main.js',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'backup.png',
        url: '/ads/richmedia/studio/pv2/60204972/20170517125756141/img/backup.png',
        isVideo: false,
        transcodeInformation: null
      }
    ],
    videoFiles: [
    ],
    videoEntries: [
    ],
    primaryAssets: [
      {
        id: '61721707',
        artworkType: 'HTML5',
        displayType: 'BANNER',
        width: '300',
        height: '1050',
        servingPath: '/ads/richmedia/studio/pv2/60204972/20170517125756141/index.html',
        zIndex: '1000000',
        customCss: '',
        flashArtworkTypeData: null,
        htmlArtworkTypeData: {
          isTransparent: false,
          sdkVersion: '01_169' // Duplicating sdk version in subsequent field as version format not the same.
        },
        floatingDisplayTypeData: null,
        expandingDisplayTypeData: null,
        imageGalleryTypeData: null,
        pageSettings:null,
layoutsConfig: null,
layoutsApi: null
      }
    ]
  }
  var rendererDisplayType = '';
  rendererDisplayType += 'html_';
  var rendererFormat = 'inpage';
  var rendererName = rendererDisplayType + rendererFormat;

  var creativeId = '120815185946';
  var adId = '0';
  var templateVersion = '200_189';
  var studioObjects = window['studioV2'] = window['studioV2'] || {};
  var creativeObjects = studioObjects['creatives'] = studioObjects['creatives'] || {};
  var creativeKey = [creativeId, adId].join('_');
  var creative = creativeObjects[creativeKey] = creativeObjects[creativeKey] || {};
  creative['creativeDefinition'] = creativeDefinition;
  var adResponses = creative['adResponses'] || [];
  for (var i = 0; i < adResponses.length; i++) {
    adResponses[i].creativeDto && adResponses[i].creativeDto.csiEvents &&
        (adResponses[i].creativeDto.csiEvents['pe'] =
            adResponses[i].creativeDto.csiEvents['pe'] || (+new Date));
  }
  var loadedLibraries = studioObjects['loadedLibraries'] = studioObjects['loadedLibraries'] || {};
  var versionedLibrary = loadedLibraries[templateVersion] = loadedLibraries[templateVersion] || {};
  var typedLibrary = versionedLibrary[rendererName] = versionedLibrary[rendererName] || {};
  if (typedLibrary['bootstrap']) {
    typedLibrary.bootstrap();
  }
})();
