var mysql = require('mysql');
var probmatFake, probmatReal
var  news
var fs = require('fs');
var con = mysql.createConnection({
                                 host: "localhost",
                                 user: "user",
                                 password: "password",
                                 database: "mysql"
                                 });
con.connect(function(err) {
            if (err) throw err;
            console.log("Connected!");
            sql = "select* from probmatfake"
            con.query(sql, function (err, result) {
                      if (err) throw err;
                      probmatFake = result
                      });
            sql = "select* from probmatreal"
            con.query(sql, function (err, result) {
                      if (err) throw err;
                      probmatReal = result
                      });
            });
detectFake = function(key){
    var probmat
    if (key==0){
        probmat = probmatFake
    }
    else if (key==1){
        probmat = probmatReal
    }
    var FRfactor=0
    for(var i=0;i<news.length-1;i++){
        for(var j=0;j<probmat.length;j++){
            if(news[i]==probmat[j].word1 && news[i+1]==probmat[j].word2){
                FRfactor+=probmat[j].prob
                //if(key==1){
                //console.log(probmat[j].word1,probmat[j].word2)
                //}
            }
        }
    }
    return FRfactor
}
var http = require('http');
http.createServer(function (req, res) {
                  if(req.method == 'POST'){
                  var FR = "real"
                  var Ffactor = 0
                  var Rfactor = 0
                  console.log("\n\n\nPOST request")
                  req.on('data',function(data){
                         news = data + ''
                         //console.log(news)
                         news = news.replace("'", " ").replace(/\./g," . ").split(" ");
                         Ffactor+=detectFake(0)
                         Rfactor+=detectFake(1)
                         var message
                         //res.writeHead(200, {'Content-Type': 'text/html'});
                         if (Ffactor-Rfactor>1){
                         message = "This news is more likely fake"
                         FR = "fake"
                         }
                         else if (Ffactor-Rfactor<-1){
                         message = "This news is probably real"
                         FR = "real"
                         }
                         else{
                         message = "Could not determine"
                         FR = "real"
                         }
                         console.log("Rfactor:",Rfactor,"Ffactor:",Ffactor)
                         console.log(message,"\n")
                         });
                  //console.log("1")
                  res.end(FR)
                  }
                  }).listen(8080);
