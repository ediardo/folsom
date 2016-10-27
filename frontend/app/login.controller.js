(function() {

  angular
    .module('folsom')
    .controller('loginCtrl',  controller);


  function controller($scope, apiService, $cookies, $rootScope, $location) {

    $scope.fakeLogin = function() {
      console.log('Attempting login')
      apiService.loginUser({
        username: $scope.username, 
        password: $scope.password
      }).then(function(response) {
        // ULTRA INSECURE LOGIN IF THE USER CHANGES COOKIE VALUE
        $cookies.put('loggedin', $scope.username);
        $rootScope.loggedIn = true;
        $location.path('/');
      }, function(response) {
        console.log('Bad Credentials'); 
      });
    };
  };

})();
