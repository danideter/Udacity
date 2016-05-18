app.controller('ScoreController', ['backend', '$scope', '$route', function(backend, $scope, $route) {
	var ctrl = this.ctrl;
	this.submitting = false;
	this.submitted = false;
	
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
	
	this.postComment = function(author, movie, science, description, ctrl) {
		this.submitting = true;
		backend.postComment(author, movie[ctrl.movieSchema.id], science.id, description, ctrl)
	}
	
	this.reload = function() {
		$route.reload();
	}
}]);