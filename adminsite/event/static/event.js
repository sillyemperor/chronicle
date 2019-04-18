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
	    search: function(start, end, q, cb) {
	        http('/event?q='+q+'&start='+convert_time(start)+'&end='+convert_time(end), "GET", true, null, cb);
	    },
	};

})();