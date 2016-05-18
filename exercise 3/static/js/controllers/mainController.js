app.controller('MainController', 
	['$scope', '$mdSidenav', '$q', 'backend', 
	function($scope, $mdSidenav, $q, backend) {
		
		var ctrl = this;
		$scope.ctrl = this;
		
		// Log in attributes and functions
		this.loggedIn = false;
		this.loading = true;
		
		this.onLoginSuccess = buildOnLoginSuccess(ctrl);
		this.onLoginFailure = function(error) {
			console.log(error);
		}
		
		backend.getHierarchy(ctrl);
		
		this.renderButton = buildRenderButton(ctrl);
		ctrl.renderButton(ctrl);
		
		this.logOut = buildLogOut(ctrl);
		
		// Navigation Attributes
		this.sidenavOpen = false;
		this.toggle = function(item) {
			item.show = !item.show;
		}
		
		function buildLogOut(ctrl){
			return function () {
				gapi.auth2.getAuthInstance().signOut();
				ctrl.loggedIn = false;
			}
		}
		
		function buildOnLoginSuccess(ctrl) {
			return function(googleUser) {
				var basicProfile =  googleUser.getBasicProfile();
				ctrl.user = {
					name: basicProfile.getName(),
					photo: basicProfile.getImageUrl(),
					email: basicProfile.getEmail(),
					raw: googleUser,
				};
				backend.postUser(ctrl, basicProfile);
			}
		}
		
		function buildRenderButton(ctrl){
			return function(){
				gapi.signin2.render('my-signin2', {
					'scope': 'profile email',
					'onsuccess': ctrl.onLoginSuccess,
					'onfailure': ctrl.onLoginFailure
				});
			}
		}
		
		$scope.$on('$routeChangeSuccess', function(event, current) {
			var ctrl = $scope.ctrl;
			$q.all({
				'movie': backend.getRandomPage("movies"),
				'science': backend.getRandomPage("science")
			}).then(function(value) {
				ctrl.randomMovie = value.movie;
				ctrl.randomScience = value.science;
			});
		});
}]);