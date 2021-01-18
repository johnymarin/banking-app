
class Post{
  String title;
  String summary;
  String thumbUrl;
  int timeStamp;
  String url;

  Post(this.title, this.summary, this.thumbUrl, this.timeStamp, this.url);

  static Post getPostFromJSONPost(dynamic jsonObject){
    String title = jsonObject['title'];
    String url = jsonObject['url'];
    String summary = jsonObject['abstract'];
    List multiMediaList =  jsonObject['multimedia'];
    //we want an average-quality image or nothing
    String thumbUrl = multiMediaList.length > 4? multiMediaList[3]['url'] : "";

    int timeStamp = DateTime.parse(jsonObject['created_date']).millisecondsSinceEpoch;

    return new Post(title, summary, thumbUrl, timeStamp, url);
  }

  @override
  String toString() {
    return "title = $title; summary = $summary; thumbnail = $thumbUrl; "
        "timeStamp = $timeStamp; url =  $url";
  }
}

