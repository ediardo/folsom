(function() {

  angular
    .module('folsom')
    .controller('folsomCtrl',  controller);


  function controller($scope, apiService, $cookies, $location) {
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
  };

})();
