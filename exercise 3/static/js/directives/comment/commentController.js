app.controller('CommentController', ['$scope', '$mdDialog', '$mdMedia', '$route', function($scope, $mdDialog, $mdMedia, $route) {
	this.editComment = function(ev, comment, schema, science) {
		var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'));
		var DialogController = function($mdDialog, backend, comment, science) {
			console.log(comment);
			this.originalComment = comment;
			this.comment = {};
			this.science = science;
			
			for (key in comment.schema) {
				this.comment[key] = comment.content[comment.schema[key]];
			}
			
			this.searchMovies = function(query, ctrl) {
				result = backend.searchMovies(query, ctrl);
			return result;
			}
			
			this.searchFields = function(query, fields){
				var filtered = [];
				for (index in fields) {
					if (fields[index].name.indexOf(query) > -1) {
						filtered.push(fields[index]);
					}
				}
				return filtered;
			}
			
			this.cancel = function() {
				$mdDialog.cancel();
			}
				
			this.submitComment = function(movie, science, ctrl) {
				console.log(ctrl);
				if(ctrl.selectedMovie) {
					ctrl.comment.movie_id = ctrl.selectedMovie[ctrl.movieSchema.id];
				}
				if(ctrl.selectedScience) {
					ctrl.comment.science_id = ctrl.selectedScience.id;
				}
				ctrl.submitting = true;
				backend.updateComment(ctrl);
			};
			
			this.confirmDelete = function(ctrl) {
				ctrl.deleting = true;
			}
			
			this.cancelDelete = function(ctrl) {
				ctrl.deleting = false;
			}
			
			this.deleteComment = function(ctrl) {
				ctrl.submitting = true;
				ctrl.deleting = false;
				backend.deleteComment(ctrl);
			};

			this.confirmSubmit = function() {
				$mdDialog.hide();
			}
		}
		
		$mdDialog.show({
			controller: DialogController,
			controllerAs: "dialCtrl",
			templateUrl: 'js/directives/comment/editcomment.html',
			parent: angular.element(document.body),
			targetEvent: ev,
			clickOutsideToClose: false,
			fullscreen: useFullScreen,
			locals: {
				comment: {
				   'content': comment,
				   'schema': schema
				},
				science: science
			}
		}).then(function() {
			$route.reload();
		});
	};
}]);