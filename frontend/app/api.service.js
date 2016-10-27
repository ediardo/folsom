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

