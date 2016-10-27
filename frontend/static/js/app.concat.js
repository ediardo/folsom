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



(function() {

  angular
    .module('folsom')
    .controller('loginCtrl',  controller);


  function controller($scope) {

    $scope.fakeLogin = function() {
      console.log($scope.username);
      console.log($scope.password);
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
