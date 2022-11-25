# zhenxun_plugin_NovelAi
**目前有第三方api版，本地版，本地附带频道版请到对应分支**  
这是调用本地stable-diffusion-webui-api的NovelAi作图插件，他能支持中文，内置[EhTagTranslation](https://github.com/EhTagTranslation/Database)词库翻译和百度机翻，支持任务队列  
  
## 用法
  
**以文本或文本加图片生成图片(可选长图、横图，默认方图）**  
  
指令：  
  `na作图 loli,hentai,girl`  
  `na作长图 loli,hentai,girl`  
  `na作横图 loli,hentai,girl [图片]`  
  ![image](https://user-images.githubusercontent.com/47291058/197211253-6d567500-027b-4806-8766-c166cc41899d.png)  
需要指定seed请在关键词前面加seed=******,(记得加逗号）    
  
**设置公开链接（本地部署sdwebui的公开链接或者本机链接）**  
  
指令：  
`设置公开链接 公开链接(仅主人使用)`  

## 安装前置条件
~~本插件使用的不是官方的webui，虽然官方也刚出api，但还没有图生图的调用，所以我fork了一个我觉得不错的webuiapi项目，删掉了个影响正常调用的代码。
所以你需要使用[这个仓库](https://github.com/CCYellowStar/stable-diffusion-webui-api)~~  
~~其他方面都会与官方同步更新~~  
现在官方版已更新图生图api，所以本插件移植为[官方版](https://github.com/AUTOMATIC1111/stable-diffusion-webui)  
**如果你没有部署过sdwebui**   
请下载官方那个仓库的压缩包，解压到一个地方运行`webui-user.bat`等他自动部署  
**如果你已经部署过sdwebui**   
也请下载官方那个仓库的压缩包，覆盖你的sdwebui根目录使他更新为最新即可使用  
**如果你已经部署过我的那个仓库的weiui**   
你可以选择继续更新[我那个仓库](https://github.com/CCYellowStar/stable-diffusion-webui-api)的版，因为也包含官方api  
也可以下载[官方版](https://github.com/AUTOMATIC1111/stable-diffusion-webui)的压缩包直接覆盖就替换为官方版了，然后以后的更新跟着官方版  
  
部署完后，你需要在`webui-user.bat`里的`COMMANDLINE_ARGS=`后面加上`--api`来启用api  
如果不是本机部署，你需要再加一个`--share`来打开公开链接  
建议ai部署环境显存6g以上  

## 安装本体与机翻配置
将`Releases`的压缩包下载的插件文件放到真寻第三方插件目录（没有手动指定就放到`extensive_plugin`）  
先运行一次机器人，然后关掉，然后在`config.yaml`里刚生成的  
![image](https://user-images.githubusercontent.com/47291058/197219144-b60cd585-82a4-48a8-b8de-b0ea6a721cd6.png)  
填入配置，其中百度机翻的appid和key要在百度翻译的[开发者中心里](http://api.fanyi.baidu.com/product/11)获取(实名认证一下就够用了） 
如果没填百度的就不会调用机翻，EhTagTranslation词汇翻译还是会调用的  
其他可以照着我的填  
**你需要先设置公开链接才能使用**

## 参考和使用
[EhTagTranslation](https://github.com/EhTagTranslation/Database)  
[nonebot_plugin_baidutranslate](https://github.com/NumberSir/nonebot_plugin_baidutranslate)
