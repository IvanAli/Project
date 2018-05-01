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
	// 	int i =0;
	// 	while (i<7){
	// 		if(i<$scope.path.size()) $scope.appears[i]=true;
	// 		else $scope.apperas[i]=false;
	// 		i++;
	// 	}
	// };



}])
   
.controller('page2Ctrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {

	$scope.appears = $stateParams.appears;

}])
 