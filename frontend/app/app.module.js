(function() {
  'use strict';

  angular
    .module('folsom', ['ngRoute', 'ngCookies', 'ngTable'])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/', {
          templateUrl: '/static/partials/index.html?anticache',
          controller: 'folsomCtrl',
          requiredAuth: true,
          activeMenu: 'index'
        })
        .when('/results', {
          templateUrl: '/static/partials/results.html',
          controller: 'resultsCtrl',
          requiredAuth: true,
          activeMenu: 'results'
        })
        .when('/upload', {
          templateUrl: '/static/partials/upload.html?anticache=',
          controller: 'uploadCtrl',
          requiredAuth: true,
          activeMenu: 'upload'
        })
        .when('/login', {
          templateUrl: '/static/partials/login.html?anticache=',
          controller: 'loginCtrl',
          activeMenu: 'login'
        })

      $locationProvider.html5Mode({ enabled: true, requireBase: false });
    }]);

})();

