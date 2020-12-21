# CarTeller
汽车识别（包括车牌、车型、车品牌、属性、及驾驶员违规行为识别检测）

---------------项目文件说明---------------

html文件夹内内容：本项目Web端前端代码实现

CarTeller文件夹内容：本项目服务器端和后端深度学习代码的实现，包括（服务器端：app文件夹内内容，以及后端：汽车的属性识别、车型识别、车辆检测、车牌识别、  驾驶员违规行为检测）。

CarInfoTeller文件夹内容：拥有车型识别的训练代码内容（CarTeller文件夹主要为训练完后使用的代码，所以没有将车型识别的训练代码加入，现在单独补上）

【注意：其他的识别训练代码由于不是很多就没有和使用代码分离，所以在CarTeller里，没有单独补发】

---------------各个部分作者说明---------------

html文件夹内内容：

     主要作者：wqx
          五个功能界面，个人信息界面，历史界面以及其功能。接口文档微调。
          登录功能，滑块检测功能，界面弹窗效果。
     协作者：cj
          登录界面，API界面及部分调整
		 
AndroidPart文件夹内容:

	作者：cjj
		登录、注册界面，tab滑动切换Fragments，从手机存储读取照片，基于okHttp框架的以Json为载体的数据传输和解析逻辑
		，通过http协议与服务器交互进行几种车辆识别。
     
CarTeller文件夹内容：

      服务器端：
      flask文件内内容,主要作者：gxk （flask+gunicorn)
      服务器环境配置和项目部署,主要作者：gxk(centos7+flask+gunicorn+mysql,apache)
         主要配置centos7环境，部署flask项目和html项目，与前端配合调试，将模型整合到flask项目中并调试
      后台深度学习用于汽车识别代码：
      
      车牌识别（CarBoardTeller): 主要作者 ： cj
              技术：OpenCV + SVM
      
      车辆检测（CarTypeTellerMore):多车检测类型并统计各种车数量 ：主要作者：cj
              重要库：ImageAI
      
      车辆检测（CarTypeTellerOne):单车分类检测： 主要作者：zhj
             数据集：自己制作寻找
             网络：VGG16
      
      车型识别（CarInfoTeller）：识别汽车品牌： 主要作者：zhj
             数据集：Stanford Cars 196种常见汽车车型和其年份品牌信息
             网络：ResNet152
     
      驾驶员行为检测（DriverBehavior）：识别驾驶员在车上的各种违规行为（9种，如使用手机等） 主要作者： zhj
             数据集：Kaggle的State Farm Distracted Driver Detection
             网络：ResNet152
      
      属性检测（CarAttribute）：调用百度API

【我们是一个团队，中间避免不了相互协作、帮助，共同调试BUG，所以各个板块除了主要作者外，还有团队其他人员提供的各种支持，比如最终一起调试，一起寻找数据集，一起为前端界面提出自己的想法等等】


需要搭配的环境

1. pytorch 1.0.1版本 torchvision 0.2.2版本
2. imageai 库
3. keras tensorflow框架
4. effecient-net
5. opencv
6. 如果要运行训练，需要安装cuda
