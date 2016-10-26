(function() {

  angular
    .module('folsom')
    .controller('loginCtrl',  controller);


  function controller($scope) {

    $scope.fakeLogin = function() {
      console.log($scope.username);
      console.log($scope.password);
    };
  };

})();
