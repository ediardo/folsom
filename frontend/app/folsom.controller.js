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
