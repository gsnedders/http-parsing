function empty(element)
{
	while (element.firstChild)
	{
		element.removeChild(element.firstChild);
	}
}

function test_result(ord, result)
{
	var results = document.getElementById('results').getElementsByTagName('tbody')[0];
	var result = results.insertRow(-1);
	result.insertCell(0).appendChild(document.createTextNode('0x' + ord.toString(16)));
	result.insertCell(1).appendChild(document.createTextNode(result));
}

function update_status(s)
{
	var status_element = document.getElementById('status');
	empty(status_element);
	status_element.appendChild(document.createTextNode(s));
}

function new_xhr()
{
	return window.XMLHttpRequest ? new window.XMLHttpRequest() : new ActiveXObject('MSXML2.XMLHTTP.3.0');
}

function run_test(test_url, i)
{
	var xhr = new_xhr();
	xhr.onreadystatechange = function()
	{
		if (xhr.readyState != 4)
		{
			return;
		}
		test_result(i, xhr.status);
	}
	try
	{
		xhr.open('FO' + String.fromCharCode(i) + 'O', test_url, false);
		xhr.send(null);
	}
	catch(e)
	{
		test_result(i, e.name);
	}
}

function start(test_url)
{
	empty(document.getElementById('results').getElementsByTagName('tbody')[0]);
	for (var i = 0; i <= 0xFF; i++)
	{
		update_status('Running… (test ' + (i + 1) + '/256)');
		run_test(test_url, i);
	}
	
	update_status('Finished.');
}

window.onload = function()
{
	document.getElementById('test_form').onsubmit = function()
	{
		start(document.getElementById('test_url').value);
		return false;
	}
}