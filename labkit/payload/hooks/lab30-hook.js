Java.perform(function () {
  const Auth = Java.use('com.BugBazaar.controller.UserAuthSave');
  const getPasscode = Auth.getpasscode.overload();
  getPasscode.implementation = function () {
    console.log('[lab30] getpasscode called; substituting lab value');
    return '0000';
  };
  console.log('[lab30] hook installed');
});
