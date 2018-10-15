var elements = document.getElementsByTagName('*');
var pagetext = '';
for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    for (var j = 0; j < element.childNodes.length; j++) {
        var node = element.childNodes[j];
        if (node.nodeType === 3) {
            var text = node.nodeValue;
            for (var k = 0;k<text.length;k++){
                if (/[a-zA-Z]/.test(text[0]) && text.length>100 && pagetext.length<100000){
                    pagetext += text;
                }
            }
        }
    }
}
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        if(xhttp.responseText == "fake"){
            alert("THIS PAGE MIGHT CONTAIN FAKE NEWS!");
        }
        //else if(xhttp.responseText == "real"){
        //alert("All good");
        //}
        //else{
        //alert("This is no good!");
        //}
    }
};
xhttp.open("POST", "http://localhost:8080/", true);
xhttp.send(pagetext);
