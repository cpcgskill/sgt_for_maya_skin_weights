# sgt_for_maya_skin_weights

一个调用sgt接口来自动输出maya的蒙皮权重的插件， 你可以通过这个插件来自动输出maya的蒙皮权重。

[Demo](https://www.bilibili.com/video/BV1Ts4y1w7rL)

* [English](./README.en-US.md)
* [中文](./README.md)

## 目录

- [快速开始](#快速开始)
    * [配置sgt服务](#配置sgt服务)
    * [构建插件](#构建插件)
    * [构建安装包](#构建安装包)
- [版权说明](#版权说明)

## 快速开始

单纯的使用存在一个[教学视频](https://www.bilibili.com/video/BV1Re411S7XD)，
但是在使用之前， 你需要先配置[sgt服务](#配置sgt服务)

### 配置sgt服务

但是在使用插件之前需要配置sgt服务， 这里需要一个json文件：

```json
{
  "end_point": "https://u200470-9a3e-998256de.westc.gpuhub.com:8443/sgt"
}
```

在这个json文件中， end_point是你的sgt服务的地址， 你需要将这个json文件的url填入到sgtone_url_root这个环境变量中。

### 构建插件

- 构建依赖：
  * mayapy(2022)
  * pandoc 
  * make 
  * 7z 
  * pyeal

构建插件需要使用make工具， 你可以通过以下命令构建插件：

```commandline
make build
```

### 构建安装包

install_package相对于build来说， 它会将构建好的插件打包成一个zip文件， 你可以通过以下命令构建安装包：

```commandline
make install_package
```

## 版权说明

该项目签署了Apache-2.0 授权许可，详情请参