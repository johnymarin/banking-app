



import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'post.dart';
import 'post_details.dart';


class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  
  final String title;
  
  @override
  _MyHomePageState createState() => new _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  List<Post> postList = [];
  bool _isRequestSent = false;
  bool _isRequestFailed = false;

  @override
  Widget build (BuildContext context) {

    if (!_isRequestSent){
      _sendRequest();
    }

    return new Scaffold(
      appBar: new AppBar(
        title: new Text(widget.title),
      ),
      body: new Container(
        alignment: Alignment.center,
        child: !_isRequestSent
        // Reques has not been sent, let's show a progress indicator
        ? new CircularProgressIndicator()

        // Request has been sent. Show the results
        : new Container(
          child: new ListView.builder(
              itemCount: postList.length,
              scrollDirection: Axis.vertical,
              itemBuilder: (BuildContext context, int index){
                return _getPostWidgets(index);
              }),
        ),
      ),
    );
  }

  void _sendRequest() async {
    String url = "https://api.nytimes.com/svc/topstories/v2/business"
        ".json?api-key=XW7AM6JluoNs9k9U7bzChxA29XDeWW5g";
    http.Response response = await http.get(url);
    Map decode = json.decode(response.body);
    List results = decode["results"];
    for (var jsonObject in results) {
      var post = Post.getPostFromJSONPost(jsonObject);
      postList.add(post);
      print (post);
    }
    setState(() => _isRequestSent = true);
  }

  Widget _getPostWidgets(int index){
    var post = postList[index];
    return new GestureDetector(
      onTap: (){
        openDetailsUI(post);
      },
      child: new Container(
        margin: const EdgeInsets.symmetric(horizontal:5.0, vertical: 5.0),
        child: new Card(
          elevation: 3.0,
          child: new Row(
            children: <Widget>[
              new Container(
                width: 150.0,
                child: new Image.network(
                  post.thumbUrl,
                  fit: BoxFit.cover,
                ),
              ),
              new Expanded(
                  child: new Container(
                    margin: new EdgeInsets.all(10.0),
                    child: new Text(
                      post.title,
                      style: new TextStyle(color: Colors.black, fontSize: 18.0),
                    ),
                  )),

            ],
          ),
        ),
      ),
    );
  }

  openDetailsUI(Post post){
    Navigator.push(
      context,
      new MaterialPageRoute(
          builder: (BuildContext context) => new PostDetails(post))
    );
  }

}



