angular.module('app.routes', [])

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider
    

      .state('page', {
    url: '/page1',
    params:{
      path:null,
      appears:null
    },
    templateUrl: 'templates/page.html',
    controller: 'pageCtrl'
  })

  .state('page2', {
    url: '/page2',
    params:{

      appears:null // is the list of boolean permiting the apparition of the avatars in page2 with the ng-if
    },
    templateUrl: 'templates/page2.html',
    controller: 'page2Ctrl'
  })

  .state('show_graph', {
    url: '/show_graph',
    templateUrl: 'templates/show_graph.html',
    controller: 'show_graphCtrl'
  })

  .state('show_shortest_path', {
    url: '/show_shortest_path',
    templateUrl: 'templates/show_shortest_path.html',
    controller: 'show_shortest_pathCtrl'
  })

$urlRouterProvider.otherwise('/page1')


});