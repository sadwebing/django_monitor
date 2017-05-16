var TcbsApp = angular.module("TcbsApp",  ['ngAnimate', 'ui.router']);
TcbsApp.config(function ($stateProvider, $urlRouterProvider) {

    //$urlRouterProvider.when("", "mainnav");

    $urlRouterProvider.otherwise("/malfunction_all");
    $stateProvider
        .state("malfunction_all", {
            url:"/malfunction_all",
            templateUrl: "/malfunction/all"
        })
        .state("malfunction_op_history", {
            url:"/op_history",
            templateUrl: "/malfunction/op_history"
        })
        .state("tomcat_tomcat_url", {
            url:"/tomcat_url",
            templateUrl: "/tomcat/tomcat_url"
        })
        .state("tomcat_project", {
            url:"/tomcat_project",
            templateUrl: "/tomcat/project/"
        })
        .state("saltstack_command", {
            url:"/saltstack_command",
            templateUrl: "/saltstack/command"
        })
        .state("saltstack_restart", {
            url:"/saltstack_restart",
            templateUrl: "/saltstack/restart"
        })
        .state("saltstack_saltstack_id", {
            url:"/saltstack_id",
            templateUrl: "/saltstack/saltstack_id"
        })
});