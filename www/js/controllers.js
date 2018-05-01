angular.module('app.controllers', [])
  
.controller('pageCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams,$http) {

  $scope.mdl = {};

  $scope.getPath=function(){


            source_id = $scope.mdl.source;
            sink_id= $scope.mdl.destination;
            url = "http://localhost:5000/shortest_path?source="+source_id+"&sink="+sink_id;
            
            $http.get(url).then(function(response){
            $scope.path = response.data.name;

        },function(error){
            alert("Unable to retrieve a path");
        });

  };

  // $scope.AvatarList=function(){
  //  int i =0;
  //  while (i<7){
  //    if(i<$scope.path.size()) $scope.appears[i]=true;
  //    else $scope.apperas[i]=false;
  //    i++;
  //  }
  // };



}])
   
.controller('page2Ctrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {

  $scope.appears = $stateParams.appears;

}])

.controller('show_graphCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {
  $scope.$on("$ionicView.loaded", function() {
    // create an array with nodes
    var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);

    // create an array with edges
    var edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5}
    ]);

    // create a network
    var container = document.getElementById('mynetwork');

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};

    // initialize your network!
    var network = new vis.Network(container, data, options);
  });

}])
 
 