---
layout: post
title:  "[python][자동화]mouseinfo 모듈을 이용한 좌표 얻어오기"
date:   2022-12-20 11:03:13 +0900
categories: python pyautogui mouseInfo

tags:
- python
- pyautogui
- mouseinfo
---


* 목차
{:toc}
_

## mouseinfo

[mouseInfo](https://pypi.org/project/MouseInfo/)를 이용해서 화면의 좌표를 얻어 올 수 있다.

##  mouseinfo를 사용하려는 이유

그럼 내가 왜 이걸 사용해려고 했는지 이야기 해보려고한다.

요즘 들어 상당한 심심함이 찾아와서 게임을 해보고 있는중이다... 

게임을 하는데 의외로 번거로운작업이 많이 있다.. 게임을 위해서 조사도 해야하고.. 

그래서 생각 봇을 만들어보자.. 

봇 만들기를 해볼까 하고 찾아보다보니 [pyautogui](https://pyautogui.readthedocs.io/en/latest/) 라는 모듈로 스크립트를 하고 자동화를 할 수 있는것을 발견 해보려고 시도..

예제를 보니 좌표를 읽어서 클릭하고 이동하고 더블클릭등 여러가지들을 할수 있는것같았다.

```python
>>> import pyautogui

>>> screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
>>> screenWidth, screenHeight
(2560, 1440)

>>> currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.
>>> currentMouseX, currentMouseY
(1314, 345)

>>> pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.

>>> pyautogui.click()          # Click the mouse.
>>> pyautogui.click(100, 200)  # Move the mouse to XY coordinates and click it.
>>> pyautogui.click('button.png') # Find where button.png appears on the screen and click it.

>>> pyautogui.move(400, 0)      # Move the mouse 400 pixels to the right of its current position.
>>> pyautogui.doubleClick()     # Double click the mouse.
>>> pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

>>> pyautogui.write('Hello world!', interval=0.25)  # type with quarter-second pause in between each key
>>> pyautogui.press('esc')     # Press the Esc key. All key names are in pyautogui.KEY_NAMES

>>> with pyautogui.hold('shift'):  # Press the Shift key down and hold it.
        pyautogui.press(['left', 'left', 'left', 'left'])  # Press the left arrow key 4 times.
>>> # Shift key is released automatically.

>>> pyautogui.hotkey('ctrl', 'c') # Press the Ctrl-C hotkey combination.

>>> pyautogui.alert('This is the message to display.') # Make an alert box appear and pause the program until OK is clicked.
```
오호.. 일단.. 자동화 잘못하다가 계정 정지 당할수 도 있으니 일단은 계정을 하나 만들고 자동화가 되는지 시도해봤다.. 

봇으로 오인해서 계정정지 안당해야한다..ㅎㅎ

오 되네.. ? 안될줄알았는데 의외로 쉽게 되었다. 

그래서 좌표를 얻고 눌러서 해보려고 시도를 해보려고 했다.

그래서 좌표를 어떻게 얻을까 고민하다.. 그냥 출력해보자고 생각.. 

아래와 같이 print 로 좌표를 일일이 확인후 넣어주면 되겠다고 생각.. 

``` python
import pyautogui as pg
import time

# 좌표출력
pg.PAUSE = 1
pg.FAILSAFE = True

 while True:
        print('current mouse posion', pg.position())
        time.sleep(1)
```

실행결과 : 
```
current mouse posion Point(x=3794, y=1459)
current mouse posion Point(x=3767, y=1481)
current mouse posion Point(x=3833, y=1840)
current mouse posion Point(x=4548, y=874)
current mouse posion Point(x=4878, y=724)
current mouse posion Point(x=4916, y=719)
```
의외로 이동하면서 나오니 괜찬았다... 
그런데 조금해보니.. 화면으로 보면서 하니.. 귀찬다... 이런식으로 찍어주고 보고 하는 걸로 하려니 한두개 하는데는 괜찬은데 가짓수가 가 많이지니.. 화딱지가난다... 

다른 방법이 뭐가 있을까 찾아보기... 
- [이런것들이 존재..](https://ddolcat.tistory.com/1714) 
- [마우스 커서정보](https://ggondae.tistory.com/18)
역시 [mouseInfo](https://pypi.org/project/MouseInfo/) 라는 모듈이 존재했다.. 

시도..

그래서 다시 실행
```
import pyautogui as pg
import mouseinfo

mouseinfo.mouseInfo()
```


## 에러 발생

에러가 발생했다.. Mac 환경이니 참고

역시.. 바로 되면 이상하지..ㅎㅎ 

```
import mouseinfo
  File "/opt/homebrew/lib/python3.10/site-packages/mouseinfo/__init__.py", line 289, in <module>
    import tkinter
  File "/opt/homebrew/Cellar/python@3.10/3.10.9/Frameworks/Python.framework/Versions/3.10/lib/python3.10/tkinter/__init__.py", line 37, in <module>
    import _tkinter # If this fails your Python may not be configured for Tk
ModuleNotFoundError: No module named '_tkinter'
```
tkinter는 Python의 GUI 모듈인듯? 암튼 Mac이니.. 

간단히 아래 사항을 실행해주면된다.[참고](https://bobbyhadz.com/blog/python-no-module-named-tkinter) 


```
brew install python-tk@3.10
```

일단 해결.. 


## mouseinfo 로 좌표얻기

이걸 해결하고 나면 아래 그림과 같이 화면상에서 출력없이 GUI 환경에서 좌표를 얻을수 있었다. 

![mouseinfo]({{ site.url }}/assets/images/mouseinfo.png){: width="100%" height="100%"}

windows 에서는 RGB 색상까지 얻어오는것같다. Mac에서는 좌표만..

윈도우를 안쓴지 몇년이 지나.. 다음에 다시 윈도우에서 해본다면 시도해볼까..

오늘은 여기까지..

다음엔 자동화를 어떻게 했는지 시간이 남는다면 좀더 적어볼까 한다.

