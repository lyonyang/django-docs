<!-- TOC -->

- [API文档](#API文档)
	- [文章相关API](#文章相关API)
		- [文章列表](#文章列表)
		- [添加文章](#添加文章)
		- [删除文章](#删除文章)
		- [编辑文章](#编辑文章)

<!-- /TOC -->

# API文档

## 文章相关API

### 文章列表

~/article/list

GET 请求方式

**请求参数**:


Header
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
authorization | False | str |  | Token |


请求示例:
```json
{
    "return_code":0,
    "return_data":[
        {
            "article_id":4,
            "author":"Lyon",
            "content":"一个构建Web API的工具",
            "create_time":"2019-03-20 16:14:12",
            "title":"API Docs"
        },
        {
            "article_id":5,
            "author":"Lyon",
            "content":"一个构建Web API的工具",
            "create_time":"2019-03-20 16:15:38",
            "title":"API Docs"
        }
    ]
}
```

### 添加文章

~/article/add

POST 请求方式

**请求参数**:


Header
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
authorization | False | str |  | Token |

Body
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
title | True | str | API Docs | 标题 |
content | True | str | 一个构建Web API的工具 | 内容 |
author | True | str | Lyon | 作者 |

请求示例:
```json
{
    "return_code":10000,
    "return_msg":"Invalid parameter."
}
```

### 删除文章

~/article/delete

POST 请求方式

**请求参数**:


Header
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
authorization | False | str |  | Token |

Body
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
article_id | True | int | 1 | 文章ID |

请求示例:
```json
{
    "return_code":10000,
    "return_msg":"Invalid parameter."
}
```

### 编辑文章

~/article/edit

POST 请求方式

**请求参数**:


Header
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
authorization | False | str |  | Token |

Body
字段名 | 必填 | 类型 | 示例值 | 描述
:-: | :-: | :-: | :-: | :-:
article_id | True | int | 1 | 文章ID |
title | True | str | API Docs | 标题 |
content | True | str | 一个构建Web API的工具 | 内容 |
author | True | str | Lyon | 作者 |

请求示例:
```json
{
    "return_code":10000,
    "return_msg":"Invalid parameter."
}
```

