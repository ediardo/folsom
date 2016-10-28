(function() {
  'use strict';

  angular
    .module('folsom')
    .service('apiService', ['$http', function($http) {

      var baseUrl = '/';
      
      this.uploadFile = function(file) {
        var formData = new FormData()
        formData.append('file', file)
        return $http.post('/upload', formData, {
          headers: { 'Content-Type': undefined }, 
          transformRequest: angular.identity
        });
      }


      this.loginUser = function(credentials) {
        return $http({
          method: 'POST',
          url: '/login',
          headers: { 'content-type' : 'application/json'},
          data: JSON.stringify(credentials)
        });
      };

      this.getRecords = function() {
        return $http.get('/viewall');
      }

    }]);

})();

