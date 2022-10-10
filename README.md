# 使用命令行登录南京大学校园网(p.nju.edu.cn)
* 本项目是使用统一身份验证来登录，还有更简单的登录方法如下：
  ```bash
  # Windows需要安装最新的PowerShell
  # 登录
  curl -s http://p.nju.edu.cn/portal_io/login -X POST -d "username=学号&password=密码"
  # 登出
  curl -s http://p.nju.edu.cn/portal_io/logout
  ```
* 这种方法使用的密码还是改版之前的校园网登录密码，新生或者忘记了这个密码可能还是需要使用下述统一身份验证的方法来登录。

## 使用方法
* 本项目使用Python3编写，需要安装`requests`、`opencv-python`、`numpy`、`lxml`、`pandas`库。
  ```bash
  pip install requirements.txt
  ```
* 登录
  ```bash
  python3 main.py -i
  ```
  会在终端打印统一身份验证的二维码，使用手机扫码登录即可。(未测试字体，若出问题请尝试更换终端字体，如`MesloLGS NF`、`Fira Code`)
* 登出
  ```bash
  python3 main.py -o
  ```
* 无感认证管理：
  * 启用当前设备的无感认证：
    ```bash
    python3 main.py -a 笔记本电脑
    ```
  * 启用其他设备的无感认证，当前只能做Linux下以超级用户身份运行。  
    原理是将Linux下的mac地址更改到与另一个设备相同，开启无感认证后恢复为原来的mac地址，有一定概率出现bug。   
    需要指定当前设备连接校园网的网卡，如`wlo1`(使用`ifconfig`查看)，并指定另一个设备的MAC地址，可以连接到Windows笔记本的热点并在设置里面查看，其他方法也可自行查找。
    ```bash
    python3 main.py -a 树莓派 -m ab:cd:ef:01:23:45 -n wlo1
    ```
  * 删除设备的无感认证，需要指定设备id，使用`python3 main.py -p`查看。
    ```bash
    python3 main.py -d 166541052xxxxx
    ```
* 也可以使用`-h`参数查看更多功能
  ```bash
  python3 main.py -h
  ```

## 模块介绍
欢迎用于其他登录场景，使用请注明出处。
</br>
* `clear.py`：清空命令行
* `config.py`：配置文件，包含超时、url等
* `getQR.py`：二维码类，包含获取二维码、打印二维码等方法
* `login.py`：登录主程序
* `logout.py`：登出主程序
* `printInfo.py`：打印信息：余额、在线设备、无感认证设备
* `quickLogin.py`：管理无感认证设备