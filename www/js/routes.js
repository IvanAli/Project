angular.module('app.routes', [])

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider
    

      .state('menu.show_graph', {
    url: '/show_graph',
    params:{
      name:null,
      lastname:null
    },
    views: {
      'side-menu21': {
        templateUrl: 'templates/show_graph.html',
        controller: 'show_graphCtrl'
      }
    }
  })

  .state('menu.show_induced_subgraph', {
    url: '/show_induced_subgraph',
    views: {
      'side-menu21': {
        templateUrl: 'templates/show_induced_subgraph.html',
        controller: 'show_induced_subgraphCtrl'
      }
    }
  })

  .state('menu.show_shortest_path', {
    url: '/show_shortest_path',
    views: {
      'side-menu21': {
        templateUrl: 'templates/show_shortest_path.html',
        controller: 'show_shortest_pathCtrl'
      }
    }
  })

  .state('menu', {
    url: '/side-menu21',
    templateUrl: 'templates/menu.html',
    controller: 'menuCtrl'
  })

  .state('menu.theFriendshipNetwork', {
    url: '/welcome',
    views: {
      'side-menu21': {
        templateUrl: 'templates/theFriendshipNetwork.html',
        controller: 'theFriendshipNetworkCtrl'
      }
    }
  })

$urlRouterProvider.otherwise('/side-menu21/welcome')


});