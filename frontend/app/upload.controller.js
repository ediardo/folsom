(function() {

  'use strict';

  angular
    .module('folsom')
    .controller('uploadCtrl', controller);

  function controller($scope, apiService, $route) {
    $scope.$route = $route;

    $scope.processUpload = function() {
      $scope.file = {}
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
