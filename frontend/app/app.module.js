(function() {
  'use strict';

  angular
    .module('folsom', ['ngRoute'])
    .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/', {
          templateUrl: '/static/partials/index.html?anticache',
          controller: 'mainCtrl'
        })
        .when('/upload', {
          templateUrl: '/static/partials/upload.html?anticache=',
          controller: 'uploadCtrl'
        })
        .when('/login', {
          templateUrl: '/static/partials/login.html?anticache=',
          controller: 'loginCtrl'
        })

      $locationProvider.html5Mode({ enabled: true, requireBase: false });
    }])
    .service('apiService', ['$http', function($http) {

      var baserUrl = '/';
      
      this.uploadFile = function(file) {
        console.log('uploading');
      }


    }]);

})();

