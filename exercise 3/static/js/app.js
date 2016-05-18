var app = angular.module('BadMovieScience', ['ngRoute', 'ngMaterial', 'ngMessages']);

app.config(function ($routeProvider, $mdThemingProvider, $interpolateProvider) { 
	$routeProvider 
		.when('/', {
			controller: 'HomeController',
			controllerAs: 'home',
			templateUrl: 'html/views/home.html'
		})
		.when('/directory', {
			controller: 'RouteController',
			controllerAs: 'directory',
			templateUrl: 'html/views/directory.html',
			resolve: {
				backendData: function (backend) {
					return backend.getMovies();
				}
			}
		})
		.when('/genres/', {
			controller: 'RouteController',
			controllerAs: 'genres',
			templateUrl: 'html/views/genreDirectory.html',
			resolve: {
				backendData: function (backend) {
					return backend.getGenres();
				}
			}
		})
		.when('/genres/:id', {
			controller: 'RouteController',
			controllerAs: 'genresCtrl',
			templateUrl: 'html/views/genre.html',
			resolve: {
				backendData: function ($route, $q, backend) {
					var deferred = $q.defer()
					
					var id = Number($route.current.params.id);
					
					$q.all({
						'genre': backend.getGenres(id),
						'movies': backend.getGenreMovies(id)
					}).then(function(value) {
						deferred.resolve({
							'genre': value.genre.genres[0],
							'genreSchema': value.genre.schema,
							'movies': value.movies.movies,
							'movieSchema': value.movies.schema
						})
					});
					return deferred.promise;
				}
			}
		})
		.when('/movie/:id', {
			controller: 'RouteController',
			controllerAs: 'comments',
			templateUrl: 'html/views/movie.html',
			resolve: {
				backendData: function ($route, $q, backend) {
					var deferred = $q.defer()
					
					var id = Number($route.current.params.id);
					
					$q.all({
						'comment': backend.getComments({'movie_id': id}),
						'movie': backend.getMovies(id)
					}).then(function(value) {
						deferred.resolve({
							'comment': value.comment.comment,
							'commentSchema': value.comment.schema,
							'movie': value.movie.movies[0],
							'movieSchema': value.movie.schema
						})
					});
					return deferred.promise;
				}
			}
		})
		.when('/science/', {
			controller: 'RouteController',
			controllerAs: 'science',
			templateUrl: 'html/views/scienceDirectory.html',
			resolve: {
				backendData: function (backend) {
					return backend.getScience();
				}
			}
		})
		.when('/science/:id', {
			controller: 'RouteController',
			controllerAs: 'comments',
			templateUrl: 'html/views/science.html',
			resolve: {
				backendData: function ($route, $q, backend) {
					var deferred = $q.defer()
					
					var id = Number($route.current.params.id);
					
					$q.all({
						'comment': backend.getComments({'science_id': id}),
						'science': backend.getScience(id)
					}).then(function(value) {
						deferred.resolve({
							'comment': value.comment.comment,
							'commentSchema': value.comment.schema,
							'science': value.science.science[0],
							'scienceSchema': value.science.schema
						})
					});
					return deferred.promise;
				}
			}
		})
		.when('/user/:id', {
			controller: 'RouteController',
			controllerAs: 'userCtrl',
			templateUrl: 'html/views/user.html',
			resolve: {
				backendData: function ($route, backend) {
					var id = Number($route.current.params.id);

					return backend.getComments({'author': id});
				}
			}
		})
		.otherwise({ 
			redirectTo: '/' 
		});
	$mdThemingProvider.theme('default').dark()
		.primaryPalette('grey')
		.accentPalette('yellow');
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});