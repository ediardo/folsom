(function() {

  'use strict';

  angular
    .module('folsom')
    .controller('resultsCtrl', controller);

  function controller($scope, apiService, $route) {
    $scope.$route = $route;

  };

})();
