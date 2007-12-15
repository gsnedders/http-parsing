function test_result(test, pass)
{
	var results = document.getElementById("results").getElementsByTagName('tbody')[0];
	var result = results.insertRow(-1);
	result.insertCell(0).appendChild(document.createTextNode(test));
	result.insertCell(1).appendChild(document.createTextNode(pass ? "PASS" : "FAIL"));
}

function log(s)
{
	document.getElementById('log').appendChild(document.createElement('p')).appendChild(document.createTextNode(s));
}

function update_status(s)
{
	var status_element = document.getElementById('status');
	while (status_element.firstChild)
	{
		status_element.removeChild(status_element.firstChild);
	}
	status_element.appendChild(document.createTextNode(s));
}

function compare(exp, got)
{
	var failed = false;
	function fail(msg)
	{
		log(msg);
		failed = true;
	}
	// Check status code matches expected
	if (exp.HTTP.status != got.status)
	{
		fail('Got status code ' + got.status + ', expected ' + exp.HTTP.status);
	}
	// Check status text matches expected
	if (exp.HTTP.reason != got.statusText)
	{
		fail('Got status text ' + got.statusText + ', expected ' + exp.HTTP.reason);
	}
	// Check each and every header matches expected
	for (var n in exp.headers)
	{
		var exp_v = exp.headers[n];
		var got_v = got.getResponseHeader(n);
		if (exp_v != got_v)
		{
			fail('Got "' + n + '" header "' + got_v + '", expected "' + exp_v + '"');
		}
	}
	// Check the body matches expected
	if (exp.body != got.responseText)
	{
		fail('Got response body "' + got.responseText + '", expected "' + exp.body + '"');
	}

	return !failed;
}

function new_xhr()
{
	return window.XMLHttpRequest ? new window.XMLHttpRequest() : new ActiveXObject('MSXML2.XMLHTTP.3.0');
}

function run_test(test)
{
	var ok = false;
	var expected_xhr = new_xhr();
	expected_xhr.onreadystatechange = function()
	{
		if (expected_xhr.readyState != 4)
		{
			return;
		}
		if (expected_xhr.status != 200)
		{
			log('Failed to get ' + test + '.expected: got HTTP status ' + expected_xhr.status);
			return;
		}
		try
		{
			var expected = eval('(' + expected_xhr.responseText + ')');
		}
		catch (e)
		{
			log('Failed to parse ' + test + '.expected: ' + e);
			return;
		}
		var test_xhr = new_xhr();
		test_xhr.onreadystatechange = function()
		{
			if (test_xhr.readyState != 4)
			{
				return;
			}
			var ok = compare(expected, test_xhr);
		};
		test_xhr.open('GET', 'tests/' + test + '.http');
		test_xhr.send(null);
	}
	expected_xhr.open('GET', 'expected/' + test + '.expected');
	expected_xhr.send(null);
	return ok;
}

function start()
{
	var tests_frame = document.getElementById('tests').contentWindow.document;
	var as = tests_frame.getElementsByTagName('a');
	var test_names = [];
	for (var i = 0; i < as.length; i++)
	{
		var href = as[i].getAttribute('href');
		var m = href.match(/(?:.*\/|^)?([^\/]*)\.http$/); // strip .http extension, and any path prefix (for IE)
		if (!m) continue;
		test_names.push(m[1]);
	}
	
	var passes = 0;
	for (var i = 0; i < test_names.length; i++)
	{
		update_status('Running... (test ' + (i + 1) + '/' + (test_names.length + 1) + ', currently passed ' + passes + ')');
        log('Test ' + (i + 1) + ': ' + test_names[i]);
		var pass = run_test(test_names[i]);
		test_result(test_names[i], pass);
		if (pass)
		{
			passes++;
		}
	}
	log('Completed');
	update_status('Finished. Passed ' + passes + '/' + (test_names.length + 1) + '.');
}

window.onload = start;