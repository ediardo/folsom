(function() {

  'use strict';

  angular
    .module('folsom')
    .controller('resultsCtrl', controller);

  function controller($scope, apiService, $route, NgTableParams) {
    $scope.$route = $route;

    $scope.results = new NgTableParams({}, {
      getData: function(params) {
        return apiService.getResults()
          .success(function(response) {
            return response
          })
          .error(function(response) {
            $scope.flash = {
              alert_type: 'danger',
              message: response
            };
          });
      }
    });
  };

})();
