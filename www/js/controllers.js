// var autocomplete = angular.module('ion-autocomplete', []);
angular.module('app.controllers', [])

  
.controller('show_graphCtrl', ['$scope', '$stateParams', '$http',
function ($scope, $stateParams, $http) {
  $scope.name = $stateParams.name;
  $scope.lastname = $stateParams.lastname;
  getRank = function(value) {
    if (value < 0.1) {
      return "#808080";
    }
    if (value < 0.2) {
      return "#469751";
    }
    if (value < 0.3) {
      return "#33A992";
    }
    if (value < 0.4) {
      return "#3C2BE2";
    }
    if (value < 0.6) {
      return "#8F2D8B";
    }
    if (value < 0.7) {
      return "#EBA246";
    }
    return "#B62A3C";
  };
  $scope.$on("$ionicView.loaded", function() {
    // First make request data (should put all of this in a new fun)
    $http.get("http://ec2-18-144-6-174.us-west-1.compute.amazonaws.com:5000/get_user_id?name="+$scope.name).then(function(response2){
      var userId= response2.data;
      url = "http://ec2-18-144-6-174.us-west-1.compute.amazonaws.com:5000/induced_subgraph?root=" + userId + "&limit=" + 2;
      $http.get(url).then(function(response) {
        var DIR = '../img/';
        var nodes = [];
        var edges = [];
        // Add nodes and edges to list
        cnt = 0
        for (var key in response.data) {
          if (response.data.hasOwnProperty(key)) {
            // console.log("pushing node " + cnt);
            cnt++;
            nodes.push({
              id: parseInt(key), 
            shape: 'circularImage', 
            image: DIR + response.data[key]["photo_filename"],
            brokenImage: DIR + 'missing_image.png',
            label: response.data[key]["name"],
            color: {
              border: getRank(response.data[key]["closeness"])
            },
            font: {
              color: '#ffffff'
            },
            size: 15 + 25 * response.data[key]["vertex_betweenness"],
            borderWidth: 3 + 3 * response.data[key]["articulation"],
            borderWidthSelected: 5 + 3 * response.data[key]["articulation"],
            title: "<textarea rows='6' cols='100'>"+"Aprox "+response.data[key]["vertex_betweenness"].toString()+" people can use you to know others\n" +  "You are the core friend of aprox: "+ response.data[key]["closeness"].toString()+" people"   + "\n If you dissapear,"+ (response.data[key]["local_clustering"]+1)+" people would never meet!" +"</textarea>"
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
        options={};
        network = new vis.Network(container, data, options);
      });
    });
  });

}])
   
.controller('show_induced_subgraphCtrl', ['$scope', '$stateParams', '$http',
function ($scope, $stateParams, $http) {
  $scope.model = {};
  
  getRank = function(value) {
    if (value < 0.1) {
      return "#808080";
    }
    if (value < 0.2) {
      return "#469751";
    }
    if (value < 0.3) {
      return "#33A992";
    }
    if (value < 0.4) {
      return "#3C2BE2";
    }
    if (value < 0.6) {
      return "#8F2D8B";
    }
    if (value < 0.7) {
      return "#EBA246";
    }
    return "#B62A3C";
  };

  // get the induced subgraph starting from some vertex for some given limit depth
  $scope.getInducedSubgraph = function() {
    // First make request data (should put all of this in a new fun)
    root_id = $scope.model.root_id;
    limit = $scope.model.limit;
    url = "http://ec2-18-144-6-174.us-west-1.compute.amazonaws.com:5000/induced_subgraph?root=" + root_id + "&limit=" + limit;
    $http.get(url).then(function(response) {
      var DIR = '../img/';
      var nodes = [];
      var edges = [];
      console.log("response received");
      // Add nodes and edges to list
      cnt = 0
      for (var key in response.data) {
        if (response.data.hasOwnProperty(key)) {
          nodes.push({
            id: parseInt(key), 
            shape: 'circularImage', 
            image: DIR + response.data[key]["photo_filename"],
            brokenImage: DIR + 'missing_image.png',
            label: response.data[key]["name"],
            color: {
              border: getRank(response.data[key]["closeness"])
            },
            font: {
              color: '#ffffff'
            },
            size: 15 + 25 * response.data[key]["vertex_betweenness"],
            borderWidth: 3 + 3 * response.data[key]["articulation"],
            borderWidthSelected: 5 + 3 * response.data[key]["articulation"],
            title: "<textarea rows='6' cols='100'>"+"Aprox "+response.data[key]["vertex_betweenness"].toString()+" people can use you to know others\n" +  "You are the core friend of aprox: "+ response.data[key]["closeness"].toString()+" people"   + "\n If you dissapear, "+ (response.data[key]["local_clustering"]+1)+" people would never meet!" +"</textarea>"
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
      /*
      var options = {
        nodes: {
          borderWidth: 3,
          size: 15,
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
      */
      var options = {};
      network = new vis.Network(container, data, options);
    });
  };

}])
   
.controller('show_shortest_pathCtrl', ['$scope', '$stateParams', '$http',
function ($scope, $stateParams, $http) {
  //   $scope.$on("$ionicView.loaded", function() {
  $scope.model = {};

  getRank = function(value) {
    if (value < 0.1) {
      return "#CCCCCC";
    }
    if (value < 0.3) {
      return "#469751";
    }
    if (value < 0.6) {
      return "#33A992";
    }
    if (value < 0.8) {
      return "#3C2BE2";
    }
    if (value < 1.1) {
      return "#8F2D8B";
    }
    if (value < 1.6) {
      return "#EBA246";
    }
    return "#B62A3C";
  };

  $scope.getShortestPath = function() {
    // First make request data (should put all of this in a new fun)
    source_id = $scope.model.source_id;
    target_id = $scope.model.target_id;
    url = "http://ec2-18-144-6-174.us-west-1.compute.amazonaws.com:5000/shortest_path?source=" + source_id + "&target=" + target_id;
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
            background: '#666666',
            highlight: {
              border: 'white'
            }
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
   
.controller('menuCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {

}])
   
.controller('menuCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])
.controller('theFriendshipNetworkCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {
  /*
  $scope.shit = function() {
    console.log("fuck");
  };

  $scope.callbackMethod = function (query, isInitializing) {
    console.log("calling this shit");
    return [query];
  };
  */
   $scope.items = [
      {display: 'Hello'},
      {display: 'Baha'},
      {display: 'Ala'},
      {display: 'Siwar'},
      {display: 'Monira'},
      {display: 'Samir'},
      {display: 'Spange Bob'},
      {display: 'Deneris Targariant'},
      {display: 'Ned Stark'}
  ];
  $scope.onSelect = function (item) {
      console.log('item', item);
  };

}])
 