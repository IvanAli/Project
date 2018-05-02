angular.module('app.controllers', [])
  
.controller('pageCtrl', ['$scope', '$stateParams', '$http', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams,$http) {

  $scope.mdl = {};

  $scope.getPath = function(){

    source_id = $scope.mdl.source;
    sink_id = $scope.mdl.destination;
    url = "http://localhost:5000/shortest_path?source="+source_id+"&target="+sink_id;
    
    $http.get(url).then(function(response){
    $scope.path = response.data.name;

    }, function(error) {
      alert("Unable to retrieve a path");
    });

  };

}])
   
.controller('page2Ctrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {

  $scope.appears = $stateParams.appears;

}])


.controller('show_graphCtrl', ['$scope', '$stateParams', '$http',
function ($scope, $stateParams, $http) {
  $scope.$on("$ionicView.loaded", function() {
    // First make request data (should put all of this in a new fun)
    url = "http://localhost:5000/whole_graph";
    $http.get(url).then(function(response) {
      var DIR = '../img/';
      var nodes = [];
      var edges = [];
      // Add nodes and edges to list
      cnt = 0
      for (var key in response.data) {
        if (response.data.hasOwnProperty(key)) {
          console.log("pushing node " + cnt);
          cnt++;
          nodes.push({
            id: parseInt(key), 
            shape: 'circularImage', 
            image: DIR + response.data[key]["photo_filename"],
            brokenImage: DIR + 'missing_image.png',
            label: response.data[key]["name"]
          });
          for (var j = 0; j < response.data[key]["friends"].length; j++) {
            var friend_id = response.data[key]["friends"][j];
            edges.push({from: parseInt(key), to: parseInt(friend_id)});
          }
        }
      }
      // create a network
      var container = document.getElementById('mynetwork');
      var data = {
        nodes: nodes,
        edges: edges
      };
      var options = {
        nodes: {
          borderWidth: 1,
          size: 5,
          color: {
            border: '#222222',
            background: '#666666'
          },
          font:{color:'#eeeeee'}
        },
        edges: {
          color: 'lightgray'
        }
      };
      network = new vis.Network(container, data, options);
    });
  });

}])
 
.controller('show_shortest_pathCtrl', ['$scope', '$stateParams', '$http',
function ($scope, $stateParams, $http) {
  //   $scope.$on("$ionicView.loaded", function() {
  $scope.model = {};

  $scope.getShortestPath = function() {
    // First make request data (should put all of this in a new fun)
    source_id = $scope.model.source_id;
    target_id = $scope.model.target_id;
    url = "http://localhost:5000/shortest_path?source=" + source_id + "&target=" + target_id;
    $http.get(url).then(function(response) {
      var DIR = '../img/';
      var nodes = [];
      var edges = [];
      // Add nodes to list
      for (var i = 0; i < response.data.length; i++) {
        nodes.push({
          id: response.data[i]["id"], 
          shape: 'circularImage', 
          image: DIR + response.data[i]["photo_filename"],
          brokenImage: DIR + 'missing_image.png',
          label: response.data[i]["name"]
        });
      }
      // Add edges to list
      for (var i = 0; i + 1 < response.data.length; i++) {
        edges.push({from: response.data[i]["id"], to: response.data[i + 1]["id"]});
      }
      // create a network
      var container = document.getElementById('mynetwork');
      var data = {
        nodes: nodes,
        edges: edges
      };
      var options = {
        nodes: {
          borderWidth: 4,
          size: 30,
          color: {
            border: '#222222',
            background: '#666666'
          },
          font:{color:'#eeeeee'}
        },
        edges: {
          color: 'lightgray'
        }
      };
      network = new vis.Network(container, data, options);
    });
  };

}])
 
 