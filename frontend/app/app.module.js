(function() {
  'use strict';

  angular
    .module('folsom', ['ngRoute'])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/', {
          templateUrl: '/static/partials/index.html',
          controller: 'mainCtrl'
        })
        .when('/upload', {
          templateUrl: '/static/partials/upload.html',
          controller: 'uploadCtrl'
        })
        .when('/login', {
          templateUrl: '/static/partials/login.html',
          controller: 'loginCtrl'
        })

      $locationProvider.html5Mode({ enabled: true, requireBase: false });
    }]);

})();

