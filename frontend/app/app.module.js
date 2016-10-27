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

