---
layout: post
title:  "Jmeter-자주사용하는 스크립트 정리"
date:   2019-07-21 00:05:13 +0900
categories: jmeter update
tags:
- jmeter
- tip
---
jmeter 에서 자주사용하는 스크립트 팁을 정리중이다.
하나씩 생각날때마다 리스트업 할 예정이다.

* 목차
{:toc}

# thread loop count

getIteration() function 을 사용하면 thread loop count 를 얻어올수 있다.

- in property
``` ruby
${__BeanShell(vars.getIteration();,)}
```
- in shell

``` ruby
vars.getIteration();
log.info("\n\nloop : "+ vars.getIteration() );
```

# response
응답에대해서 저장 하고 싶을때
- shell
``` ruby
vars.put("response", prev.getResponseDataAsString());
```
- Regular Expression Extractor

```
Reference Name: response
Regular Expression: (?s)(^.*)
Template: $1$
```
[Jmeter-Response Data 저장하기](../jmeter-save-response-data)


# current directory

현재 디랙토리 정보를 가져오고 싶을때

- in shell

``` ruby
import org.apache.jmeter.gui.GuiPackage;
import org.apache.commons.io.FilenameUtils;

String testPlanFile = GuiPackage.getInstance().getTestPlanFile();
String testPlanFileDir = FilenameUtils.getFullPathNoEndSeparator(testPlanFile).replace('\\', '/');

vars.put("currentDIR", testPlanFileDir+"/");
```

# foreach controller

반복하고 싶을때 아래 와 같이 하면 된다.

- in shell

``` ruby
String filePath = "path\\to\\your\\csv\\userdata.csv";

BufferedReader fbr = new BufferedReader(new FileReader(filePath));
String user;
int counter = 1;
while ((user = fbr.readLine()) != null) {
   vars.put("user_" + counter, user);
   counter++;
}
fbr.close();
```
- ForEach Controller
물론 컨트롤러에서도 가능하다.
![jmeter]({{ site.url }}/assets/images/Jmeter-tip-01.png){: width="80%" height="80%"}
![jmeter]({{ site.url }}/assets/images/Jmeter-tip-02.png){: width="80%" height="80%"}
![jmeter]({{ site.url }}/assets/images/Jmeter-tip-03.png){: width="80%" height="80%"}

#  current Thread Number

현재 수행중인 스레드의 갯수를 확인하고싶을때

- in shell

``` ruby
 int tpos = ctx.getThreadNum();
```

- in property

``` ruby
${__threadNum}
```

# current UNIX time stamp

UNIX 시간 값 가져오기


- config

``` ruby
${__javaScript(new Date().getTime();)}
```

- shell

``` ruby
 time = System.currentTimeMillis();
```

# How to use simple JSON with jMeter
simple JSON 을 사용하려면 lib 폴더에 아래 링크로 다운받아 설치후 하면된다.
http://www.java2s.com/Code/Jar/j/Downloadjsonsimple11jar.htm

``` json
{
    "users": {
        "name": "myname",
        "age": "20"
    }
}
```
- Shell

```ruby
String response = prev.getResponseDataAsString();
JSONParser parser = new JSONParser();

try {
    Object obj = parser.parse(response);
    JSONObject jsonObject = (JSONObject) obj;
    JSONObject user= (JSONObject) jsonObject.get("user");

    log.info("Name : "+ user.name);

} catch (FileNotFoundException e) {
    e.printStackTrace();
} catch (IOException e) {
    e.printStackTrace();
} catch (ParseException e) {
    e.printStackTrace();
}
```

- Iterating through JSON Object

``` ruby
String response = prev.getResponseDataAsString();
JSONParser parser = new JSONParser();

try{
    Object obj = parser.parse(response);
    JSONObject jsonObject = (JSONObject) obj;
    JSONObject message = (JSONObject) jsonObject.get("message");

    Set keys = message.keySet();
    Iterator a = keys.iterator();
    while(a.hasNext()) {
        String key = (String)a.next();
        // loop to get the dynamic key
        String value = (String)jsonObject.get(key);

        log.info("key : "+key);
        log.info(" value :"+value);
    }

} catch (FileNotFoundException e) {
    e.printStackTrace();
} catch (IOException e) {
    e.printStackTrace();
} catch (ParseException e) {
    e.printStackTrace();
}
```

- Iterating through JSON Array

``` ruby
- Iterating through JSON Array
String response = prev.getResponseDataAsString();
JSONParser parser = new JSONParser();

try {

   Object obj = parser.parse(response);
   JSONObject jsonObject = (JSONObject) obj;

   JSONArray  changesArray = (JSONArray) jsonObject.get("changes");

   int le= changesArray .size();
   for(int i = 0 ; i < le; i++){
      log.info("\n"+ changesArray .get(i));
   }

} catch (FileNotFoundException e) {
   e.printStackTrace();
} catch (IOException e) {
   e.printStackTrace();
} catch (ParseException e) {
   e.printStackTrace();
}
```

# How to add external packages(jar) in to jMeter

외부 JAR 라이브러리를 이용하려면 Jmeter 가 설치된 폴더의 /lib 폴더내부에

jar 파일을 복사해 넣은후 Jmeter 를 재시작 해주면 실행시 해당 라이브러리를 사용 할 수 있다.


# How to Log in jMeter BeanShell
매번쓰는 기능중하나인 jmeter console 에서 로그 보는것은 아래와 같이 해준다.
String 형식으로 만출력이 가능한거같다.
다른 형식일경우  toString() 을 이용해서 출력해야하는듯
``` ruby
log.info("Welcome");

log.info("\n\nName : "+ vars.get("title") );
```

# Bean shell Add or Remove request header

- For removing existing header

``` ruby
sampler.getHeaderManager().removeHeaderNamed("Authorization");
```
- For Adding new header

``` ruby
sampler.getHeaderManager().add(new Header("Authorization",Authorization ));
```

# URL encoding

``` ruby
${__urlencode(${token})}
```

``` ruby
import java.net.URLEncoder;

URLEncoder.encode(data,System.getProperty("file.encoding"));
```
- 참 고 https://wiki.workassis.com/jmeter-url-encoding/

# json extractor extract-all values of one key in a string

id 값만 가져와서 변수화 하려면

- match no 값은 -1 로 하고
- all 체크

참고적으로 match no 가 1 이면 첫번째 값이다.
아래 와 같을경우 id = 3

```json
[ {
   "id" : 3,
   "description" : "Back",
   "name" : "back"
}, {
   "id" : 1,
   "description" : "Front",
   "name" : "front"
}, {
   "id" : 6,
   "description" : "Left",
   "name" : "left"
}]
```
아래와 같이 설정하면

- foo_1=3
- foo_2=1
- foo_3=6

과 같이 순번이 자동으로 붙어서 저장된다.

![jmeter]({{ site.url }}/assets/images/Jmeter-tip-04.png){: width="100%" height="100%"}
![jmeter]({{ site.url }}/assets/images/Jmeter-tip-05.png){: width="100%" height="100%"}
