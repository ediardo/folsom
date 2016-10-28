(function() {
  'use strict'

  angular
    .module('folsom')
    .directive('flashMessage', function() {

      return {
        templateUrl: '/static/partials/flash.html'
      };

    })
    .directive('fileModel', ['$parse', function($parse) {
      return {
        restrict: 'A',
        link: function(scope, element, attrs) {
          var model = $parse(attrs.fileModel);
          var modelSetter = model.assign;
          element.bind('change', function() {
            console.log(model);

            console.log('changed');
            scope.$apply(function() {
              modelSetter(scope, element[0].files[0])
            });
          });
        }
      }
    }]);
})();
