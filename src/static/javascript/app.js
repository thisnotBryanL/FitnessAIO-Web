(function () {

    var app = angular.module('app', [
        //'ui.router', 
        'ui.bootstrap',
        'ngStorage',
    ]);

    app.run(function () {
        console.log("app run");
    });

    //app.config(function($stateProvider, $urlRouterProvider) {
    app.config(function () {
        console.log("app config");

        //$urlRouterProvider.otherwise('/home');
    });

})();