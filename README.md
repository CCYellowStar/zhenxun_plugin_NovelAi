# zhenxun_plugin_NovelAi-aidraw_api

这是某第三方api的NovelAi作图插件，他能支持中文，内置[EhTagTranslation](https://github.com/EhTagTranslation/Database)词库翻译和百度机翻，支持任务队列  
  
## 用法
  
**以文本或文本加图片生成图片(可选长图、横图，默认方图）**  
  
指令：  
  `na作图 loli,hentai,girl`  
  `na作长图 loli,hentai,girl`  
  `na作横图 loli,hentai,girl [图片]`  
  ![image](https://user-images.githubusercontent.com/47291058/197211253-6d567500-027b-4806-8766-c166cc41899d.png)  
需要指定seed请在关键词前面加seed=******,(记得加逗号）    
  
**设置token（在http://lulu.uedbq.xyz/token获取）**  
  
指令：  
`设置tokrn tokrn(仅主人使用)`  



## 安装本体与机翻配置
将本分支的压缩包下载的插件文件放到真寻第三方插件目录（没有手动指定就放到`extensive_plugin`）  
先运行一次机器人，然后关掉，然后在`config.yaml`里刚生成的  
![image](https://user-images.githubusercontent.com/47291058/197219144-b60cd585-82a4-48a8-b8de-b0ea6a721cd6.png)  
填入配置，其中百度机翻的appid和key要在百度翻译的[开发者中心里](http://api.fanyi.baidu.com/product/11)获取(实名认证一下就够用了） 
如果没填百度的就不会调用机翻，EhTagTranslation词汇翻译还是会调用的  
其他可以照着我的填  

## 参考和使用
[EhTagTranslation](https://github.com/EhTagTranslation/Database)  
[nonebot_plugin_baidutranslate](https://github.com/NumberSir/nonebot_plugin_baidutranslate)
