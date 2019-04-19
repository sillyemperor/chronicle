function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

var Events = (function(){

	function http(url, method, isjson, data, callback, nologin) {

        var headers = new Headers();

		fetch(url, {
			  method: method,
			  body: data,
			  headers: headers
		}).then(function(resp) {
		    if(resp.status>300) {
                throw resp.statusText;
            }
			return resp.json();
		}).then(function(json){
			callback(json, json.error);
		}).catch(function(err) {
			console.log(err);
			callback(null,err);
		});
	}

	function convert_time(s) {
	    var dt = new Date(s)
	    var s = dt.getFullYear()>=0?1:-1;

	    return s*(Math.abs(dt.getFullYear())*10000+dt.getMonth()*100+dt.getDate());
	}

	return {
	    search: function(start, end, q, tags, cb) {
	        http('/event?q='+q+'&start='+convert_time(start)+'&end='+convert_time(end)+'&tags='+tags, "GET", true, null, cb);
	    },
	    list_tags: function(cb) {
	        http('/tag', "GET", true, null, cb);
	    },
	};

})();