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



(function() {
  'use strict'

  angular
    .module('folsom')
    .directive('flashMessage', function() {

      return {
        templateUrl: '/static/partials/flash.html'
      };

    })
    .directive('fileModel', ['$parse', function($parse) {
      return {
        restrict: 'A',
        link: function(scope, element, attrs) {
          var model = $parse(attrs.fileModel);
          var modelSetter = model.assign;
          element.bind('change', function() {
            console.log(model);

            console.log('changed');
            scope.$apply(function() {
              modelSetter(scope, element[0].files[0])
            });
          });
        }
      }
    }]);
})();


(function() {
  'use strict';

  angular
    .module('folsom')
    .service('apiService', ['$http', function($http) {

      var baseUrl = '/';
      
      this.uploadFile = function(file) {
        var formData = new FormData();
        for (var key in file) {
          formData.append(key, file[key]);
        }
        return $http.post('/upload', formData, {
          headers: { 'Content-Type': undefined }, 
          transformRequest: angular.identity
        });
      }

      this.loginUser = function(credentials) {
        return $http({
          method: 'POST',
          url: '/auth',
          headers: { 'content-type' : 'application/json'},
          data: JSON.stringify(credentials)
        });
      };

      this.getRecords = function() {
        return $http.get('/viewall');
      }

    }]);
})();



(function() {

  angular
    .module('folsom')
    .controller('folsomCtrl',  controller);


  //controller.$inject = ['NgTableParams'];

  function controller($scope, apiService, $cookies, $location, $route, NgTableParams) {
    $scope.$route = $route;

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

    $scope.tableParams = new NgTableParams({}, {
      getData: function(params) {
        return apiService.getRecords().then(function(response) {
          return response.data.message
        }, function(response) {

        });
      } 
    });
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
        user: $scope.user, 
        password: $scope.password
      }).success(function(response) {
        // ULTRA INSECURE LOGIN IF THE USER CHANGES COOKIE VALUE
        $cookies.put('loggedin', $scope.user);
        $rootScope.loggedIn = true;
        $location.path('/');
      })
      .error(function(response) {
        console.log(response);
        $scope.flash = {
          alert_type: 'danger',
          message: response.msg 
        };
      });
    };
  };

})();


(function() {

  'use strict';

  angular
    .module('folsom')
    .controller('resultsCtrl', controller);

  function controller($scope, apiService, $route) {
    $scope.$route = $route;

  };

})();


(function() {

  'use strict';

  angular
    .module('folsom')
    .controller('uploadCtrl', controller);

  function controller($scope, apiService, $route) {
    $scope.$route = $route;
    $scope.file = {};

    $scope.processUpload = function() {
      $scope.flash = {
        alert_type: 'info',
        message: 'Uploading your file now...'
      };
      console.log($scope.file);
      apiService.uploadFile($scope.file).then(function(response) {
        $scope.flash = {
          alert_type: 'success',
          message: 'Your file was uploaded successfully!'
        };
      }, function(response) {
        $scope.flash = {
          alert_type: 'danger',
          message: response.data.message 
        };
      });
    }
  };

})();
