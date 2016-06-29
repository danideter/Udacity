app.factory('backend', ['$http', '$q', function($http, $q) {
 
    this.stateId = "";

	return {
        setOAuthId: function (googleUser) {
            this.userOAuthId = function() {
                return googleUser.getAuthResponse().id_token;
            };
        },
		deleteComment: function (ctrl) {
			$http({ 
				url: '/deleteComment',
				method: 'DELETE',
				data: {
					'id': ctrl.comment.id,
                    'token': this.userOAuthId(),
                    'stateid': this.stateId,
				}, 
				headers: {'Content-Type': 'application/json'}
					}).success(function(data) {
						ctrl.submitting = false;
						ctrl.submitted = true;
					});
		},
		getComments: function (params) {
			var deferred = $q.defer();
			
			$http({ 
				url: '/getComments',
				method: 'POST',
				data: {
					'params': params
				}, 
				headers: {'Content-Type': 'application/json'}
					}).success(function(data) {
						deferred.resolve(data);
					});
					
			return deferred.promise;
		},
		getGenres: function(id = null) {
			var deferred = $q.defer();
			var data = {};
			
			if(id != null){
				data = {'id': id}
			}
			
			$http({
				url: '/getGenres',
				method: "POST",
				data: {
                    'id': id
                    },
				headers: { 'Content-Type': 'application/json' },
					}).success(function(data) {
						deferred.resolve(data);
			});
			
			return deferred.promise;
		},
		getGenreMovies: function(id = null) {
			//Combine with getMovies someday
			var deferred = $q.defer();
			var data = {};
			
			if(id != null){
				data = {'id': id}
			}
			
			$http({
				url: '/getGenreMovies',
				method: "POST",
				data: {
                    'id': id
                    },
				headers: { 'Content-Type': 'application/json' },
					}).success(function(data) {
						deferred.resolve(data);
			});
			
			return deferred.promise;
		},
		getHierarchy: function(ctrl){
			var deferred = $q.defer();
			
			$http({
				url: '/getAppInit',
				method: "GET",
				headers: { 'Content-Type': 'application/json' }
					}).success(function(data) {
						// Success callback where value is an array containing the success values
						var hierarchy = data;
						
						// Setup menu schema
						var schemaId = 0;
						var schemaName = 1;
						var menuGenres = 0;
						var menuFields = 1;
						
						//Setup science and genre controller reference
						var genresInfo = [];
						var fieldsInfo = [];
						
						// Set up menu
						var menu = [
						{
							name: "Movie Genres",
							route: "#/genres",
							show: false,
							children: []} , 
						{
							name: "Science Fields",
							route: "#/science",
							show: false,
							children: []} , 
						{
							name: "Film Directory",
							route: "#/directory",
							show: false}
						];
						
						for (index in hierarchy.genres) {
							menu[menuGenres].children.push({
								name: hierarchy.genres[index][schemaName],
								route: "#/genres/" + hierarchy.genres[index][schemaId],
								show: true
							});
							genresInfo.push({
								name: hierarchy.genres[index][schemaName],
								id: hierarchy.genres[index][schemaId]
							});
						}
						
						for (index in hierarchy.fields) {
							menu[menuFields].children.push({
								name: hierarchy.fields[index][schemaName],
								route: "#/science/" + hierarchy.fields[index][schemaId],
								show: true
							});
							fieldsInfo.push({
								name: hierarchy.fields[index][schemaName],
								id: hierarchy.fields[index][schemaId]
							});
						}
						
						deferred.resolve(menu);
						
						ctrl.menu = menu;
						ctrl.genresInfo = genresInfo;
						ctrl.fieldsInfo = fieldsInfo;
						
						ctrl.loading = false;
						});
			
			return deferred.promise;
		},
		getMovies: function(id = null) {
			var deferred = $q.defer();
			var data = {};
			
			if(id != null){
				data = {'id': id}
			}
			
			$http({
				url: '/getMovies',
				method: "POST",
				data: {
                    'id': id
                    },
				headers: { 'Content-Type': 'application/json' },
					}).success(function(data) {
						deferred.resolve(data);
			});
			
			return deferred.promise;
		},
		getRandomPage: function(table) {
			var deferred = $q.defer();
			
			$http({
				url: '/getRandomPage',
				method: "POST",
				data: {
                    'table': table,
                    },
				headers: { 'Content-Type': 'application/json' },
					}).success(function(data) {
						deferred.resolve(data.id);
			});
			
			return deferred.promise;
		},
		getScience: function(id = null) {
			var deferred = $q.defer();
			var data = {};
			
			if(id != null){
				data['id'] = id
			}
			
			$http({
				url: '/getScience',
				method: "POST",
				data: data,
				headers: { 'Content-Type': 'application/json' },
					}).success(function(data) {
						deferred.resolve(data);
			});
			
			return deferred.promise;
		},
		postComment: function (author, movie, science, description, ctrl) {
			$http({ 
				url: '/postComment',
				method: 'POST',
				data: {
					'author': author,
					'movie': movie,
					'science': science,
					'description': description,
                    'token': this.userOAuthId(),
                    'stateid': this.stateId,
				}, 
				headers: {'Content-Type': 'application/json'}
					}).success(function(data) {
						ctrl.submittedComment = data;
						ctrl.submitting = false;
						ctrl.submitted = true;
					});
		},
		postUser: function(ctrl){
			var deferred = $q.defer();
            var service = this;
			
			$http({
				url: '/getUser',
				method: "POST",
				headers: { 'Content-Type': 'application/json' },
				data: {
                    'user': ctrl.user.email,
                    'token': this.userOAuthId(),
                }
					}).success(function(data) {
						ctrl.user.id = data.id;
						ctrl.loggedIn = true;

                        service.stateId = data.csrf;
                        
						deferred.resolve(data);
			}).error(function(message) {
                deferred.resolve(message);
            });
			
			return deferred.promise;
		},
		searchMovies: function(query, ctrl){
			var deferred = $q.defer();
			
			$http({
				url: '/searchMovies',
				method: "POST",
				headers: { 'Content-Type': 'application/json' },
				data: {
                    'query': query,
                    }
                    }).success(function(data) {
						if (!('movieSchema' in ctrl)) {
							ctrl.movieSchema = data.schema;
						}
						deferred.resolve(data.movies);
			});
			return deferred.promise;
		},
		updateComment: function (ctrl) {
			$http({
				url: '/updateComment',
				method: 'PUT',
				data: {
					'author': ctrl.comment.author,
					'movie': ctrl.comment.movie_id,
					'science': ctrl.comment.science_id,
					'description': ctrl.comment.description,
					'id': ctrl.comment.id,
                    'token': this.userOAuthId(),
                    'stateid': this.stateId,
				}, 
				headers: {'Content-Type': 'application/json'}
					}).success(function(data) {
						ctrl.submitting = false;
						ctrl.submitted = true;
					});
		}
	}
}]);