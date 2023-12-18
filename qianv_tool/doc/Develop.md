# 一、开发步骤

#### 1、设计程序页面和编写gui代码

gui包下 【80%】

#### 2、通过图片快速生成点击目标的坐标

dev_tools/button_extract.py 【100%】

```text
 有选择性的迁移代码
 增加文本的获取
 增加适配需要的buildGrid功能的initial_area字段
```

#### 3、adb连通安卓手机并能截图后根据坐标能正确执行点击

##### 连通手机

  module/devices/connection 【100%】
  
##### 截图和点击

 module/devices/devices 【100%】
 module/devices/connection 【100%】
 

#### 4、跑通文字识别程序

 module/base/button 【100%】

#### 5、开发通用的devices操作程序 

 module/devices/devices 【100%】
 
#### 6、开发可用的文字识别、图片识别、颜色识别工具

 module/base/button 【100%】
 module/base/button_match 【100%】
 
 ```text
 有选择性的迁移代码
 增加适配需要的buildGrid
 完善 button_match 功能
```
 
#### 7、运行目标应用，梳理任务执行流程并输出到任务拆解文档

师门：100% 待验证
一条：20%

#### 8、根据任务拆解文档，截图处理后生成目标坐标

```text

action_window
mian_window
pop_frame
shopping
task_long
task_sm
 ---- 分任务说明
 师门：100% 
 一条：80% 

```

#### 9、根据任务拆解文档，分解动作单元，并编程该动作单元的代码

```text

师门 （module/game_action/task_sm/match.py）： 100% 

```
#### 10、根据任务拆解文档 与 动作单元拼接成一个完整的任务执行流程

```text

师门 （module/game_action/task_sm/task_sm_run.py）： 100%  待测试

```