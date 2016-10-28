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
