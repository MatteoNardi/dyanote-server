'use strict';

angular.module('clientApp')
  .factory('authFailureInterceptor', ['$q', '$injector', 'authRetryQueue', function authFailureInterceptor ($q, $injector, queue) {
    return {
      'responseError': function (request) {
        // do something on error
        if (request.status === 401) {
          var promise = queue.pushRetryFn('unauthorized-server', function retryRequest () {
            return $injector.get('$http')(request.config);
          });
          return promise;
        }
        return $q.reject(request);
      }
    }
  }])
  .config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('authFailureInterceptor');
  }]);
