// to compile JSX javascript to vanilla javascript for deploy:
// $ npm install -g react-tools
// $ cd email-subscriber
// $ jsx --watch demo/ public/

require.config({
  paths: {
    'vendor/react' : 'https://cdnjs.cloudflare.com/ajax/libs/react/0.13.2/react.min'
  }
});

// to allow crossdomain communication with mobile.nytimes.com
// Skip this in scoop.nyt.net previews, since it causes a crossdomain error.
if(!window.top && window.top.hostname && window.top.hostname.match(/nyt\.net$/)) {
  document.domain = 'nytimes.com';
}

define('nytint/email-subscriber',[
  'jquery/nyt',
  'underscore/nyt',
  'foundation/models/user-data',
  'vendor/react'
], function($, _, userData, React) {

  // Navigation overrides applied in mobile.nytimes.com iframes or in-app webviews
  // so that clicking links opens the new page in the parent frame rather than
  // loading the page in the tiny webview cell.
  var is_mobile = window.top.location.href.match(/mobile\.(stg\.)?nytimes\.com/);
  var is_iframe = window.top !== window.self;
  var is_embedded = window.location.href.match('.embedded.html');
  var has_nytapp_querystring = window.location.search.match('nytapp=embedded_webview');

  if((is_mobile && is_iframe) || is_embedded || has_nytapp_querystring) {
    $(document).on("click", "a", function(e) {
        e.preventDefault();
        var dest = $(e.currentTarget).attr('href');

        if (is_mobile && is_iframe) {
          window.top.open(dest, '_top');
        } else if (is_embedded || has_nytapp_querystring) {
          window.top.location = dest.replace(/http/, 'nytinteractive');
        }
    });
  }

  var NotifyForm = React.createClass({displayName: "NotifyForm",
    getInitialState: function() {
      return {
        status: 'initial', // 'initial', 'working', 'success'
        alreadySubscribed: false,
        lastError: null,
        subscriberEmail: null,
        optIn: this.props.optInValue !== null,
        isAttributeEmail: this.props.productCode.indexOf('attribute-') !== -1
      };
    },

    onButtonClick: function(data) {
      this.setState({ status: 'working' });
    },

    onSuccess: function(data) {
      this.setState({
        status: 'subscribed',
        lastError: null,
        subscriberEmail: data.email
      });

      var tagxSubmit = function(productCode) {
        TAGX.EventProxy.trigger('newsletter-signup-intent',
          {action:    'Click',
           module:    'newsletter-signup-int',
           eventName: 'subscribe',
           pgtype:    'subscriptionspage',
           version:   productCode,
           sourceApp: 'regilite-module'},
        'interactions');
      };
      if (typeof(TAGX) !== 'undefined' && !this.state.isAttributeEmail) {
        tagxSubmit(this.props.productCode);
      }

      if(typeof(localStorage) !== 'undefined' && localStorage) {
        localStorage.setItem(this.localStorageKey, 'subscribed');
      }
    },

    onError: function(data) {
      var response = data.responseText ? JSON.parse(data.responseText) : {};
      var errorMessage = response.error_message || this.props.text.errorMessage;
      this.setState({ lastError: errorMessage, status: 'initial' });
    },

    hideAsSubscribed: function() {
      this.setState({ alreadySubscribed: true, status: 'subscribed' });
      $(this.props.elementToHide).hide();
    },

    componentWillMount: function() {
      this.localStorageKey = 'nytint-email-subscriber:' + this.props.productCode;

      // Check if user is already subscribed, if so set module to "You've been subscribed".

      // If the subscribed flag is set in localStorage, consider user subscribed.
      // Note that it is possible user has unsubscribed through Member Center, which
      // will not be reflected in localStorage.
      if (typeof(localStorage) !== 'undefined' && localStorage && localStorage.getItem(this.localStorageKey) === 'subscribed') {
        this.hideAsSubscribed();

      // For logged-in users viewing a signup to a Paperboy email, check the Paperboy subscription set in NYT5 UserData.
      // If the user subscribed through some other means (another computer, via Member Center, etc.) also set subscribed state.
      } else if(!this.state.isAttributeEmail && userData.isLoggedIn() && _.contains(userData.getEmailSubscriptions(), this.props.productCode)) {
        this.hideAsSubscribed();
      }
    },

    componentDidMount: function() {
      // If we are in a NYT5 Interactive or some other type of embedded mobile webview,
      // load the AppCommunicator and invoke a resize. This ensures that the mobile web
      // or webview cell is sized appropriately.
      if($('html').hasClass('app-interactive') || has_nytapp_querystring) {
        require(['shared/interactive/instances/app-communicator'], function(AppCommunicator) {
          AppCommunicator.triggerResize();
        });
      }
    },

    handleOptinChange: function(event) {
      this.setState({ optIn: event.target.checked });
    },

    subscribe: function(payload) {
      payload.product_code = this.props.productCode;
      payload.auth_token = 'ByWeE-R9MfPXEdeksakyylmrv0hG3AbMSPGCvIeNPn8_gRaAkb3WcegJ9CeeElbTvLrW3zzhL6bMBrNnEYuGDA';

      if(this.state.optIn) {
        payload.opt_in = this.props.optInValue;
      }

      return $.ajax('https://www.nytimes.com/svc/int/email-subscriber/subscribe', {
        method: 'POST',
        data: payload,
        xhrFields: {
           withCredentials: true
        }
      }).done(this.onSuccess).fail(this.onError);
    },

    buildEmailPreferencesLink: function() {
      if(!this.state.isAttributeEmail && userData.isLoggedIn()) {
        return React.createElement("a", {href: "https://myaccount.nytimes.com/mem/email.html"}, this.props.text.emailPreferencesLinkText);
      } else {
        return null;
      }
    },

    render: function() {
      var loginClass = this.props.loggedIn ? 'user-logged-in' : 'user-logged-out';

      if(this.state.alreadySubscribed) {
        return (
          React.createElement("div", {className: loginClass, "data-status": this.state.status}, 
            React.createElement(Message, {type: "success"}, 
              this.props.text.alreadySubscribedMessage, React.createElement("br", null), 
              this.buildEmailPreferencesLink()
            )
          )
        );
      } else if(this.state.status == 'subscribed') {

        // Thanks must be templated as dangerouslySetInnerHTML since it includes a <span> around the username placeholder
        var thanksHTML = this.props.text.thanksMessage.replace('%email%', '<span class="email-address">' + this.state.subscriberEmail + '<span>');
        var thanksMarkup = { __html: thanksHTML };
        var thanksMessage = React.createElement("span", {dangerouslySetInnerHTML: thanksMarkup})

        return (
          React.createElement("div", {className: loginClass, "data-status": this.state.status}, 
            React.createElement(Message, {type: "success"}, 
              thanksMessage, React.createElement("br", null), 
              this.buildEmailPreferencesLink()
            )
          )
        );
      }

      var loggedInView = React.createElement(SubmitButton, {subscribe: this.subscribe, 
                                       status: this.state.status, 
                                       onButtonClick: this.onButtonClick, 
                                       text: this.props.text});

      var loggedOutView = React.createElement(EmailForm, {subscribe: this.subscribe, 
                                     status: this.state.status, 
                                     onButtonClick: this.onButtonClick, 
                                     text: this.props.text});

      var form = this.props.loggedIn ? loggedInView : loggedOutView;
      var error = this.state.lastError ? React.createElement(Message, {type: "error"}, this.state.lastError) : null;

      if(this.props.optInValue) {
        var optInMarkup = { __html: this.props.text.optIn };
        var optIn = React.createElement("div", {className: "optin"}, 
          React.createElement("input", {type: "checkbox", checked: this.state.optIn, onChange: this.handleOptinChange}), 
          React.createElement("span", {dangerouslySetInnerHTML: optInMarkup})
        );
      } else {
        var optIn = null;
      }

      return (
        React.createElement("div", {className: loginClass, "data-status": this.state.status}, 
          form, 
          optIn, 
          error
        )
      );
    }
  });

  var EmailForm = React.createClass({displayName: "EmailForm",
    getInitialState: function() {
      return {
        dirty: false,
        invalidEmail: false
      };
    },

    onKeyUp: function() {
     this.setState({ dirty: true });
    },

    onSubmit: function(event) {
      event.preventDefault();
      if (this.props.status == 'working') { return false; }

      this.props.onButtonClick();

      var email = $(this.refs.emailInput.getDOMNode()).val();
      var emailRegex = new RegExp("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", 'ig');
      var emailValidates = emailRegex.test(email);

      if (emailValidates) {this.setState({ invalidEmail: false });
        this.props.subscribe({ email: email });
      } else {
        this.setState({ invalidEmail: true });
      }
    },

    render: function() {
      var inputClassString = 'notify-email ';
      inputClassString += this.state.invalidEmail ? 'error' : '';
      inputClassString += this.state.dirty ? 'dirty' : '';

      return (
        React.createElement("form", {ref: "form", onSubmit: this.onSubmit, onKeyUp: this.onKeyUp}, 
          React.createElement("input", {className: inputClassString, required: true, type: "email", ref: "emailInput", placeholder: this.props.text.unregisteredPlaceholder, ref: "emailInput"}), 
          React.createElement("button", {className: "email-submit", className: "button"}, React.createElement("span", null, this.props.text.unregisteredButton))
        )
      );
    }
  });

  var SubmitButton = React.createClass({displayName: "SubmitButton",
    onSubmit: function() {
      if (this.props.status == 'working') { return false; }
      this.props.onButtonClick();
      this.props.subscribe({});
    },

    render: function() {
      var welcome;

      if(this.props.text.registeredWelcome) {
        var welcomeMessage = this.props.text.registeredWelcome.replace('%username%', '<span class="account-name">' + userData.getUserName() + '<span>');
        var markup = { __html: welcomeMessage };
        welcome = React.createElement("div", {dangerouslySetInnerHTML: markup})
      }

      return (
        React.createElement("div", null, 
          welcome, 
          React.createElement("button", {className: "notify-submit", className: "button", onClick: this.onSubmit}, React.createElement("span", null, this.props.text.registeredButton))
        )
      );
    }
  });

  var Message = React.createClass({displayName: "Message",
    render: function() {
      var classString = this.props.type !== 'success' ? 'error' : '';
      return React.createElement("div", {className: "messaging", className: classString}, this.props.children)
    }
  });

  var setup = function(opts) {
    var text = _.extend({
      unregisteredButton: 'Sign Up',
      unregisteredPlaceholder: 'Email address',
      registeredButton: 'Sign Up',
      alreadySubscribedMessage: 'You are already subscribed.',
      thanksMessage: 'You are subscribed as %email%.',
      emailPreferencesLinkText: 'Email Preferences',
      errorMessage: 'Error submitting, please try again.',
      optIn: ''
    }, opts.text);

    // This is not set as a default, but you can also provide a welcome message for registered users:
    // registeredWelcome: 'You are logged in as %username%.',

    // Backwards-compatible support for general buttonText option:
    if(opts.buttonText) {
      text.registeredButton   = opts.buttonText;
      text.unregisteredButton = opts.buttonText;
    }

    userData.ready(function() {
      React.render(
        React.createElement(NotifyForm, {loggedIn: userData.isLoggedIn(), 
                    productCode: opts.productCode, 
                    optInValue: opts.optInValue, 
                    elementToHide: opts.elementToHideOnSubscribe, 
                    text: text}),
        document.getElementById(opts.containerId)
      );
    });
  };

  return {
    setup: setup
  };

});