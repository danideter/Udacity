app.controller('RouteController', ['$route', function($route) {
	 this.routeData = $route.current.locals.backendData;
}]);