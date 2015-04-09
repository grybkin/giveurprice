/**
 * @fileoverview
 * Provides methods for the Give Your Price sample UI and interaction with the
 * Give Your Price API.
 *
 * @author danielholevoet@google.com (Dan Holevoet)
 */

/** google global namespace for Google projects. */
var google = google || {};

/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for AppEngine sample code. */
google.appengine.samples = google.appengine.samples || {};

/** hello namespace for this sample. */
google.appengine.samples.hello = google.appengine.samples.hello || {};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
google.appengine.samples.hello.CLIENT_ID =
    '361494477850-7qu3tdv4f3sl8ph3culmd3r5gt91d81f.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
google.appengine.samples.hello.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email';

/**
 * Whether or not the user is signed in.
 * @type {boolean}
 */
google.appengine.samples.hello.signedIn = false;

/**
 * Loads the application UI after the user has completed auth.
 */
google.appengine.samples.hello.userAuthed = function() {
  var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
    if (!resp.code) {
      google.appengine.samples.hello.signedIn = true;
      document.querySelector('#signinButton').textContent = 'Sign out';
      document.querySelector('#authedProduct').disabled = false;
    }
  });
};

/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
google.appengine.samples.hello.signin = function(mode, callback) {
  gapi.auth.authorize({client_id: google.appengine.samples.hello.CLIENT_ID,
      scope: google.appengine.samples.hello.SCOPES, immediate: mode},
      callback);
};

/**
 * Presents the user with the authorization popup.
 */
google.appengine.samples.hello.auth = function() {
  if (!google.appengine.samples.hello.signedIn) {
    google.appengine.samples.hello.signin(false,
        google.appengine.samples.hello.userAuthed);
  } else {
    google.appengine.samples.hello.signedIn = false;
    document.querySelector('#signinButton').textContent = 'Sign in';
    document.querySelector('#authedProduct').disabled = true;
  }
};

/**
 * Prints a Product to the Product log.
 * param {Object} Product Product to print.
 */
google.appengine.samples.hello.print = function(Product) {
  var element = document.createElement('div');
  element.classList.add('row');
  element.innerHTML = Product.message;
  document.querySelector('#outputLog').appendChild(element);
};

/**
 * Gets a numbered Product via the API.
 * @param {string} id ID of the Product.
 */
google.appengine.samples.hello.getProduct = function(id) {
  gapi.client.giveurprice.products.getProduct({'id': id}).execute(
      function(resp) {
        if (!resp.code) {
          google.appengine.samples.hello.print(resp);
        }
      });
};

/**
 * Lists products via the API.
 */
google.appengine.samples.hello.listProduct = function() {
  gapi.client.giveurprice.products.listProduct().execute(
      function(resp) {
        if (!resp.code) {
          resp.items = resp.items || [];
          for (var i = 0; i < resp.items.length; i++) {
            google.appengine.samples.hello.print(resp.items[i]);
          }
        }
      });
};

/**
 * Gets a Product a specified number of times.
 * @param {string} Product Product to repeat.
 * @param {string} count Number of times to repeat it.
 */
google.appengine.samples.hello.multiplyProduct = function(
    Product, times) {
  gapi.client.giveurprice.products.multiply({
      'message': Product,
      'times': times
    }).execute(function(resp) {
      if (!resp.code) {
        google.appengine.samples.hello.print(resp);
      }
    });
};

/**
 * Greets the current user via the API.
 */
google.appengine.samples.hello.authedProduct = function(id) {
  gapi.client.giveurprice.products.authed().execute(
      function(resp) {
        google.appengine.samples.hello.print(resp);
      });
};

/**
 * Enables the button callbacks in the UI.
 */
google.appengine.samples.hello.enableButtons = function() {
  var getProduct = document.querySelector('#getProduct');
  getProduct.addEventListener('click', function(e) {
    google.appengine.samples.hello.getProduct(
        document.querySelector('#id').value);
  });

  var listProduct = document.querySelector('#listProduct');
  listProduct.addEventListener('click',
      google.appengine.samples.hello.listProduct);

  var multiplyproducts = document.querySelector('#multiplyproducts');
  multiplyproducts.addEventListener('click', function(e) {
    google.appengine.samples.hello.multiplyProduct(
        document.querySelector('#Product').value,
        document.querySelector('#count').value);
  });

  var authedProduct = document.querySelector('#authedProduct');
  authedProduct.addEventListener('click',
      google.appengine.samples.hello.authedProduct);

  var signinButton = document.querySelector('#signinButton');
  signinButton.addEventListener('click', google.appengine.samples.hello.auth);
};

/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
google.appengine.samples.hello.init = function(apiRoot) {
  // Loads the OAuth and giveurprice APIs asynchronously, and triggers login
  // when they have completed.
  var apisToLoad;
  var callback = function() {
    if (--apisToLoad == 0) {
      google.appengine.samples.hello.enableButtons();
      google.appengine.samples.hello.signin(true,
          google.appengine.samples.hello.userAuthed);
    }
  }

  apisToLoad = 2; // must match number of calls to gapi.client.load()
  gapi.client.load('giveurprice', 'v1', callback, apiRoot);
  gapi.client.load('oauth2', 'v2', callback);
};
