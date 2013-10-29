'use strict';

describe('Service: authRetryQueue', function () {

  // load the service's module
  beforeEach(module('clientApp'));

  // instantiate service
  var authRetryQueue;
  beforeEach(inject(function (_authRetryQueue_) {
    authRetryQueue = _authRetryQueue_;
  }));

  it('should do something', function () {
    expect(!!authRetryQueue).toBe(true);
  });

});
