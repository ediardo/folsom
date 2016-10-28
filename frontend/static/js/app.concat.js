(function() {
  'use strict';

  angular
    .module('folsom', ['ngRoute', 'ngCookies'])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/', {
          templateUrl: '/static/partials/index.html?anticache',
          controller: 'mainCtrl',
          requiredAuth: true
        })
        .when('/upload', {
          templateUrl: '/static/partials/upload.html?anticache=',
          controller: 'uploadCtrl',
          requiredAuth: true
        })
        .when('/login', {
          templateUrl: '/static/partials/login.html?anticache=',
          controller: 'loginCtrl'
        })

      $locationProvider.html5Mode({ enabled: true, requireBase: false });
    }]);

})();



(function() {
  'use strict';

  angular
    .module('folsom')
    .service('apiService', ['$http', function($http) {

      var baseUrl = '/';
      
      this.uploadFile = function(data) {
        return $http({
          method: 'POST',
          url: baseUrl + '/upload'
        });
      }


      this.loginUser = function(credentials) {
        console.log(JSON.stringify(credentials));
        return $http({
          method: 'POST',
          url: '/login',
          headers: { 'content-type' : 'application/json'},
          data: JSON.stringify(credentials)
        });
      }
    }]);

})();



(function() {

  angular
    .module('folsom')
    .controller('folsomCtrl',  controller);


  function controller($scope, apiService, $cookies, $location) {
    $scope.$on('$routeChangeStart', function(angularEvent, url) {
      console.log(url);
      if (url.requiredAuth && !$cookies.get('loggedin')) {
        $location.path('/login');
      } else {
        $scope.loggedIn = true;
        console.log('asda');
      }
    });

    $scope.logout = function() {
      $cookies.remove('loggedin');
      $scope.loggedIn = false;
      $location.path('/login');
    }
  };

})();


(function() {

  angular
    .module('folsom')
    .controller('loginCtrl',  controller);


  function controller($scope, apiService, $cookies, $rootScope, $location) {

    $scope.fakeLogin = function() {
      console.log('Attempting login')
      apiService.loginUser({
        username: $scope.username, 
        password: $scope.password
      }).then(function(response) {
        // ULTRA INSECURE LOGIN IF THE USER CHANGES COOKIE VALUE
        $cookies.put('loggedin', $scope.username);
        $rootScope.loggedIn = true;
        $location.path('/');
      }, function(response) {
        console.log('Bad Credentials'); 
      });
    };
  };

})();


(function() {

  angular
    .module('folsom')
    .controller('mainCtrl',  controller);

  function controller($scope) {
    console.log('main');
  };

})();


(function() {

  'use strict';

  angular
    .module('folsom')
    .controller('uploadCtrl', controller);

  function controller($scope, apiService) {

    $scope.processUpload = function() {
      console.log('upload1');
      apiService.uploadFile('a');
    }
    
  };

})();
