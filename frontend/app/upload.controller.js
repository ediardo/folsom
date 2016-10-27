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
