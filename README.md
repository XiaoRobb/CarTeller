# CarTeller
汽车识别（包括车牌、车型、车品牌、属性、及驾驶员违规行为识别检测）

---------------项目文件说明---------------

html文件夹内内容：本项目Web端前端代码实现

CarTeller文件夹内容：本项目服务器端和后端深度学习代码的实现，包括（服务器端：app文件夹内内容，以及后端：汽车的属性识别、车型识别、车辆检测、车牌识别、  驾驶员违规行为检测）。

CarInfoTeller文件夹内容：拥有车型识别的训练代码内容（CarTeller文件夹主要为训练完后使用的代码，所以没有将车型识别的训练代码加入，现在单独补上）

【注意：其他的识别训练代码由于不是很多就没有和使用代码分离，所以在CarTeller里，没有单独补发】

---------------各个部分作者说明---------------

html文件夹内内容：

     主要作者：王崎璇（xxxxx)
     
     次要作者：陈嘉(xxxxx)
     
CarTeller文件夹内容：

      服务器端：app文件内内容
              主要作者：高晓凯 （xxxx)
      
      后台深度学习用于汽车识别代码：
      
      车牌识别（CarBoardTeller): 主要作者 ： 陈嘉
              技术：OpenCV + SVM
      
      车辆检测（CarTypeTellerMore):多车检测类型并统计各种车数量 ：主要作者：陈嘉
              重要库：ImageAI
      
      车辆检测（CarTypeTellerOne):单次分类检测： 主要作者：周宏俊
             数据集：自己制作寻找
             网络：VGG16
      
      车型识别（CarInfoTeller）：识别汽车品牌： 主要作责：周宏俊
             数据集：Stanford Cars 196种常见汽车车型和其年份品牌信息
             网络：ResNet152
     
      驾驶员行为检测（DriverBehavior）：识别驾驶员在车上的各种违规行为（9种，如使用手机等） 主要作者： 周宏俊
             数据集：Kaggle的State Farm Distracted Driver Detection
             网络：ResNet152
      
      属性检测（CarAttribute）：调用百度API

