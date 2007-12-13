function findElements(tag, className)
{
    var matched = [];
    var els = document.getElementsByTagName(tag);
    var elsLen = els.length;
    var pattern = new RegExp("\\b"+className+"\\b");
    for (var i = 0; i < els.length; ++i)
    if (pattern.test(els[i].className))
        matched.push(els[i]);
    return matched;
}

var width = 800;

function getText(node)
{
    var t = node.textContent;
    if (t === undefined)
        t = node.innerText;
    return t;
}

function convertHistogram(table, pop_size)
{
    var data = [];
    var trs = table.getElementsByTagName('tr');
    var max = 0;
    var total = 0;
    for (var i = 0; i < trs.length; ++i)
    {
        var tr = trs[i];
        var n = getText(tr.firstChild);
        var v = +getText(tr.firstChild.nextSibling);
        if (v > max)
            max = v;
        total += v;
        data.push([n, v]);
    }

    if (pop_size)
        total = pop_size;

    for (var i = 0; i < trs.length; ++i)
    {
        var wrapper = document.createElement('span');
        wrapper.title = data[i][0];

        var bar = document.createElement('span');
        bar.style.width = (width * data[i][1] / max) + 'px';
        bar.className = 'bar';
        wrapper.appendChild(bar);

        var label = document.createElement('span');
        label.className = 'label';
        label.appendChild(document.createTextNode(data[i][1]));
        wrapper.appendChild(label);

        var td = trs[i].firstChild.nextSibling;
        td.removeChild(td.firstChild);
        td.appendChild(wrapper);
    }

    var colgroup = document.createElement('colgroup');
    colgroup.appendChild(document.createElement('col')).style.width = '5em';
    table.insertBefore(colgroup, table.firstChild);
}

window.onload = function ()
{
    var e = findElements('table', 'histogram-total');
    for (var i = 0; i < e.length; ++i)
        convertHistogram(e[i]);
};
